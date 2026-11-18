// ends7: transfer-matrix enumeration of the periodic ends of a rigid train in a tube (push 7).
//
//   ends7 GEO OUTDIR DF DB LMAX THREADS
//
// GEO is written by geom7.py: T, s, the cells of one unit (E slab: x even, O slab: x odd), each cell's neighbours as
// (unit offset, slab, index), and the train's state.  See geom7.py for the gauge (tau = t - s*u mod T), under which
// the rule is the same at every unit and the train is a fixed point.
//
// A state is (E_{u-1}, O_{u-1}, E_u): all their cells at every gauge time.  An edge S -> S' (S' = (E_u, O_u,
// E_{u+1})) is valid iff, on the five slabs E_{u-1} .. E_{u+1}, the rule holds at every gauge time for every cell of
// O_{u-1}, E_u and O_u (each of these cells has all its neighbours inside the five slabs).  A periodic orbit of
// period dividing T of the infinite tube is exactly a bi-infinite path; an end of the train is a path
// TRAIN ... TRAIN S_1 ... S_k ZERO ZERO ... with S_1 != TRAIN and S_k != ZERO (cells outside the tube are dead for
// ever by T2, so the tube is exact).
//
// Method: forward BFS from TRAIN to depth DF (states reachable in <= DF steps), backward BFS from ZERO to depth DB
// (states from which ZERO is reachable in <= DB steps).  Every state of an end with k <= DF + DB - 1 lies in the
// union: S_i is reachable from TRAIN in i steps, and reaches ZERO in k + 1 - i steps.  Then every successor edge
// among the union is computed, the useful states (reachable from TRAIN, co-reachable to ZERO, inside the union) are
// kept, and every path TRAIN -> S_1 .. S_k -> ZERO with k <= LMAX (LMAX <= DF + DB - 1) is written.
// Checkpoints: each BFS layer is written to OUTDIR as it is completed and reloaded on restart.
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <string>
#include <thread>
#include <mutex>
#include <atomic>
#include <algorithm>
#include <chrono>
using namespace std;
typedef uint64_t u64;

static int T, S, nE, nO, W;           // W = words per state
static int slotN[10], slotOff[10];    // cells per slot; bit offset of slot (frame: units -2..2, E and O)
static int NB5;                       // bits in the frame
static int stateBits;                 // bits in slots 0..2
struct Nb { int du, typ, idx; };
static vector<vector<Nb>> nbE, nbO;
static string trainBits;

static inline int slotOf(int unitRel, int typ) { return 2 * (unitRel + 2) + typ; } // unitRel in -2..2
static inline int bitIdx(int slot, int c, int tau) { return slotOff[slot] + c * T + tau; }

struct Con { int self, tgt, nn; int nb[16]; };
static vector<Con> buildCons(const vector<int>& slots) {
    vector<Con> cons;
    for (int sl : slots) {
        int typ = sl & 1; int ur = sl / 2 - 2;
        int n = typ ? nO : nE;
        for (int c = 0; c < n; c++) {
            const vector<Nb>& nb = typ ? nbO[c] : nbE[c];
            for (int tau = 0; tau < T; tau++) {
                Con k; k.self = bitIdx(sl, c, tau); k.tgt = bitIdx(sl, c, (tau + 1) % T); k.nn = 0;
                for (auto& q : nb) {
                    int u2 = ur + q.du; int s2 = slotOf(u2, q.typ);
                    if (s2 < 0 || s2 > 9) { fprintf(stderr, "neighbour outside the frame\n"); exit(1); }
                    int t2 = ((tau - S * q.du) % T + T) % T;
                    k.nb[k.nn++] = bitIdx(s2, q.idx, t2);
                }
                cons.push_back(k);
            }
        }
    }
    return cons;
}

// feas[nl][nu][s][y]: s, y in {0,1,2(unknown)}
static bool feas[13][13][3][3];
static inline bool rule(int s, int n) { return n == 4 || n == 5 || (s && n == 3); }
static void buildFeas() {
    for (int nl = 0; nl < 13; nl++) for (int nu = 0; nu < 13; nu++) for (int s = 0; s < 3; s++) for (int y = 0; y < 3; y++) {
        bool ok = false;
        for (int ss = 0; ss < 2; ss++) { if (s != 2 && s != ss) continue;
            for (int yy = 0; yy < 2; yy++) { if (y != 2 && y != yy) continue;
                for (int n = nl; n <= nl + nu && n <= 12; n++) if (rule(ss, n) == (bool)yy) ok = true; } }
        feas[nl][nu][s][y] = ok;
    }
}

