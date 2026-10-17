#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reaplica o patch aprovado das 474 keywords P0 sem modificar lotes originais.

Requer: correcoes-objetivas-p0.csv do pacote de revisao P0,
saneamento-revisao-30-lotes/lote-001-saneado-v1.1-barras-v2.csv,
lote-003-v1.1-barras-v2-aprovado.zip, demais lotes classificados.
Uso:
 python3 aplicar_correcoes_p0_de_csv_v1.py --root . \
   --patch revisao-p0-30-lotes/correcoes-objetivas-p0.csv \
   --out revisao-p0-30-lotes-reproduzido
"""
import argparse
import csv
import json
import zipfile
from collections import defaultdict
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('--root', default='.')
ap.add_argument('--patch', required=True)
ap.add_argument('--out', default='revisao-p0-reproduzido')
args = ap.parse_args()
root = Path(args.root).resolve()
patch_path = Path(args.patch)
if not patch_path.is_absolute():
    patch_path = root / patch_path
dest = Path(args.out)
if not dest.is_absolute():
    dest = root / dest
dest.mkdir(parents=True, exist_ok=True)

def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream, delimiter=';'))

def write_csv(path, rows, fields):
    with path.open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter=';')
        writer.writeheader()
        writer.writerows(rows)

patches = read_csv(patch_path)
if len(patches) != 462:
    raise ValueError(f'Esperado patch aprovado com 462 linhas; encontrado: {len(patches)}')
by_lot = defaultdict(dict)
for item in patches:
    lot = int(item['lote'])
    key = item['id_global']
    if key in by_lot[lot]:
        raise ValueError('ID duplicado no patch: ' + key)
    by_lot[lot][key] = item
assert len({p['id_global'] for p in patches}) == 462

original_fields = [
    'tipo_registro', 'id_global', 'lote_id', 'familia_id', 'controle_id',
    'Keyword', 'ocorrencias_origem', 'areas_origem', 'qtd_areas',
    'Avg. monthly searches', 'Mudança em três meses', 'Mudança YoY',
    'Competition', 'Competition (indexed value)',
    'Top of page bid (low range)', 'Top of page bid (high range)'
]
total_base = 0
total_changed = 0
for lot in range(1, 31):
    if lot == 1:
        rows = read_csv(root / 'saneamento-revisao-30-lotes' / 'lote-001-saneado-v1.1-barras-v2.csv')
    elif lot == 3:
        with zipfile.ZipFile(root / 'lote-003-v1.1-barras-v2-aprovado.zip') as archive:
            matches = [name for name in archive.namelist()
                       if name.endswith('lote-003-classificado-v1.1-barras-v2.csv')]
            if len(matches) != 1:
                raise ValueError('CSV do lote 003 não encontrado de modo único no ZIP')
            rows = list(csv.DictReader(
                archive.read(matches[0]).decode('utf-8-sig').splitlines(),
                delimiter=';'
            ))
    else:
        rows = read_csv(root / f'lote-{lot:03d}-classificado-v1.1-barras-v2.csv')
    fields = list(rows[0])
    if not all(f in fields for f in original_fields):
        raise ValueError(f'Colunas Google Ads inesperadas no lote {lot}')
    local = by_lot[lot]
    seen = set()
    ids = set()
    controls = 0
    for row in rows:
        if row['tipo_registro'] == 'controle':
            controls += 1
            if row['id_global'] in local:
                raise ValueError('Patch tentou modificar controle')
            continue
        ids.add(row['id_global'])
        if row['id_global'] not in local:
            continue
        patch = local[row['id_global']]
        if row['Keyword'] != patch['Keyword']:
            raise ValueError('Keyword divergente do patch: ' + row['id_global'])
        before = json.loads(patch['antes_json'])
        after = json.loads(patch['depois_json'])
        if set(before) != set(after):
            raise ValueError('Campos antes/depois divergentes')
        if any(key in original_fields for key in after):
            raise ValueError('Patch tentou alterar coluna original')
        for key, old in before.items():
            if row.get(key, '') != old:
                raise ValueError(f'Pré-condição incorreta no ID {row["id_global"]}, campo {key}')
        row.update(after)
        seen.add(row['id_global'])
        total_changed += 1
    if seen != set(local):
        raise ValueError(f'Lote {lot}: IDs do patch não encontrados: {set(local) - seen}')
    if controls != 73 or len(ids) != sum(r['tipo_registro']=='base' for r in rows):
        raise ValueError(f'Lote {lot}: controle/IDs inválidos')
    if any(r['tipo_registro']=='base' and r['tipo_intencao']=='conversão direta'
           and not all(r[field] for field in ('unidade_origem','unidade_destino','direcao_conversao'))
           for r in rows):
        raise ValueError(f'Lote {lot}: conversões diretas base sem metadados')
    total_base += len(ids)
    write_csv(dest / f'lote-{lot:03d}-revisado-p0-v1.1-barras-v2.csv', rows, fields)
if total_base != 294905 or total_changed != 462:
    raise ValueError(f'Invariantes falharam: {total_base} bases, {total_changed} mudanças')
print('Revisão P0 reaplicada: 30 lotes; 294905 bases; 462 alterações; 2190 controles preservados.')
