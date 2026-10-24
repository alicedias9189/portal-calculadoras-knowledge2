#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""Gera a planilha de QA P3 v1.9 (artifact_tool)."""
import argparse,csv,json
from pathlib import Path
from artifact_tool import Workbook,SpreadsheetFile

def readcsv(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def mk(wb,name,columns,rows,widths=None):
 sh=wb.worksheets.add(name)
 data=[columns]+[[r.get(c,'') for c in columns] if isinstance(r,dict) else r for r in rows]
 rg=sh.get_range_by_indexes(0,0,len(data),len(columns));rg.values=data
 rg.format.horizontal_alignment='center';rg.format.vertical_alignment='center';rg.format.row_height=23
 rg.format.wrap_text=True
 hd=sh.get_range_by_indexes(0,0,1,len(columns));hd.format={'fill':'#17324D','font':{'bold':True,'color':'#FFFFFF'},'horizontal_alignment':'center','vertical_alignment':'center','row_height':30,'wrap_text':True}
 for k,w in enumerate(widths or [26]*len(columns)):sh.get_range_by_indexes(0,k,len(data),1).format.column_width=w
 sh.freeze_panes.freeze_rows(1)
 return sh

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--saida',required=True,type=Path);a=ap.parse_args();o=a.saida
 review=readcsv(o/'p3-v1.9-pareceres-83.csv');patch=readcsv(o/'p3-v1.9-patches-10.csv');rules=readcsv(o/'p3-v1.9-qa-por-regra.csv');reg=readcsv(o/'p3-v1.9-regressao-independente-30-lotes.csv')
 info=json.loads((o/'p3-v1.9-resumo.json').read_text());wb=Workbook.create()
 mk(wb,'Resumo',['Indicador','Resultado'],[
  ['Etapa','P3 v1.9 — Revisão crítica da P3 v1.8'],['IDs auditados',83],['Correções efetivas',10],['Mantidas sem alerta',19],['Mantidas com ressalva',54],
  ['Famílias expandidas nesta passagem',0],['P3 ainda fora dos pilotos',20672],['P2 pendências preservadas',4660],['Lotes auditados',30],['Registros-base',294905],['Controles',2190],['Regressão independente','PASSOU'],['Critério','Decisões por ID; não propagar para família inteira'],['Limite','Parecer técnico por texto, sem homologação editorial externa']], [37,83])
 mk(wb,'QA por regra',['regra','examinados','ajustados','mantidos_com_ressalva','mantidos'],rules,[36,18,16,30,18])
 cols=['id_global','lote','familia_id','Keyword','regra_v18','area_resultante','tipo_intencao_resultante','parecer_v19','houve_patch','nota_qa','homologacao_editorial']
 mk(wb,'Pareceres 83',cols,review,[14,13,26,50,31,23,26,28,17,88,27])
 r=[]
 for x in patch:
  row=dict(x);row['antes_json']='; '.join(f'{k}: {v}' for k,v in json.loads(x['antes_json']).items());row['depois_json']='; '.join(f'{k}: {v}' for k,v in json.loads(x['depois_json']).items());r.append(row)
 cols=['id_global','lote','Keyword','regra_v18','campos_alterados','antes_json','depois_json','motivo']
 mk(wb,'Patches 10',cols,r,[13,10,50,35,58,87,87,95])
 cols=['lote','registros_base','controles','patches','status']
 mk(wb,'Regressão 30',cols,reg,[55,22,19,17,20])
 mk(wb,'Continuidade',['Campo','Informação'],[
  ['Base original','P3 v1.8. Os 30 lotes ficam no ZIP P3 v1.9 sem sobrescrever P3 v1.8.'],
  ['Consulta crítica','83 decisões; 10 corrigidas; 73 mantidas com/sem ressalva.'],
  ['Próximo passo','Auditar novas famílias P3 de forma seletiva com amostragem e revisão das regras frágeis.'],
  ['Risco','Consultas financeiras e trabalhistas podem exigir período/competência ou dados adicionais.'],
  ['Taxonomia','Preservadas áreas e agrupamentos aprovados, sem alteração automática por família.'],
  ['GitHub','Importação manual do ZIP; ver README e registro de continuidade.']],[30,115])
 p=o/'qa-P3-v1.9-centralizada.xlsx';SpreadsheetFile.export_xlsx(wb).save(str(p));print(p,p.stat().st_size)
if __name__=='__main__':main()