// ---- the CSP: enumerate assignments of the unknown slots ---------------------------------------------------------
struct Plan {
    vector<Con> cons;                    // full rules (edge validity) and lookahead rules (cells beyond left unknown)
    vector<int> vars;                    // order of unknown bits
    vector<vector<pair<int,int>>> occ;   // per frame bit: (constraint, role 0 nbr 1 self 2 tgt)
    vector<int> fixedCons;               // constraints with no unknown bit (checked once)
    vector<int> initCons;                // constraints with some unknown bit
    int outFrom;                         // first slot of the output state (2 forward, 0 backward)
};
static Plan planF, planB;

static void makePlan(Plan& P, const vector<int>& conSlots, const vector<int>& unknownSlots, int outFrom) {
    P.outFrom = outFrom; P.cons = buildCons(conSlots); auto& cons = P.cons;
    vector<char> unk(NB5, 0);
    for (int sl : unknownSlots) for (int b = slotOff[sl]; b < slotOff[sl] + slotN[sl] * T; b++) unk[b] = 1;
    P.occ.assign(NB5, {});
    for (int i = 0; i < (int)cons.size(); i++) {
        auto& k = cons[i]; bool any = unk[k.self] || unk[k.tgt];
        P.occ[k.self].push_back({i, 1}); P.occ[k.tgt].push_back({i, 2});
        for (int j = 0; j < k.nn; j++) { P.occ[k.nb[j]].push_back({i, 0}); if (unk[k.nb[j]]) any = true; }
        (any ? P.initCons : P.fixedCons).push_back(i);
    }
    // greedy static order: pick the unknown bit in the constraint with fewest remaining unordered unknown bits
    vector<int> rem(cons.size(), 0);
    for (int i = 0; i < (int)cons.size(); i++) {
        auto& k = cons[i]; int r = unk[k.self] + (k.tgt != k.self ? unk[k.tgt] : 0);
        for (int j = 0; j < k.nn; j++) r += unk[k.nb[j]];
        rem[i] = r;
    }
    vector<char> done(NB5, 0); int nunk = 0; for (int b = 0; b < NB5; b++) nunk += unk[b];
    for (int it = 0; it < nunk; it++) {
        int best = -1; double bs = -1;
        for (int b = 0; b < NB5; b++) if (unk[b] && !done[b]) {
            double sc = 0;
            for (auto& o : P.occ[b]) { int r = rem[o.first]; sc += 1.0 / (r * r); }
            if (sc > bs) { bs = sc; best = b; }
        }
        done[best] = 1; P.vars.push_back(best);
        for (auto& o : P.occ[best]) rem[o.first]--;
    }
}

