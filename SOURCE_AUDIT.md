# Source audit

## Paper identity

| Field | Record |
| --- | --- |
| Title | An Exponential Separation Between Quantum and Quantum-Inspired Classical Algorithms for Linear Systems |
| Authors | Allan Grønlund; Kasper Green Larsen |
| Primary source | arXiv:2411.02087 |
| OpenReview record | eTUljZ6e8c |
| Submission number | 11696 |
| Venue record | ICML 2026 |
| Pinned source retrieval | 2026-08-01 |
| Public record note | arXiv v5 is dated 2025-12-02; this audit does not silently replace the pinned snapshot |
| PDF SHA-256 | 581d57e998439c2ad73b68f02dcf62fb3a54c655f6d8903c4767de2ce3968a70 |
| LaTeX source archive SHA-256 | 1729ecf6489a345ff10b6433ce8256a9bc88028dcf68b469e0dd2de50e223eb6 |
| Contract manifest SHA-256 | a5fe8f32a92be2d7bda9647535221a7d551b0f7cf76cb40c082340f1d4fe499f |

The exact local inputs are evidence/source/arxiv.pdf and
evidence/source/arxiv_source.tar.gz. The source member used for the finite
mechanism audit is lower.tex, and the source inventory lists all archive
members.

## Claim anchors

| Claim | Source anchor | Local scope |
| --- | --- | --- |
| C1 | Theorem 1 | Finite random-walk mechanism only; the separation theorem remains unproved. |
| C2 | Equation 1 | Quantum scaling and precision audit not started. |
| C3 | Theorem 2 and Section 2.1 | Oracle-to-matrix reduction audit not started. |
| C4 | Lemma 2 | Target-root solution-mass and spectral audit not started. |
| C5 | Section 1 conclusion | End-to-end separation audit not started. |

The claim text used for this workspace is preserved in
contract/live_claims.json. Its Claim 1 wording uses the earlier
Omega(n^1/12) contract form; the source also discusses the parameterized
theorem and a separate k-Forrelation route. Those versions are disclosed
rather than merged into one unverified result.

## Implementation status

No author executable implementation, dataset, checkpoint, quantum backend, or
QIC runtime was identified in the pinned source archive. This repository
contains an independent source audit and finite clean-room oracle fixture, not
an official reproduction package.

## Repository identity

- Former repository:
  MachineLearning-Nerd/icml26-repro-eTUljZ6e8c-quantum-qic-linear-systems
- Canonical repository:
  MachineLearning-Nerd/icml26-quantum-qic-linear-systems-separation
- Canonical branch: main
- Repository homepage: https://arxiv.org/abs/2411.02087
