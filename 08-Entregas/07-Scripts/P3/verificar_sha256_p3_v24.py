#!/usr/bin/env python3
# coding: utf-8
"""Verifica os hashes SHA256 de todos os arquivos da entrega P3 v2.4.
Uso: python verificar_sha256_p3_v24.py <pasta_extraida>
"""
import pathlib,hashlib,sys

def main():
    root=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
    manifest=root/'SHA256SUMS-P3-V2.4.txt'
    assert manifest.is_file(),'Manifesto SHA-256 ausente'
    entries=0
    for line in manifest.read_text(encoding='utf-8').splitlines():
        if not line.strip(): continue
        sha,rel=line.split('  ',1)
        target=(root/rel).resolve()
        assert root in target.parents and target.is_file(),('arquivo ausente/inválido',rel)
        h=hashlib.sha256()
        with target.open('rb') as f:
            for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
        assert h.hexdigest()==sha,('SHA-256 divergente',rel)
        entries+=1
    print(f'PASSOU: {entries} arquivos conferidos com SHA-256')
if __name__=='__main__':main()
