#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera a planilha de QA de um lote com todas as células usadas centralizadas.

Dependência do ambiente de execução desta rotina: artifact_tool.

Uso:
    python3 gerar_qa_centralizado_v1.py --lote 4 --root .

Entradas esperadas:
    lote-NNN-classificado-v1.1-barras-v2.csv
    lote-NNN-golden-qa-v1.1.csv

Saída:
    lote-NNN-v1.1-barras-v2-qa.xlsx
"""
import argparse
import csv
from collections import Counter
from pathlib import Path
from artifact_tool import Workbook, SpreadsheetFile

parser = argparse.ArgumentParser()
parser.add_argument('--lote', type=int, required=True)
parser.add_argument('--root', default='.')
args = parser.parse_args()
LOT = args.lote
ROOT = Path(args.root).resolve()


def read_csv(path):
    with path.open('r', encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter=';'))


classified = read_csv(ROOT / f'lote-{LOT:03d}-classificado-v1.1-barras-v2.csv')
golden = read_csv(ROOT / f'lote-{LOT:03d}-golden-qa-v1.1.csv')
base = [r for r in classified if r['tipo_registro'] == 'base']
controls = [r for r in classified if r['tipo_registro'] == 'controle']
area_dist = Counter(r['area_principal'] for r in base)
intent_dist = Counter(r['tipo_intencao'] for r in base)
conf_dist = Counter(r['confianca'] for r in base)
bar_rows = [r for r in base if r.get('reconstrucao_barra_status') == 'aplicada']
direct_missing = sum(
    r['tipo_intencao'] == 'conversão direta'
    and (not r['unidade_origem'] or not r['unidade_destino'] or not r['direcao_conversao'])
    for r in base
)
review = sum(r['revisao_manual'] == 'sim' for r in base)
gold_exact = sum(r.get('match_exato') == 'sim' for r in golden)

wb = Workbook.create()
header_fmt = {
    'fill': '#1F4E78',
    'font': {'bold': True, 'color': '#FFFFFF'},
    'horizontal_alignment': 'center',
    'vertical_alignment': 'center',
    'wrap_text': True,
}


def centered_format(rng):
    rng.format = {
        'horizontal_alignment': 'center',
        'vertical_alignment': 'center',
        'wrap_text': True,
    }


def add_table(name, headers, data, widths):
    sh = wb.worksheets.add(name)
    matrix = [headers] + data
    sh.get_range_by_indexes(0, 0, len(matrix), len(headers)).values = matrix
    centered_format(sh.get_range_by_indexes(0, 0, len(matrix), len(headers)))
    sh.get_range_by_indexes(0, 0, 1, len(headers)).format = header_fmt
    sh.freeze_panes.freeze_rows(1)
    for j, width in enumerate(widths[:len(headers)]):
        sh.get_range_by_indexes(0, j, len(matrix), 1).format.column_width = width
    return sh


summary = [
    [f'Lote {LOT:03d} — QA v1.1 + barras v2', ''],
    ['Keywords base', len(base)],
    ['Controles incorporados', len(controls)],
    ['IDs base únicos', len({r['id_global'] for r in base})],
    ['Golden Set v1.1', f'{gold_exact}/107'],
    ['Reconstruções de /', len(bar_rows)],
    ['Conversões diretas sem metadados', direct_missing],
    ['Confiança alta', conf_dist['alta']],
    ['Confiança média', conf_dist['média']],
    ['Confiança baixa', conf_dist['baixa']],
    ['Revisão manual', review],
]
ws = wb.worksheets.add('Resumo')
ws.get_range_by_indexes(0, 0, len(summary), 2).values = summary
centered_format(ws.get_range_by_indexes(0, 0, len(summary), 2))
ws.get_range('A1:B1').format = {
    'fill': '#1F4E78',
    'font': {'bold': True, 'color': '#FFFFFF', 'size': 14},
    'horizontal_alignment': 'center',
    'vertical_alignment': 'center',
    'wrap_text': True,
}
ws.get_range('A:A').format.column_width = 42
ws.get_range('B:B').format.column_width = 52

add_table('Areas', ['Área', 'Quantidade'], [[k, v] for k, v in area_dist.most_common()], [34, 18])
add_table('Intencoes', ['Tipo de intenção', 'Quantidade'], [[k, v] for k, v in intent_dist.most_common()], [34, 18])
add_table(
    'Barras',
    ['id_global', 'Keyword', 'keyword_interpretada', 'tipo_reconstrução', 'Área', 'Subcluster', 'Intenção'],
    [[r['id_global'], r['Keyword'], r['keyword_interpretada'], r['tipos_reconstrucao_barra'], r['area_principal'], r['subcluster'], r['tipo_intencao']] for r in bar_rows],
    [12, 44, 44, 28, 20, 34, 24],
)
headers = list(golden[0].keys())
add_table('Golden_107', headers, [[r[h] for h in headers] for r in golden], [12, 44, 20, 28, 34, 22, 20, 28, 34, 22, 14, 18, 18])

out = ROOT / f'lote-{LOT:03d}-v1.1-barras-v2-qa.xlsx'
SpreadsheetFile.export_xlsx(wb).save(str(out))
print(f'Criado: {out}')