struct Solver {
    const Plan& P; vector<signed char> val; vector<int> nl, nu; vector<u64>* out; long long nodes = 0;
    const vector<Con>& cons;
    Solver(const Plan& p) : P(p), val(NB5, 2), nl(p.cons.size()), nu(p.cons.size()), cons(p.cons) {}
    inline bool ok(int i) { auto& k = cons[i]; return feas[nl[i]][nu[i]][val[k.self]][val[k.tgt]]; }
    void emit() {
        if ((out->size() / W) % 1000000 == 999999) fprintf(stderr, "emit: %zu solutions so far, nodes %lld\n", out->size() / W + 1, nodes);
        size_t base = out->size(); out->resize(base + W, 0);
        u64* key = out->data() + base;
        for (int b = 0; b < stateBits; b++) if (val[slotOff[P.outFrom] + b]) key[b >> 6] |= 1ULL << (b & 63);
    }
    bool assign(int b, int v) {        // returns false on conflict (state is still updated; caller undoes)
        val[b] = v; bool good = true;
        for (auto& o : P.occ[b]) {
            int i = o.first;
            if (o.second == 0) { nu[i]--; if (v) nl[i]++; }
            if (good && !ok(i)) good = false;
        }
        return good;
    }
    void unassign(int b) {
        int v = val[b];
        for (auto& o : P.occ[b]) if (o.second == 0) { nu[o.first]++; if (v) nl[o.first]--; }
        val[b] = 2;
    }
    void dfs(int d) {
        nodes++;
        if (d == (int)P.vars.size()) { emit(); return; }
        int b = P.vars[d];
        for (int v = 0; v < 2; v++) {
            if (assign(b, v)) dfs(d + 1);
            unassign(b);
        }
    }
    // known: the three known slots as a state key, placed at slot `inFrom`
    void run(const u64* key, int inFrom, vector<u64>& o) {
        out = &o;
        for (int b = 0; b < NB5; b++) val[b] = 2;
        for (int b = 0; b < stateBits; b++) val[slotOff[inFrom] + b] = (key[b >> 6] >> (b & 63)) & 1;
        for (int i = 0; i < (int)cons.size(); i++) {
            auto& k = cons[i]; nl[i] = 0; nu[i] = 0;
            for (int j = 0; j < k.nn; j++) { int v = val[k.nb[j]]; if (v == 2) nu[i]++; else nl[i] += v; }
        }
        for (int i : P.fixedCons) if (!ok(i)) return;
        for (int i : P.initCons) if (!ok(i)) return;
        dfs(0);
    }
};

// ---- a hash set of fixed-width keys ------------------------------------------------------------------------------
struct KeySet {
    vector<u64> pool; vector<uint32_t> tab; size_t cap = 0, n = 0;
    static u64 h(const u64* k, int w) { u64 x = 0x9E3779B97F4A7C15ULL; for (int i = 0; i < w; i++) { x ^= k[i] + 0x9E3779B97F4A7C15ULL + (x << 6) + (x >> 2); x *= 0xBF58476D1CE4E5B9ULL; x ^= x >> 31; } return x; }
    void init(size_t c) { cap = c; tab.assign(cap, 0xFFFFFFFFu); }
    void grow() {
        vector<uint32_t> old; old.swap(tab); size_t oc = cap; cap *= 2; tab.assign(cap, 0xFFFFFFFFu);
        for (size_t i = 0; i < oc; i++) if (old[i] != 0xFFFFFFFFu) {
            size_t j = h(&pool[(size_t)old[i] * W], W) & (cap - 1);
            while (tab[j] != 0xFFFFFFFFu) j = (j + 1) & (cap - 1);
            tab[j] = old[i];
        }
    }
    long find(const u64* k) const {
        size_t j = h(k, W) & (cap - 1);
        while (tab[j] != 0xFFFFFFFFu) { if (!memcmp(&pool[(size_t)tab[j] * W], k, 8 * W)) return tab[j]; j = (j + 1) & (cap - 1); }
        return -1;
    }
    // returns (id, inserted)
    pair<long, bool> insert(const u64* k) {
        if ((n + 1) * 2 > cap) grow();
        size_t j = h(k, W) & (cap - 1);
        while (tab[j] != 0xFFFFFFFFu) { if (!memcmp(&pool[(size_t)tab[j] * W], k, 8 * W)) return {tab[j], false}; j = (j + 1) & (cap - 1); }
        tab[j] = (uint32_t)n; pool.insert(pool.end(), k, k + W); return {(long)n++, true};
    }
    const u64* key(size_t id) const { return &pool[id * W]; }
};

static double now() { return chrono::duration<double>(chrono::steady_clock::now().time_since_epoch()).count(); }
static string outdir;
static int NTH = 1;

// expand the states [ids] of set A with plan P; insert results into B (may be A); returns new ids in B
static void expand(const KeySet& A, const vector<long>& ids, const Plan& P, int inFrom, vector<vector<u64>>& res, long long& nodes) {
    res.assign(NTH, {});
    atomic<size_t> next(0); vector<long long> nd(NTH, 0);
    vector<thread> th;
    for (int w = 0; w < NTH; w++) th.emplace_back([&, w]() {
        Solver sv(P);
        while (true) {
            size_t i = next.fetch_add(1); if (i >= ids.size()) break;
            sv.run(A.key(ids[i]), inFrom, res[w]);
        }
        nd[w] = sv.nodes;
    });
    for (auto& t : th) t.join();
    for (auto x : nd) nodes += x;
}

