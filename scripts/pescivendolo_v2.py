"""V22Y: replace all surviving fishmonger providers over V22X; keep rollback intact."""
import argparse,base64,hashlib,json,re
from pathlib import Path
BASE_SHA='41ea64dc502648e07b3b669ad0c8ce4a91ad1942138899ea8d35a4f76e7cb65c'
ASSET_SHA='fa2fb2711747bddafffef1d2d8f6ed34ebe5cfe578a00b590b4feb84ec77f899'
def sha(b):return hashlib.sha256(b).hexdigest()
def overlay(html,asset,runtime):
 if sha(html)!=BASE_SHA:raise ValueError('Expected exact V22X baseline')
 if sha(asset)!=ASSET_SHA:raise ValueError('Unexpected Pescivendolo V2 checksum')
 if b'PESCIVENDOLO_V2_ASSET' not in runtime or b'</script' in runtime.lower():raise ValueError('Unexpected runtime')
 def replace(a,b):
  nonlocal html
  a,b=(x.encode() if isinstance(x,str) else x for x in (a,b))
  if html.count(a)!=1:raise ValueError('Missing or repeated anchor: '+a[:100].decode())
  html=html.replace(a,b,1)
 m=list(re.finditer(rb"const PESCIVENDOLO_V06B_RIG_B64='[A-Za-z0-9+/=]+';",html))
 if len(m)!=1:raise ValueError('Expected one old shared fishmonger model')
 replace(m[0].group(),b"const PESCIVENDOLO_V2_RIG_B64='"+base64.b64encode(asset)+b"';")
 if html.count(b'b64:()=>PESCIVENDOLO_V06B_RIG_B64')!=1:raise ValueError('Unexpected fishmonger population')
 replace("name:'Pescivendolo',room:'v19:station',kind:'station',b64:()=>PESCIVENDOLO_V06B_RIG_B64", "name:'Zombie Pescivendolo V2',room:'v19:station',kind:'station',b64:()=>PESCIVENDOLO_V2_RIG_B64")
 replace("root.name='V19_'+v.kind+'_'+v.name;\n   const model=gl.scene;if(v.name==='Edoardo')edoardoNuovoConfigure(model);root.add(model);", "root.name='V19_'+v.kind+'_'+v.name;\n   const model=gl.scene;if(v.name==='Edoardo')edoardoNuovoConfigure(model);if(v.name==='Zombie Pescivendolo V2')pescivendoloV2Configure(model);root.add(model);")
 replace('function n19LoadEnemy(v){',runtime+b'\nfunction n19LoadEnemy(v){')
 replace('<title>PARTENOBIA V22X TEST — Edoardo nuovo nel vagone</title>','<title>PARTENOBIA V22Y TEST — Zombie Pescivendolo V2</title>')
 replace("const V22T={version:'V22X TEST - Edoardo nuovo nel vagone'", "const V22T={version:'V22Y TEST - Zombie Pescivendolo V2'")
 replace('// V22R: approved Pescivendolo V06B, original rig and corrected front-facing apron texture.', '// V22Y: Zombie Pescivendolo V2, photo-profile Python reconstruction approved for replacement.')
 if b'PESCIVENDOLO_V06B_RIG_B64' in html:raise ValueError('Old fishmonger still referenced')
 return html

def build(baseline,asset,runtime,output,receipt):
 baseline,asset,runtime,output,receipt=map(Path,(baseline,asset,runtime,output,receipt))
 if output.resolve() in [x.resolve() for x in (baseline,asset,runtime)]:raise ValueError('Output overwrites input')
 html=overlay(baseline.read_bytes(),asset.read_bytes(),runtime.read_bytes());output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(html)
 result=dict(version='V22Y',status='TEST',stable=False,change='Zombie Pescivendolo V2 sostituisce tutti i vecchi Pescivendoli ancora attivi; Edoardo nel vagone conservato',baseline_sha256=BASE_SHA,asset_id='ZOMBIE_PESCIVENDOLO_V2',asset_sha256=ASSET_SHA,html_sha256=sha(html),html_bytes=len(html),rooms=['station'])
 receipt.parent.mkdir(parents=True,exist_ok=True);receipt.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));return result
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for key in ('baseline','asset','runtime','output','receipt'):p.add_argument('--'+key,required=True)
 build(**vars(p.parse_args()))
