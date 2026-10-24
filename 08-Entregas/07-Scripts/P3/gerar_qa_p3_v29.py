#!/usr/bin/env python3
# coding: utf-8
"""Planilha QA P3 v2.9: artifact_tool; todas as células usadas centralizadas."""
import csv,collections,json
from pathlib import Path
from artifact_tool import Workbook,SpreadsheetFile
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'08-Entregas/P3-v2.9'
def load(n):
 with (OUT/n).open(encoding='utf-8-sig',newline='') as f:
  return list(csv.DictReader(f,delimiter=';'))
reviews=load('p3-v2.9-revisao-66.csv')
patches=load('p3-v2.9-patches.csv')
reg=load('p3-v2.9-regressao-independente-30-lotes.csv')
assert len(reviews)==66 and len(patches)==2 and len(reg)==30
sums=collections.Counter((r['regra_v28'],r['parecer_v29']) for r in reviews)
wb=Workbook.create()
head_fmt={'fill':'#17324D','font':{'bold':True,'color':'#FFFFFF'},'horizontal_alignment':'center','vertical_alignment':'center','row_height':26,'wrap_text':True}

def create(name,head,values,width=24):
 sh=wb.worksheets.add(name)
 matrix=[head]+values
 last=len(matrix); n=len(head)
 rng=sh.get_range_by_indexes(0,0,last,n)
 rng.values=matrix
 rng.format.horizontal_alignment='center'
 rng.format.vertical_alignment='center'
 rng.format.wrap_text=True
 rng.format.row_height=34
 sh.get_range_by_indexes(0,0,1,n).format=head_fmt
 for j in range(n):
  sh.get_range_by_indexes(0,j,last,1).format.column_width=(42 if any(s in head[j].lower() for s in ('keyword','nota','justificativa','antes','depois')) else width)
 sh.freeze_panes.freeze_rows(1)
 return sh

create('Resumo',['Indicador','Valor','Interpretação'],[
 ['Versão','P3 v2.9','Revisão crítica da expansão P3 v2.8'],
 ['Decisões individualizadas',66,'Todas com parecer por ID'],
 ['Correções efetivas',2,'Refinamento de subcluster e intenção'],
 ['Mantidas com ressalvas',64,'Nenhum sinal suficiente para reclassificar'],
 ['Taxas de financiamento de veículos',45,'Regra prioritária revisada integralmente'],
 ['Restantes fora do piloto',20308,'Sem novas inclusões nesta versão'],
 ['Pendências P2',4660,'Nenhuma alterada'],
 ['Quarentena global',98,'Conteúdo idêntico'],
 ['Regressão independente','30/30','Campos protegidos e filas conferidos'],
 ['Homologação editorial','Pendente','Parecer técnico, não aprovação humana definitiva'],
],30)
stat=[]
for rule in sorted({r['regra_v28'] for r in reviews}):
 n=sum(x['regra_v28']==rule for x in reviews)
 changed=sums[(rule,'CORRIGIDO')]
 stat.append([rule,n,changed,n-changed,'Amostra integral das novas decisões, não estimativa global de erro'])
create('Analise por regra',['Regra v2.8','Revisados','Corrigidos','Mantidos','Limitação metodológica'],stat)
use=['id_global','lote','familia_id','Keyword','regra_v28','parecer_v29','nota_qa_v29','area_v28','cluster_v28','subcluster_v28','tipo_v28','area_v29','cluster_v29','subcluster_v29','tipo_v29','mudou_lote','revisao_editorial_final']
create('QA 66 casos',use,[[r.get(k,'') for k in use] for r in reviews],20)
create('Patches 2',list(patches[0]),[[r[k] for k in patches[0]] for r in patches],20)
create('Regressao 30 lotes',list(reg[0]),[[int(r[k]) if k in ('base','controles','patches') else r[k] for k in reg[0]] for r in reg],19)
create('Casos de atencao',['Expressão','Decisão','Justificativa'],[
 ['calcular taxa financiamento veiculo','cálculo contextual da taxa implícita','Não confundir taxa deduzida dos pagamentos com taxa publicada'],
 ['como calcular juros de financiamento carro','informacional sobre método de cálculo','Sem principal, prazo e parcelas fornecidos'],
 ['tabela de juros banco central','informacional','Sem taxa numérica inventada; fonte e data são necessárias'],
 ['taxa atual ou 2022','informacional com referência temporal','Não calcular prestações a partir do texto da busca'],
 ['conversão W e kWh','contextual (tempo necessário)','Grandezas dimensionalmente diferentes'],
 ['Fahrenheit x Celsius','conversão contextual','Direção não informada pela palavra x'],
 ['INSS em obra','previdenciário/construção','Regime e regularização não podem ser presumidos'],
])
# programmatic compact confirmation
check=wb.inspect({'kind':'table','range':'Resumo!A1:C5','include':'values','table_max_rows':5,'table_max_cols':3})
print(check.ndjson[:1400])
SpreadsheetFile.export_xlsx(wb).save(str(OUT/'qa-auditoria-P3-v2.9-centralizada.xlsx'))
print('XLSX exportada')
