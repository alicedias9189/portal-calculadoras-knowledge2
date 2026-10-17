#!/usr/bin/env python3
"""Gera auditoria consolidada centralizada para os 30 lotes."""
import argparse
import csv
from pathlib import Path
from artifact_tool import Workbook, SpreadsheetFile
ap=argparse.ArgumentParser(description='Gera workbook centrado de auditoria dos 30 lotes')
ap.add_argument('--root', default='.', help='Pasta contendo CSV consolidado e pendências')
R=Path(ap.parse_args().root).resolve()
def rd(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.reader(f,delimiter=';'))
data=rd(R/'resumo-consolidado-30-lotes.csv')
pending=rd(R/'pendencias-metadados-diretos-lote-001.csv')
wb=Workbook.create()
def table(name,matrix,widths):
 s=wb.worksheets.add(name)
 s.get_range_by_indexes(0,0,len(matrix),len(matrix[0])).values=matrix
 rng=s.get_range_by_indexes(0,0,len(matrix),len(matrix[0]));rng.format.horizontal_alignment='center';rng.format.vertical_alignment='center'
 s.get_range_by_indexes(0,0,1,len(matrix[0])).format={"fill":"#1F4E78","font":{"bold":True,"color":"#FFFFFF"},"horizontal_alignment":"center","vertical_alignment":"center"}
 s.freeze_panes.freeze_rows(1)
 for i,w in enumerate(widths):s.get_range_by_indexes(0,i,len(matrix),1).format.column_width=w
 return s
summary=[['Auditoria global — 30 lotes',''],['Status','30/30 lotes processados; pendência histórica no lote 001'],['Base completa',294905],['IDs únicos',294905],['Controles',2190],['Golden Set','3210/3210'],['Flags finais',0],['Conversões diretas sem metadados — lote 001',73],['Conversões diretas sem metadados — lotes 002 a 030',0],['Confiança alta',199960],['Confiança média',46361],['Confiança baixa',48584],['Revisão manual pendente',52050],['Reconstruções de barras',835],['Duplicações entre lotes',0]]
table('Resumo',summary,[55,65])
table('Lotes',data,[12,12,14,13,12,12,16,17,17,18,22,23,24,25])
table('Pendencias_lote_001',pending,[10,14,58,22,32])
out=R/'auditoria-consolidada-30-lotes-centralizada.xlsx'
SpreadsheetFile.export_xlsx(wb).save(str(out));print(out)
