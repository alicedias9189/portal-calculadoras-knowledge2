#!/usr/bin/env python3
# coding: utf-8
"""Parecer contextual dos 50 casos globais A e expansão P3 segura (17 IDs).

Reexecução a partir da raiz do ZIP descompactado:
    python3 07-Scripts/P3/auditar_global_e_p3_v26.py
Não sobrescreve fontes v2.5: produz arquivos sob 08-Entregas/P3-v2.6.
Usa apenas a biblioteca padrão Python.
"""
import csv, io, json, pathlib, zipfile, hashlib, re, collections
ROOT=pathlib.Path(__file__).resolve().parents[2]
SRC=ROOT/'08-Entregas/P3-v2.6/FONTES-P3-v2.5'
DST=ROOT/'08-Entregas/P3-v2.6'
DST.mkdir(parents=True,exist_ok=True)
LOTE=SRC/'lotes-001-a-030-p3-v2.3.zip'
FILA_P3=SRC/'p3-v2.3-fila-23965.csv'
FILA_GERAL=SRC/'fila-geral-p0-p1-p2-p3-v2.3.csv'
BACKLOG=SRC/'backlog-global-98-priorizado.csv'
PROTECTED={'tipo_registro','id_global','lote_id','familia_id','controle_id','Keyword'}
EDIT={'area_principal','cluster','subcluster','dominio_ou_grandeza','tipo_intencao','intencao_principal','confianca','revisao_manual','justificativa_curta'}

