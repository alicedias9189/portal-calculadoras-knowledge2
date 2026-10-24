#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Empacota P3 v5.5 e verifica integridade ZIP e SHA-256 de todos os membros."""
from pathlib import Path
import hashlib,zipfile,json
R=Path(__file__).resolve().parents[2];D=R/'08-Entregas/P3-v5.5'
paths=[]
paths+=list(R.glob('06-Decisoes/DEC-092*.md'))
paths+=list(R.glob('08-Continuidade/Registros/*P3-v5.5*.md'))
paths.append(R/'LEIA-ME-IMPORTAR-P3-V5.5.md')
paths+=list(R.glob('07-Scripts/P3/*p3_v55.py'))
paths += [p for p in D.rglob('*') if p.is_file() and not p.name.startswith('SHA256SUMS-')]
paths=sorted(set(paths),key=lambda x:str(x.relative_to(R)))
assert all(p.is_file() for p in paths)
sha=R/'SHA256SUMS-P3-V5.5.txt'
sha.write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(R))+'\n' for p in paths),encoding='utf-8')
zip_path=Path('/mnt/data/portal-calculadoras-auditoria-P3-v5.5-unico.zip')
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zipout:
 for p in paths+[sha]:zipout.write(p,str(p.relative_to(R)))
with zipfile.ZipFile(zip_path) as z:
 assert z.testzip() is None and len(z.namelist())==len(paths)+1
 for line in z.read('SHA256SUMS-P3-V5.5.txt').decode('utf-8').splitlines():
  expected,relative=line.split('  ',1);assert hashlib.sha256(z.read(relative)).hexdigest()==expected,relative
summary={'arquivo':str(zip_path),'total_membros':len(paths)+1,'tamanho_bytes':zip_path.stat().st_size,'sha256':hashlib.sha256(zip_path.read_bytes()).hexdigest()}
print(json.dumps(summary,ensure_ascii=False,indent=2))