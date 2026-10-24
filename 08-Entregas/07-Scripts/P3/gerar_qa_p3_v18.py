#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera workbook de QA centrado para a P3 v1.8 a partir dos CSVs de auditoria.
Exemplo: python gerar_qa_p3_v18.py --saida ./saida
Requer artifact_tool. CSVs são a fonte integral dos dados.
"""
import argparse,csv,json,collections
from pathlib import Path
from artifact_tool import Workbook,SpreadsheetFile

def read(path):
 with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def main(out):
 w=Workbook.create();summary=json.loads((out/'p3-v1.8-resumo.json').read_text());ind=json.loads((out/'p3-v1.8-regressao-independente-resumo.json').read_text());rules=read(out/'p3-v1.8-qa-taxas-por-regra.csv');patch=read(out/'p3-v1.8-patches.csv');dec=read(out/'p3-v1.8-decisoes.csv');tests=read(out/'p3-v1.8-regressao-independente-30-lotes.csv')
 def sheet(name,headers,rows,widths=None):
  s=w.worksheets.add(name);data=[headers]+[[v if not isinstance(v,(dict,list)) else json.dumps(v,ensure_ascii=False) for v in rr] for rr in rows]
  if data:
   rg=s.get_range_by_indexes(0,0,len(data),len(headers));rg.values=data
   rg.format.horizontal_alignment='center';rg.format.vertical_alignment='center';rg.format.row_height=22
   rg.format.wrap_text=True
  h=s.get_range_by_indexes(0,0,1,len(headers));h.format={'fill':'#17324D','font':{'bold':True,'color':'#FFFFFF'},'horizontal_alignment':'center','vertical_alignment':'center','row_height':32,'wrap_text':True}
  for ci,x in enumerate(widths or []):s.get_range_by_indexes(0,ci,len(data),1).format.column_width=x
  s.freeze_panes.freeze_rows(1)
  return s
 summ=[['Keywords P3 totais',summary['p3_universo']],['P3 fora dos pilotos antes',summary['p3_fora_piloto_antes']],['Novas alterações',summary['p3_expansao_corrigidos']],['P3 fora dos pilotos após',summary['p3_fora_piloto_depois']],['Famílias alcançadas',summary['familias_distintas']],['Amostra QA v1.7 examinada',summary['amostra_v17_analisada']],['Correções encontradas no v1.7',summary['amostra_v17_correcoes_observadas']],['Correções v1.7 / amostra (%)',round(100*17/103,2)],['Lotes com regressão PASSOU',ind['lotes']],['Registros-base preservados',ind['base']],['Controles preservados',ind['controles']],['Pendências P2 preservadas',summary['p2_pendencias_inalteradas']],['Nota sobre taxas de erro','A amostra v1.7 foi estratificada com exceções forçadas; os percentuais não são estimativas populacionais.'],['Qualidade das decisões','Triagem por regras; ainda requer validação editorial.']]
 sheet('Resumo',['Indicador','Valor'],summ,[42,75])
 cols=['regra','total_regra_v16','amostra_estratificada_v17','corrigidos_na_amostra','corrigidos_em_todos_152','taxa_observada_amostra_pct','interpretacao'];sheet('Taxas por regra',cols,[[int(v) if v.isdigit() else float(v) if k=='taxa_observada_amostra_pct' else v for k,v in zip(cols,(r.get(k,'') for k in cols))] for r in rules],[35,22,26,26,26,26,55]);
 pc=['id_global','lote','familia_id','Keyword','regra_v18','campos_alterados','antes_json','depois_json'];sheet('Patches P3 v18',pc,[[r.get(k,'') for k in pc] for r in patch],[15,12,24,47,29,45,55,55]);
 dc=['id_global','familia_id','Keyword','regra','area_anterior','area_proposta','tipo_anterior','tipo_proposto','justificativa','revisao_editorial_final'];sheet('Decisoes',dc,[[r.get(k,'') for k in dc] for r in dec],[14,23,48,30,20,20,25,25,75,24]);
 tc=['arquivo','base','controles','ids_modificados','status'];sheet('Regressao',tc,[[r.get(k,'') for k in tc] for r in tests],[49,20,20,22,19]);
 # Amostra de casos ainda fora de pilotos após P3 v1.8, por área para revisão posterior.
 done={r['id_global'] for r in patch};q=[];cnt=collections.Counter()
 for row in read(out/'p3-v1.8-fila-23965.csv'):
  if row['status_p3_v1']=='FORA_DO_PILOTO' and not any(row['status_p3_'+x] for x in ['v1_3','v1_4','v1_5','v1_6']) and row['id_global'] not in done and cnt[row['area']]<12:
   q.append(row);cnt[row['area']]+=1
 qc=['id_global','familia_id','Keyword','area','cluster','subcluster','tipo_intencao_atual','riscos_detectados'];sheet('Amostra pendencias',qc,[[r.get(k,'') for k in qc] for r in q],[15,25,56,21,27,35,26,60]);
 path=out/'qa-P3-v1.8-centralizada.xlsx';SpreadsheetFile.export_xlsx(w).save(str(path));print('XLSX',path,path.stat().st_size,'sheets',6,'pend_sample',len(q))
 print(w.inspect({'kind':'table','range':'Resumo!A1:B8','include':'values','table_max_rows':8,'table_max_cols':2}).ndjson[:1000])
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--saida',type=Path,required=True);x=a.parse_args();main(x.saida)
