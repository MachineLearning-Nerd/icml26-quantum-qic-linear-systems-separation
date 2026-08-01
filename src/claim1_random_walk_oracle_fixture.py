#!/usr/bin/env python3
"""Finite local fixture for the Childs-style two-binary-tree random-walk oracle game.

This is a clean-room reduced experiment, not a lower-bound proof.  It builds two
height-h perfect binary trees, joins their leaves by an alternating random cycle,
and estimates the probability that an oracle-neighbor random walk from root T1
finds root T2.  A matched destructive control removes cross-tree cycle edges.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, math, random
from collections import defaultdict
from pathlib import Path


def add(g, a, b):
    g[a].append(b); g[b].append(a)


def build(height: int, seed: int, broken: bool=False):
    rng=random.Random(seed)
    g=defaultdict(list)
    leaves=[]
    # nodes are (tree, depth, index); two perfect binary trees
    for t in (0,1):
        for d in range(height):
            for i in range(2**d):
                p=(t,d,i)
                add(g,p,(t,d+1,2*i)); add(g,p,(t,d+1,2*i+1))
        leaves.append([(t,height,i) for i in range(2**height)])
    # alternating cycle: interleave a shuffled order from each leaf set.
    a,b=leaves
    rng.shuffle(a); rng.shuffle(b)
    cycle=[]
    for x,y in zip(a,b): cycle.extend((x,y))
    if not broken:
        for i in range(len(cycle)): add(g,cycle[i],cycle[(i+1)%len(cycle)])
    return g,(0,0,0),(1,0,0),len(cycle)


def run_cell(height, graph_seed, walk_seed, walks, steps, broken):
    g,start,target,cycle_nodes=build(height,graph_seed,broken)
    rng=random.Random(walk_seed)
    hits=0; queries=0; first=[]
    for _ in range(walks):
        x=start; hit=None
        for step in range(1,steps+1):
            ns=g[x]; queries += 1
            x=ns[rng.randrange(len(ns))]
            if x==target:
                hit=step; break
        if hit is not None:
            hits += 1; first.append(hit)
    return {"height":height,"graph_seed":graph_seed,"walk_seed":walk_seed,
            "walks":walks,"steps":steps,"broken_cross_tree_control":broken,
            "vertices":len(g),"cycle_vertices":cycle_nodes,"hits":hits,
            "hit_probability":hits/walks,"mean_first_hit_step":(sum(first)/len(first) if first else None),
            "neighbor_oracle_queries":queries}


def sha(path):
    h=hashlib.sha256(); h.update(path.read_bytes()); return h.hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',required=True); ap.add_argument('--height',type=int,default=4)
    ap.add_argument('--walks',type=int,default=10000); ap.add_argument('--steps',type=int,default=256)
    ap.add_argument('--seeds',type=int,nargs='+',default=[20260801,20260802,20260803,20260804,20260805])
    a=ap.parse_args(); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    config=vars(a); (out/'config.json').write_text(json.dumps(config,indent=2)+'\n')
    rows=[]
    for seed in a.seeds:
        for broken in (False,True):
            r=run_cell(a.height,seed,seed+100000,a.walks,a.steps,broken); rows.append(r)
    fields=list(rows[0]);
    with (out/'results.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    good=[r['hit_probability'] for r in rows if not r['broken_cross_tree_control']]
    bad=[r['hit_probability'] for r in rows if r['broken_cross_tree_control']]
    summary={"protocol":"clean-room finite oracle-neighbor random-walk fixture based on pinned lower.tex:6-18",
             "verdict":"toy","scope":"height-4 finite random-walk oracle diagnostic; not a QIC query lower-bound proof or quantum runtime reproduction",
             "connected_cycle_mean_hit_probability":sum(good)/len(good),"broken_cross_tree_mean_hit_probability":sum(bad)/len(bad),
             "control_expected_zero":all(x==0 for x in bad),"rows":len(rows)}
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (out/'run.log').write_text(' '.join(['python3',__file__]+__import__('sys').argv[1:])+'\nexit=0\n')
    files=['config.json','results.csv','summary.json','run.log']
    (out/'SHA256SUMS').write_text(''.join(f'{sha(out/x)}  {x}\n' for x in files))
if __name__=='__main__': main()
