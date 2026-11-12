#!/usr/bin/env python3
"""V22W TEST: Diego V2 in Gesu church and Pulcinella footsteps for every undead."""
import argparse,base64,hashlib,json,re
from pathlib import Path
BASE_SHA='442240998f4e104cc99a66775622db0398cd33c9257247188eed443967dbf169'
ASSET_SHA='658a2cd501eeef95270727e34043d32741909a44cdb9be642c8a9f7f79ed2718'
def sha(b):return hashlib.sha256(b).hexdigest()
def overlay(html,asset,runtime):
 if sha(html)!=BASE_SHA:raise ValueError('Expected exact GOLD V22U baseline')
 if sha(asset)!=ASSET_SHA:raise ValueError('Unexpected Diego V2 GLB')
 if b'DIEGO_V2_ASSET' not in runtime or b'</script' in runtime.lower():raise ValueError('Unexpected runtime')
 def replace(a,b):
  nonlocal html
  a,b=(v.encode() if isinstance(v,str) else v for v in (a,b))
  if html.count(a)!=1:raise ValueError('Missing/repeated patch anchor: '+a[:100].decode())
  html=html.replace(a,b,1)
 pattern=rb'(<script[^>]*id="partenobia-zombie-diego"[^>]*>)[A-Za-z0-9+/=\s]+(</script>)'
 html,n=re.subn(pattern,lambda m:m[1]+base64.b64encode(asset)+m[2],html)
 if n!=1:raise ValueError('Expected one church Diego asset')
 replace('function sfxDrag(pan,vol){',runtime+b'\nfunction sfxDrag(pan,vol){')
 replace("const root=new THREE.Group();root.name='DIEGO';const model=g.scene;", "const root=new THREE.Group();root.name='DIEGO';const model=g.scene;diegoV2Configure(model);")
 replace("assetName:'Zombie Diego · BUITONI #10 · V05 HERO rig'", "assetName:'Zombie Diego V2 · BUITONI #10 · 78717 volto corretto'")
 replace("model.rotation.y=Math.PI;root.scale.setScalar(1.20);", "model.rotation.y=Math.PI;root.scale.setScalar(1.0); // V2 is already 1.80 m tall.")
 replace("if(!tag){DIEGO.error='Approved V05 GLB missing';return}","if(!tag){DIEGO.error='Zombie Diego V2 GLB missing';return}")
 # Keep Pulcinella's original trigger and both synthesis functions byte-identical.
 replace('ZOM.lastHalf=half;sfxDrag(pan,vol);sfxUndeadFootstep(pan,.65*vol)', 'ZOM.lastHalf=half;sfxZombieStep(pan,vol)')
 replace('DIEGO.lastHalf=half;sfxDrag(pan,vol);sfxUndeadFootstep(pan,.65*vol);','DIEGO.lastHalf=half;sfxZombieStep(pan,vol);')
 replace('sfxDrag(pan,audible*.52);sfxUndeadFootstep(pan,audible*.62)', 'sfxZombieStep(pan,audible*.62/.65)')
 replace('sfxDrag(Math.max(-1,Math.min(1,(n.x-actor.x)/5)),.32);sfxUndeadFootstep(Math.max(-1,Math.min(1,(n.x-actor.x)/5)),.42)', 'sfxZombieStep(Math.max(-1,Math.min(1,(n.x-actor.x)/5)),.42/.65)')
 for v in ('VECCHIO','EDOARDO'):
  anchor=f'  {v}.next=(Number.isFinite({v}.next)?{v}.next:5.5+Math.random()*6)-dt;'
  replace(anchor,f'  zombieTravelStep({v},walked,pan,vol);\n'+anchor)
 replace(' const traveled=Math.hypot(v.x-prevX,v.z-prevZ);', ' const traveled=Math.hypot(v.x-prevX,v.z-prevZ);\n zombieTravelStep(v,traveled,Math.max(-1,Math.min(1,(v.x-actor.x)/5)),Math.max(0,Math.min(1,3.4/(1+dist*dist*.1))));')
 replace('if(v.footDistance>.43){v.footDistance=0;sfxUndeadFootstep(Math.max(-1,Math.min(1,(v.x-actor.x)/5)),.35)}','if(v.footDistance>.43){v.footDistance=0;sfxZombieStep(Math.max(-1,Math.min(1,(v.x-actor.x)/5)),.35/.65)}')
 # The transformed protagonist is an undead too; ordinary player footsteps stay intact.
 replace('function audioFootsteps(dt,speed,run){\n  if(!AUD.ctx||speed<.2)return;', 'function audioFootsteps(dt,speed,run){\n  if(!AUD.ctx||speed<.2)return;\n  if(V20.zombie){zombieTravelStep(actor,speed*dt,0,.85);return}')
 replace('<title>PARTENOBIA — V22U · Edoardo nuovo</title>','<title>PARTENOBIA V22W TEST — Diego V2 e passi zombie</title>')
 replace("const V22T={version:'V22U - Edoardo nuovo'", "const V22T={version:'V22W TEST - Diego V2 e passi zombie'")
 return html

def build(baseline,asset,runtime,output,receipt):
 baseline,asset,runtime,output,receipt=map(Path,(baseline,asset,runtime,output,receipt))
 if output.resolve() in {p.resolve() for p in (baseline,asset,runtime)}:raise ValueError('Output overwrites input')
 data=overlay(baseline.read_bytes(),asset.read_bytes(),runtime.read_bytes())
 output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(data)
 result=dict(version='V22W',status='TEST',stable=False,change='Zombie Diego V2 nella chiesa del Gesu; tutti gli zombie usano i passi di Pulcinella',baseline_sha256=BASE_SHA,asset_sha256=ASSET_SHA,html_sha256=sha(data),html_bytes=len(data))
 receipt.parent.mkdir(parents=True,exist_ok=True);receipt.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));return result
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for name in ('baseline','asset','runtime','output','receipt'):p.add_argument('--'+name,required=True)
 build(**vars(p.parse_args()))
