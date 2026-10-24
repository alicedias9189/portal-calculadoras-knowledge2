#!/usr/bin/env python3
"""Gera planilha centralizada da revisão P3 v2.7 a partir dos CSVs produzidos.
Execução: python3 07-Scripts/P3/gerar_qa_p3_v27.py
Dependência: artifact_tool.
"""
import csv, pathlib, json
from artifact_tool import Workbook, SpreadsheetFile
ROOT=pathlib.Path(__file__).resolve().parents[2]
E=ROOT/'08-Entregas/P3-v2.7'

def read(name):
 with (E/name).open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f,delimiter=';'))

def sheet(wb,name,headers,rows):
 sh=wb.worksheets.add(name)
 allvalues=[headers]+rows
 n=len(allvalues);m=len(headers)
 sh.get_range_by_indexes(0,0,n,m).values=allvalues
 sh.get_range_by_indexes(0,0,n,m).format.horizontal_alignment='center'
 sh.get_range_by_indexes(0,0,n,m).format.vertical_alignment='center'
 sh.get_range_by_indexes(0,0,n,m).format.wrap_text=True
 sh.get_range_by_indexes(0,0,1,m).format={'fill':'#17324D','font':{'bold':True,'color':'#FFFFFF'},'horizontal_alignment':'center','vertical_alignment':'center','row_height':32}
 sh.get_range_by_indexes(0,0,n,m).format.row_height=34
 for i in range(m):
  sh.get_range_by_indexes(0,i,n,1).format.column_width = 37 if i in [2,3,4,5,6] else 21
 sh.freeze_panes.freeze_rows(1)
 return sh

W=Workbook.create()
sumry=json.loads((E/'p3-v2.7-resumo.json').read_text(encoding='utf-8'))
summary=[['Revisão P3 v2.7','Resultado'],['Decisões P3 revisadas',17],['Refinamentos P3 aplicados',1],['Decisões mantidas com ressalva',16],['Global B revisadas',30],['Global C revisadas',18],['Propostas globais aplicadas',0],['Lotes íntegros',30],['Registros-base',294905],['Controles',2190],['P3 fora dos pilotos',20383],['Pendências P2',4660],['Estado','Revisão técnica sem homologação editorial']]
sh=W.worksheets.add('Resumo')
sh.get_range_by_indexes(0,0,len(summary),2).values=summary
sh.get_range_by_indexes(0,0,len(summary),2).format.horizontal_alignment='center'
sh.get_range_by_indexes(0,0,len(summary),2).format.vertical_alignment='center'
sh.get_range_by_indexes(0,0,len(summary),2).format.row_height=29
sh.get_range('A1:B1').format={'fill':'#17324D','font':{'bold':True,'color':'#FFFFFF'},'horizontal_alignment':'center','vertical_alignment':'center'}
sh.get_range('A1:A13').format.column_width=39
sh.get_range('B1:B13').format.column_width=56

rr=read('p3-v2.7-revisao-critica-17.csv')
cols=['id_global','familia_id','Keyword','parecer_critico_v27','fundamentacao_v27','alteracao_no_lote_v27','homologacao_editorial_v27']
sheet(W,'P3 - 17 pareceres',cols,[[v.get(c,'') for c in cols] for v in rr])
rr=read('global-v27-pareceres-48.csv')
cols=['id_global','familia_id','Keyword','faixa_prioridade_global','regra','status_tecnico_v27','tipo_intencao_recomendado_v27','subtipo_recomendado_v27','fundamentacao_v27','homologacao_editorial_v27','aplicacao_lotes_v27']
sheet(W,'Global - 48 pareceres',cols,[[v.get(c,'') for c in cols] for v in rr])
rr=read('p3-v2.7-patches.csv')
cols=list(rr[0]);sheet(W,'Patch antes e depois',cols,[[v.get(c,'') for c in cols] for v in rr])
rr=read('p3-v2.7-regressao-independente.csv')
cols=list(rr[0]);sheet(W,'Regressao por lote',cols,[[v.get(c,'') for c in cols] for v in rr])
rr=read('backlog-global-98-com-parecer-v27.csv')
cols=['id_global','Keyword','faixa_prioridade_global','status_revisao_A','status_tecnico_v27','aplicacao_lotes_v27']
sheet(W,'Backlog global - 98',cols,[[v.get(c,'') for c in cols] for v in rr])
output=E/'qa-P3-v2.7-centralizada.xlsx'
SpreadsheetFile.export_xlsx(W).save(str(output))
print(output)
