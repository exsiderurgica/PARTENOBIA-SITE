#!/usr/bin/env python3
"""V23B: Sansevero fishmonger, 30-second ride, left cab spawn, softer Diego arms."""
import argparse,hashlib,json
from pathlib import Path
BASE_SHA='5c910cdc7e0afef48cb181e053f0f5f603a93b5d428a56e8359f9f2f2ee89b8a'
def sha(b):return hashlib.sha256(b).hexdigest()
def overlay(data,runtime):
 if sha(data)!=BASE_SHA:raise ValueError('Expected exact V23A')
 if b'function v23bCabLeftSpawn(v)' not in runtime or b'</script' in runtime.lower():raise ValueError('Unexpected runtime')
 def rep(a,b):
  nonlocal data
  a,b=(v.encode() if isinstance(v,str) else v for v in (a,b))
  if data.count(a)!=1:raise ValueError('Missing/repeated anchor: '+a[:110].decode())
  data=data.replace(a,b,1)
 rep("{name:'GNO',room:'v19:vicolo',kind:'vicolo',b64:()=>document.getElementById('partenobia-v19-gno-glb').textContent.trim(),spawn:[655,718],shotOrder:['arm_l','arm_r','head']}","{name:'Zombie Pescivendolo V2',room:'v19:vicolo',kind:'vicolo',b64:()=>PESCIVENDOLO_V2_RIG_B64,spawn:[655,718],shotOrder:['arm_l','arm_r','head']}")
 rep('rideStartedAt:0,rideElapsed:0,rideDuration:60,','rideStartedAt:0,rideElapsed:0,rideDuration:30,')
 rep('Funicolare · Viaggio in salita: 60 secondi','Funicolare · Viaggio in salita: 30 secondi')
 rep('La funicolare parte. Viaggio di un minuto.','La funicolare parte. Viaggio di 30 secondi.')
 rep('// Elapsed wall time, not frame count, so tab throttling cannot prolong a minute.','// Elapsed wall time, not frame count, so tab throttling cannot prolong the ride.')
 rep("{name:'Edoardo',room:'v19:cab',kind:'cab',b64:()=>EDOARDO_RIG_B64,spawn:[386,883]","{name:'Edoardo',room:'v19:cab',kind:'cab',b64:()=>EDOARDO_RIG_B64,spawn:[180,880]")
 rep('function n19AttachOne(v){',runtime+b'\nfunction n19AttachOne(v){')
 rep("if(!N19.active||v.kind!==N19.kind||!v.ready)return;\n if(v.root.parent!==N19.scene)","if(!N19.active||v.kind!==N19.kind||!v.ready)return;\n if(v.kind==='cab'&&v.name==='Edoardo')v23bCabLeftSpawn(v);\n if(v.root.parent!==N19.scene)")
 rep('const upper=(22+48*reach)*Math.PI/180,lower=(32+45*reach)*Math.PI/180;','const upper=(8+35*reach)*Math.PI/180,lower=(12+35*reach)*Math.PI/180;')
 rep('<title>PARTENOBIA V23A TEST — Diego braccia avanti e proporzioni</title>','<title>PARTENOBIA V23B TEST — San Severo e funicolare</title>')
 rep("const V22T={version:'V23A TEST - Diego braccia avanti e proporzioni'", "const V22T={version:'V23B TEST - San Severo e funicolare'")
 return data
def build(baseline,runtime,output,receipt):
 baseline,runtime,output,receipt=map(Path,(baseline,runtime,output,receipt))
 if output.resolve() in {baseline.resolve(),runtime.resolve()}:raise ValueError('Output overwrites input')
 data=overlay(baseline.read_bytes(),runtime.read_bytes());output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(data)
 result=dict(version='V23B',status='TEST',stable=False,baseline_sha256=BASE_SHA,change='Pescivendolo V2 nel vicolo San Severo; viaggio 30 s; Edoardo dal bordo sinistro; braccia Diego meno protese',html_sha256=sha(data),html_bytes=len(data));receipt.parent.mkdir(parents=True,exist_ok=True);receipt.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));return result
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ('baseline','runtime','output','receipt'):p.add_argument('--'+k,required=True)
 build(**vars(p.parse_args()))
