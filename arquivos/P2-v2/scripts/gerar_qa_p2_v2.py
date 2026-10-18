#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera relatório de amostragem P2 v1 e planilha de QA para P2 v2.
Depende de artifact_tool para XLSX; script da triagem gera os CSVs-base.
"""
import csv, json, re, collections, random
from pathlib import Path
from artifact_tool import Workbook, SpreadsheetFile
BASE=Path('/mnt/data/p2_validation_v2/out'); BASE.mkdir(parents=True,exist_ok=True)
SRC=Path('/mnt/data/p2_work/out')

def rows(name):
 with open(name,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def outcsv(name, rs, cols):
 with open(BASE/name,'w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore',delimiter=';',lineterminator='\n');w.writeheader();w.writerows(rs)

old=rows(SRC/'p2-validacao-semantica-25050.csv');new=rows(BASE/'p2-v2-decisoes-25050.csv');pend=[x for x in new if x['status_p2_v2']=='PENDENTE_REAL'];confirmed=[x for x in new if x['status_p2_v2'] in ('RESOLVIDO_ALTA','RESOLVIDO_COM_RESSALVA')]
summary=json.loads((BASE/'resumo-p2-v2.json').read_text(encoding='utf-8'))
# Risk tests on prior P2-v1 accepted decisions. These only flag: no update without review.
def risk(r):
 t=r['Keyword'].lower();tags=[]
 if r['tipo_intencao_final_p2']=='conversão direta' and (not r['unidade_origem_final_p2'] or not r['unidade_destino_final_p2']):tags.append('CONVERSAO_SEM_PAR_METADADOS')
 if r['area_final_p2']=='Conversores' and r['cluster_final_p2']=='Moedas e câmbio' and re.search(r'moeda (?:de )?(?:um|1|2|5|10|25|50) (?:real|centav|eur)|beija flor',t):tags.append('POSSIVEL_NUMISMATICA')
 if r['tipo_intencao_final_p2']=='conversão de arquivo/mídia' and re.search(r'exerc[ií]c|atividade|gabarito|apostila',t):tags.append('PDF_MATERIAL_DIDATICO')
 if r['area_final_p2']=='Conversores' and re.search(r'gravidez|gesta[cç]|gr[aá]vid|parto|ultrassom',t):tags.append('SAUDE_COMO_CONVERSOR')
 if r['area_final_p2']=='Conversores' and re.search(r'\b(?:kwh|quilowatt.?hora)\b',t) and re.search(r'\breais?\b',t):tags.append('KWH_COMO_CAMBIO')
 return ' | '.join(tags)
accepted=[x for x in old if x['status_p2']!='PENDENTE_CONTEXTUAL'];assert len(accepted)==16237
flags=[dict(id_global=x['id_global'],Keyword=x['Keyword'],regra_p2=x['regra_p2'],status_p2=x['status_p2'],area=x['area_final_p2'],intencao=x['tipo_intencao_final_p2'],alerta=risk(x),disposicao='REVISAR_SEM_MODIFICACAO_AUTOMATICA') for x in accepted if risk(x)]
outcsv('p2-v1-sinalizacoes-qa.csv',flags,['id_global','Keyword','regra_p2','status_p2','area','intencao','alerta','disposicao'])
# Reproducible stratified QA sample of pre-existing classifications (no claim of manual review).
seed=random.Random(20261017); groups=collections.defaultdict(list)
for x in accepted:groups[(x['regra_p2'],x['status_p2'])].append(x)
sampled=[]
for group,rr in sorted(groups.items(),key=lambda x:-len(x[1])):
 for x in seed.sample(rr,min(4,len(rr))):
  sampled.append(dict(id_global=x['id_global'],Keyword=x['Keyword'],regra_p2=x['regra_p2'],status_p2=x['status_p2'],area=x['area_final_p2'],cluster=x['cluster_final_p2'],intencao=x['tipo_intencao_final_p2'],alerta=risk(x) or 'SEM_ALERTA_DE_REGRAS_AUTOMATICAS',observacao='Amostra para leitura editorial posterior; não verificada individualmente por humano'))
outcsv('p2-v1-amostra-auditoria.csv',sampled,list(sampled[0]))

wb=Workbook.create()
heading={'fill':'#17324D','font':{'bold':True,'color':'#FFFFFF'},'horizontal_alignment':'center','vertical_alignment':'center','row_height':25}

def sheet(name,header,data,widths=None,max_rows=None):
 sh=wb.worksheets.add(name)
 if max_rows is not None:data=data[:max_rows]
 nr=1+len(data);nc=len(header)
 # write chunks, within 500 row blocks to minimize memory spikes
 sh.get_range_by_indexes(0,0,1,nc).values=[header]
 for i in range(0,len(data),350):
  block=data[i:i+350]
  sh.get_range_by_indexes(i+1,0,len(block),nc).values=[[str(v) if not isinstance(v,(int,float)) else v for v in row] for row in block]
 sh.get_range_by_indexes(0,0,1,nc).format=heading
 full=sh.get_range_by_indexes(0,0,nr,nc)
 full.format.horizontal_alignment='center';full.format.vertical_alignment='center'
 # shorter row height and moderate widths avoids extreme autofit
 if nr>1:sh.get_range_by_indexes(1,0,nr-1,nc).format.row_height=20
 for j,w in enumerate(widths or [20]*nc): sh.get_range_by_indexes(0,j,nr,1).format.column_width=w
 sh.freeze_panes.freeze_rows(1)
 return sh
statuses=summary['classificacoes_v2']
sheet('Resumo',['Indicador','Quantidade','Interpretação'],[
 ['Total P2',25050,'Palavras-chave do conjunto completo'],
 ['Pendências examinadas',8813,'Somente casos pendentes da P2 v1'],
 ['Resolvidas sem ressalva',statuses['RESOLVIDO_ALTA'],'Confiança na regra contextual, não aprovação editorial'],
 ['Resolvidas com ressalva',statuses['RESOLVIDO_COM_RESSALVA'],'Exige parâmetros adicionais ou checagem de contexto'],
 ['Pendências mantidas',statuses['PENDENTE_REAL'],'Evidência textual insuficiente'],
 ['P2 v1 preservada',statuses['MANTIDO_P2_V1'],'Sem reprocessar decisões já feitas na P2 v1'],
 ['Alterações em campos analíticos',summary['qtd_patches'],'Preserva dados Ads, controles, P0 e P1'],
 ['Registros-base',294905,'Integridade confirmada em 30 lotes'],
 ['Controles',2190,'Todos idênticos ao arquivo de entrada'],
 ['Sinalizações P2 v1',len(flags),'Alertas automáticos, não comprovação de erro'],
 ['Amostra P2 v1',len(sampled),'Estratificada por regra e status'],
],widths=[34,17,69])
sheet('Regras P2 v2',['Regra','Qtd.'],[[k,v] for k,v in sorted(summary['qtd_regras_p2_v2'].items(),key=lambda x:-x[1]) if k not in ('nao_pendente_p2_v1','evidencia_insuficiente_v2')],widths=[40,15])
sheet('Regressão por lote',['Lote','Base','Controles','Mudanças P2 v2','Status'],[[r['lote'],int(r['base']),int(r['controles']),int(r['mudancas_p2_v2']),r['status']] for r in rows(BASE/'p2-v2-regressao-30-lotes.csv')],widths=[18,17,17,22,17])
sheet('Amostra revisada',['Keyword','Área final','Intenção','Status P2 v2','Regra','Justificativa'],[[r['Keyword'],r['area_final_p2_v2'],r['tipo_intencao_final_p2_v2'],r['status_p2_v2'],r['regra_p2_v2'],r['justificativa_p2_v2']] for r in rows(BASE/'p2-v2-amostra-auditoria.csv')],widths=[47,20,25,27,32,75],max_rows=700)
sheet('Pendências prioritárias',['Keyword','Área anterior','Cluster anterior','Busca média mensal','Regra v1','Situação'],[[r['Keyword'],r['area'],r['cluster'],r['Avg. monthly searches'],r['regra_p2'],'PENDENTE_REAL'] for r in sorted(pend,key=lambda x:-int(x['Avg. monthly searches'] or 0))],widths=[50,18,27,22,30,25],max_rows=600)
sheet('QA P2 anterior',['Keyword','Regra P2 v1','Área final','Status','Alerta'],[[r['Keyword'],r['regra_p2'],r['area'],r['status_p2'],r['alerta']] for r in flags] or [['Nenhum alerta','','','','']],widths=[52,35,27,31,40])
out=BASE/'qa-validacao-p2-v2-centralizada.xlsx'
SpreadsheetFile.export_xlsx(wb).save(str(out))
print('Workbook:',out,'flags:',len(flags),'sampled old:',len(sampled),'remaining:',len(pend),'new decisions:',len(confirmed))
print(wb.inspect({'kind':'table','range':'Resumo!A1:C7','include':'values','table_max_rows':8,'table_max_cols':3}).ndjson[:1500])
