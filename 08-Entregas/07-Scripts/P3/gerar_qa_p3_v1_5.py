#!/usr/bin/env python3
"""Cria Excel P3 v1.5 exclusivamente com artifact_tool, todas células centralizadas.
Uso: python gerar_qa_p3_v1_5.py --saida DIR
"""
import argparse,csv,json,collections
from pathlib import Path
from artifact_tool import Workbook,SpreadsheetFile

def rows(path):
 with open(path,encoding='utf-8-sig',newline='') as f:
  r=csv.reader(f,delimiter=';'); return [[str(x) for x in row] for row in r]
def make(wb,name,matrix):
 s=wb.worksheets.add(name)
 if not matrix:return
 width=max(map(len,matrix));matrix=[r+['']*(width-len(r)) for r in matrix]
 chunk=120
 for n in range(0,len(matrix),chunk):
  s.get_range_by_indexes(n,0,min(chunk,len(matrix)-n),width).values=matrix[n:n+chunk]
 rg=s.get_range_by_indexes(0,0,len(matrix),width)
 rg.format.horizontal_alignment='center';rg.format.vertical_alignment='center'
 rg.format.row_height=26
 s.get_range_by_indexes(0,0,1,width).format={'fill':'#17324D','font':{'bold':True,'color':'#FFFFFF'},'horizontal_alignment':'center','vertical_alignment':'center','row_height':32}
 s.get_range_by_indexes(0,0,len(matrix),width).format.column_width=24
 for j,header in enumerate(matrix[0]):
  if 'Keyword' in header or 'justificativa' in header or 'motivo' in header:
   s.get_range_by_indexes(0,j,len(matrix),1).format.column_width=48
  elif 'antes_json' in header or 'depois_json' in header:
   s.get_range_by_indexes(0,j,len(matrix),1).format.column_width=56
  elif 'id_global' in header:s.get_range_by_indexes(0,j,len(matrix),1).format.column_width=15
 if len(matrix)>1:s.freeze_panes.freeze_rows(1)
 return s

def main():
 p=argparse.ArgumentParser();p.add_argument('--saida',type=Path,required=True);a=p.parse_args();out=a.saida
 stats=json.loads((out/'p3-v1.5-resumo.json').read_text(encoding='utf8'));qa=json.loads((out/'p3-v1.5-regressao-resumo.json').read_text(encoding='utf8'))
 r=rows(out/'p3-v1.5-decisoes-por-id.csv');rule_counts=collections.Counter(x[5] for x in r[1:]);families=collections.defaultdict(set)
 for x in r[1:]:families[x[5]].add(x[2])
 metrics=[['Indicador','Resultado'],['Etapa','P3 v1.5'],['Amostra crítica',stats['amostra_critica']],['Correções na amostra',stats['corrigidos_na_amostra']],['Correções propagadas (inclui amostra)',stats['propagacao_qa_total']],['Novas reclassificações',stats['expansao_novas_keywords']],['Novas famílias distintas',stats['expansao_familias']],['Patches totais',stats['patches_totais']],['P3 ainda fora dos pilotos',stats['p3_fora_pilotos_depois']],['P3 universo',stats['p3_universo']],['Controles intactos',qa['controles']],['Bases intactas',qa['registros_base']],['Lotes com regressão PASSOU',qa['lotes_PASSOU']],['Resultado geral',qa['result']],['Importante','Revisão por regras: ainda não é homologação editorial.'],['Próxima fase','Auditar amostra de novas decisões e ampliar com regras específicas.']]
 wb=Workbook.create()
 make(wb,'Resumo',metrics)
 make(wb,'Pareceres amostra 98',rows(out/'p3-v1.5-amostra-98-pareceres.csv'))
 make(wb,'Decisoes P3 v1.5',rows(out/'p3-v1.5-decisoes-por-id.csv'))
 make(wb,'Patches antes depois',rows(out/'p3-v1.5-patches.csv'))
 make(wb,'Regras e familias',[['regra','patches','familias']]+[[key,num,len(families[key])] for key,num in sorted(rule_counts.items(),key=lambda x:-x[1])])
 make(wb,'Pendencias temporais',rows(out/'p3-v1.5-exclusoes-contextuais.csv'))
 make(wb,'Regressao 30 lotes',rows(out/'p3-v1.5-regressao-independente-30-lotes.csv'))
 dest=out/'qa-auditoria-P3-v1.5-centralizada.xlsx';SpreadsheetFile.export_xlsx(wb).save(str(dest));print('Output:',dest,'size',dest.stat().st_size)
 print(wb.inspect({'kind':'table','range':'Resumo!A1:B16','include':'values','table_max_rows':16,'table_max_cols':2}).ndjson[:1600])
if __name__=='__main__':main()