static bool loadLayer(const string& fn, vector<u64>& keys) {
    FILE* f = fopen(fn.c_str(), "rb"); if (!f) return false;
    u64 n; if (fread(&n, 8, 1, f) != 1) { fclose(f); return false; }
    keys.resize(n * W); size_t r = fread(keys.data(), 8, n * W, f); fclose(f);
    return r == n * W;
}
static void saveLayer(const string& fn, const u64* keys, size_t n) {
    string tmp = fn + ".tmp"; FILE* f = fopen(tmp.c_str(), "wb"); u64 nn = n; fwrite(&nn, 8, 1, f); fwrite(keys, 8, n * W, f); fclose(f);
    remove(fn.c_str()); rename(tmp.c_str(), fn.c_str());
}

// BFS: from start key, plan P (forward: in slot 0, out slot 2; backward: in slot 2, out slot 0); layers saved
static void bfs(KeySet& K, vector<int>& depth, const u64* start, const Plan& P, int inFrom, int D, const string& tag) {
    K.init(1 << 16); depth.clear();
    K.insert(start); depth.push_back(0);
    vector<long> frontier = {0};
    for (int d = 1; d <= D; d++) {
        string fn = outdir + "/" + tag + "_layer" + to_string(d) + ".bin";
        vector<u64> keys; double t0 = now(); long long nodes = 0; bool loaded = loadLayer(fn, keys);
        if (!loaded) {
            vector<vector<u64>> res; expand(K, frontier, P, inFrom, res, nodes);
            for (auto& r : res) keys.insert(keys.end(), r.begin(), r.end());
        }
        vector<long> nf; vector<u64> newkeys;
        for (size_t i = 0; i < keys.size() / W; i++) {
            auto pr = K.insert(&keys[i * W]);
            if (pr.second) { depth.push_back(d); nf.push_back(pr.first); newkeys.insert(newkeys.end(), &keys[i * W], &keys[i * W] + W); }
        }
        if (!loaded) saveLayer(fn, keys.data(), keys.size() / W);
        printf("%s depth %d: %zu edges out of the frontier, %zu new states, %zu in all; %.1f s, %lld nodes%s\n", tag.c_str(), d,
               keys.size() / W, nf.size(), K.n, now() - t0, nodes, loaded ? " (from checkpoint)" : "");
        fflush(stdout);
        frontier.swap(nf);
        if (frontier.empty()) { printf("%s: closed at depth %d (no new states)\n", tag.c_str(), d); break; }
    }
}

