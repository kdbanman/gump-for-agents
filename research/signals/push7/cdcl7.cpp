// cdcl7: a small CDCL SAT solver (MiniSat-style) with projected all-solutions enumeration (push 7).
// Written because no SAT solver is installed on this machine.  Two watched literals, 1UIP learning with clause
// minimisation, VSIDS, phase saving (default phase false), Luby restarts, LBD-based clause deletion.
//
//   cdcl7 CNF PROJ SOLS [SECONDS] [CUBE]
//
// CNF: DIMACS.  PROJ: whitespace-separated variable ids (the projection: generation-0 free cells).  SOLS: output, one
// line per solution "S <bits>" (the projection variables' values, '0'/'1', in PROJ order), and a final line "DONE n"
// when the enumeration is complete (the formula plus the blocking clauses is UNSAT) or "TIMEOUT n".  If SOLS already
// exists, its S lines are read back and blocked first, so a stopped run resumes where it was (checkpoint); a file
// ending in DONE is left alone.  CUBE (optional): a file of literals forced as unit clauses (a part of the search).
// Every solution is checked against every original clause before it is written.
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <string>
#include <algorithm>
#include <chrono>
#include <cmath>
using namespace std;

static double now() { return chrono::duration<double>(chrono::steady_clock::now().time_since_epoch()).count(); }

struct Clause { int lbd; float act; bool learnt; bool del; vector<int> lits; };
struct Watch { Clause* c; int blocker; };

struct Solver {
    int nv = 0;
    vector<Clause*> clauses, learnts;
    vector<vector<Watch>> watches;   // by literal index (2v+neg): clauses watching ~lit... we watch lit, visit when lit becomes false
    vector<signed char> assign;      // per var: -1 unassigned, 0 false, 1 true
    vector<int> level, trail, trailLim; vector<Clause*> reason;
    vector<double> act; double varInc = 1, claInc = 1; vector<char> phase, seen;
    vector<int> heap, heapPos; size_t qhead = 0; bool ok = true;
    long long conflicts = 0, decisions = 0, props = 0;

    static int lv(int l) { return l >> 1; }
    static int neg(int l) { return l ^ 1; }
    inline int val(int l) const { int a = assign[l >> 1]; return a < 0 ? -1 : (a ^ (l & 1)); }
    void init(int n) {
        nv = n; watches.assign(2 * n + 2, {}); assign.assign(n + 1, -1); level.assign(n + 1, 0); reason.assign(n + 1, nullptr);
        act.assign(n + 1, 0); phase.assign(n + 1, 0); seen.assign(n + 1, 0); heapPos.assign(n + 1, -1);
        for (int v = 1; v <= n; v++) heapInsert(v);
    }
    // heap
    bool hless(int a, int b) { return act[a] > act[b]; }
    void up(int i) { int v = heap[i]; while (i > 0) { int p = (i - 1) / 2; if (!hless(v, heap[p])) break; heap[i] = heap[p]; heapPos[heap[i]] = i; i = p; } heap[i] = v; heapPos[v] = i; }
    void down(int i) { int v = heap[i]; int n = heap.size(); while (true) { int c = 2 * i + 1; if (c >= n) break; if (c + 1 < n && hless(heap[c + 1], heap[c])) c++; if (!hless(heap[c], v)) break; heap[i] = heap[c]; heapPos[heap[i]] = i; i = c; } heap[i] = v; heapPos[v] = i; }
    void heapInsert(int v) { if (heapPos[v] >= 0) return; heap.push_back(v); heapPos[v] = heap.size() - 1; up(heap.size() - 1); }
    int heapPop() { int v = heap[0]; int last = heap.back(); heap.pop_back(); heapPos[v] = -1; if (!heap.empty()) { heap[0] = last; heapPos[last] = 0; down(0); } return v; }
    void bump(int v) { act[v] += varInc; if (act[v] > 1e100) { for (int i = 1; i <= nv; i++) act[i] *= 1e-100; varInc *= 1e-100; } if (heapPos[v] >= 0) up(heapPos[v]); }
    void bumpC(Clause* c) { c->act += claInc; if (c->act > 1e20) { for (auto x : learnts) x->act *= 1e-20; claInc *= 1e-20; } }

