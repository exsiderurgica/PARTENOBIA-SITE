#!/usr/bin/env python3
"""V23A: Diego arms hang forward, and church characters share depth scaling."""
import argparse,hashlib,json
from pathlib import Path
BASE_SHA='3b6e9e3401865f8cf18897c02cbcbd0dab6d3d34ac373449491221be34b5e8dc'
def sha(b):return hashlib.sha256(b).hexdigest()
def overlay(data,runtime):
 if sha(data)!=BASE_SHA:raise ValueError('Expected exact V22Z')
 if b'function diegoV2ForwardArms(' not in runtime or b'</script' in runtime.lower():raise ValueError('Unexpected runtime')
 def rep(a,b):
  nonlocal data
  a,b=(v.encode() if isinstance(v,str) else v for v in (a,b))
  if data.count(a)!=1:raise ValueError('Missing/repeated anchor: '+a[:110].decode())
  data=data.replace(a,b,1)
 rep('function diegoV2CalibrateArms(H){',runtime+b'\nfunction diegoV2CalibrateArms(H){')
 rep('function churchHeroScale(){\n  const near=Math.max(0,Math.min(1,(-actor.z-7.0)/18.5));\n  const s=1.255-.255*near;\n  actor.root.scale.setScalar(s);\n  return s;\n}', 'function churchCharacterScaleAt(z){\n  const near=Math.max(0,Math.min(1,(-z-7.0)/18.5));\n  return 1.255-.255*near;\n}\nfunction churchHeroScale(){\n  const s=churchCharacterScaleAt(actor.z);\n  actor.root.scale.setScalar(s);\n  return s;\n}')
 rep('// B22 perspective compensation on hero only; 3-D occlusion and collision remain unscaled.','// V23A: shared depth compensation for hero and Diego; collision stays unscaled.')
 rep('zombieExpressiveArms(DIEGO.H,0,DIEGO.walkPhase||0,0);','diegoV2ForwardArms(DIEGO.H,0,DIEGO.walkPhase||0,0);')
 rep('zombieExpressiveArms(DIEGO.H,dt,DIEGO.walkPhase,DIEGO.actualSpeed);','diegoV2ForwardArms(DIEGO.H,dt,DIEGO.walkPhase,DIEGO.actualSpeed);')
 rep('const corrected=cl(.106-low,0,.20);\n       DIEGO.root.position.y=corrected;', 'const corrected=cl(.106*DIEGO.root.scale.x-low,0,.20*DIEGO.root.scale.x);\n       DIEGO.root.position.y=corrected;')
 rep('<title>PARTENOBIA V22Z TEST — Diego V2 braccia corrette</title>','<title>PARTENOBIA V23A TEST — Diego braccia avanti e proporzioni</title>')
 rep("const V22T={version:'V22Z TEST - Diego V2 braccia corrette'", "const V22T={version:'V23A TEST - Diego braccia avanti e proporzioni'")
 return data
def build(baseline,runtime,output,receipt):
 baseline,runtime,output,receipt=map(Path,(baseline,runtime,output,receipt))
 if output.resolve() in {baseline.resolve(),runtime.resolve()}:raise ValueError('Output overwrites input')
 data=overlay(baseline.read_bytes(),runtime.read_bytes());output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(data)
 result=dict(version='V23A',status='TEST',stable=False,baseline_sha256=BASE_SHA,change='Diego V2: braccia penzoloni in avanti e scala prospettica condivisa col protagonista',html_sha256=sha(data),html_bytes=len(data));receipt.parent.mkdir(parents=True,exist_ok=True);receipt.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));return result
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ('baseline','runtime','output','receipt'):p.add_argument('--'+k,required=True)
 build(**vars(p.parse_args()))