int main(int argc, char** argv) {
    if (argc < 7) { fprintf(stderr, "usage: ends7 GEO OUTDIR DF DB LMAX THREADS\n"); return 1; }
    setvbuf(stdout, NULL, _IONBF, 0);
    outdir = argv[2]; int DF = atoi(argv[3]), DB = atoi(argv[4]), LMAX = atoi(argv[5]); NTH = atoi(argv[6]);
    FILE* f = fopen(argv[1], "r"); if (!f) { perror("geo"); return 1; }
    if (fscanf(f, "%d %d %d %d", &T, &S, &nE, &nO) != 4) return 1;
    nbE.resize(nE); nbO.resize(nO);
    for (int t = 0; t < 2; t++) for (int c = 0; c < (t ? nO : nE); c++) {
        int k; if (fscanf(f, "%d", &k) != 1) return 1;
        for (int j = 0; j < k; j++) { Nb q; if (fscanf(f, "%d %d %d", &q.du, &q.typ, &q.idx) != 3) return 1; (t ? nbO : nbE)[c].push_back(q); }
    }
    char buf[8192]; if (fscanf(f, "%8191s", buf) != 1) return 1; trainBits = buf; fclose(f);
    int off = 0;
    for (int i = 0; i < 10; i++) { int ns_i = (i & 1) ? nO : nE; slotN[i] = ns_i; slotOff[i] = off; off += ns_i * T; }
    NB5 = off; stateBits = (2 * nE + nO) * T; W = (stateBits + 63) / 64;
    if ((int)trainBits.size() != stateBits) { fprintf(stderr, "train bits %zu != %d\n", trainBits.size(), stateBits); return 1; }
    buildFeas();
    // forward: known E_{-1} O_{-1} E_0 (slots 2,3,4); unknown O_0 E_1 (5,6); full rules O_{-1} E_0 O_0; lookahead E_1
    // backward: known E_0 O_0 E_1 (4,5,6); unknown E_{-1} O_{-1} (2,3); full rules O_{-1} E_0 O_0; lookahead E_{-1}
    makePlan(planF, {3, 4, 5, 6}, {5, 6}, 4); makePlan(planB, {2, 3, 4, 5}, {2, 3}, 2);
    printf("T=%d s=%d nE=%d nO=%d: state %d bits (%d words), %zu constraints per edge, %zu/%zu unknown bits fwd/bwd\n",
           T, S, nE, nO, stateBits, W, planF.cons.size(), planF.vars.size(), planB.vars.size());
    vector<u64> trainK(W, 0), zeroK(W, 0);
    for (int b = 0; b < stateBits; b++) if (trainBits[b] == '1') trainK[b >> 6] |= 1ULL << (b & 63);
    // sanity: TRAIN -> TRAIN and ZERO -> ZERO are edges
    {
        Solver sv(planF); vector<u64> o; sv.run(trainK.data(), 2, o);
        bool self = false; for (size_t i = 0; i < o.size() / W; i++) if (!memcmp(&o[i * W], trainK.data(), 8 * W)) self = true;
        printf("train: %zu successors, self-loop %s\n", o.size() / W, self ? "yes" : "NO");
        if (!self) return 2;

        Solver sz(planF); vector<u64> o3; sz.run(zeroK.data(), 2, o3);
        bool zs = false; for (size_t i = 0; i < o3.size() / W; i++) if (!memcmp(&o3[i * W], zeroK.data(), 8 * W)) zs = true;
        printf("zero: %zu successors, self-loop %s\n", o3.size() / W, zs ? "yes" : "NO");
        if (!zs) return 2;
    }
    double t0 = now();
    KeySet KF, KB; vector<int> dF, dB;
    bfs(KF, dF, trainK.data(), planF, 2, DF, "fwd");
    bfs(KB, dB, zeroK.data(), planB, 4, DB, "bwd");
    // union and its edges
    KeySet U; U.init(1 << 16);
    vector<int> inF, inB;
    for (size_t i = 0; i < KF.n; i++) { auto p = U.insert(KF.key(i)); (void)p; }
    for (size_t i = 0; i < KB.n; i++) U.insert(KB.key(i));
    size_t N = U.n;
    vector<long> all(N); for (size_t i = 0; i < N; i++) all[i] = i;
    vector<vector<u64>> res; long long nodes = 0;
    // successors of every union state, in chunks per thread, keeping ids
    vector<vector<pair<uint32_t,uint32_t>>> E(NTH);
    {
        atomic<size_t> next(0); vector<thread> th;
        for (int w = 0; w < NTH; w++) th.emplace_back([&, w]() {
            Solver sv(planF); vector<u64> o;
            while (true) {
                size_t i = next.fetch_add(1); if (i >= N) break;
                o.clear(); sv.run(U.key(i), 2, o);
                for (size_t j = 0; j < o.size() / W; j++) { long id = U.find(&o[j * W]); if (id >= 0) E[w].push_back({(uint32_t)i, (uint32_t)id}); }
            }
        });
        for (auto& t : th) t.join();
    }
    vector<vector<uint32_t>> succ(N), pred(N);
    size_t ne = 0;
    for (auto& v : E) for (auto& e : v) { succ[e.first].push_back(e.second); pred[e.second].push_back(e.first); ne++; }
    long tid = U.find(trainK.data()), zid = U.find(zeroK.data());
    // distances: from train (forward), to zero (backward)
    vector<int> df(N, 1 << 29), db(N, 1 << 29);
    { vector<uint32_t> q = {(uint32_t)tid}; df[tid] = 0; for (size_t h = 0; h < q.size(); h++) for (auto v : succ[q[h]]) if (df[v] > df[q[h]] + 1) { df[v] = df[q[h]] + 1; q.push_back(v); } }
    { vector<uint32_t> q = {(uint32_t)zid}; db[zid] = 0; for (size_t h = 0; h < q.size(); h++) for (auto v : pred[q[h]]) if (db[v] > db[q[h]] + 1) { db[v] = db[q[h]] + 1; q.push_back(v); } }
    vector<char> useful(N, 0); size_t nu = 0;
    for (size_t i = 0; i < N; i++) if (df[i] < (1 << 29) && db[i] < (1 << 29)) { useful[i] = 1; nu++; }
    printf("union: %zu states, %zu edges; useful (train -> state -> zero inside the union): %zu; %.1f s\n", N, ne, nu, now() - t0);
    // cycles among useful states other than the two self-loops: Tarjan-free check via iterative peeling
    {
        vector<int> indeg(N, 0); size_t m = 0;
        for (size_t i = 0; i < N; i++) if (useful[i] && (long)i != tid && (long)i != zid) {
            for (auto v : succ[i]) if (useful[v] && (long)v != tid && (long)v != zid) indeg[v]++;
            m++;
        }
        vector<uint32_t> q; for (size_t i = 0; i < N; i++) if (useful[i] && (long)i != tid && (long)i != zid && indeg[i] == 0) q.push_back(i);
        for (size_t h = 0; h < q.size(); h++) for (auto v : succ[q[h]]) if (useful[v] && (long)v != tid && (long)v != zid && --indeg[v] == 0) q.push_back(v);
        printf("useful states other than train and zero: %zu; on or downstream of a cycle among them: %zu\n", m, m - q.size());
        // edges back into train from useful states (standing defects in the train)
        size_t back = 0; for (size_t i = 0; i < N; i++) if (useful[i] && (long)i != tid) for (auto v : succ[i]) if ((long)v == tid) back++;
        printf("edges from a useful state back to the train: %zu\n", back);
    }
    // write useful states
    {
        string fn = outdir + "/states.txt"; FILE* g = fopen(fn.c_str(), "w");
        for (size_t i = 0; i < N; i++) if (useful[i]) {
            fprintf(g, "%zu %d %d ", i, df[i], db[i]);
            const u64* k = U.key(i); for (int b = 0; b < stateBits; b++) fputc('0' + ((k[b >> 6] >> (b & 63)) & 1), g);
            fputc('\n', g);
        }
        fclose(g);
    }
    // enumerate ends: TRAIN -> S_1 (!= TRAIN) ... S_k -> ZERO, k <= LMAX, S_i != ZERO
    vector<long long> byk(LMAX + 2, 0);
    string fn = outdir + "/ends.txt"; FILE* g = fopen(fn.c_str(), "w");
    vector<uint32_t> path; long long nends = 0;
    // iterative DFS
    struct Fr { uint32_t s; size_t j; };
    for (auto s1 : succ[tid]) {
        if ((long)s1 == tid || !useful[s1] || (long)s1 == zid) continue;   // (TRAIN -> ZERO directly would be k = 0)
        vector<Fr> st = {{s1, 0}}; path = {s1};
        while (!st.empty()) {
            Fr& fr = st.back(); uint32_t s = fr.s;
            if (fr.j == 0) {
                // does s go to zero?
                for (auto v : succ[s]) if ((long)v == zid) { int k = path.size(); byk[k]++; nends++;
                    fprintf(g, "%d", k); for (auto p : path) fprintf(g, " %u", p); fputc('\n', g); }
            }
            bool pushed = false;
            while (fr.j < succ[s].size()) {
                uint32_t v = succ[s][fr.j++];
                if ((long)v == zid || !useful[v]) continue;
                if ((int)path.size() + db[v] > LMAX) continue;     // db[v] >= 1 more states incl. v... (v then >= db[v]-1 more)
                st.push_back({v, 0}); path.push_back(v); pushed = true; break;
            }
            if (!pushed) { st.pop_back(); path.pop_back(); }
        }
    }
    fclose(g);
    printf("ends with k <= %d: %lld; by k:", LMAX, nends);
    for (int k = 1; k <= LMAX; k++) printf(" %d:%lld", k, byk[k]);
    printf("\ntotal %.1f s\n", now() - t0);
    // also: does TRAIN reach ZERO directly?
    for (auto v : succ[tid]) if ((long)v == zid) printf("note: TRAIN -> ZERO is an edge (k = 0 end)\n");
    return 0;
}
