"""Finite source-aligned sparse-system fixture, not a theorem proof."""
import json
from pathlib import Path
def run():
 return {'n':64,'sparsity_max':2,'kappa_fixture':4.0,'epsilon':0.01,'quantum_formula_variables':['s','kappa','log(1/epsilon)','log(n)'],'scope':'finite source-audited CPU fixture; not a QIC lower-bound or quantum runtime reproduction'}
if __name__=='__main__':
 out=Path('outputs/claim1_source_audit');out.mkdir(parents=True,exist_ok=True);(out/'result.json').write_text(json.dumps(run(),indent=2)+'\n')
