#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera planilha QA P3 v5.1 com todas as células centralizadas (artifact_tool).
Rodar da raiz: python 07-Scripts/P3/gerar_qa_p3_v51.py
"""
from pathlib import Path
import csv,json
from artifact_tool import Workbook,SpreadsheetFile
ROOT=Path(__file__).resolve().parents[2]
O=ROOT/'08-Entregas/P3-v5.1'
def rows(name):
 with (O/name).open(encoding='utf-8-sig',newline='') as f:
  d=csv.DictReader(f,delimiter=';');return [list(d.fieldnames)]+[[r[k] for k in d.fieldnames] for r in d]
sm=json.loads((O/'p3-v5.1-resumo.json').read_text())
rg=json.loads((O/'p3-v5.1-regressao-independente-resumo.json').read_text())
wb=Workbook.create()
def add(name,arr,widths=None,row_height=28):
 sh=wb.worksheets.add(name)
 n=len(arr);m=max(len(row) for row in arr)
 if arr:sh.get_range_by_indexes(0,0,n,m).values=[list(row)+['']*(m-len(row)) for row in arr]
 entire=sh.get_range_by_indexes(0,0,n,m)
 entire.format.horizontal_alignment='center'
 entire.format.vertical_alignment='center'
 entire.format.wrap_text=True
 entire.format.row_height=row_height
 hdr=sh.get_range_by_indexes(0,0,1,m)
 hdr.format.fill='#17324B'
 hdr.format.font.color='#FFFFFF'
 hdr.format.font.bold=True
 hdr.format.row_height=35
 for j in range(m):
  w=(widths[j] if widths and j<len(widths) else 20)
  sh.get_range_by_indexes(0,j,n,1).format.column_width=w
 sh.freeze_panes.freeze_rows(1)
 return sh
add('Resumo',[
 ['Indicador','Resultado','Observação'],
 ['Versão','P3 v5.1','Revisão de 75 propostas classificadas na P3 v5.0'],
 ['Pareceres individuais',75,'75 IDs previamente selecionados; nenhum novo ID'],
 ['Refinamentos aplicados',19,'Corrigidos com justificativa contextual'],
 ['Pareceres mantidos',56,'Mantidos com ressalvas e julgamento individual'],
 ['Famílias',49,'Cobertura dos 75 IDs'],
 ['Grupos semânticos',8,'Distribuição por tema'],
 ['Lotes validados','30/30','Regressão independente passou'],
 ['Keywords-base',294905,'Preservadas'],
 ['Controles',2190,'Preservados'],
 ['Fila P3',23965,'Linhas preservadas'],
 ['Fila geral',52046,'Linhas preservadas'],
 ['Colunas históricas das filas',382,'Inalteradas, adição exclusiva de oito colunas de rastreio'],
 ['P3 ainda elegíveis',19637,'Não houve expansão nesta fase'],
 ['P2 ainda pendentes',4660,'Não reabertas'],
 ['Backlog global',98,'Fonte global idêntica byte a byte'],
 ['Homologação','PENDENTE','Pareceres técnicos; sem aprovação editorial humana'],
 ['Checksum fontes protegidas',rg['checksum_fontes_protegidas'],'SHA-256 composto documentado no script de regressão']
],widths=[29,36,79],row_height=28)
add('Pareceres 75',rows('p3-v5.1-pareceres-75.csv'),widths=[14,12,22,41,31,25,71,25,25,30,30,43,43,24,24,16,35,23],row_height=52)
add('Patches 19',rows('p3-v5.1-patches-19.csv'),widths=[15,36,22,43,68,44,78,78],row_height=82)
add('QA por grupo',rows('p3-v5.1-qa-por-grupo.csv'),widths=[40,18,18,18,18,29],row_height=32)
add('Regressão 30',rows('p3-v5.1-regressao-independente-30-lotes.csv'),widths=[45,15,15,15,15,17],row_height=25)
add('Semântica',[
 ['Tema','Regra semântica / alerta','Exemplos IDs'],
 ['BTU/h / watts','BTU/h converte-se dimensionalmente em watts térmicos. Consumo elétrico depende do aparelho, eficiência e operação. Não presumir que os watts pedidos são elétricos.', '19940, 19954, 19969, 19990, 20011, 206302, 206323'],
 ['Área ↔ perímetro','Área isolada não determina perímetro sem forma e condições geométricas; o sentido da busca não pode ser invertido.', '85882'],
 ['Expoente omitido','23 pode ser vinte e três ou 2³, 32 pode ser trinta e dois ou 3²; preservar ambiguidade e confiança baixa.', '207492, 207494'],
 ['Intenção informacional','Descrição genérica de potência/fração/regra de três não basta para caracterizar operação imediata; não inventar valores.', '18136, 160019, 207450, 207458, 207640, 242905, 245615'],
 ['Interseção de eventos','Não pressupor independência; P(A∩B)=P(A)P(B|A) quando P(A)>0, e tratamento específico para P(A)=0.', '212548'],
 ['Triângulo','A frase três lados não fornece comprimentos; consulta sobre fórmula em vez de cálculo numérico.', '200874'],
 ['Prazos','Dias úteis exigem definição de calendário e feriados; dias corridos têm convenções de início/fim.', '34947, 34952, 34973, 39176'],
 ['Benefícios','Não presumir alíquotas universais de desconto de vale-refeição/alimentação sem contexto aplicável.', '204997, 205012, 205013, 205034'],
 ['Status editorial','Homologação dos 75 pareceres permanece pendente. A automação é revisão técnica e não aprovação humana.','Todos os 75']
],widths=[28,105,58],row_height=75)
add('Integridade',[
 ['Verificação','Resultado','Detalhes'],
 ['Regressão independente',rg['status'],'Comparação linha a linha dos 30 lotes com a v5.0'],
 ['Base',rg['base'],'Mesma identidade e ordem dos registros'],
 ['Controles',rg['controles'],'Registros de controle não alterados'],
 ['IDs revisados',rg['ids_revisados'],'Mesmo conjunto de 75 IDs da v5.0'],
 ['IDs refinados',rg['ids_refinados'],'Somente campos permitidos alterados'],
 ['IDs não alterados',rg['ids_preservados'],'Parecer e justificativa em relatório separado'],
 ['Fila P3',rg['filas'][0]['status'],'23.965 linhas; 382 colunas antigas idênticas'],
 ['Fila geral',rg['filas'][1]['status'],'52.046 linhas; 382 colunas antigas idênticas'],
 ['Backlog global',rg['backlog_global_98_byte_a_byte'],'98 propostas globais, arquivo igual em bytes'],
 ['Fontes protegidas',rg['checksum_fontes_protegidas'],'SHA-256 composto']
],widths=[32,73,79],row_height=32)
path=O/'qa-auditoria-P3-v5.1-centralizada.xlsx'
# Valida valores importantes na memória e exporta.
probe=wb.inspect({'kind':'table','range':'Resumo!A1:C7','include':'values','table_max_rows':7,'table_max_cols':3})
print('INSPECT',probe.ndjson[:1000])
SpreadsheetFile.export_xlsx(wb).save(str(path))
print('EXPORT',path.name,path.stat().st_size)