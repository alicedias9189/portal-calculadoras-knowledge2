#!/usr/bin/env python3
"""Cria planilha de auditoria P1 v2 com artifact_tool; todas as células centralizadas."""
import csv,json,collections,argparse
from pathlib import Path
from artifact_tool import Workbook,SpreadsheetFile
p=argparse.ArgumentParser();p.add_argument('--dir',default='/mnt/data/p1_validacao_final');args=p.parse_args()
R=Path(args.dir)

def readcsv(name):
    with (R/name).open(encoding='utf-8-sig',newline='') as f:
        rd=csv.DictReader(f,delimiter=';');return rd.fieldnames,list(rd)

def colname(n):
    v='';n+=1
    while n:n,r=divmod(n-1,26);v=chr(65+r)+v
    return v

wb=Workbook.create()
navy='#16324F'; teal='#137F83'; muted='#EAF2F5'; amber='#FFF1D5'; text='#273545'

def build(name,source,cols=None,maxcolwidth=28):
    fields,rows=readcsv(source)
    if cols is not None:fields=cols
    sh=wb.worksheets.add(name)
    matrix=[fields]+[[str(r.get(c,'')) for c in fields] for r in rows]
    end=colname(len(fields)-1)
    sh.get_range(f'A1:{end}{len(matrix)}').values=matrix
    sh.get_range(f'A1:{end}{len(matrix)}').format={'horizontal_alignment':'center','vertical_alignment':'center'}
    sh.get_range(f'A1:{end}1').format={'fill':navy,'font':{'color':'#FFFFFF','bold':True},'horizontal_alignment':'center','vertical_alignment':'center','row_height':32,'wrap_text':True}
    sh.get_range(f'A2:{end}{len(matrix)}').format.row_height=23
    sh.freeze_panes.freeze_rows(1)
    sh.freeze_panes.freeze_columns(4 if len(fields)>12 else 1)
    for i,f in enumerate(fields):
        width=14
        if f.lower() in ('keyword','justificativa','justificativa_validacao_v2','antes','depois','observacao_revisor'):width=43
        elif f.startswith(('cluster','subcluster','regra','status','intencao','area','tipo','adequacao','revisao_manual','confianca','justificativa')):width=24
        elif f in ('id_global','lote','lote_id','ordem','familia_id','volume_ads_patamar'):width=15
        sh.get_range(f'{colname(i)}:{colname(i)}').format.column_width=width
    return sh,len(rows)

summary=json.loads((R/'resumo-validacao-p1-v2.json').read_text(encoding='utf-8'))
sh=wb.worksheets.add('Resumo')
rows=[
 ['AUDITORIA SEMÂNTICA — PRIORIDADE P1',''],
 ['Indicador','Resultado'],
 ['Pendências originais',1093],
 ['Validadas semanticamente',summary['validados']],
 ['Validadas com ressalva',summary['validados_com_ressalva']],
 ['Pendências realmente abertas',summary['pendencias_restantes']],
 ['Registros P1 com patch',summary['patches_lotes']],
 ['Registros-base preservados',summary['base_preservada']],
 ['Controles preservados',summary['controles_preservados']],
 ['Lotes inspecionados',30],
 ['','',''],
 ['Legenda dos resultados',''],
 ['VALIDADO','Intenção e categoria determinadas por contexto explícito'],
 ['VALIDADO_COM_RESSALVA','Intenção clara, mas parâmetros/sentido não devem ser presumidos'],
 ['PENDENTE_CONTEXTUAL','Termo truncado, incompleto ou genuinamente ambíguo'],
 ['','',''],
 ['Metodologia','Regras contextuais especializadas e curadoria de exceções; não revisão humana independente de todos os termos'],
 ['Integridade','16 campos de origem, IDs, Ads e controles preservados; P0/P2/P3 intactos'],
 ['Atenção','Nunca inferir direção em moeda/unidade apenas por justaposição; não multiplicar volumes do Google Ads'],
]
sh.get_range('A1:B19').values=[[v for v in r[:2]] for r in rows]
sh.get_range('A1:B19').format={'horizontal_alignment':'center','vertical_alignment':'center','row_height':29}
sh.get_range('A1:B1').format={'fill':navy,'font':{'bold':True,'color':'#FFFFFF'},'row_height':39,'horizontal_alignment':'center','vertical_alignment':'center'}
sh.get_range('A2:B2').format={'fill':teal,'font':{'bold':True,'color':'#FFFFFF'},'horizontal_alignment':'center','vertical_alignment':'center','row_height':29}
sh.get_range('A12:B12').format={'fill':muted,'font':{'bold':True,'color':text},'horizontal_alignment':'center','vertical_alignment':'center'}
sh.get_range('A3:A10').format={'font':{'bold':True},'horizontal_alignment':'center','vertical_alignment':'center'}
sh.get_range('A:A').format.column_width=33
sh.get_range('B:B').format.column_width=95
sh.get_range('B13:B19').format.wrap_text=True
sh.get_range('B17:B19').format.row_height=44
sh.freeze_panes.freeze_rows(2)

build('Validação 1093','validacao-semantica-1093-p1-v2.csv')
build('Pendências 32','p1-v2-pendencias-reais.csv')
build('Ressalvas 361','p1-v2-ressalvas-de-operacao.csv')
build('Patches 1061','patches-semanticos-p1-v2.csv')
build('Regressão 30 lotes','regressao-30-lotes-p1-v2.csv')
sh=wb.worksheets.add('Regras utilizadas')
rr=sorted(summary['regras_aplicadas'].items(),key=lambda x:-x[1])
sh.get_range(f'A1:B{len(rr)+1}').values=[['Regra contextual','Registros']]+[[k,n] for k,n in rr]
sh.get_range(f'A1:B{len(rr)+1}').format={'horizontal_alignment':'center','vertical_alignment':'center','row_height':22}
sh.get_range('A1:B1').format={'fill':navy,'font':{'bold':True,'color':'#FFFFFF'},'row_height':30,'horizontal_alignment':'center','vertical_alignment':'center'}
sh.get_range('A:A').format.column_width=40
sh.get_range('B:B').format.column_width=18
sh.freeze_panes.freeze_rows(1)

out=R/'qa-validacao-semantica-p1-v2-centralizada.xlsx'
SpreadsheetFile.export_xlsx(wb).save(str(out))
print('EXPORTADO',str(out),out.stat().st_size,'bytes')
try:
    print(wb.inspect({'kind':'table','range':'Resumo!A1:B10','include':'values','table_max_rows':10,'table_max_cols':2}).ndjson[:2200])
except Exception as e:print('inspecao opcional falhou:',repr(e))
