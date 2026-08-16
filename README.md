# An Exponential Separation Between Quantum and Quantum-Inspired Classical Algorithms for Linear Systems

Independent claim audit and clean-room reproduction workspace for:

> Allan Grønlund and Kasper Green Larsen, “An Exponential Separation Between Quantum and Quantum-Inspired Classical Algorithms for Linear Systems.”

Paper: [arXiv:2411.02087](https://arxiv.org/abs/2411.02087) · [HTML paper](https://arxiv.org/html/2411.02087) · [OpenReview record](https://openreview.net/forum?id=eTUljZ6e8c)

This is an independent reproduction/audit repository, not an author-maintained implementation. The pinned source archive and PDF were retrieved on 2026-08-01. The current arXiv record is v5 (2025-12-02); the local challenge contract contains the five claims audited below.

## Current status

**Overall: partial, toy-level evidence only.**

Machine-readable status labels are TOY and UNVERIFIED; neither label claims a
full theorem reproduction.

Claim 1 has a finite random-walk oracle fixture. It builds two height-4 binary trees joined by an alternating leaf cycle, runs five fixed-seed batches of 10,000 walks for 256 steps, and includes a destructive disconnected control. This checks a reduced graph mechanism, not the QIC lower bound, the quantum algorithm, or the claimed exponential separation. Claims 2–5 have not been independently reproduced.

## Audit dossier

The standardized audit record is split into reviewable files:

- CLAIM_EVIDENCE.md maps each claim to its producer, evidence, status, and limitation.
- SOURCE_AUDIT.md pins the paper snapshot, contract, source inventory, and claim anchors.
- BRANCH_AUDIT.md records the final branch map and commit attribution.
- ENVIRONMENT.md records the fixed local command, checksums, and compute boundary.
- REPORT.md states the scoped decision and what remains unverified.
- CITATION.cff and AUTHOR_THANK_YOU.md provide citation and author acknowledgement.
- EVIDENCE_MANIFEST.json content-addresses the dossier and source/evidence inputs.
- verify_final.py performs fail-closed checks on a local or fresh clone.

The dossier is a documentation and provenance publication. It does not change
the Claim 1 toy verdict or imply that Claims 2–5 have been reproduced.

| Paper claim | Repository status | What the evidence supports |
| --- | --- | --- |
| Theorem 1: QIC algorithms require a polynomial/exponential-in-input-dimension query lower bound while quantum linear-system algorithms are polylogarithmic in the dimension under the stated promises | **Toy only** | The finite oracle fixture is compatible with the random-walk intuition; it does not construct a hard matrix, simulate a QIC algorithm, or prove a query lower bound. |
| Equation 1: quantum upper-bound scaling in sparsity, condition number, precision, and dimension | **Unverified** | `outputs/claim1_source_audit/result.json` records a finite source audit of the variables; no quantum runtime was implemented. |
| Theorem 2 / Section 2.1: hardness reduces to a random-walk oracle game on two binary trees | **Unverified** | The finite graph is a mechanism diagnostic only; the oracle-to-matrix reduction and its query accounting are not independently proved. |
| Lemma 2: the target-root solution component has squared mass `Omega(n^-5)` relative to the solution norm | **Unverified** | No independent spectral or linear-system calculation has been completed. |
| Section 1: the result establishes a first natural exponential quantum-versus-QIC separation | **Unverified** | No end-to-end comparison of QIC queries and quantum runtime is present. |

The local contract phrases Claim 1 as an `Omega(n^{1/12})` QIC lower bound. The current arXiv v5 theorem is parameterized by `k` and states a stronger-looking `n^{1-1/k}` form under its stated constants and promises. This repository has not independently reconciled or verified the version-specific theorem statements.

## What the paper does

The paper studies the linear-systems problem in the sampling/query access model used by quantum-inspired classical (QIC) algorithms. Given a sparse, well-conditioned matrix `M` and a vector `y`, the task is to sample from an approximation to the solution `x = M^-1 y`, rather than to output all `n` coordinates.

The paper’s contribution is an unconditional separation:

- a quantum algorithm has polylogarithmic dependence on the dimension for the promised sparse, well-conditioned instances; and
- every QIC algorithm needs many oracle queries on some such instance.

The random-walk route starts with two perfect binary trees whose leaves are joined by a random alternating cycle. A classical algorithm receives only a label-neighbor oracle and must find the second tree’s root. The reduction encodes this graph into a sparse matrix `M = lambda I - A` on the graph block, chooses `lambda` near `sqrt(8)`, and uses the target-root coordinate of `M^-1 e_1` to turn a successful linear-system sampler into a successful random-walk solver. The paper also gives a separate `k`-Forrelation route.

## How claims become evidence here

```text
pinned arXiv source + OpenReview contract
        -> claim list and source inventory
        -> one scoped audit script per claim attempt
        -> JSON/CSV outputs plus checksums
        -> logbook entry and README verdict
```

For the completed Claim 1 attempt:

1. `evidence/source/` pins the paper PDF and source archive with SHA-256 checksums.
2. `evidence/source/source_inventory.txt` records the source files used for the local audit.
3. `src/claim1_source_audit.py` records a finite source-aligned fixture (`n=64`, sparsity at most 2, `kappa=4`, `epsilon=0.01`, and the quantum complexity variables). This is a source/parameter audit, not theorem verification.
4. `src/claim1_random_walk_oracle_fixture.py` builds two finite binary trees, optionally joins their leaves by an alternating cycle, and estimates target-root hit probability through neighbor queries.
5. `outputs/claim1_random_walk_oracle_fixture/` stores the configuration, raw per-seed results, summary, run log, and checksums.
6. `logbook/claim-1.md` records the exact command, result, control, and verdict.

## Claim 1 evidence

The fixture uses the local source’s random-walk mechanism at reduced scale:

| Check | Result |
| --- | --- |
| Tree height | 4 |
| Graph construction | Two perfect binary trees with an alternating cycle across 32 leaves |
| Connected fixture | Mean target-root hit probability 0.78006 across 5 graph/walk seeds |
| Walk budget | 10,000 walks per seed, 256 steps per walk |
| Negative control | Removing all cross-tree cycle edges gives target-root hit probability 0.0 in every row |
| Recorded rows | 10 total: 5 connected and 5 broken-control runs |
| Verdict | Finite mechanism toy only |

The connected fixture demonstrates that the constructed cross-tree connection changes reachability in the reduced oracle game. The zero-hit control is a construction sanity check. Neither result establishes the paper’s hard-instance distribution, the matrix reduction, the `Omega(n^{1/12})` or parameterized QIC lower bound, or any quantum runtime.

## Repository contents

| Path | Purpose |
| --- | --- |
| `contract/metadata.json` | OpenReview and paper metadata |
| `contract/live_claims.json` | Five claims used by this audit |
| `contract/contract_manifest.json` | Retrieval metadata and contract checksums |
| `evidence/source/` | Pinned arXiv PDF/source archive and source inventory |
| `src/` | Source audit and finite random-walk fixture |
| `outputs/` | Checked JSON/CSV results, logs, and checksums |
| `logbook/` | Claim-level audit notes |
| `STATUS.md` | Machine-readable project status summary |
| `AUTONOMOUS_STATE.json` | Handoff state for the next audit session |
| `branch-audit.md` | Branch and attribution audit |

No official executable code, dataset, or model checkpoint was identified in the pinned source archive. The reproduction is clean-room local CPU code and does not use paid, remote, or Hugging Face Job compute.

## Reproduce the completed attempt

From the repository root:

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python src/claim1_source_audit.py
.venv/bin/python src/claim1_random_walk_oracle_fixture.py \
  --out outputs/claim1_random_walk_oracle_fixture
(cd outputs/claim1_random_walk_oracle_fixture && sha256sum -c SHA256SUMS)
(cd evidence/source && sha256sum -c SHA256SUMS)
```

The fixture’s default run is the recorded configuration: height 4, 10,000 walks, 256 steps, and seeds `20260801` through `20260805`. The output directory is tracked so a reviewer can compare generated results with the recorded evidence.

## Branch map

Only `main` exists. It contains the source-pinned workspace, the finite Claim 1 fixture, its evidence, and this documentation. There are no historical `orx/*` branches or undocumented experiment branches. See [branch-audit.md](branch-audit.md) for the final branch and attribution audit.

## Citation

```bibtex
@article{gronlund2024exponential,
  title         = {An Exponential Separation Between Quantum and Quantum-Inspired Classical Algorithms for Linear Systems},
  author        = {Gr{\o}nlund, Allan and Larsen, Kasper Green},
  journal       = {arXiv preprint arXiv:2411.02087},
  year          = {2024},
  doi           = {10.48550/arXiv.2411.02087}
}
```

Please cite the paper using the version and venue information preferred by the authors when available.

## Thank you

Thank you to Allan Grønlund and Kasper Green Larsen for making this work available and for developing a precise, important separation result for quantum and quantum-inspired linear-system algorithms. This repository is an independent reproduction and audit intended to make the paper’s claims, evidence boundaries, and remaining work easy to inspect.

## Limitations and next work

- The height-4 random walk is a reduced diagnostic, not the paper’s asymptotic hard distribution.
- The fixture does not implement the QIC sampling/query model or a quantum linear-system algorithm.
- Claims 2, 4, and 5 need separate formula, spectral, and end-to-end audits.
- Theorem 2’s reduction needs an explicit proof-level audit connecting the oracle game to the constructed matrix.
- Results are CPU-local and are not a scaled replication of an author experiment.

The next appropriate step is an independent finite audit of the source’s matrix construction and Lemma 2’s target-root mass claim, while keeping the distinction between source inspection, mechanism evidence, and theorem verification.
