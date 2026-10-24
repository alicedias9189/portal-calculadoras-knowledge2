#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Revisão crítica P3 v1.9: lê 83 decisões da P3 v1.8 e altera somente IDs auditados.

Uso: python3 auditar_p3_v19.py --fonte /CAMINHO/RAIZ --saida /CAMINHO/SAIDA
Dependência: Python 3 stdlib. A fonte precisa conter 08-Entregas/P3-v1.8.
O script não substitui arquivos da v1.8, nem reclassifica IDs fora dos 83.
"""
import argparse,csv,io,json,re,zipfile,collections
from pathlib import Path

BASEFIELDS={'tipo_intencao','intencao_principal','confianca','justificativa_curta'}
# Correções estritamente por ID; revisão das 83 expressões, não extrapolação por regex ou família.
REV={
 '12304':('ajustar', {'tipo_intencao':'informacional','intencao_principal':'Consultar explicação, fórmula ou exemplos de média ponderada','confianca':'média'},'Expressão nominal sem valores ou verbo operacional; v1.8 presumiu solicitação de cálculo.'),
 '143774':('ajustar', {'confianca':'média','intencao_principal':'Consultar ou calcular a média ponderada do ENEM, conforme pesos definidos por curso/instituição'},'A busca não distingue tutorial de cálculo de nota; pesos do ENEM podem variar conforme seleção.'),
 '182921':('ajustar', {'confianca':'média','intencao_principal':'Consultar ou calcular a nota ponderada do ENEM segundo os pesos aplicáveis'},'A consulta não especifica universidade/curso nem o objetivo exato; não afirmar somente tutorial.'),
 '182930':('ajustar', {'intencao_principal':'Aprender a calcular média ponderada no LibreOffice Calc','confianca':'média'},'Referência explícita a software: instrução de uso, não simples explicação genérica da fórmula.'),
 '182934':('ajustar', {'intencao_principal':'Aprender a fazer média ponderada em calculadora ou dispositivo HP','confianca':'média'},'Referência à marca HP, sem modelo; não presumir procedimento de tecla específico.'),
 '272562':('ajustar', {'intencao_principal':'Consultar tabela ou referência sobre média ponderada','confianca':'média'},'A palavra tabela indica material de referência, já classificado assim; descrição anterior dizia tutorial.'),
 '172646':('ajustar', {'tipo_intencao':'informacional','intencao_principal':'Consultar incidência e tratamento do IRRF em adiantamento salarial','confianca':'média'},'Não há verbo calcular, valores nem simulador; objetivo informacional é mais defensável.'),
 '172679':('ajustar', {'tipo_intencao':'informacional','intencao_principal':'Consultar incidência e tratamento do IRRF sobre adiantamento salarial','confianca':'média'},'Expressão genérica sobre tributo, sem pedido explícito de simulação.'),
 '85135':('ajustar', {'tipo_intencao':'informacional','intencao_principal':'Aprender como converter kWh em Wh (unidades e direção explícitas)','confianca':'média'},'Como converter indica busca por procedimento; preservar direção kWh→Wh e dimensões.'),
 '85495':('ajustar', {'tipo_intencao':'informacional','intencao_principal':'Aprender como converter Wh em kWh (unidades e direção explícitas)','confianca':'média'},'Como converter indica busca por procedimento; preservar direção Wh→kWh e dimensões.'),
}

TRACK=['status_p3_v1_9','parecer_p3_v1_9','nota_qa_p3_v1_9','area_final_p3_v1_9','cluster_final_p3_v1_9','subcluster_final_p3_v1_9','tipo_intencao_final_p3_v1_9','classificacao_alterada_p3_v1_9']
FROZEN={'tipo_registro','id_global','lote_id','familia_id','controle_id','Keyword','ocorrencias_origem','areas_origem','qtd_areas','Avg. monthly searches','Mudança em três meses','Mudança YoY','Competition','Competition (indexed value)','Top of page bid (low range)','Top of page bid (high range)','unidade_origem','unidade_destino','direcao_conversao','keyword_interpretada','reconstrucao_barra_status','tipos_reconstrucao_barra','confianca_reconstrucao_barra','observacao_reconstrucao_barra'}

def decode(b):return list(csv.DictReader(io.StringIO(b.decode('utf-8-sig')),delimiter=';'))
def encode(rows,heads):
 out=io.StringIO(newline='');w=csv.DictWriter(out,fieldnames=heads,delimiter=';',extrasaction='ignore',lineterminator='\n');w.writeheader();w.writerows(rows);return ('\ufeff'+out.getvalue()).encode('utf-8')
def read(path):
 with open(path,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def write(path,rows,headers=None):
 assert rows or headers,path
 path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(encode(rows,headers or list(rows[0])))

def rationale(item):
 rule=item['regra']; q=item['Keyword'].lower();rid=item['id_global']
 if rid in REV:return 'AJUSTADA',REV[rid][2]
 if rule=='irrf_tributario_contextual':
  if any(x in q for x in ('2021','2022')):return 'MANTIDA_COM_RESSALVA','Competência histórica explícita; execução tributária exige regra aplicável àquele ano e base de cálculo.'
  if 'aluguel' in q or 'motorista autonomo' in q:return 'MANTIDA_COM_RESSALVA','Subtipo de rendimento identificado, mas regras de retenção e base dependem do contexto tributário.'
  if 'simulador' in q or 'calculadora' in q:return 'MANTIDA_COM_RESSALVA','Pedido de ferramenta identificado; apuração exige valores, competência e regime.'
  return 'MANTIDA_COM_RESSALVA','Domínio do IRRF sustentado; consulta genérica não fixa incidência, faixa ou alíquota.'
 if rule=='media_ponderada':
  if any(x in q for x in ('excel','tabela dinamica')):return 'MANTIDA','Termos de aplicação em planilha indicam orientação de uso; não há valores para cálculo.'
  if any(x in q for x in ('como','fórmula','formula','exemplo','significa','funciona')):return 'MANTIDA','Termos explicitamente didáticos sustentam intenção informacional.'
  if q.startswith('calcular'):return 'MANTIDA_COM_RESSALVA','Operação solicitada sem lista de valores e pesos; precisa preencher parâmetros.'
  return 'MANTIDA_COM_RESSALVA','Referência à média ponderada sem dados; preservar necessidade de contexto.'
 if rule=='ferias_medias':return 'MANTIDA_COM_RESSALVA','Domínio trabalhista explícito; composição depende de período, rubricas e regras vigentes.'
 if rule=='dias_uteis_calendario':return 'MANTIDA_COM_RESSALVA','Consulta a calendário histórico; feriados municipais/estaduais podem variar.'
 if rule=='dias_uteis_contagem':return 'MANTIDA_COM_RESSALVA','Pedido de contagem plausível; necessita datas e localidade para feriados.'
 if rule=='conversao_energia_dimensional':return 'MANTIDA','Unidades compatíveis, sentido explícito e metadados dimensionais íntegros.'
 if rule=='regra_tres':return 'MANTIDA','Consulta didática sobre regra de três; área matemática e proporções coerentes.'
 if rule=='poupanca_taxa_informacao':
  if any(x in q for x in ('hoje','2021')):return 'MANTIDA_COM_RESSALVA','Busca por taxa atual ou histórica; não incluir rentabilidade fixa ou afirmar taxa sem período.'
  return 'MANTIDA_COM_RESSALVA','Busca de rendimento sem capital e prazo especificados; informação de taxa é interpretação plausível.'
 return 'MANTIDA_COM_RESSALVA','Interpretação original mantida sem evidência de ajuste por este contexto.'

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--fonte',required=True,type=Path);ap.add_argument('--saida',required=True,type=Path);a=ap.parse_args()
 src=a.fonte/'08-Entregas/P3-v1.8'; out=a.saida;out.mkdir(parents=True,exist_ok=True)
 decisions=read(src/'p3-v1.8-decisoes.csv'); oldpatch=read(src/'p3-v1.8-patches.csv');
 assert len(decisions)==len(oldpatch)==83 and len({x['id_global'] for x in decisions})==83
 assert set(REV)<=set(x['id_global'] for x in decisions)
 index={x['id_global']:x for x in decisions};patches=[];reviews=[];tests=[];modified={};bases=controls=0
 with zipfile.ZipFile(src/'lotes-001-a-030-p3-v1.8.zip') as zin,zipfile.ZipFile(out/'lotes-001-a-030-p3-v1.9.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=5) as zout:
  files=sorted(x for x in zin.namelist() if x.endswith('.csv'));assert len(files)==30
  for oldfile in files:
   rows=decode(zin.read(oldfile));heads=list(rows[0]);nb=nc=nm=0
   for row in rows:
    if row['tipo_registro']=='base':bases+=1;nb+=1
    else:controls+=1;nc+=1;continue
    rid=row['id_global'];
    if rid not in index:continue
    item=index[rid]; assert row['Keyword']==item['Keyword']
    status,note=rationale(item); before={};after={}
    if rid in REV:
     for key,value in REV[rid][1].items():
      if row[key]!=value:
       assert key in BASEFIELDS
       before[key]=row[key];after[key]=value;row[key]=value
     if after:
      before['justificativa_curta']=row['justificativa_curta'];row['justificativa_curta']='P3 v1.9 — '+note;after['justificativa_curta']=row['justificativa_curta']
      nm+=1;modified[rid]=dict(row)
      patches.append({'id_global':rid,'lote':row['lote_id'],'familia_id':row['familia_id'],'Keyword':row['Keyword'],'regra_v18':item['regra'],'parecer_v19':status,'campos_alterados':','.join(after),'antes_json':json.dumps(before,ensure_ascii=False,sort_keys=True),'depois_json':json.dumps(after,ensure_ascii=False,sort_keys=True),'motivo':note})
    reviews.append({'id_global':rid,'lote':row['lote_id'],'familia_id':row['familia_id'],'Keyword':row['Keyword'],'regra_v18':item['regra'],'area_resultante':row['area_principal'],'tipo_intencao_resultante':row['tipo_intencao'],'parecer_v19':status,'houve_patch':'sim' if after else 'não','nota_qa':note,'homologacao_editorial':'pendente'})
   name=oldfile.replace('v1.8','v1.9');zout.writestr(name,encode(rows,heads));tests.append({'lote_v18':oldfile,'lote_v19':name,'bases':nb,'controles':nc,'patches':nm,'status':'AGUARDA_REGRESSAO_INDEPENDENTE'})
 assert (bases,controls)==(294905,2190)
 assert len(reviews)==83 and len(patches)==len(REV)==10 and sum(int(t['patches']) for t in tests)==10
 assert len({x['id_global'] for x in patches})==10
 for srcname in ['p3-v1.8-fila-23965.csv','fila-geral-p0-p1-p2-p3-v1.8.csv']:
  source=src/srcname;dst=out/srcname.replace('v1.8','v1.9')
  with source.open(encoding='utf-8-sig',newline='') as fin,dst.open('w',encoding='utf-8-sig',newline='') as fout:
   reader=csv.DictReader(fin,delimiter=';');fields=reader.fieldnames;assert not set(TRACK)&set(fields)
   writer=csv.DictWriter(fout,fieldnames=fields+TRACK,delimiter=';',lineterminator='\n');writer.writeheader()
   for row in reader:
    rid=row['id_global'];row.update({k:'' for k in TRACK})
    if rid in index:
     s,n=rationale(index[rid]); real=modified.get(rid)
     row.update({'status_p3_v1_9':'REVISADA_COM_AJUSTE' if real else 'REVISADA_SEM_MUDANCA','parecer_p3_v1_9':s,'nota_qa_p3_v1_9':n,'classificacao_alterada_p3_v1_9':'sim' if real else 'não'})
     if real:row.update({'area_final_p3_v1_9':real['area_principal'],'cluster_final_p3_v1_9':real['cluster'],'subcluster_final_p3_v1_9':real['subcluster'],'tipo_intencao_final_p3_v1_9':real['tipo_intencao']})
    writer.writerow(row)
 reviews.sort(key=lambda x:int(x['id_global']));patches.sort(key=lambda x:int(x['id_global']))
 write(out/'p3-v1.9-pareceres-83.csv',reviews);write(out/'p3-v1.9-patches-10.csv',patches);write(out/'p3-v1.9-regressao-30-lotes.csv',tests)
 status=collections.Counter(x['parecer_v19'] for x in reviews);rules={}
 for rule in sorted(set(x['regra_v18'] for x in reviews)):
  arr=[x for x in reviews if x['regra_v18']==rule]
  rules[rule]={'examinados':len(arr),'ajustados':sum(x['houve_patch']=='sim' for x in arr),'mantidos_com_ressalva':sum(x['parecer_v19']=='MANTIDA_COM_RESSALVA' for x in arr),'mantidos':sum(x['parecer_v19']=='MANTIDA' for x in arr)}
 write(out/'p3-v1.9-qa-por-regra.csv',[{'regra':k,**v} for k,v in rules.items()])
 info={'etapa':'P3 v1.9','origem':'P3 v1.8','amostra':'revisao contextual de todos os 83 IDs da expansao anterior','ids_examinados':len(reviews),'patches_efetivos':len(patches),'pareceres':dict(status),'regras':rules,'lotes':len(tests),'base':bases,'controles':controls,'p3_fora_dos_pilotos':20672,'p2_pendencias':4660,'nota':'Parecer contextual por expressão, sem aprovação editorial externa. Nenhuma expansão nova nesta revisão.'}
 (out/'p3-v1.9-resumo.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(info,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