    int dl() const { return trailLim.size(); }
    void enqueue(int l, Clause* r) { int v = l >> 1; assign[v] = (l & 1) ^ 1; level[v] = dl(); reason[v] = r; trail.push_back(l); }
    void attach(Clause* c) { watches[neg(c->lits[0])].push_back({c, c->lits[1]}); watches[neg(c->lits[1])].push_back({c, c->lits[0]}); }

    // add an original or blocking clause at level 0
    bool addClause(vector<int> ls, bool learnt = false) {
        if (!ok) return false;
        sort(ls.begin(), ls.end()); ls.erase(unique(ls.begin(), ls.end()), ls.end());
        vector<int> out;
        for (size_t i = 0; i < ls.size(); i++) {
            if (i + 1 < ls.size() && ls[i + 1] == neg(ls[i])) return true;   // tautology (l and ~l adjacent after sort)
            int v = val(ls[i]);
            if (v == 1 && level[ls[i] >> 1] == 0) return true;
            if (v == 0 && level[ls[i] >> 1] == 0) continue;
            out.push_back(ls[i]);
        }
        if (out.empty()) { ok = false; return false; }
        if (out.size() == 1) { if (val(out[0]) == 0) { ok = false; return false; } if (val(out[0]) < 0) enqueue(out[0], nullptr); if (propagate()) { ok = false; return false; } return true; }
        Clause* c = new Clause{0, 0, learnt, false, out}; clauses.push_back(c); attach(c); return true;
    }
    Clause* propagate() {
        while (qhead < trail.size()) {
            int p = trail[qhead++]; props++;   // p became true; visit clauses watching ~p, i.e. watches[p]
            vector<Watch>& ws = watches[p];
            size_t i = 0, j = 0;
            while (i < ws.size()) {
                Watch w = ws[i];
                if (val(w.blocker) == 1) { ws[j++] = ws[i++]; continue; }
                Clause* c = w.c;
                if (c->del) { i++; continue; }
                vector<int>& L = c->lits; int fl = neg(p);
                if (L[0] == fl) swap(L[0], L[1]);
                i++;
                if (val(L[0]) == 1) { ws[j++] = {c, L[0]}; continue; }
                bool found = false;
                for (size_t k = 2; k < L.size(); k++) if (val(L[k]) != 0) {
                    swap(L[1], L[k]); watches[neg(L[1])].push_back({c, L[0]}); found = true; break;
                }
                if (found) continue;
                ws[j++] = {c, L[0]};
                if (val(L[0]) == 0) { while (i < ws.size()) ws[j++] = ws[i++]; ws.resize(j); qhead = trail.size(); return c; }
                enqueue(L[0], c);
            }
            ws.resize(j);
        }
        return nullptr;
    }
    void cancel(int lvl) {
        if (dl() <= lvl) return;
        for (int i = trail.size() - 1; i >= trailLim[lvl]; i--) { int v = trail[i] >> 1; phase[v] = assign[v]; assign[v] = -1; reason[v] = nullptr; heapInsert(v); }
        trail.resize(trailLim[lvl]); trailLim.resize(lvl); qhead = trail.size();
    }
    bool redundant(int l, uint32_t abst, vector<int>& toClear) {
        vector<int> st = {l}; size_t top = toClear.size();
        while (!st.empty()) {
            int q = st.back(); st.pop_back(); Clause* r = reason[q >> 1];
            for (size_t i = 1; i < r->lits.size(); i++) {
                int x = r->lits[i]; int v = x >> 1;
                if (!seen[v] && level[v] > 0) {
                    if (reason[v] && ((1u << (level[v] & 31)) & abst)) { seen[v] = 1; st.push_back(x); toClear.push_back(x); }
                    else { for (size_t k = top; k < toClear.size(); k++) seen[toClear[k] >> 1] = 0; toClear.resize(top); return false; }
                }
            }
        }
        return true;
    }
    void analyze(Clause* confl, vector<int>& out, int& btl, int& lbd) {
        out.clear(); out.push_back(-1); int pathC = 0; int p = -1; int idx = trail.size() - 1;
        do {
            if (confl->learnt) bumpC(confl);
            for (size_t k = (p == -1 ? 0 : 1); k < confl->lits.size(); k++) {
                int q = confl->lits[k]; int v = q >> 1;
                if (!seen[v] && level[v] > 0) { seen[v] = 1; bump(v); if (level[v] >= dl()) pathC++; else out.push_back(q); }
            }
            while (!seen[trail[idx] >> 1]) idx--;
            p = trail[idx]; confl = reason[p >> 1]; seen[p >> 1] = 0; pathC--; idx--;
            if (pathC > 0 && confl->lits[0] != p) { auto it = find(confl->lits.begin(), confl->lits.end(), p); swap(*it, confl->lits[0]); }
        } while (pathC > 0);
        out[0] = neg(p);
        // minimisation
        uint32_t abst = 0; for (size_t i = 1; i < out.size(); i++) abst |= 1u << (level[out[i] >> 1] & 31);
        vector<int> toClear(out.begin(), out.end()); size_t j = 1;
        for (size_t i = 1; i < out.size(); i++) { int v = out[i] >> 1; if (!reason[v] || !redundant(out[i], abst, toClear)) out[j++] = out[i]; }
        out.resize(j);
        for (int x : toClear) seen[x >> 1] = 0;
        for (int x : out) seen[x >> 1] = 0;
        if (out.size() == 1) btl = 0;
        else { size_t mi = 1; for (size_t i = 2; i < out.size(); i++) if (level[out[i] >> 1] > level[out[mi] >> 1]) mi = i; swap(out[1], out[mi]); btl = level[out[1] >> 1]; }
        vector<int> lv2; for (int x : out) lv2.push_back(level[x >> 1]); sort(lv2.begin(), lv2.end()); lbd = unique(lv2.begin(), lv2.end()) - lv2.begin();
    }
    void reduceDB() {
        vector<Clause*> keep, cand;
        for (auto c : learnts) { if (c->del) continue; bool locked = val(c->lits[0]) == 1 && reason[c->lits[0] >> 1] == c; if (c->lbd <= 2 || locked) keep.push_back(c); else cand.push_back(c); }
        sort(cand.begin(), cand.end(), [](Clause* a, Clause* b) { return a->lbd != b->lbd ? a->lbd > b->lbd : a->act < b->act; });
        size_t half = cand.size() / 2;
        for (size_t i = 0; i < cand.size(); i++) { if (i < half) cand[i]->del = true; else keep.push_back(cand[i]); }
        learnts.swap(keep);
        // purge watches of deleted clauses
        for (auto& ws : watches) { size_t j = 0; for (size_t i = 0; i < ws.size(); i++) if (!ws[i].c->del) ws[j++] = ws[i]; ws.resize(j); }
        for (auto c : cand) if (c->del) delete c;
    }
    static double luby(double y, int x) { int size, seq; for (size = 1, seq = 0; size < x + 1; seq++, size = 2 * size + 1); while (size - 1 != x) { size = (size - 1) >> 1; seq--; x = x % size; } return pow_(y, seq); }
    static double pow_(double y, int s) { double r = 1; while (s-- > 0) r *= y; return r; }
    // returns 1 SAT, 0 UNSAT, -1 timeout
    int solve(double deadline) {
        if (!ok) return 0;
        if (propagate()) { ok = false; return 0; }
        int curr = 0; long long nextReduce = 4000;
        while (true) {
            long long budget = (long long)(luby(2, curr++) * 100);
            long long c0 = conflicts;
            while (true) {
                Clause* confl = propagate();
                if (confl) {
                    conflicts++;
                    if (dl() == 0) { ok = false; return 0; }
                    vector<int> lc; int btl, lbd; analyze(confl, lc, btl, lbd);
                    cancel(btl);
                    if (lc.size() == 1) enqueue(lc[0], nullptr);
                    else { Clause* c = new Clause{lbd, 0, true, false, lc}; learnts.push_back(c); attach(c); bumpC(c); enqueue(lc[0], c); }
                    varInc /= 0.95; claInc /= 0.999;
                    if ((conflicts & 1023) == 0 && now() > deadline) return -1;
                } else {
                    if (conflicts - c0 >= budget) { cancel(0); break; }
                    if (conflicts >= nextReduce) { reduceDB(); nextReduce = conflicts + 4000 + 300 * (long long)sqrt((double)conflicts); }
                    int next = -1;
                    while (!heap.empty()) { int v = heapPop(); if (assign[v] < 0) { next = v; break; } }
                    if (next < 0) return 1;
                    decisions++; trailLim.push_back(trail.size()); enqueue(2 * next + (phase[next] ? 0 : 1), nullptr);
                }
            }
        }
    }
};

