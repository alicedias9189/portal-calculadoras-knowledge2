#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Empacotamento P3 v5.4 único, integridade ZIP e hashes SHA-256 por arquivo."""
from pathlib import Path
import hashlib,zipfile,json
R=Path(__file__).resolve().parents[2];D=R/'08-Entregas/P3-v5.4'
paths=[]
paths.extend(R.glob('06-Decisoes/DEC-091*.md'))
paths.extend(R.glob('08-Continuidade/Registros/*P3-v5.4*.md'))
paths.append(R/'LEIA-ME-IMPORTAR-P3-V5.4.md')
paths.extend(R.glob('07-Scripts/P3/*p3_v54.py'))
paths.extend(p for p in D.rglob('*') if p.is_file() and not p.name.startswith('SHA256SUMS-'))
paths=sorted(set(paths),key=lambda p:str(p.relative_to(R)))
assert all(p.is_file() for p in paths)
manifest=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(R))+'\n' for p in paths)
sha=R/'SHA256SUMS-P3-V5.4.txt';sha.write_text(manifest,encoding='utf-8')
allpaths=paths+[sha]
dest=Path('/mnt/data/portal-calculadoras-auditoria-P3-v5.4-unico.zip')
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in allpaths:z.write(p,str(p.relative_to(R)))
with zipfile.ZipFile(dest) as z:
 assert z.testzip() is None and len(z.namelist())==len(allpaths)
 for line in z.read('SHA256SUMS-P3-V5.4.txt').decode().splitlines():
  digest,rel=line.split('  ',1)
  assert hashlib.sha256(z.read(rel)).hexdigest()==digest,rel
print(json.dumps({'zip':str(dest),'arquivos':len(allpaths),'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()},ensure_ascii=False,indent=2))