def read(path):
 with open(path,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def write(path,rs,cols=None):
 cols=cols or list(rs[0]);path.parent.mkdir(parents=True,exist_ok=True)
 with open(path,'w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,delimiter=';',fieldnames=cols,lineterminator='\n',extrasaction='ignore');w.writeheader();w.writerows(rs)
def source_lots():
 lots={};lookup={};meta={};ctrl=collections.Counter()
 with zipfile.ZipFile(LOTE) as z:
  assert len(z.namelist())==30
  for name in z.namelist():
   text=z.read(name).decode('utf-8-sig');rows=list(csv.DictReader(io.StringIO(text),delimiter=';'));fields=next(csv.reader(io.StringIO(text),delimiter=';'))
   lots[name]=(rows,fields)
   for r in rows:
    ctrl[r['tipo_registro']]+=1
    if r['tipo_registro']=='base':
     assert r['id_global'] not in lookup;lookup[r['id_global']]=(name,r)
 assert ctrl['base']==294905 and ctrl['controle']==2190,ctrl
 return lots,lookup
lots,lookup=source_lots()
p3_rows=read(FILA_P3);general_rows=read(FILA_GERAL);backlog=read(BACKLOG)
assert len(p3_rows)==23965 and len(general_rows)==52046 and len(backlog)==98
p3={r['id_global']:r for r in p3_rows};general={r['id_global']:r for r in general_rows}
assert len(p3)==len(p3_rows) and len(general)==len(general_rows)
for rid,r in p3.items():
 assert rid in general and general[rid]['prioridade']=='P3' and rid in lookup
 assert lookup[rid][1]['Keyword']==r['Keyword']==general[rid]['Keyword']
 assert lookup[rid][1]['familia_id']==r['familia_id']==general[rid]['familia_id']
# Validate all priority A records truly out of scope.
for r in backlog:
 rid=r['id_global']
 assert rid in lookup and rid not in p3 and rid not in general
 assert r['Keyword']==lookup[rid][1]['Keyword']
assert len({r['id_global'] for r in backlog})==98

# Do not treat an unqualified keyword as a definitive instruction for a tax/credit calculation.
def opinion(r):
 k=r['Keyword'].lower();rule=r['regra'];base=lookup[r['id_global']][1]
 is_cet=rule=='P3V22_CET_CREDITO';is_tax=rule=='P3V22_IRRF_BASE_FINANCAS'
 assert is_cet or is_tax
 historical=bool(re.search(r'\b(?:20(?:1\d|2[0-6]))\b',k))
 if is_cet:
  if 'calculadora' in k:
   tipo='cálculo contextual';signal='Busca por ferramenta de cálculo do custo efetivo total.'
  elif k.startswith('como calcular'):
   tipo='informacional';signal='Pergunta sobre método, fórmula ou passos; não solicita um resultado com dados fornecidos.'
  elif k.startswith('calcular ') and 'como' not in k:
   tipo='cálculo contextual';signal='Busca uma operação de cálculo, mas carece das parcelas e condições contratuais.'
  else:
   tipo='informacional';signal='Busca conceito, comparação ou taxa do CET; não equivale à taxa nominal.'
  cluster='Crédito';sub='Custo efetivo total (CET) de crédito'
  if 'imobili' in k:cluster='Crédito e financiamentos';sub='Custo Efetivo Total (CET) imobiliário'
  conf='ALTA' if ('calculadora' in k or 'como calcular' in k or 'custo efetivo total' in k) else 'MEDIA'
  caution='CET depende de tarifas, tributos, seguros, fluxo de pagamentos, prazo e contrato; nenhum valor real foi inferido.'
 else:
  cluster='Tributos';sub='IRRF e base de cálculo'
  if k.startswith('tabela') or (('base de calculo' in k) and not k.startswith('calcular')):
   tipo='informacional';signal='Consulta a base/tabela do IRRF, não cálculo executável sem dados.'
  elif 'calculadora' in k or k.startswith('calcular') or 'calculo' in k or 'cálculo' in k:
   tipo='cálculo contextual';signal='Operação tributária depende dos valores, beneficiário e regra correspondente ao período.'
  else:
   tipo='informacional';signal='Referência tributária mencionada sem valores para calcular.'
  conf='ALTA' if ('irrf' in k) else 'MEDIA'
  caution='IRRF sobre aluguel ou base genérica exige natureza do rendimento, beneficiário e tabela vigente no período consultado.'
 if historical:caution+=' Referência histórica explícita: usar regras do ano citado, não tabela atual.'
 # individual explanation retaining per-keyword meaning
 note=f"{signal} Keyword: «{r['Keyword']}». {caution}"
 if base['area_principal'] not in ['Finanças','Trabalho'] and is_tax:
  note+=' A área atual está incorreta (não é energia, datas nem outro domínio incidental).'
 if base['area_principal']!='Finanças' and is_cet:
  note+=' A área original diverge de crédito/finanças.'
 verdict='REVISAR_PROPOSTA_E_SUBTIPO' if tipo!=r['proposta_tipo'] else 'FAVORAVEL_COM_RESSALVAS'
 return {**r,
  'status_revisao_A':'REVISADO_CONTEXTUALMENTE',
  'parecer_tecnico':'AJUSTAR_INTENCAO' if tipo!=r['proposta_tipo'] else 'PLAUSIVEL_COM_CONDICOES',
  'area_sugerida':'Finanças','cluster_sugerido':cluster,'subcluster_sugerido':sub,
  'tipo_intencao_sugerido':tipo,'evidencia_textual':signal,'ressalva_individual':caution,
  'justificativa_individual':note,'homologacao_editorial':'PENDENTE','autoriza_aplicacao':'NÃO',
  'destino':'BACKLOG_GLOBAL_FORA_DAS_FILAS','revisao_semantica':'POR_CONTEXTO','status_proposta':verdict}

A=sorted((r for r in backlog if r['faixa_prioridade_global']=='A_ALTA'),key=lambda r:int(r['ordem_global']))
assert len(A)==50
review=[opinion(r) for r in A]
write(DST/'revisao-contextual-global-50-alta.csv',review)
review_by_id={r['id_global']:r for r in review}
all_rows=[]
for r in backlog:
 q={k:'' for k in list(review[0]) if k not in r}
 if r['id_global'] in review_by_id:q={k:review_by_id[r['id_global']][k] for k in q}
 else:
  q['status_revisao_A']='AGUARDA_REVISAO_FAIXA_B_C';q['homologacao_editorial']='PENDENTE';q['autoriza_aplicacao']='NÃO';q['destino']='BACKLOG_GLOBAL_FORA_DAS_FILAS'
 all_rows.append({**r,**q})
write(DST/'backlog-global-98-com-parecer-50.csv',all_rows)
# 17 carefully selected P3 IDs; no classification outside P3 allowed.
SPEC={
 '72641':('Previdência e benefícios','Contribuições ao INSS','informacional','Pergunta sobre idade de início de contribuição previdenciária, não duração de curso.'),
 '72576':('Previdência e benefícios','Tempo de contribuição e aposentadoria','informacional','Pergunta sobre elegibilidade/tempo de contribuição; não é duração escolar.'),
 '44076':('Previdência e benefícios','Contribuições em atraso do contribuinte individual','cálculo contextual','Cálculo de contribuição previdenciária em atraso exige competência e enquadramento.'),
 '44085':('Previdência e benefícios','Contribuições em atraso do contribuinte individual','cálculo contextual','Mesmo tema de contribuição em atraso com ordem textual invertida.'),
 '190795':('Previdência e benefícios','Piso e reajuste de benefícios do INSS','informacional','Consulta de piso previdenciário, não preço de combustíveis.'),
 '190796':('Previdência e benefícios','Piso e reajuste de benefícios do INSS','informacional','Consulta de piso de aposentadoria, não preço de combustíveis.'),
 '48429':('Previdência e benefícios','Salário-maternidade','cálculo contextual','Valor do benefício depende da condição da segurada e referência temporal.'),
 '254592':('Previdência e benefícios','Salário-maternidade','cálculo contextual','Consulta a cálculo do benefício, não insalubridade/periculosidade.'),
 '58427':('Previdência e benefícios','Salário-maternidade','cálculo contextual','Cálculo do benefício para contribuinte individual, não salário líquido padrão.'),
 '39787':('Previdência e benefícios','Salário-maternidade','cálculo contextual','Calculadora histórica do benefício; requer normas e valores do ano indicado.'),
 '39788':('Previdência e benefícios','Salário-maternidade','cálculo contextual','Calculadora histórica do benefício; requer normas e valores do ano indicado.'),
 '47350':('Previdência e benefícios','Salário-maternidade','cálculo contextual','Cálculo de salário-maternidade para ano histórico, não operação numérica direta.'),
 '47452':('Previdência e benefícios','Salário-maternidade','cálculo contextual','Cálculo de salário-maternidade para ano histórico, não operação numérica direta.'),
 '125397':('Previdência e benefícios','Salário-maternidade','cálculo contextual','Cálculo de salário-maternidade para empregada doméstica, sujeito a vínculo e regras.'),
 '125398':('Previdência e benefícios','Salário-maternidade','cálculo contextual','Cálculo de salário-maternidade para empresária, sujeito a enquadramento e regras.'),
 '255603':('Previdência e benefícios','Salário-maternidade','informacional','Consulta de elegibilidade de pessoa desempregada, não seguro-desemprego.'),
 '255612':('Previdência e benefícios','Tempo de contribuição e salário-maternidade','informacional','Pergunta sobre contagem de período do benefício para contribuição previdenciária, não salário líquido.'),
}
# guardians
assert len(SPEC)==17 and all(i in p3 and i in general and i in lookup for i in SPEC)
for rid in SPEC:
 assert p3[rid]['prioridade']==general[rid]['prioridade']=='P3'
 assert all(not p3[rid].get(k) or p3[rid][k]=='FORA_DO_PILOTO' for k in p3[rid] if k.startswith('status_p3_'))
assert not set(SPEC).intersection({r['id_global'] for r in backlog})
newrows={}; patches=[];decisions=[]
for rid,(cluster,sub,tipo,reason) in SPEC.items():
 lot,r=lookup[rid]
 new=r.copy(); new.update({
  'area_principal':'Trabalho','cluster':cluster,'subcluster':sub,
  'dominio_ou_grandeza':'Previdência e benefícios do INSS',
  'tipo_intencao':tipo,
  'intencao_principal':('Consultar informação: ' if tipo=='informacional' else 'Calcular com contexto: ')+sub,
  'confianca':'média','revisao_manual':'sim',
  'justificativa_curta':reason+' (P3 v2.6; proposta técnica; não homologação editorial).'
 })
 diff=[k for k in r if r[k]!=new[k]]
 assert diff and set(diff)<=EDIT
 newrows[rid]=new
 patches.append({'id_global':rid,'lote':lot,'familia_id':r['familia_id'],'Keyword':r['Keyword'],'campos_modificados':','.join(diff),'antes_json':json.dumps({k:r[k] for k in diff},ensure_ascii=False,sort_keys=True),'depois_json':json.dumps({k:new[k] for k in diff},ensure_ascii=False,sort_keys=True),'justificativa':reason})
 decisions.append({'id_global':rid,'familia_id':r['familia_id'],'Keyword':r['Keyword'],'area_anterior':r['area_principal'],'area_sugerida':'Trabalho','cluster_sugerido':cluster,'subcluster_sugerido':sub,'tipo_intencao_sugerido':tipo,'parecer':'CLASSIFICACAO_TECNICA_CONTEXTUAL','aprovacao_editorial':'PENDENTE','justificativa':reason})
patches.sort(key=lambda r:int(r['id_global'])); decisions.sort(key=lambda r:int(r['id_global']))
write(DST/'p3-v2.6-patches-17.csv',patches)
write(DST/'p3-v2.6-decisoes-17.csv',decisions)
# Write only new lot versions
with zipfile.ZipFile(DST/'lotes-001-a-030-p3-v2.6.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for fname,(rows,fields) in lots.items():
  out=[]
  for r in rows:out.append(newrows.get(r['id_global'],r))
  bf=io.StringIO();w=csv.DictWriter(bf,delimiter=';',fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(out)
  z.writestr(fname.replace('v2.3','v2.6'),('\ufeff'+bf.getvalue()).encode('utf-8'))
# queue append audit columns; preserve historic columns values
cols=['status_p3_v2_6','regra_p3_v2_6','justificativa_p3_v2_6','area_final_p3_v2_6','cluster_final_p3_v2_6','subcluster_final_p3_v2_6','tipo_intencao_final_p3_v2_6','classificacao_alterada_p3_v2_6']
for inname,outname,rows in [('p3-v2.3-fila-23965.csv','p3-v2.6-fila-23965.csv',p3_rows),('fila-geral-p0-p1-p2-p3-v2.3.csv','fila-geral-p0-p1-p2-p3-v2.6.csv',general_rows)]:
 fields=list(rows[0]);assert not set(cols)&set(fields)
 out=[]
 for r in rows:
  new=r.copy(); id=r['id_global']; d=newrows.get(id)
  if d:new.update({'status_p3_v2_6':'REVISADO','regra_p3_v2_6':'P3V26_PREVIDENCIA_DOMINIO','justificativa_p3_v2_6':d['justificativa_curta'],'area_final_p3_v2_6':d['area_principal'],'cluster_final_p3_v2_6':d['cluster'],'subcluster_final_p3_v2_6':d['subcluster'],'tipo_intencao_final_p3_v2_6':d['tipo_intencao'],'classificacao_alterada_p3_v2_6':'sim'})
  else:new.update({x:'' for x in cols})
  out.append(new)
 write(DST/outname,out,fields+cols)
# Independently re-open both lot ZIPs and compare row by row, including patch JSON
prev={r['id_global']:r for r in patches};seen=set(); reg=[]; prot_a=hashlib.sha256();prot_b=hashlib.sha256()
with zipfile.ZipFile(LOTE) as za,zipfile.ZipFile(DST/'lotes-001-a-030-p3-v2.6.zip') as zb:
 for fname in za.namelist():
  newname=fname.replace('v2.3','v2.6')
  old=list(csv.DictReader(io.StringIO(za.read(fname).decode('utf-8-sig')),delimiter=';'))
  new=list(csv.DictReader(io.StringIO(zb.read(newname).decode('utf-8-sig')),delimiter=';'))
  assert len(old)==len(new);base=ctrl=changed=0
  for a,b in zip(old,new):
   assert a['id_global']==b['id_global'] and a['tipo_registro']==b['tipo_registro'] and a.keys()==b.keys()
   if a['tipo_registro']=='base':base+=1
   else:ctrl+=1
   diff={k for k in a if a[k]!=b[k]}
   if diff:
    assert a['id_global'] in prev and diff<=EDIT and a['tipo_registro']=='base'
    p=prev[a['id_global']];assert diff==set(p['campos_modificados'].split(','))
    assert json.loads(p['antes_json'])=={k:a[k] for k in diff}
    assert json.loads(p['depois_json'])=={k:b[k] for k in diff}
    assert a['id_global'] not in seen;seen.add(a['id_global']);changed+=1
   for col in a:
    if col not in EDIT:
     prot_a.update((col+'\0'+a[col]+'\x1e').encode());prot_b.update((col+'\0'+b[col]+'\x1e').encode())
  reg.append({'lote':fname,'registros_base':base,'controles':ctrl,'alteracoes_autorizadas':changed,'alteracoes_indevidas':0,'status':'PASSOU'})
assert seen==set(SPEC) and prot_a.hexdigest()==prot_b.hexdigest()
assert sum(x['registros_base'] for x in reg)==294905 and sum(x['controles'] for x in reg)==2190
write(DST/'regressao-independente-30-lotes.csv',reg)
# compare queue historical columns; separate P3-IDs and outsider 98 remain untouched
for a,b in ((FILA_P3,DST/'p3-v2.6-fila-23965.csv'),(FILA_GERAL,DST/'fila-geral-p0-p1-p2-p3-v2.6.csv')):
 pre=read(a);post=read(b)
 assert len(pre)==len(post)
 for x,y in zip(pre,post):
  assert all(x[f]==y[f] for f in x)
# 98 blocked control test with mixed eligible candidates
blocked=[r['id_global'] for r in backlog if r['id_global'] not in p3 and r['id_global'] not in general]
assert len(blocked)==98
control={'casos_globais_bloqueados':len(blocked),'novos_ids_elegiveis_p3':len(SPEC),'ids_fora_da_fila_alterados':0,'duplicidades':0,'prioridade_p3_confirmada':True,'regressao_30_lotes':'PASSOU'}
(DST/'controle-elegibilidade-v26.json').write_text(json.dumps(control,ensure_ascii=False,indent=2),encoding='utf-8')
summary={'revisados_global_A':len(review),'pendentes_global_BC':48,'propostas_globais_aplicadas':0,'microexpansao_P3':len(SPEC),'familias_p3_novas':len({p3[i]['familia_id'] for i in SPEC}),'P3_nao_revisados_antes':20400,'P3_nao_revisados_depois':20400-len(SPEC),'pendencias_P2':4660,'lotes':30,'base':294905,'controles':2190,'sha256_campos_protegidos':prot_a.hexdigest(),'status':'PASSOU','parecer_nao_equivale_a_homologacao':True}
(DST/'resumo-v26.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
