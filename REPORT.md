# Audit report

## Decision

**PARTIAL_TOY_ONLY**

The repository provides a finite height-4 two-tree random-walk oracle fixture
with a matched destructive control. This is useful evidence for a reduced
mechanism, but it is not a reproduction of the paper’s QIC lower bound,
quantum upper bound, or exponential separation.

## Claim decisions

- C1 is **TOY**: the connected fixture reaches the target root with mean
  probability 0.78006, while the disconnected control reaches it with 0.0.
- C2 is **UNVERIFIED**: no quantum runtime or scaling audit is committed.
- C3 is **UNVERIFIED**: no independent oracle-to-matrix reduction audit is
  committed.
- C4 is **UNVERIFIED**: no target-root solution-mass or spectral certificate is
  committed.
- C5 is **UNVERIFIED**: no end-to-end quantum-versus-QIC comparison is
  committed.

## Evaluation boundary

No judge score, external logbook score, official author implementation, or
author endorsement is claimed. The pinned source and local finite output
checksums are the reproducibility boundary. The current arXiv v5 note is
disclosed as version context, not used to rewrite the pinned snapshot.

## Publication state

The repository uses the canonical
icml26-quantum-qic-linear-systems-separation name, a single documented main
branch, canonical MachineLearning-Nerd attribution, a claim-to-evidence
dossier, citation, author thanks, content manifest, and fail-closed verifier.
