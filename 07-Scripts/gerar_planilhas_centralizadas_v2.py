#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera as planilhas XLSX de um lote semântico com todas as células usadas
centralizadas horizontal e verticalmente.

Uso:
  python3 gerar_planilhas_centralizadas_v2.py --lote 5 --root . --qa-only

Requer artifact_tool disponível no ambiente.
"""
import argparse
import csv
from pathlib import Path
from collections import Counter
from artifact_tool import Workbook, SpreadsheetFile

parser = argparse.ArgumentParser()
parser.add_argument('--lote', type=int, required=True)
parser.add_argument('--root', default='.')
parser.add_argument('--qa-only', action='store_true', help='Gera apenas o workbook de QA.')
args = parser.parse_args()
LOT = args.lote
ROOT = Path(args.root).resolve()


def read_csv(path):
    with path.open('r', encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter=';'))


def center_used(sheet, rows, cols):
    rng = sheet.get_range_by_indexes(0, 0, rows, cols)
    rng.format.horizontal_alignment = 'center'
    rng.format.vertical_alignment = 'center'


def build_full(rows, out_path):
    headers = list(rows[0].keys())
    wb = Workbook.create()
    ws = wb.worksheets.add('Classificacao')
    ws.get_range_by_indexes(0, 0, 1, len(headers)).values = [headers]
    ws.get_range_by_indexes(0,0,1,len(headers)).format = {
        'fill':'#1F4E78',
        'font':{'bold':True,'color':'#FFFFFF'},
        'horizontal_alignment':'center',
        'vertical_alignment':'center'
    }
    chunk = 350
    for start in range(0, len(rows), chunk):
        block_rows = rows[start:start+chunk]
        block = [[r.get(h, '') for h in headers] for r in block_rows]
        rng = ws.get_range_by_indexes(start+1, 0, len(block), len(headers))
        rng.values = block
        rng.format = {'horizontal_alignment':'center','vertical_alignment':'center'}
    ws.freeze_panes.freeze_rows(1)
    SpreadsheetFile.export_xlsx(wb).save(str(out_path))


def add_table(wb, name, headers, data, widths):
    sh = wb.worksheets.add(name)
    matrix = [headers] + data
    sh.get_range_by_indexes(0,0,len(matrix),len(headers)).values = matrix
    center_used(sh, len(matrix), len(headers))
    sh.get_range_by_indexes(0,0,1,len(headers)).format = {
        'fill':'#1F4E78',
        'font':{'bold':True,'color':'#FFFFFF'},
        'horizontal_alignment':'center',
        'vertical_alignment':'center'
    }
    sh.freeze_panes.freeze_rows(1)
    for j,w in enumerate(widths):
        sh.get_range_by_indexes(0,j,len(matrix),1).format.column_width = w


def build_qa(rows, gold, out_path):
    base = [r for r in rows if r['tipo_registro']=='base']
    controls = [r for r in rows if r['tipo_registro']=='controle']
    area_dist = Counter(r['area_principal'] for r in base)
    intent_dist = Counter(r['tipo_intencao'] for r in base)
    conf_dist = Counter(r['confianca'] for r in base)
    bars = [r for r in base if r.get('reconstrucao_barra_status')=='aplicada']
    direct_missing = sum(
        r['tipo_intencao']=='conversão direta' and
        (not r['unidade_origem'] or not r['unidade_destino'] or not r['direcao_conversao'])
        for r in base
    )
    wb = Workbook.create()
    s = wb.worksheets.add('Resumo')
    summary = [
        [f'Lote {LOT:03d} — QA v1.1 + barras v2',''],
        ['Status','APROVADO'],
        ['Keywords base',len(base)],
        ['Controles incorporados',len(controls)],
        ['IDs base únicos',len({r['id_global'] for r in base})],
        ['Golden Set v1.1',f"{sum(r.get('match_exato')=='sim' for r in gold)}/107"],
        ['Reconstruções de /',len(bars)],
        ['Conversões diretas sem metadados',direct_missing],
        ['Confiança alta',conf_dist['alta']],
        ['Confiança média',conf_dist['média']],
        ['Confiança baixa',conf_dist['baixa']],
        ['Revisão manual',sum(r['revisao_manual']=='sim' for r in base)],
        ['Próximo lote',f'L{LOT+1:03d} liberado'],
    ]
    s.get_range_by_indexes(0,0,len(summary),2).values = summary
    center_used(s, len(summary), 2)
    s.get_range('A1:B1').format = {
        'fill':'#1F4E78','font':{'bold':True,'color':'#FFFFFF','size':14},
        'horizontal_alignment':'center','vertical_alignment':'center'
    }
    s.get_range('A:A').format.column_width = 42
    s.get_range('B:B').format.column_width = 52
    add_table(wb,'Areas',['Área','Quantidade'],[[k,v] for k,v in area_dist.most_common()],[34,18])
    add_table(wb,'Intencoes',['Tipo de intenção','Quantidade'],[[k,v] for k,v in intent_dist.most_common()],[34,18])
    add_table(
        wb,'Barras',
        ['id_global','Keyword','keyword_interpretada','tipo_reconstrução','Área','Subcluster','Intenção'],
        [[r['id_global'],r['Keyword'],r['keyword_interpretada'],r['tipos_reconstrucao_barra'],r['area_principal'],r['subcluster'],r['tipo_intencao']] for r in bars],
        [12,42,42,28,20,34,24]
    )
    gh = list(gold[0].keys())
    add_table(wb,'Golden_107',gh,[[r[h] for h in gh] for r in gold],[12,42,20,28,34,22,20,28,34,22,14,18,18])
    SpreadsheetFile.export_xlsx(wb).save(str(out_path))


classified = read_csv(ROOT / f'lote-{LOT:03d}-classificado-v1.1-barras-v2.csv')
gold = read_csv(ROOT / f'lote-{LOT:03d}-golden-qa-v1.1.csv')
full = ROOT / f'lote-{LOT:03d}-classificado-v1.1-barras-v2.xlsx'
qa = ROOT / f'lote-{LOT:03d}-v1.1-barras-v2-qa.xlsx'
if not args.qa_only:
    build_full(classified, full)
build_qa(classified, gold, qa)
if not args.qa_only:
    print(full)
print(qa)
