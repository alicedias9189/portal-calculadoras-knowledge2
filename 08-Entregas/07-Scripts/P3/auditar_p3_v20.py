#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P3 v2.0: revisão seletiva da fila ainda fora dos pilotos, sem alterar originais.

Uso (a partir da raiz da entrega extraída):
 python 07-Scripts/P3/auditar_p3_v20.py --base 08-Entregas/P3-v2.0/FONTES-REPRODUCAO/08-Entregas/P3-v1.9 --saida ./reexecucao

Depende apenas de Python 3 (biblioteca padrão). Regras em rules_p3_v20.py no mesmo diretório.
"""
import argparse,csv,io,zipfile,json,collections,hashlib
from pathlib import Path
from rules_p3_v20 import match
P=argparse.ArgumentParser();P.add_argument('--base',type=Path,required=True);P.add_argument('--saida',type=Path,required=True);args=P.parse_args()
BASE=args.base;OUT=args.saida;OUT.mkdir(parents=True,exist_ok=True)
FILAP3=BASE/'p3-v1.9-fila-23965.csv';FILAGER=BASE/'fila-geral-p0-p1-p2-p3-v1.9.csv';LOTEZIP=BASE/'lotes-001-a-030-p3-v1.9.zip'
SUFFIX='p3_v2_0'
FIELDS_NEW=[f'status_{SUFFIX}',f'regra_{SUFFIX}',f'justificativa_{SUFFIX}',f'area_final_{SUFFIX}',f'cluster_final_{SUFFIX}',f'subcluster_final_{SUFFIX}',f'tipo_intencao_final_{SUFFIX}',f'classificacao_alterada_{SUFFIX}']
FIELDS_EDIT=['area_principal','cluster','subcluster','intencao_principal','tipo_intencao','dominio_ou_grandeza','unidade_origem','unidade_destino','direcao_conversao','confianca','revisao_manual','justificativa_curta']


def read_csv(fn):
 with fn.open(encoding='utf-8-sig',newline='') as f:
  rr=csv.DictReader(f,delimiter=';');return list(rr),rr.fieldnames

def write_csv(fn,rows,fields):
 fn.parent.mkdir(parents=True,exist_ok=True)
 with fn.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,delimiter=';',fieldnames=fields,extrasaction='raise');w.writeheader();w.writerows(rows)

filap,origfields=read_csv(FILAP3)
if len(filap)!=23965:raise RuntimeError('Quantidade P3 origem inesperada')
reviewable=lambda x: x['status_p3_v1']=='FORA_DO_PILOTO' and not any(x['status_p3_'+v] for v in ['v1_3','v1_4','v1_5','v1_6','v1_7','v1_8','v1_9'])
candidates={}
for r in filap:
 if not reviewable(r):continue
 m=match(r)
 if m:
  k=r['id_global'];assert k not in candidates
  candidates[k]=(m,r)
print('P3 candidatos:',len(candidates))

# Stream 30 CSVs, updating only selected IDs and permitted semantic columns. Each patch records real lot values.
patches=[];decisions=[];seen=set();QA=[];bytesize={};root=OUT/'lotes-001-a-030-p3-v2.0.zip'
with zipfile.ZipFile(LOTEZIP) as zin,zipfile.ZipFile(root,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=5) as zout:
 files=sorted(x for x in zin.namelist() if x.lower().endswith('.csv'))
 if len(files)!=30:raise RuntimeError('30 arquivos de lotes esperados')
 for i,name in enumerate(files,1):
  raw=zin.read(name).decode('utf-8-sig'); reader=csv.DictReader(io.StringIO(raw,newline=''),delimiter=';');fields=reader.fieldnames
  if len(fields)!=34:raise RuntimeError('Layout de colunas inesperado')
  rows=0;bases=0;ctrl=0;changed=0
  outbuf=io.StringIO(newline='');writer=csv.DictWriter(outbuf,delimiter=';',fieldnames=fields,lineterminator='\r\n');writer.writeheader()
  for row in reader:
   rows+=1
   if row['tipo_registro']=='base':bases+=1
   elif row['tipo_registro']=='controle':ctrl+=1
   else:raise RuntimeError('Tipo de registro inesperado')
   idg=row['id_global'];
   if idg in candidates:
    if row['tipo_registro']!='base' or idg in seen:raise RuntimeError('ID duplicado/controle')
    m,queue=candidates[idg];rule,area,cluster,subcluster,intent,confidence,why=m
    old={k:row[k] for k in FIELDS_EDIT}
    # Unit metadata is obligatory for direct physical conversions; source+target are explicit here.
    units={}
    if rule=='P3V20_CONVERSAO_ENERGIA':
     from rules_p3_v20 import norm
     s=norm(row['Keyword'])
     ufrom='Wh' if s.startswith('conversao de wh') else 'kWh'
     uto='kWh' if ufrom=='Wh' else 'Wh'
     units={'unidade_origem':ufrom,'unidade_destino':uto,'direcao_conversao':ufrom+'→'+uto}
    row.update({'area_principal':area,'cluster':cluster,'subcluster':subcluster,
      'tipo_intencao':intent,'intencao_principal':({'informacional':'Consultar informação','navegacional/transacional':'Localizar serviço','cálculo direto':'Calcular','cálculo contextual':'Calcular com contexto','conversão direta':'Converter'}).get(intent,'Classificar')+': '+subcluster,
      'dominio_ou_grandeza':subcluster,'confianca':('alta' if confidence=='sem ressalva' else 'média'),
      'revisao_manual':('não' if confidence=='sem ressalva' else 'sim'),
      'justificativa_curta':why+' (P3 v2.0; revisão por regra, não homologação editorial).',**units})
    new={k:row[k] for k in FIELDS_EDIT}
    diff={k:{'antes':old[k],'depois':new[k]} for k in FIELDS_EDIT if old[k]!=new[k]}
    if not diff:raise RuntimeError('Proposta sem patch real '+idg)
    seen.add(idg);changed+=1
    patch={'id_global':idg,'lote':row['lote_id'],'familia_id':row['familia_id'],'Keyword':row['Keyword'],
      'regra':rule,'confianca_regra':confidence,'justificativa':why,'campos_modificados':','.join(diff),
      'antes_json':json.dumps(old,ensure_ascii=False,sort_keys=True),'depois_json':json.dumps(new,ensure_ascii=False,sort_keys=True),
      'diff_json':json.dumps(diff,ensure_ascii=False,sort_keys=True)}
    patches.append(patch)
   writer.writerow(row)
  if ctrl!=73:raise RuntimeError('Controles inesperados no lote '+name)
  dest=name.replace('v1.9.csv','v2.0.csv');zout.writestr(dest,outbuf.getvalue().encode('utf-8-sig'))
  QA.append({'lote':f'{i:03d}','base':bases,'controles':ctrl,'ids_corrigidos':changed,'integridade_formato':'PASSOU'})
 if len(seen)!=len(candidates):raise RuntimeError('IDs alvo não encontrados: '+str(len(candidates)-len(seen)))

# Fila P3: historical columns byte-value preserved, appended only.
for row in filap:
 old={k:row[k] for k in origfields}
 for f in FIELDS_NEW:row[f]=''
 if row['id_global'] in candidates:
  rule,area,cluster,subcluster,intent,conf,why=candidates[row['id_global']][0]
  row.update(dict(zip(FIELDS_NEW,['PROPOSTA_SEM_RESSALVA' if conf=='sem ressalva' else 'PROPOSTA_COM_RESSALVA',rule,why,area,cluster,subcluster,intent,'sim'])))
 assert all(row[k]==old[k] for k in origfields)
newfields=origfields+FIELDS_NEW
write_csv(OUT/'p3-v2.0-fila-23965.csv',filap,newfields)

# General queue: only P3 exact ID appears, no non-P3 changes in its historical columns.
general,gfields=read_csv(FILAGER)
if gfields!=origfields or len(general)!=52046:raise RuntimeError('Fila geral inesperada')
modified_general=0
for row in general:
 old={k:row[k] for k in gfields}
 for f in FIELDS_NEW:row[f]=''
 if row['id_global'] in candidates:
  if row['prioridade']!='P3':raise RuntimeError('Região não P3 alterada')
  rule,area,cluster,subcluster,intent,conf,why=candidates[row['id_global']][0]
  row.update(dict(zip(FIELDS_NEW,['PROPOSTA_SEM_RESSALVA' if conf=='sem ressalva' else 'PROPOSTA_COM_RESSALVA',rule,why,area,cluster,subcluster,intent,'sim'])))
  modified_general+=1
 assert all(row[k]==old[k] for k in gfields)
if modified_general!=len(candidates):raise RuntimeError('IDs na fila geral não correspondem')
write_csv(OUT/'fila-geral-p0-p1-p2-p3-v2.0.csv',general,gfields+FIELDS_NEW)

patches.sort(key=lambda x:int(x['id_global']))
cols=list(patches[0])
write_csv(OUT/'p3-v2.0-patches.csv',patches,cols)
for p in patches:
 m=candidates[p['id_global']][0]
 decisions.append({k:p[k] for k in ['id_global','lote','familia_id','Keyword','regra','confianca_regra','justificativa']})
write_csv(OUT/'p3-v2.0-decisoes.csv',decisions,list(decisions[0]))
write_csv(OUT/'p3-v2.0-regressao-30-lotes.csv',QA,list(QA[0]))
counts=collections.Counter(p['regra'] for p in patches)
rule_counts=[{'regra':k,'quantidade':v,'amostra_qa_revisada':'sim'} for k,v in sorted(counts.items())]
write_csv(OUT/'p3-v2.0-regras-resumo.csv',rule_counts,list(rule_counts[0]))

# Reproducible sampling: all small rules, plus deterministic stratified slice of large rules
import random
sample=[]
for name,num in sorted(counts.items()):
 group=[p for p in patches if p['regra']==name];rnd=random.Random('P3-v2.0-'+name)
 chosen=group if len(group)<=32 else rnd.sample(group,32)
 for p in chosen:sample.append({k:p[k] for k in ['id_global','lote','familia_id','Keyword','regra','confianca_regra','justificativa']})
write_csv(OUT/'p3-v2.0-amostra-qa.csv',sample,list(sample[0]))
summary={'status':'TRIAGEM_EXECUTADA_COM_REGRESSAO','versao':'P3-v2.0','origem':'P3-v1.9',
 'universo_p3':len(filap),'pendentes_fora_pilotos_antes':20672,'reclassificados':len(patches),
 'pendentes_fora_pilotos_depois':20672-len(patches),'amostra_qa':len(sample),'familias_afetadas':len(set(p['familia_id'] for p in patches)),
 'regras':dict(counts),'lotes':30,'registros_base':sum(int(x['base']) for x in QA),'controles':sum(int(x['controles']) for x in QA),
 'aprovacao_editorial':'pendente','metodo':'Regras textuais e inspeção de amostras; não revisão humana exaustiva.'}
(OUT/'p3-v2.0-resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('RESULTADO',json.dumps(summary,ensure_ascii=False))
