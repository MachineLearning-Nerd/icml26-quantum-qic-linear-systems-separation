# Claim-to-evidence map

The repository’s production graph is:

    pinned source and contract -> scoped claim contract
        -> executable producer -> committed output/checksum
        -> limitation and verdict

Only Claim 1 currently reaches an executable-producer stage, and even that
stage is a finite mechanism toy. Claims 2–5 are documented as unverified
rather than represented by guessed quantum or asymptotic experiments.

## Evidence boundary

- The five-claim contract is in contract/live_claims.json; retrieval metadata
  and contract hashes are in contract/contract_manifest.json.
- evidence/source/ pins the PDF, LaTeX source archive, and source inventory.
  The source snapshot was retrieved on 2026-08-01; the public arXiv record is
  now v5.
- Claim 1 has a source-parameter audit, a finite two-tree random-walk fixture,
  a destructive disconnected control, raw CSV rows, a run log, and checksums.
- Claims 2–5 have no independent producer, checker, raw result, or verdict
  beyond the unverified contract entries. The Claim 1 mechanism toy is not
  promoted into a proof of Theorem 2.
- No official executable implementation, dataset, checkpoint, quantum
  runtime, paid or remote compute run, judge score, or author endorsement is
  claimed.

## C1 — Theorem 1 separation

Paper anchor: Theorem 1.

Producer path:

1. src/claim1_source_audit.py records a finite source-aligned fixture with
   n=64, sparsity at most 2, kappa=4, epsilon=0.01, and the variables in the
   quantum upper-bound formula.
2. src/claim1_random_walk_oracle_fixture.py builds two height-4 perfect binary
   trees and joins their leaves with a shuffled alternating cycle.
3. Five fixed graph/walk seeds run 10,000 neighbor-oracle walks for 256 steps
   in the connected fixture and in a matched control with all cross-tree edges
   removed.
4. outputs/claim1_random_walk_oracle_fixture/ stores the configuration, ten
   raw rows, summary, command log, and SHA-256 checksums.
5. tests/test_claim1_random_walk_oracle.py checks construction, deterministic
   execution, and the destructive control.

Observed result: the connected fixture has mean target-root hit probability
0.78006; the broken-cross-tree control has mean 0.0 in every recorded row.

Verdict: **TOY**. This checks a finite random-walk mechanism and its control.
It does not prove the Omega(n^1/12) QIC query lower bound, simulate the
quantum algorithm, establish the matrix reduction, or reproduce an
asymptotic separation.

## C2 — Equation 1 quantum upper-bound scaling

No quantum linear-system implementation, runtime measurement, or precision
scaling study has been committed.

Verdict: **UNVERIFIED**.

## C3 — Theorem 2 random-walk reduction

The finite fixture is compatible with the random-walk intuition, but it does
not independently prove the oracle-to-matrix reduction, simulate SQ(M), or
establish the reduction’s query accounting and success bound.

Verdict: **UNVERIFIED**.

## C4 — Lemma 2 target-root solution mass

No independent construction of the matrix M, spectral calculation, inverse
solution, or x_i^2 = Omega(n^-5 ||x||^2) certificate has been committed.

Verdict: **UNVERIFIED**.

## C5 — Section 1 end-to-end separation conclusion

No end-to-end comparison of QIC query complexity and quantum runtime has been
performed. The finite oracle fixture cannot establish this conclusion.

Verdict: **UNVERIFIED**.

## Reproduction boundary

The fixed local Claim 1 command is recorded in ENVIRONMENT.md. Re-running the
fixture can change output hashes if its implementation or interpreter changes;
such a rerun must update the output checksums and this dossier together.
