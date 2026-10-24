#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cria workbook QA da P3 v3.1 com artifact_tool, células centralizadas.
Uso: python 07-Scripts/P3/gerar_qa_p3_v31.py
"""
import csv,json,collections
from pathlib import Path
from artifact_tool import Workbook, SpreadsheetFile
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'08-Entregas/P3-v3.1'

def read(name):
 with (OUT/name).open(encoding='utf-8-sig',newline='') as f:
  rd=csv.DictReader(f,delimiter=';');return list(rd),list(rd.fieldnames)

def make_sheet(wb,title,cols,data):
 ws=wb.worksheets.add(title)
 table=[list(cols)]+[[(r.get(c,'') if isinstance(r,dict) else r[i]) for i,c in enumerate(cols)] for r in data]
 rg=ws.get_range_by_indexes(0,0,len(table),len(cols))
 rg.values=table
 rg.format.horizontal_alignment='center'
 rg.format.vertical_alignment='center'
 rg.format.row_height=29
 rg.format.column_width=21
 header=ws.get_range_by_indexes(0,0,1,len(cols))
 header.format.fill='#17324D'
 header.format.font.color='#FFFFFF'
 header.format.font.bold=True
 header.format.row_height=34
 if len(table)>1:
  body=ws.get_range_by_indexes(1,0,len(table)-1,len(cols))
  body.format.wrap_text=True
 ws.freeze_panes.freeze_rows(1)
 return ws

parecer,pareccols=read('p3-v3.1-pareceres-36.csv')
patches,patchcols=read('p3-v3.1-patches.csv')
reg,regcols=read('p3-v3.1-regressao-independente-30-lotes.csv')
info=json.loads((OUT/'p3-v3.1-resumo.json').read_text(encoding='utf-8'))
counts=collections.Counter(r['parecer_p3_v3_1'] for r in parecer)
rules=collections.Counter(r['regra'] for r in parecer)
fixrules=collections.Counter(r['regra_qa'] for r in patches)
wb=Workbook.create()
rows=[
 ('Indicador','Resultado'),('Versão','P3 v3.1'),('Decisões criticamente revisadas',info['auditoria_de_registros']),
 ('Correções efetivas',info['patches']),('Mantidas com ressalvas',info['mantidos_com_ressalvas']),
 ('30 lotes validados','PASSOU'),('Registros-base',info['bases']),('Controles',info['controles']),
 ('P3 fora dos pilotos',info['pendencias_p3_fora_dos_pilotos']),('Pendências P2',info['pendencias_p2']),
 ('Casos globais separados',info['quarentena_global']),('Homologação editorial','Pendente')]
ws=wb.worksheets.add('Resumo')
ws.get_range('A1:B12').values=[list(x) for x in rows]
ws.get_range('A1:B12').format.horizontal_alignment='center'
ws.get_range('A1:B12').format.vertical_alignment='center'
ws.get_range('A1:B12').format.row_height=26
ws.get_range('A1:A12').format.column_width=35
ws.get_range('B1:B12').format.column_width=24
ws.get_range('A1:B1').format.fill='#17324D'
ws.get_range('A1:B1').format.font.color='#FFFFFF'
ws.get_range('A1:B1').format.font.bold=True
ws.freeze_panes.freeze_rows(1)
# exclude repeated commentary columns? retain full review in CSV and XLSX
make_sheet(wb,'Pareceres 36',pareccols,parecer)
make_sheet(wb,'Patches 8',patchcols,patches)
make_sheet(wb,'Regressao 30',regcols,reg)
rdata=[{'regra':k,'avaliados':n,'corrigidos':sum(x['parecer_p3_v3_1']=='CORRIGIDO' for x in parecer if x['regra']==k)} for k,n in sorted(rules.items())]
make_sheet(wb,'Regras v3.0',['regra','avaliados','corrigidos'],rdata)
fdata=[{'regra_correcao':k,'registros':n} for k,n in sorted(fixrules.items())]
make_sheet(wb,'Refinamentos',['regra_correcao','registros'],fdata)
path=OUT/'qa-auditoria-P3-v3.1-centralizada.xlsx'
SpreadsheetFile.export_xlsx(wb).save(str(path))
print(f'Excel gerado: {path} ({path.stat().st_size} bytes), 6 abas')
