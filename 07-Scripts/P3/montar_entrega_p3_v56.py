#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Empacotar P3 v5.6, preservar fontes, verificar hashes SHA-256."""
from pathlib import Path
import hashlib,zipfile,json
ROOT=Path(__file__).resolve().parents[2]
D=ROOT/'08-Entregas/P3-v5.6'
files=[]
files+=list(ROOT.glob('06-Decisoes/DEC-093*.md'))
files+=list(ROOT.glob('08-Continuidade/Registros/*P3-v5.6*.md'))
files.append(ROOT/'LEIA-ME-IMPORTAR-P3-V5.6.md')
files+=list(ROOT.glob('07-Scripts/P3/*p3_v56.py'))
files += [p for p in D.rglob('*') if p.is_file() and not p.name.startswith('SHA256SUMS-')]
files=sorted(set(files),key=lambda p:str(p.relative_to(ROOT)))
assert all(p.is_file() for p in files)
manifest=ROOT/'SHA256SUMS-P3-V5.6.txt'
manifest.write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(ROOT))+'\n' for p in files),encoding='utf-8')
output=Path('/mnt/data/portal-calculadoras-auditoria-P3-v5.6-unico.zip')
with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zout:
 for p in files+[manifest]:zout.write(p,str(p.relative_to(ROOT)))
with zipfile.ZipFile(output) as z:
 assert z.testzip() is None and len(z.namelist())==len(files)+1
 for line in z.read('SHA256SUMS-P3-V5.6.txt').decode('utf-8').splitlines():
  sha,path=line.split('  ',1)
  assert hashlib.sha256(z.read(path)).hexdigest()==sha,path
print(json.dumps({'arquivo':str(output),'arquivos':len(files)+1,'tamanho_bytes':output.stat().st_size,'sha256':hashlib.sha256(output.read_bytes()).hexdigest()},ensure_ascii=False,indent=2))