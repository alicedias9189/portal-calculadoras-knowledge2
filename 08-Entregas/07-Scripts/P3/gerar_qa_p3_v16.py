#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera Excel de QA centralizado via artifact_tool para P3 v1.6."""
import argparse,csv,json,collections
from pathlib import Path
from artifact_tool import Workbook,SpreadsheetFile

def read(p):
 with open(p,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def safe(v,max_len=250):
 if isinstance(v,(int,float)):return v
 if v is None:return ''
 s=str(v);return s[:max_len] + ('…' if len(s)>max_len else '')
def add_sheet(wb,name,cols,rows,widths=None):
 ws=wb.worksheets.add(name)
 table=[list(cols)]+[[safe(r.get(c,'')) if isinstance(r,dict) else safe(r[j]) for j,c in enumerate(cols)] for r in rows]
 ws.get_range_by_indexes(0,0,len(table),len(cols)).values=table
 rg=ws.get_range_by_indexes(0,0,len(table),len(cols))
 rg.format.horizontal_alignment='center';rg.format.vertical_alignment='center';rg.format.row_height=25
 rg.format.wrap_text=True
 header=ws.get_range_by_indexes(0,0,1,len(cols))
 header.format={'fill':'#183A52','font':{'bold':True,'color':'#FFFFFF'},'horizontal_alignment':'center','vertical_alignment':'center','row_height':32,'wrap_text':True}
 for i,c in enumerate(cols):
  col=ws.get_range_by_indexes(0,i,len(table),1)
  col.format.column_width=(widths.get(c,23) if widths else 25)
 ws.freeze_panes.freeze_rows(1)
 return ws

def main():
 p=argparse.ArgumentParser();p.add_argument('--saida',type=Path,required=True);a=p.parse_args();d=a.saida
 summary=json.loads((d/'p3-v1.6-resumo.json').read_text());qa=json.loads((d/'p3-v1.6-regressao-independente-resumo.json').read_text())
 s=[('Universo P3',23965),('Revisadas individualmente da P3 v1.5',78),('Correções nas 78 decisões',summary['correcoes_qa']),('Novos ajustes P3',summary['novas_classificacoes']),('Novas famílias',summary['familias_expansao']),('Total de patches',summary['total_alteracoes']),('P3 fora dos pilotos ANTES',summary['p3_fora_pilotos_antes']),('P3 fora dos pilotos DEPOIS',summary['p3_fora_pilotos_depois']),('Lotes aprovados',qa['lotes_aprovados']),('IDs originais',qa['registros_base']),('Controles preservados',qa['controles']),('Pendências P2 preservadas',4660),('Estado editorial','Proposta semântica automatizada com revisão contextual; não homologada em definitivo'),('SHA256 campos protegidos',qa['protegidoss_sha256'])]
 wb=Workbook.create();add_sheet(wb,'Resumo',['Indicador','Valor'],[{'Indicador':a,'Valor':b} for a,b in s],{'Indicador':41,'Valor':68})
 sample=read(d/'p3-v1.6-amostra-78-pareceres.csv')
 add_sheet(wb,'QA 78',['id_global','Keyword','regra_v1_5','parecer_v1_6','justificativa','area_v1_5','area_v1_6','tipo_v1_5','tipo_v1_6'],sample,{'Keyword':40,'justificativa':54,'regra_v1_5':28,'parecer_v1_6':26})
 patches=read(d/'p3-v1.6-patches.csv')
 add_sheet(wb,'Patches 163',['id_global','familia_id','Keyword','origem','regra','campos_alterados','antes_json','depois_json'],patches,{'Keyword':36,'regra':33,'antes_json':55,'depois_json':55,'campos_alterados':38})
 decisions=read(d/'p3-v1.6-decisoes-por-id.csv')
 add_sheet(wb,'Decisoes 163',['id_global','Keyword','regra','area_antes','area_depois','subcluster_antes','subcluster_depois','tipo_antes','tipo_depois','justificativa'],decisions,{'Keyword':42,'subcluster_antes':38,'subcluster_depois':38,'justificativa':50})
 regs=[{'Regra':k,'Quantidade':v} for k,v in sorted(summary['regras'].items(),key=lambda x:(-x[1],x[0]))]
 add_sheet(wb,'Regras',['Regra','Quantidade'],regs,{'Regra':45,'Quantidade':18})
 perlot=read(d/'p3-v1.6-regressao-independente-30-lotes.csv')
 add_sheet(wb,'Regressao 30',['lote','bases','controles','alteracoes','status'],perlot,{'lote':43,'bases':18,'controles':18,'alteracoes':18,'status':16})
 # Amostra deterministica apenas para triagem: CSV completo fica nas filas e no ZIP.
 candidate=read(d/'p3-v1.6-fila-23965.csv');rest=[r for r in candidate if r['status_p3_v1']=='FORA_DO_PILOTO' and not any(r.get('status_p3_v1_'+i) for i in ['3','4','5','6'])]
 assert len(rest)==20755,len(rest)
 sample_rest=rest[::max(1,len(rest)//160)][:160]
 add_sheet(wb,'P3 abertas amostra',['id_global','familia_id','Keyword','area','tipo_intencao_atual','riscos_detectados'],sample_rest,{'Keyword':47,'riscos_detectados':45})
 target=d/'qa-auditoria-P3-v1.6-centralizada.xlsx';SpreadsheetFile.export_xlsx(wb).save(str(target))
 check=wb.inspect({'kind':'table','range':'Resumo!A1:B15','include':'values,formulas','table_max_rows':15,'table_max_cols':2})
 print('SALVO',target,target.stat().st_size,'inspecao',check.ndjson[:750]);
if __name__=='__main__':main()
