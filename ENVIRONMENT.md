# Environment and artifact record

## Fixed local command

From a clean checkout:

~~~text
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python src/claim1_source_audit.py
.venv/bin/python src/claim1_random_walk_oracle_fixture.py --out outputs/claim1_random_walk_oracle_fixture
(cd outputs/claim1_random_walk_oracle_fixture && sha256sum -c SHA256SUMS)
(cd evidence/source && sha256sum -c SHA256SUMS)
.venv/bin/python -m pytest -q
~~~

The producer uses the Python standard library; pytest is the only declared
test dependency. No Hugging Face Job, paid compute, remote GPU, quantum
backend, author implementation, dataset, or checkpoint is part of the
evidence.

## Pinned inputs

| Input | SHA-256 |
| --- | --- |
| evidence/source/arxiv.pdf | 581d57e998439c2ad73b68f02dcf62fb3a54c655f6d8903c4767de2ce3968a70 |
| evidence/source/arxiv_source.tar.gz | 1729ecf6489a345ff10b6433ce8256a9bc88028dcf68b469e0dd2de50e223eb6 |
| contract/contract_manifest.json | a5fe8f32a92be2d7bda9647535221a7d551b0f7cf76cb40c082340f1d4fe499f |

## Claim 1 checkpoint

| Measurement | Recorded value |
| --- | --- |
| Tree height | 4 |
| Walk seeds | 20260801 through 20260805 |
| Walks per seed | 10,000 |
| Steps per walk | 256 |
| Connected mean hit probability | 0.78006 |
| Broken-control mean hit probability | 0.0 |
| Recorded rows | 10 |
| Hardware | local CPU; no remote run |

The tracked output records the exact finite configuration and raw rows. The
dossier publication did not rerun the producer.

## Reproduction policy

- Label a finite oracle mechanism as a toy, not an asymptotic theorem proof.
- Keep source inspection, graph-mechanism evidence, matrix analysis, and
  quantum-runtime claims separate.
- Do not promote Claims 2–5 without a scoped producer, independent checker,
  raw output, and boundary or negative control.