int main(int argc, char** argv) {
    setvbuf(stdout, NULL, _IONBF, 0);
    if (argc < 4) { fprintf(stderr, "usage: cdcl7 CNF PROJ SOLS [SECONDS] [CUBE]\n"); return 1; }
    double secs = argc > 4 ? atof(argv[4]) : 1e18; double t0 = now(), deadline = t0 + secs;
    FILE* f = fopen(argv[1], "r"); if (!f) { perror("cnf"); return 1; }
    int nv = 0, nc = 0; char line[1 << 16];
    vector<vector<int>> orig;
    vector<int> cur;
    while (fscanf(f, " %[^\n]", line) == 1) {
        if (line[0] == 'c') continue;
        if (line[0] == 'p') { sscanf(line, "p cnf %d %d", &nv, &nc); continue; }
        char* s = line; while (*s) { char* e; long x = strtol(s, &e, 10); if (e == s) break; s = e; if (x == 0) { orig.push_back(cur); cur.clear(); } else cur.push_back((int)x); }
    }
    fclose(f);
    auto L = [](int x) { return x > 0 ? 2 * x : 2 * (-x) + 1; };
    vector<int> proj; f = fopen(argv[2], "r"); int x; while (fscanf(f, "%d", &x) == 1) proj.push_back(x); fclose(f);
    Solver S; S.init(nv);
    for (auto& c : orig) { vector<int> ls; for (int y : c) ls.push_back(L(y)); S.addClause(ls); }
    if (argc > 5) { f = fopen(argv[5], "r"); while (fscanf(f, "%d", &x) == 1) S.addClause({L(x)}); fclose(f); }
    // resume
    long long nsol = 0;
    f = fopen(argv[3], "r");
    if (f) {
        while (fscanf(f, " %[^\n]", line) == 1) {
            if (line[0] == 'D') { printf("already complete: %s\n", line); fclose(f); return 0; }
            if (line[0] == 'S') { vector<int> bl; const char* b = line + 2; for (size_t i = 0; i < proj.size(); i++) bl.push_back(L(b[i] == '1' ? -proj[i] : proj[i])); S.addClause(bl); nsol++; }
        }
        fclose(f);
        // drop a trailing TIMEOUT line by rewriting the file without it
        FILE* g = fopen(argv[3], "r"); string keep; while (fscanf(g, " %[^\n]", line) == 1) if (line[0] == 'S') { keep += line; keep += '\n'; } fclose(g);
        g = fopen(argv[3], "w"); fputs(keep.c_str(), g); fclose(g);
        printf("resumed with %lld solutions blocked\n", nsol);
    }
    FILE* out = fopen(argv[3], "a");
    printf("%d vars, %zu clauses, %zu projection vars\n", nv, orig.size(), proj.size());
    while (true) {
        int r = S.solve(deadline);
        if (r == -1) { fprintf(out, "TIMEOUT %lld\n", nsol); fclose(out); printf("TIMEOUT after %lld solutions, %.0f s, %lld conflicts\n", nsol, now() - t0, S.conflicts); return 3; }
        if (r == 0) { fprintf(out, "DONE %lld\n", nsol); fclose(out); printf("DONE: %lld solutions, %.1f s, %lld conflicts\n", nsol, now() - t0, S.conflicts); return 0; }
        // check the model against every original clause
        for (auto& c : orig) { bool sat = false; for (int y : c) if (S.val(L(y)) == 1) { sat = true; break; } if (!sat) { fprintf(stderr, "MODEL CHECK FAILED\n"); return 4; } }
        string bits; vector<int> bl;
        for (int p : proj) { bool t = S.val(L(p)) == 1; bits += t ? '1' : '0'; bl.push_back(L(t ? -p : p)); }
        fprintf(out, "S %s\n", bits.c_str()); fflush(out); nsol++;
        printf("solution %lld at %.1f s (%lld conflicts)\n", nsol, now() - t0, S.conflicts);
        S.cancel(0);
        if (bl.empty() || !S.addClause(bl)) { fprintf(out, "DONE %lld\n", nsol); fclose(out); printf("DONE: %lld solutions\n", nsol); return 0; }
    }
}
