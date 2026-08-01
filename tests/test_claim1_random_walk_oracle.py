import importlib.util
from pathlib import Path
P=Path(__file__).parents[1]/'src'/'claim1_random_walk_oracle_fixture.py'
spec=importlib.util.spec_from_file_location('rw',P); rw=importlib.util.module_from_spec(spec); spec.loader.exec_module(rw)

def test_alternating_cycle_connects_two_trees():
    g,a,b,n=rw.build(3,7,False)
    assert n==16 and len(g)>0
    assert any(v[0]==1 for v in g[(0,3,0)])

def test_destructive_control_cannot_reach_second_root():
    result=rw.run_cell(3,7,9,100,100,True)
    assert result['hits']==0 and result['hit_probability']==0

def test_connected_fixture_is_deterministic_and_queries_oracle():
    a=rw.run_cell(3,7,9,200,128,False); b=rw.run_cell(3,7,9,200,128,False)
    assert a==b and a['neighbor_oracle_queries']>0
