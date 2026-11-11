#!/usr/bin/env python3
"""Deterministic V22U overlay over checksum-pinned, immutable V22T GOLD.

Shared unchanged with the public delivery repository; stdlib only.
The approved GLB bytes are embedded once; all five active Edoardo providers
already refer to EDOARDO_RIG_B64. Other actors, placements and controllers stay intact.
"""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

BASE_SHA = '6515c8be9ffbbc3484472116b6338e894077093f4e5093a73a9804ff911a0a6e'
ASSET_SHA = '1226bd1929754f19fd1e98fecffbec849261d7f914b7ef8c5af2f1c50f0b223e'
ASSET_ID = 'EDOARDO_NUOVO_V01'
TITLE = '<title>PARTENOBIA — V22U · Edoardo nuovo</title>'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def overlay(baseline, asset, runtime):
    if sha(baseline) != BASE_SHA:
        raise ValueError('Baseline must be the exact approved GOLD V22T')
    if sha(asset) != ASSET_SHA:
        raise ValueError('Unexpected Edoardo nuovo GLB checksum')
    if b'EDOARDO_NUOVO_ASSET' not in runtime or b'</script' in runtime.lower():
        raise ValueError('Unexpected Edoardo nuovo runtime')
    html = baseline

    def replace(old, new):
        nonlocal html
        if html.count(old) != 1:
            raise ValueError('Missing or repeated V22T patch anchor: ' + old[:100].decode('utf-8'))
        html = html.replace(old, new, 1)

    pattern = rb"const EDOARDO_RIG_B64='[A-Za-z0-9+/=]+';"
    matches = list(re.finditer(pattern, html))
    if len(matches) != 1:
        raise ValueError('Expected one shared Edoardo GLB definition')
    replace(matches[0].group(), b"const EDOARDO_RIG_B64='" + base64.b64encode(asset) + b"';")
    # The new GLB contains the authoritative atlas. Do not load the old fallback
    # JPEG, which would also retain the previous appearance in the document.
    matches = list(re.finditer(rb"const EDOARDO_TEX='[^']+';", html))
    if len(matches) != 1:
        raise ValueError('Expected one old Edoardo fallback texture')
    replace(matches[0].group(), b"const EDOARDO_TEX='';")
    replace(b"const texture=new THREE.TextureLoader().load(EDOARDO_TEX);\n   texture.flipY=false;texture.colorSpace=THREE.SRGBColorSpace;",
            b'const texture=null; // Edoardo nuovo uses its embedded, shared atlas.')
    replace(b"assetName:'EDOARDO \xc2\xb7 GLB 78652 con skin HERO e animazioni Pulcinella'",
            b"assetName:'Edoardo nuovo \xc2\xb7 78648 \xc2\xb7 V01 approvato'")
    replace(b'function edoardoLoad(){', runtime + b'\nfunction edoardoLoad(){')
    replace(b"const root=new THREE.Group();root.name='EDOARDO';const model=g.scene;",
            b"const root=new THREE.Group();root.name='EDOARDO';const model=g.scene;edoardoNuovoConfigure(model);")
    replace(b"root.name='FONTANELLE_'+v.name;\n    const model=gl.scene;root.add(model);",
            b"root.name='FONTANELLE_'+v.name;\n    const model=gl.scene;if(v.name==='Edoardo')edoardoNuovoConfigure(model);root.add(model);")
    replace(b"root.name='V19_'+v.kind+'_'+v.name;\n   const model=gl.scene;root.add(model);",
            b"root.name='V19_'+v.kind+'_'+v.name;\n   const model=gl.scene;if(v.name==='Edoardo')edoardoNuovoConfigure(model);root.add(model);")
    replace(b"const V22T={version:'V22T TEST'", b"const V22T={version:'V22U - Edoardo nuovo'")
    old = '<title>PARTENOBIA V22T TEST — zombie precaricati in tutte le schermate</title>'
    replace(old.encode(), (TITLE + '\n<meta name="description" content="PARTENOBIA, survival horror a Napoli. V22U con Edoardo nuovo in tutte le sue scene.">').encode())
    # Baseline has one singleton plus these four independent spawn definitions.
    if html.count(b'b64:()=>EDOARDO_RIG_B64') != 4:
        raise ValueError('Unexpected Edoardo population: review every scene before building')
    return html


def build(baseline, asset, runtime, output, receipt=None):
    baseline, asset, runtime, output = map(Path, (baseline, asset, runtime, output))
    if output.resolve() in {p.resolve() for p in (baseline, asset, runtime)}:
        raise ValueError('Output must not overwrite an input')
    data = overlay(baseline.read_bytes(), asset.read_bytes(), runtime.read_bytes())
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=output.parent, suffix='.tmp', delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
        os.replace(temporary, output)
    finally:
        if temporary:
            temporary.unlink(missing_ok=True)
    result = {'version': 'V22U', 'change': 'Edoardo nuovo in tutte le cinque istanze',
              'baseline_sha256': BASE_SHA, 'asset_id': ASSET_ID, 'asset_sha256': ASSET_SHA,
              'html_sha256': sha(data), 'html_bytes': len(data),
              'rooms': ['vicolo-storico', 'fontanelle', 'chapel', 'station', 'stairs']}
    if receipt:
        Path(receipt).write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for option in ('baseline', 'asset', 'runtime', 'output'):
        parser.add_argument('--' + option, required=True)
    parser.add_argument('--receipt')
    args = parser.parse_args()
    build(args.baseline, args.asset, args.runtime, args.output, args.receipt)
