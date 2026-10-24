#!/usr/bin/env python3
# coding: utf-8
"""Gera planilha P3 v1.7 usando artifact_tool; todas as células centralizadas.
Usage: python3 gerar_qa_p3_v17.py --saida <diretorio com csvs P3 v1.7>
"""
import argparse,csv,json,collections
from pathlib import Path
from artifact_tool import Workbook,SpreadsheetFile

def rows(path):
 with open(path,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))

def tab(wb,name,header,data,widths=None):
 sh=wb.worksheets.add(name);matrix=[header]+data
 sh.get_range_by_indexes(0,0,len(matrix),len(header)).values=matrix
 rg=sh.get_range_by_indexes(0,0,len(matrix),len(header))
 rg.format.horizontal_alignment='center';rg.format.vertical_alignment='center';rg.format.row_height=23
 rg.format.wrap_text=True
 h=sh.get_range_by_indexes(0,0,1,len(header));h.format={'fill':'#17324D','font':{'bold':True,'color':'#FFFFFF'},'horizontal_alignment':'center','vertical_alignment':'center','row_height':34,'wrap_text':True}
 for i in range(len(header)):
  w=(widths or {}).get(i, 19 if i else 16)
  sh.get_range_by_indexes(0,i,len(matrix),1).format.column_width=w
 sh.freeze_panes.freeze_rows(1)
 return sh

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--saida',type=Path,required=True);a=ap.parse_args();p=a.saida
 sumr=json.loads((p/'p3-v1.7-resumo.json').read_text());reg=json.loads((p/'p3-v1.7-regressao-independente-resumo.json').read_text());audit=rows(p/'p3-v1.7-revisao-152.csv');sample=[r for r in audit if r['na_amostra_estratificada']=='sim'];patches=rows(p/'p3-v1.7-patches.csv');test=rows(p/'p3-v1.7-regressao-independente-30-lotes.csv')
 wb=Workbook.create()
 summary=[['Universo de novas propostas P3 v1.6',152],['Amostra estratificada',len(sample)],['Regras semânticas cobertas',7],['Correções P3 v1.7',len(patches)],['Ambiguidades reabertas',1],['Propostas mantidas',135],['P3 fora dos pilotos (inalterado)',20755],['Pendências P2 preservadas',4660],['Base total de keywords',294905],['Controles históricos',2190],['Lotes com regressão aprovada',30],['Fila geral de revisão',52046],['Fila P3',23965],['Aprovação editorial completa','NÃO — revisão contextual com ressalvas'],['Referência','P3 v1.6; DEC-053']]
 tab(wb,'Resumo',['Métrica','Resultado'],summary,{0:45,1:64})
 dist=[];alln=collections.Counter(r['regra_v16'] for r in audit);sampn=collections.Counter(r['regra_v16'] for r in sample);correct=collections.Counter(r['regra_v16'] for r in audit if r['parecer_v17'] in ('CORRIGIDA','REABERTA_POR_AMBIGUIDADE'))
 for rule,n in sorted(alln.items(),key=lambda it:-it[1]):dist.append([rule,n,sampn[rule],correct[rule]])
 tab(wb,'Cobertura por regra',['Regra P3 v1.6','Total','Amostra','Corrigidos'],dist,{0:44,1:15,2:15,3:15})
 cols=['id_global','familia_id','Keyword','regra_v16','na_amostra_estratificada','parecer_v17','nota_critica','area_v16','area_v17','subcluster_v17','tipo_v16','tipo_v17','revisao_editorial_final']
 labels=['ID','Família','Palavra-chave','Regra v1.6','Na amostra?','Parecer v1.7','Justificativa','Área anterior','Área final','Subgrupo final','Intenção anterior','Intenção final','Homologação?']
 widths={0:12,1:24,2:47,3:31,4:16,5:30,6:65,7:20,8:20,9:43,10:26,11:26,12:20}
 tab(wb,'Revisão 152',labels,[[r[k] for k in cols] for r in audit],widths)
 tab(wb,'Amostra 103',labels,[[r[k] for k in cols] for r in sample],widths)
 change_cols=['id_global','Keyword','status_qa','campos_alterados','antes_json','depois_json']
 tab(wb,'17 patches',['ID','Palavra-chave','Decisão','Campos','Antes (JSON)','Depois (JSON)'],[[r[k] for k in change_cols] for r in patches],{0:14,1:48,2:28,3:52,4:77,5:77})
 tab(wb,'Regressão 30 lotes',['Lote','Base','Controles','Alterações','Status'],[[r[k] for k in ['lote','registros_base','controles','alteracoes','status']] for r in test],{0:16,1:17,2:17,3:18,4:23})
 target=p/'qa-auditoria-P3-v1.7-centralizada.xlsx';SpreadsheetFile.export_xlsx(wb).save(str(target))
 print('XLSX',target,target.stat().st_size,'sheets=6, review=152, sample='+str(len(sample)), 'patches='+str(len(patches)))
if __name__=='__main__':main()
