#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Planilha QA resumida para P2 v5; CSVs completos seguem nos ZIPs."""
import json,zipfile,csv,io,argparse
from pathlib import Path
from collections import Counter
from artifact_tool import Workbook, SpreadsheetFile

def load(z,name):return list(csv.DictReader(io.TextIOWrapper(z.open(name),encoding='utf-8-sig',newline=''),delimiter=';'))
def main():
 p=argparse.ArgumentParser();p.add_argument('--saida',type=Path,required=True);a=p.parse_args();o=a.saida
 summ=json.loads((o/'resumo-p2-v5.json').read_text()); qa=json.loads((o/'regressao-independente-p2-v5.json').read_text());az=zipfile.ZipFile(o/'auditoria-p2-v5-csv-integral.zip')
 patches=load(az,'p2-v5-patches.csv');remaining=load(az,'p2-v5-pendencias-restantes.csv');families=load(az,'p2-v5-familias-analisadas.csv')
 wb=Workbook.create()
 def add(name,head,rows,widths=None,rown=27):
  sh=wb.worksheets.add(name);n=len(head); matrix=[head]+[list(x) for x in rows]
  sh.get_range_by_indexes(0,0,len(matrix),n).values=matrix
  rg=sh.get_range_by_indexes(0,0,len(matrix),n)
  rg.format.horizontal_alignment='center';rg.format.vertical_alignment='center';rg.format.row_height=rown
  hr=sh.get_range_by_indexes(0,0,1,n)
  hr.format={'fill':'#183F57','font':{'bold':True,'color':'#FFFFFF'},'horizontal_alignment':'center','vertical_alignment':'center','row_height':33}
  if widths:
   for i,w in enumerate(widths):sh.get_range_by_indexes(0,i,len(matrix),1).format.column_width=w
  sh.freeze_panes.freeze_rows(1)
  return sh
 add('Resumo',['Indicador','Resultado'],[
 ('Etapa','P2 v5 — revisão contextual por famílias'),('Data','2026-10-20'),('Keywords P2 no total',25050),('Pendências de entrada P2 v4',5562),('Reclassificadas',summ['reclassificadas']),('Sem ressalva',summ['sem_ressalva']),('Com ressalva',summ['com_ressalva']),('Pendências restantes',summ['pendencias_restantes']),('Famílias modificadas',summ['familias_com_patches']),('Base preservada',294905),('Controles preservados',2190),('Regressão independente',qa['status']),('Semanas e dias sem contexto',157),('Fahrenheit da família sem destino',68),('Fahrenheit com destino K explícito',1),('Aviso','Validação por regras — não é revisão humana individual'),('Dados completos','CSV dentro do ZIP de auditoria')],[39,70],31)
 add('Regras',['Regra','Registros','Exemplo'],[(k,n,' | '.join(summ.get('exemplos',{}).get(k,[])[:2])) for k,n in sorted(summ['regras'].items(),key=lambda x:-x[1])],[40,14,75])
 add('Patches',['ID','Lote','Família','Keyword','Regra','Status','Justificativa'],[(x['id_global'],x['lote'],x['familia_id'],x['Keyword'],x['regra'],x['status'],x['justificativa']) for x in patches],[14,12,20,57,38,20,74],30)
 add('Pendencias_amostra',['ID','Família','Keyword','Área anterior','Volume médio','Situação'],[(x['id_global'],x['familia_id'],x['Keyword'],x.get('area_final_p2_v4',x.get('area','')),x.get('Avg. monthly searches',''),'PENDENTE_CONTEXTUAL') for x in remaining[:500]],[14,23,75,25,17,25])
 add('Familias_prioritarias',['Família','Pendentes v4','Reclassificadas v5','Restantes','Exemplos restantes'],[(x['familia_id'],int(x['pendentes_v4']),int(x['classificados_v5']),int(x['ainda_abertos']),x['amostras_abertas']) for x in families[:220]],[25,20,23,17,95])
 add('QA_30_lotes',['Lote','Base','Controles','Alterações','Verificação'],[(x['lote'],x['base'],x['controles'],x['alteracoes'],x['status']) for x in qa['alteracoes_por_lote']],[38,19,19,19,24])
 dest=o/'qa-validacao-p2-v5-centralizada.xlsx'
 SpreadsheetFile.export_xlsx(wb).save(str(dest))
 print('XLSX',dest,dest.stat().st_size)
 # Check spreadsheet through library inspection (minimal)
 try:print('INSPECT',wb.inspect({'kind':'table','range':'Resumo!A1:B7','include':'values','table_max_rows':7,'table_max_cols':2}).ndjson[:500])
 except Exception as ex:print('Inspect skipped:',str(ex)[:180])
if __name__=='__main__':main()
