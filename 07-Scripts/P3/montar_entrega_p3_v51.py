#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Produz ZIP único v5.1 com arquivos íntegros e manifesto SHA-256."""
from pathlib import Path
from hashlib import sha256
import zipfile
ROOT=Path(__file__).resolve().parents[2]
DEST=ROOT.parent/'portal-calculadoras-auditoria-P3-v5.1-unico.zip'
paths=[]
for part in ['06-Decisoes/DEC-087 - Revisao critica P3 v5.1.md','08-Continuidade/ESTADO-ATUAL.md','08-Continuidade/Registros/2026-10-24-06-P3-v5.1-revisao-75.md','LEIA-ME-IMPORTAR-P3-V5.1.md']:
 paths.append(ROOT/part)
paths.extend(sorted((ROOT/'07-Scripts/P3').glob('*p3_v51.py')))
paths.extend(sorted((ROOT/'08-Entregas/P3-v5.1').rglob('*')))
paths=[x for x in paths if x.is_file()]
assert len(paths)>=22 and all(x.exists() for x in paths)
manifest='\n'.join(f'{sha256(x.read_bytes()).hexdigest()}  {x.relative_to(ROOT).as_posix()}' for x in paths)+'\n'
(ROOT/'SHA256SUMS-P3-V5.1.txt').write_text(manifest,encoding='utf-8')
paths.append(ROOT/'SHA256SUMS-P3-V5.1.txt')
with zipfile.ZipFile(DEST,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,strict_timestamps=False) as z:
 for x in paths:z.write(x,x.relative_to(ROOT).as_posix())
with zipfile.ZipFile(DEST) as z:
 assert z.testzip() is None
 assert len(z.namelist())==len(paths)
 for x in paths:
  assert sha256(z.read(x.relative_to(ROOT).as_posix())).digest()==sha256(x.read_bytes()).digest()
print('ARCHIVE',DEST,'bytes',DEST.stat().st_size,'files',len(paths),'sha256',sha256(DEST.read_bytes()).hexdigest())