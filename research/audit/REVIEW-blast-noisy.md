# Audit of `research/blast/noisy/` (pull request 39): the noisy hull chain and its sampler

2026-11-18. Subject: pull request 39 at a879e34 (`research/blast/noisy/`, and the entries of 14:57 and 16:40 UTC in
`research/blast/REPORT.md`); from its later head b80248c only the committed rows (`noisy/data/runs/`, 63, 84 and
108 cells) and the diff of `nz.c` were used. Everything built here is in `research/audit/blastnoisy/` (code, `run.sh`
with every command and its run time, small tables in `data/`); bulk output is in `research/scratch/audit_noisy/`.
Marks: **[measured here]** = this audit's own code and runs; **[read]** = judged from the pull request's files;
**[rows]** = computed here from the pull request's committed rows.

DRAFT: numbers are being filled in.
