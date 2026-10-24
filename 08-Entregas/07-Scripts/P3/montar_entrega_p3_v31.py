#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera SHA256SUMS e o ZIP único a partir da raiz do pacote.
Uso: python 07-Scripts/P3/montar_entrega_p3_v31.py
"""
from pathlib import Path
import hashlib,zipfile,sys
ROOT=Path(__file__).resolve().parents[2]
manifest=ROOT/'SHA256SUMS-P3-V3.1.txt'
lines=[]
for path in sorted(ROOT.rglob('*')):
 if path.is_file() and path!=manifest and path.name!='portal-calculadoras-auditoria-P3-v3.1-unico.zip':
  lines.append(hashlib.sha256(path.read_bytes()).hexdigest()+'  '+path.relative_to(ROOT).as_posix())
manifest.write_text('\n'.join(lines)+'\n',encoding='utf-8')
out=ROOT.parent/'portal-calculadoras-auditoria-P3-v3.1-unico.zip'
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for path in sorted(ROOT.rglob('*')):
  if path.is_file():z.write(path,arcname=path.relative_to(ROOT).as_posix())
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 assert len(z.namelist())==len(lines)+1
 assert all(hashlib.sha256(z.read(rel.split('  ',1)[1])).hexdigest()==rel.split('  ',1)[0] for rel in lines)
print(f'ZIP: {out} | {len(lines)+1} arquivos | {len(lines)} hashes OK')
