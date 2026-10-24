#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pacote único P3 v5.3 + manifesto SHA-256 com caminhos relativos."""
from pathlib import Path
import hashlib,zipfile,json
HERE=Path(__file__).resolve(); R=HERE.parents[2] if HERE.parent.name=='P3' and HERE.parent.parent.name=='07-Scripts' else HERE.parent
D=R/'08-Entregas/P3-v5.3'
paths=[]
for p in (R/'06-Decisoes').glob('DEC-090*.md'):paths.append(p)
paths.extend((R/'08-Continuidade/Registros').glob('*P3-v5.3*.md'))
paths.append(R/'LEIA-ME-IMPORTAR-P3-V5.3.md')
paths.extend((R/'07-Scripts/P3').glob('*p3_v53.py'))
paths.extend(p for p in D.rglob('*') if p.is_file() and p.name!='SHA256SUMS-P3-V5.3.txt')
paths.sort(key=lambda p:str(p.relative_to(R)))
manifest=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(R))+'\n' for p in paths)
sha_path=R/'SHA256SUMS-P3-V5.3.txt';sha_path.write_text(manifest,encoding='utf-8')
paths.append(sha_path)
dest=Path('/mnt/data/portal-calculadoras-auditoria-P3-v5.3-unico.zip')
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in paths:z.write(p,str(p.relative_to(R)))
with zipfile.ZipFile(dest) as z:
 assert z.testzip() is None and len(z.namelist())==len(paths)
 assert set(x.filename for x in z.infolist())=={str(p.relative_to(R)) for p in paths}
print(json.dumps({'zip':str(dest),'bytes':dest.stat().st_size,'arquivos':len(paths),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()},ensure_ascii=False,indent=2))