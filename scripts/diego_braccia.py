#!/usr/bin/env python3
"""V22Z: Diego V2's calibrated hanging arms over exact V22Y."""
import argparse,hashlib,json
from pathlib import Path
BASE_SHA='42cfb06dfacecd9e9053d5c109cf944263979c27cae7481fe748aaa1dd60d964'
def sha(b):return hashlib.sha256(b).hexdigest()
def overlay(data,runtime):
 if sha(data)!=BASE_SHA:raise ValueError('Expected exact V22Y')
 if b'function diegoV2CalibrateArms(H)' not in runtime or b'</script' in runtime.lower():raise ValueError('Unexpected arm runtime')
 changes=[(b'function diegoV2Configure(model){',runtime+b'\nfunction diegoV2Configure(model){'),
 (b'    DIEGO.H.armState={left:.08,right:.05,goalLeft:.08,goalRight:.05,',b'    diegoV2CalibrateArms(DIEGO.H);\n    DIEGO.H.armState={left:.08,right:.05,goalLeft:.08,goalRight:.05,'),
 (b"function diegoAttach(){\n if(!DIEGO.ready||!CH.active||!CH.scene)return;",b"function diegoAttach(){\n if(!DIEGO.ready||!CH.active||!CH.scene)return;\n zombieExpressiveArms(DIEGO.H,0,DIEGO.walkPhase||0,0);"),
 ('<title>PARTENOBIA V22Y TEST — Zombie Pescivendolo V2</title>'.encode(),'<title>PARTENOBIA V22Z TEST — Diego V2 braccia corrette</title>'.encode()),
 (b"const V22T={version:'V22Y TEST - Zombie Pescivendolo V2'",b"const V22T={version:'V22Z TEST - Diego V2 braccia corrette'")]
 for a,b in changes:
  if data.count(a)!=1:raise ValueError('Missing/repeated arm patch anchor: '+a[:100].decode())
  data=data.replace(a,b,1)
 return data
def build(baseline,runtime,output,receipt):
 baseline,runtime,output,receipt=map(Path,(baseline,runtime,output,receipt))
 if output.resolve() in {baseline.resolve(),runtime.resolve()}:raise ValueError('Output overwrites input')
 data=overlay(baseline.read_bytes(),runtime.read_bytes());output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(data)
 result=dict(version='V22Z',status='TEST',stable=False,change='Diego V2: posa delle braccia calibrata dalla A-pose a riposo naturale; Edoardo nel vagone e passi Pulcinella conservati',baseline_sha256=BASE_SHA,html_sha256=sha(data),html_bytes=len(data));receipt.parent.mkdir(parents=True,exist_ok=True);receipt.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));return result
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ('baseline','runtime','output','receipt'):p.add_argument('--'+k,required=True)
 build(**vars(p.parse_args()))
