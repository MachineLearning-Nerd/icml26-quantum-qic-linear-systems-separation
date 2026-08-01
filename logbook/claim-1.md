# Claim 1 — QIC lower bound versus quantum upper bound

**Exact live claim:** Theorem 1 proves an \(\Omega(n^{1/12})\) QIC-query lower bound for well-conditioned sparse linear systems while the corresponding quantum algorithm runs in polylogarithmic time.

## Attempt 1 — local random-walk oracle toy

The pinned source reduces its QIC lower-bound route to Childs-style random walks on two height-\(n\) perfect binary trees whose leaves are connected by a random alternating cycle (`evidence/source/arxiv_source.tar.gz`, `lower.tex:4-18`). We independently implemented a finite height-4 clean-room version with neighbor-oracle random walks, five fixed graph/walk seeds, 10,000 walks per seed, and 256 steps per walk.

Command:

```bash
.venv/bin/python src/claim1_random_walk_oracle_fixture.py --out outputs/claim1_random_walk_oracle_fixture
(cd outputs/claim1_random_walk_oracle_fixture && sha256sum -c SHA256SUMS)
```

The connected alternating-cycle fixture reached the second-tree root with mean probability **0.78006**. The destructive control removes every cross-tree cycle edge and reached that root with probability **0.0** across all seeds. Raw rows, configuration, command log, and hashes are retained in `outputs/claim1_random_walk_oracle_fixture/`; `tests/test_claim1_random_walk_oracle.py` checks the construction, deterministic execution, and control.

**Verdict: toy.** This executes the reduced oracle-game mechanism and its negative control, but does not prove the universal \(\Omega(n^{1/12})\) QIC query lower bound or reproduce a quantum runtime.
