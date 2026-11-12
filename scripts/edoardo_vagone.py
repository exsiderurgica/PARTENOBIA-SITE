#!/usr/bin/env python3
"""V22X: replace only the cab Pescivendolo with the existing Edoardo nuovo provider."""
import argparse,hashlib,json
from pathlib import Path
BASE_SHA='76d4fa244610195322f1aa955bdf40725cc187d28873c2a5fd433da919f17fca'
def sha(b):return hashlib.sha256(b).hexdigest()
def overlay(data):
 if sha(data)!=BASE_SHA:raise ValueError('Expected exact V22W build')
 changes=[("{name:'Pescivendolo',room:'v19:cab',kind:'cab',b64:()=>PESCIVENDOLO_V06B_RIG_B64,spawn:[386,883],shotOrder:['arm_l','arm_r','head']}","{name:'Edoardo',room:'v19:cab',kind:'cab',b64:()=>EDOARDO_RIG_B64,spawn:[386,883],shotOrder:['arm_l','arm_r','head']}"),
 ('<title>PARTENOBIA V22W TEST — Diego V2 e passi zombie</title>','<title>PARTENOBIA V22X TEST — Edoardo nuovo nel vagone</title>'),
 ("'FUNICOLARE IN SALITA · '+remaining+' s · Pescivendolo a bordo'","'FUNICOLARE IN SALITA · '+remaining+' s · Edoardo a bordo'"),
 ("const V22T={version:'V22W TEST - Diego V2 e passi zombie'","const V22T={version:'V22X TEST - Edoardo nuovo nel vagone'")]
 for a,b in changes:
  a,b=a.encode(),b.encode()
  if data.count(a)!=1:raise ValueError('Missing/repeated anchor: '+a[:100].decode())
  data=data.replace(a,b,1)
 return data
def build(baseline,output,receipt):
 baseline,output,receipt=map(Path,(baseline,output,receipt))
 if baseline.resolve()==output.resolve():raise ValueError('Output overwrites baseline')
 data=overlay(baseline.read_bytes());output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(data)
 result=dict(version='V22X',status='TEST',stable=False,change='Edoardo nuovo sostituisce solo il Pescivendolo nel vagone; Diego V2 e passi Pulcinella conservati',baseline_sha256=BASE_SHA,asset_id='EDOARDO_NUOVO_V01',asset_sha256='1226bd1929754f19fd1e98fecffbec849261d7f914b7ef8c5af2f1c50f0b223e',html_sha256=sha(data),html_bytes=len(data))
 receipt.parent.mkdir(parents=True,exist_ok=True);receipt.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));return result
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for key in ('baseline','output','receipt'):p.add_argument('--'+key,required=True)
 build(**vars(p.parse_args()))
