import json,hashlib
from pathlib import Path
D=Path(__file__).parents[1]
def test_contract_has_five_claims(): assert len(json.loads((D/'contract/live_claims.json').read_text()))==5
def test_source_manifest():
 for line in (D/'evidence/source/SHA256SUMS').read_text().splitlines():
  want,name=line.split()[:2]; assert hashlib.sha256((D/'evidence/source'/name).read_bytes()).hexdigest()==want
def test_claim1_fixture():
 from src.claim1_source_audit import run
 assert run()['sparsity_max']==2
