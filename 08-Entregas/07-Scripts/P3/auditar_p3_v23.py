#!/usr/bin/env python3
# coding: utf-8
"""P3 v2.3: auditoria de escopo e revisão das 72 amostras P3 v2.2.

Entradas auto-contidas em FONTES-REPRODUCAO, saídas paralelas em 08-Entregas/P3-v2.3.
Só 10 dos 108 IDs da v2.2 são P3. Restaura 98 IDs de fora da fila à v2.1,
conserva as propostas originais em quarentena, refina dois IDs P3.
Requisitos: Python 3 stdlib. Não altera fontes.
"""
import csv,io,json,hashlib
from pathlib import Path
from collections import Counter
from zipfile import ZipFile,ZIP_DEFLATED
ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'08-Entregas/P3-v2.3/FONTES-REPRODUCAO/08-Entregas/P3-v2.2'
OUT=ROOT/'08-Entregas/P3-v2.3'; OUT.mkdir(parents=True,exist_ok=True)
FIELDS={'area_principal','cluster','subcluster','dominio_ou_grandeza','tipo_intencao','intencao_principal','confianca','revisao_manual','justificativa_curta'}
SPECIAL={
 '41627':('Calcular CET mensal demanda custos, parcelas e fluxo financeiro: cálculo contextual, não mera consulta.', 'cálculo contextual'),
 '69676':('CET com pedido explícito de cálculo requer dados do contrato e encargos.', 'cálculo contextual'),
}

def csv_from(s):return list(csv.DictReader(io.StringIO(s),delimiter=';'))
def read(p):return csv_from(p.read_text(encoding='utf-8-sig'))
def write(path,rows,cols):
 with path.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=cols,delimiter=';',extrasaction='ignore',lineterminator='\n');w.writeheader();w.writerows(rows)

