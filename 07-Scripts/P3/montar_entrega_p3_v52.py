#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Empacota entrega v5.2 com fontes, hash de cada arquivo e ZIP verificável."""
from pathlib import Path
import hashlib,zipfile
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'08-Entregas/P3-v5.2'
PATHS=[
 '06-Decisoes/DEC-088 - Expansao seletiva P3 v5.2.md',
 '08-Continuidade/ESTADO-ATUAL.md',
 '08-Continuidade/Registros/2026-10-24-07-P3-v5.2-expansao-75.md',
 'LEIA-ME-IMPORTAR-P3-V5.2.md',
]
PATHS+=sorted(str(x.relative_to(ROOT)) for x in (ROOT/'07-Scripts/P3').glob('*p3_v52.py'))
PATHS+=sorted(str(x.relative_to(ROOT)) for x in OUT.rglob('*') if x.is_file())
PATHS=list(dict.fromkeys(PATHS))
assert all((ROOT/p).is_file() for p in PATHS)
manifest=ROOT/'SHA256SUMS-P3-V5.2.txt'
manifest.write_text(''.join(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()+'  '+p+'\n' for p in PATHS),encoding='utf-8')
zipfile_path=Path('/mnt/data/portal-calculadoras-auditoria-P3-v5.2-unico.zip')
with zipfile.ZipFile(zipfile_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
 for p in PATHS:z.write(ROOT/p,p)
 z.write(manifest,manifest.name)
with zipfile.ZipFile(zipfile_path) as z:
 assert z.testzip() is None
 assert len(z.namelist())==len(PATHS)+1
 for entry in manifest.read_text().splitlines():
  hexd,p=entry.split('  ',1)
  assert hashlib.sha256(z.read(p)).hexdigest()==hexd,p
print(f'PACOTE VALIDADO: {zipfile_path} arquivos={len(PATHS)+1} bytes={zipfile_path.stat().st_size}')