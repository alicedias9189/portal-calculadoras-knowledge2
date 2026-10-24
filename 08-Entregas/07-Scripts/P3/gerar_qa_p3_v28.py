#!/usr/bin/env python3
"""Gera workbook QA P3 v2.8 com artifact_tool, alinhamento central para TODAS as células usadas."""
import csv,json,pathlib,collections
from artifact_tool import Workbook,SpreadsheetFile
ROOT=pathlib.Path(__file__).resolve().parents[2]
E=ROOT/'08-Entregas/P3-v2.8'

def load(n):
 with (E/n).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))

def make_sheet(wb,title,columns,rows):
 sh=wb.worksheets.add(title);n=len(rows)+1;m=len(columns)
 arr=[columns]+[[r.get(c,'') for c in columns] for r in rows]
 sh.get_range_by_indexes(0,0,n,m).values=arr
 r=sh.get_range_by_indexes(0,0,n,m)
 r.format.horizontal_alignment='center';r.format.vertical_alignment='center';r.format.wrap_text=True;r.format.row_height=30
 header=sh.get_range_by_indexes(0,0,1,m)
 header.format={'fill':'#243956','font':{'color':'#FFFFFF','bold':True},'horizontal_alignment':'center','vertical_alignment':'center','row_height':33}
 for i in range(m):
  sh.get_range_by_indexes(0,i,n,1).format.column_width=(37 if columns[i] in ('Keyword','justificativa','nota_critica','antes_json','depois_json') else 24)
 sh.freeze_panes.freeze_rows(1)
 return sh
W=Workbook.create()
s=json.loads((E/'p3-v2.8-resumo.json').read_text(encoding='utf-8'))
rows=[('Indicador','Resultado'),('Versão','P3 v2.8'),('Patches P3',s['alteracoes']),('Famílias',s['familias']),('Amostra integral QA',s['qa_integral']),('Lotes aprovados',s['lotes']),('Registros-base',s['registros_base']),('Controles',s['controles']),('Fila P3','23.965'),('Fila geral','52.046'),('P3 não classificada v2.7 — reconstruída',s['elegiveis_nao_classificados_reconciliados_v27']),('P3 não classificada v2.8 — reconstruída',s['p3_elegiveis_nao_classificados_v28']),('Relatório antigo v2.7',s['p3_fora_pilotos_reportados_v27']),('Discrepância do relatório antigo',s['divergencia_em_registro_historico']),('Backlog global separado',98),('Pendências P2',4660)]
sh=W.worksheets.add('Resumo')
sh.get_range_by_indexes(0,0,len(rows),2).values=[list(x) for x in rows]
r=sh.get_range_by_indexes(0,0,len(rows),2);r.format.horizontal_alignment='center';r.format.vertical_alignment='center';r.format.row_height=27
sh.get_range('A1:B1').format={'fill':'#243956','font':{'color':'#FFFFFF','bold':True},'horizontal_alignment':'center','vertical_alignment':'center'}
sh.get_range('A1:A16').format.column_width=49;sh.get_range('B1:B16').format.column_width=26
r=load('p3-v2.8-decisoes.csv');columns=['id_global','lote','familia_id','Keyword','regra','parecer','justificativa']
make_sheet(W,'Decisoes - 66',columns,r)
r=load('p3-v2.8-revisao-qa-integral.csv');columns=['id_global','Keyword','regra','qa_critica_p3_v2_8','nota_critica','justificativa']
make_sheet(W,'QA integral - 66',columns,r)
r=load('p3-v2.8-patches.csv');columns=['id_global','Keyword','regra','campos_modificados','antes_json','depois_json']
make_sheet(W,'Patches',columns,r)
r=load('p3-v2.8-regressao-independente.csv');columns=list(r[0]);make_sheet(W,'Regressao 30',columns,r)
r=load('p3-v2.8-testes-seletor.csv');columns=list(r[0]);make_sheet(W,'Testes seletor',columns,r)
r=load('p3-v2.8-reconciliacao-contagem.csv');columns=list(r[0]);make_sheet(W,'Conciliacao P3',columns,r)
for r in W.worksheets.items if False else []:pass
print(W.inspect({'kind':'table','range':'Resumo!A1:B8','include':'values','table_max_rows':8,'table_max_cols':2}).ndjson[:900])
out=E/'qa-P3-v2.8-centralizada.xlsx'
SpreadsheetFile.export_xlsx(W).save(str(out));print(out)