def header(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return next(csv.reader(f,delimiter=';'))

D=read(SRC/'p3-v2.2-decisoes.csv'); S=read(SRC/'p3-v2.2-amostra-qa.csv');Q=read(SRC/'p3-v2.2-fila-23965.csv')
assert len(D)==108 and len(S)==72 and len(Q)==23965
ids={d['id_global'] for d in D}; sample_ids={s['id_global'] for s in S}; q_ids={q['id_global'] for q in Q}
valid_ids=ids&q_ids; outside=ids-q_ids
assert len(valid_ids)==10 and len(outside)==98 and set(SPECIAL)<=valid_ids
assert len(sample_ids&valid_ids)==4 and len(sample_ids&outside)==68

# Leitura dos 108 registros-base originais antes da v2.2 para reversão exata.
original={}
with ZipFile(SRC/'lotes-001-a-030-p3-v2.1.zip') as z:
 for name in z.namelist():
  for row in csv_from(z.read(name).decode('utf-8-sig')):
   if row['id_global'] in ids:
    assert row['tipo_registro']=='base' and row['id_global'] not in original
    original[row['id_global']]=row
assert len(original)==108

patches=[];before={};after={};reg=[];seen=set();base_total=ctrl_total=0
with ZipFile(SRC/'lotes-001-a-030-p3-v2.2.zip') as zi, ZipFile(OUT/'lotes-001-a-030-p3-v2.3.zip','w',compression=ZIP_DEFLATED,compresslevel=6) as zo:
 assert len(zi.namelist())==30
 for name in zi.namelist():
  raw=zi.read(name).decode('utf-8-sig')
  cols=next(csv.reader(io.StringIO(raw),delimiter=';'))
  rows=csv_from(raw);nr=[];nbase=nctrl=nmod=0
  for r in rows:
   id=r['id_global']
   if r['tipo_registro']=='base':nbase+=1
   else:nctrl+=1
   new=r
   if id in ids:
    assert r['tipo_registro']=='base' and id not in seen
    seen.add(id);before[id]=r
    if id in outside:
     old=original[id]
     # Restore all analytical changes introduced by v2.2, without erasing any prior stage.
     assert all(r[k]==old[k] for k in r if k not in FIELDS),(id,'Campos protegidos mudaram antes desta auditoria')
     new=r.copy();new.update({k:old[k] for k in FIELDS})
     cause='FORA_DA_FILA_P3_RESTAURADO'
     justification='ID não pertence à fila P3 de 23.965; a alteração v2.2 foi restaurada ao estado v2.1 e preservada como proposta isolada.'
    elif id in SPECIAL:
     reason,typ=SPECIAL[id];new=r.copy();new['tipo_intencao']=typ
     new['intencao_principal']='Calcular com contexto: '+r['subcluster']
     new['confianca']='média';new['revisao_manual']='sim'
     new['justificativa_curta']=reason+' (P3 v2.3, sujeito a parâmetros e revisão editorial).'
     cause='REFINAMENTO_INTENCAO_CET';justification=reason
    if new!=r:
     diff=[k for k in cols if new[k]!=r[k]]
     assert set(diff)<=FIELDS
     patches.append({'id_global':id,'lote':name,'familia_id':r['familia_id'],'Keyword':r['Keyword'],
          'natureza':cause,'justificativa':justification,'campos_modificados':','.join(diff),
          'antes_json':json.dumps({k:r[k] for k in diff},ensure_ascii=False,sort_keys=True),
          'depois_json':json.dumps({k:new[k] for k in diff},ensure_ascii=False,sort_keys=True)})
     nmod+=1
    after[id]=new
   nr.append(new)
  b=io.StringIO();w=csv.DictWriter(b,fieldnames=cols,delimiter=';',lineterminator='\n');w.writeheader();w.writerows(nr)
  zo.writestr(name.replace('v2.2','v2.3'),('\ufeff'+b.getvalue()).encode('utf-8'))
  reg.append({'lote':name,'base':nbase,'controles':nctrl,'alteracoes_autorizadas':nmod,'alteracoes_indevidas':0,'status':'PASSOU'})
  base_total+=nbase;ctrl_total+=nctrl
assert seen==ids and base_total==294905 and ctrl_total==2190
assert len(patches)==100 and len([p for p in patches if p['natureza']=='FORA_DA_FILA_P3_RESTAURADO'])==98
patches.sort(key=lambda x:int(x['id_global']))
write(OUT/'p3-v2.3-patches.csv',patches,list(patches[0]))
write(OUT/'p3-v2.3-regressao-30-lotes.csv',reg,list(reg[0]))

# Pendências legítimas de melhoria fora do escopo, com histórico v2.1 -> v2.2.
dec_map={x['id_global']:x for x in D}; quarantine=[]
for id in sorted(outside,key=int):
 r=before[id];s=original[id];d=dec_map[id]
 diff=[k for k in FIELDS if s[k]!=r[k]]
 quarantine.append({**d,'prioridade_dentro_da_fila':'NAO','estado_atual':'RESTAURADO_V2.1',
  'parecer':'PROPOSTA_FORA_DA_FILA_P3','origem_area':s['area_principal'],'origem_tipo':s['tipo_intencao'],
  'proposta_area':r['area_principal'],'proposta_tipo':r['tipo_intencao'],
  'campos_propostos':','.join(sorted(diff)),
  'antes_json':json.dumps({k:s[k] for k in diff},ensure_ascii=False,sort_keys=True),
  'proposta_json':json.dumps({k:r[k] for k in diff},ensure_ascii=False,sort_keys=True)})
write(OUT/'p3-v2.3-quarentena-98-propostas.csv',quarantine,list(quarantine[0]))

# Parecer por ID; subset exato dos 72 da amostra preservado.
assess=[]
for d in D:
 id=d['id_global'];r=after[id];k=r['Keyword'].lower()
 if id in outside:
  status='REVERTIDO_FORA_P3';note='ID ausente da fila P3 (e da fila geral priorizada). Retornado à v2.1; proposta preservada em quarentena.'
 elif id in SPECIAL:
  status='CORRIGIDO_P3';note=SPECIAL[id][0]
 else:
  status='MANTIDO_COM_RESSALVA'
  note='P3 legítima; subtipo de CET/taxa reconhecível, mas taxa, instituição, período e dados do contrato não foram informados.'
 assess.append({**d,'na_amostra_72':'sim' if id in sample_ids else 'não','pertence_a_fila_P3':'sim' if id in valid_ids else 'não',
  'parecer_qa_p3_v2_3':status,'justificativa_qa_p3_v2_3':note,
  'tipo_antes_v2_2':before[id]['tipo_intencao'],'tipo_final_v2_3':r['tipo_intencao'],
  'subcluster_final_v2_3':r['subcluster'],'alteracao_no_lote':'sim' if before[id]!=r else 'não'})
assess_s=[x for x in assess if x['na_amostra_72']=='sim']
assert len(assess_s)==72
write(OUT/'p3-v2.3-pareceres-108.csv',assess,list(assess[0]))
write(OUT/'p3-v2.3-revisao-amostra-72.csv',assess_s,list(assess_s[0]))
# Amostra suplementar: todos os 10 registros realmente P3.
valid_assess=[x for x in assess if x['pertence_a_fila_P3']=='sim']
write(OUT/'p3-v2.3-QA-10-P3-elegiveis.csv',valid_assess,list(valid_assess[0]))

# Históricos da fila preservados, anotações adicionadas apenas aos 10 elegíveis.
columns=['status_p3_v2_3','parecer_p3_v2_3','justificativa_p3_v2_3','area_final_p3_v2_3','cluster_final_p3_v2_3',
         'subcluster_final_p3_v2_3','tipo_intencao_final_p3_v2_3','alterado_p3_v2_3']
assessment={x['id_global']:x for x in assess}
for src,dst,expected in [('p3-v2.2-fila-23965.csv','p3-v2.3-fila-23965.csv',23965),
    ('fila-geral-p0-p1-p2-p3-v2.2.csv','fila-geral-p0-p1-p2-p3-v2.3.csv',52046)]:
 q=read(SRC/src);h=header(SRC/src);assert len(q)==expected and not set(columns)&set(h)
 seen_q=set()
 for row in q:
  id=row['id_global'];values={k:'' for k in columns}
  if id in valid_ids:
   seen_q.add(id);qa=assessment[id];r=after[id]
   values={'status_p3_v2_3':'CORRIGIDO' if id in SPECIAL else 'PRESERVADO',
    'parecer_p3_v2_3':qa['parecer_qa_p3_v2_3'],'justificativa_p3_v2_3':qa['justificativa_qa_p3_v2_3'],
    'area_final_p3_v2_3':r['area_principal'],'cluster_final_p3_v2_3':r['cluster'],
    'subcluster_final_p3_v2_3':r['subcluster'],'tipo_intencao_final_p3_v2_3':r['tipo_intencao'],
    'alterado_p3_v2_3':'sim' if id in SPECIAL else 'não'}
  row.update(values)
 assert seen_q==valid_ids
 write(OUT/dst,q,h+columns)

num_prev_reviewed=sum(any(q.get(k)=='sim' for k in q if k.startswith('classificacao_alterada_p3_') and k!='classificacao_alterada_p3_v2_2') for q in Q if q['id_global'] in valid_ids)
# previous uncovered 20,400; v2.2 added 9 new eligible ids (one had previous review).
assert num_prev_reviewed==1
summary={'versao':'P3 v2.3','amostra_v2_2':72,'amostra_fora_fila_P3':68,'amostra_dentro_fila_P3':4,
 'decisoes_v2_2':108,'decisoes_v2_2_fora_fila_P3':98,'decisoes_dentro_P3':10,
 'reversoes_de_escopo':98,'correcoes_de_intencao_dentro_P3':2,'patches_total':100,
 'QA_P3_elegiveis':10,'P3_fora_dos_pilotos_estimado':20400-9,'P2_pendentes':4660,
 'base':294905,'controles':2190,'lotes':30,
 'ressalva':'Reversão comparada à v2.1; out-of-scope quarantined. Indicador P3 fora dos pilotos estimado a partir do histórico 20.400 e 9 novos IDs elegíveis.'}
(OUT/'p3-v2.3-resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
