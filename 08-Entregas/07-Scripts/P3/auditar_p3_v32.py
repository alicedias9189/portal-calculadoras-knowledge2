#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P3 v3.2: expansão seletiva estrita, reexecutável apenas com FONTES-REPRODUCAO.
Uso: python 07-Scripts/P3/auditar_p3_v32.py
Não altera entradas; somente 68 IDs elegíveis, regras contextualizadas e auditáveis.
"""
from pathlib import Path
from collections import Counter, defaultdict
import csv, io, zipfile, json, re, unicodedata, hashlib
ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'08-Entregas/P3-v3.2/FONTES-REPRODUCAO/08-Entregas/P3-v3.1'
OUT=ROOT/'08-Entregas/P3-v3.2';OUT.mkdir(parents=True,exist_ok=True)
ALLOWED={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','dominio_ou_grandeza','confianca','revisao_manual','justificativa_curta'}
ADDED=['status_p3_v3_2','regra_p3_v3_2','parecer_p3_v3_2','justificativa_p3_v3_2','area_final_p3_v3_2','cluster_final_p3_v3_2','subcluster_final_p3_v3_2','tipo_intencao_final_p3_v3_2','classificacao_alterada_p3_v3_2']
BASE_REMAIN=20272
EXPECTED={'HORAS_EXTRAS':32,'PAYBACK':18,'DIAS_EXCEL':9,'IPVA':7,'CARTAO':1,'ENERGIA':1}

def readcsv(path):
 with path.open(encoding='utf-8-sig',newline='') as f:
  d=csv.DictReader(f,delimiter=';');return list(d),list(d.fieldnames)
def zread(z,name):
 with io.StringIO(z.read(name).decode('utf-8-sig')) as f:
  d=csv.DictReader(f,delimiter=';');return list(d),list(d.fieldnames)
def csvbytes(rows,cols):
 b=io.StringIO();w=csv.DictWriter(b,delimiter=';',fieldnames=cols,lineterminator='\n');w.writeheader();w.writerows(rows);return ('\ufeff'+b.getvalue()).encode('utf-8')
def save(path,rows,cols):path.write_bytes(csvbytes(rows,cols))
def norm(s):return ''.join(x for x in unicodedata.normalize('NFKD',s.lower()) if not unicodedata.combining(x))

def match(q):
 k=norm(q['Keyword']);a=q['area']
 if 'payback' in k:return 'PAYBACK'
 if 'dias entre' in k and 'excel' in k and a!='Datas':return 'DIAS_EXCEL'
 if 'horas extras' in k and a!='Trabalho':return 'HORAS_EXTRAS'
 if 'ipva' in k and a!='Finanças':return 'IPVA'
 if k=='juros do cartao de credito como calcular':return 'CARTAO'
 if k=='preco kwh tarifa simples':return 'ENERGIA'
 return None

def proposal(old,code):
 k=norm(old['Keyword']);r=old.copy();tipo='informacional';conf='alta'
 if code=='PAYBACK':
  area='Finanças';cluster='Investimentos';sub='Payback descontado' if 'descontado' in k else ('VPL, TIR e payback' if 'vpl' in k else 'Payback e retorno do investimento')
  if any(x in k for x in ['calculadora','calculo','calcule','calcular vpl']) and not any(x in k for x in ['como calcular','como fazer']): tipo='cálculo contextual'
  if 'hp12c' in k:tipo='informacional'
  note='Payback é período de retorno de investimento; fluxo de caixa, aporte e, no descontado, taxa de desconto são necessários. Não presumir resultados.'
 elif code=='DIAS_EXCEL':
  area='Datas';cluster='Intervalos';sub='Diferença entre datas no Excel'
  tipo='informacional' if 'como calcular' in k else 'cálculo contextual'
  note='Operação de diferença entre datas ou instrução no Excel. Datas concretas não foram fornecidas; não tratar como estatística nem construção.'
 elif code=='HORAS_EXTRAS':
  area='Trabalho';cluster='Jornada e adicionais';sub='Horas extras e apuração'
  if any(x in k for x in ['repouso','descanso remunerado','reflexos']):sub='DSR e reflexos de horas extras'
  if any(x in k for x in ['media de horas extras','média de horas extras','valor medio de horas extras']):sub='Média de horas extras'
  if any(x in k for x in ['planilha','tabela de controle','modelo de controle','controle de ponto','ferramenta de verificacao']):sub='Controle e planilhas de horas extras';tipo='informacional'
  elif any(x in k for x in ['permitidas','acima de 2 horas']):sub='Limites e regras de horas extras';tipo='informacional'
  elif any(x in k for x in ['como calcular','como somar','passo a passo']):tipo='informacional'
  elif any(x in k for x in ['calcular','calculo','contagem','porcentagem']):tipo='cálculo contextual'
  else:tipo='informacional'
  note='Horas extras têm contexto trabalhista. Percentuais, direitos e reflexos dependem de jornada, norma e período; planilhas/modelos não são cálculo instantâneo.'
 elif code=='IPVA':
  area='Finanças';cluster='Tributos';sub='IPVA — parcelamento e consulta'
  if 'quanto vou pagar' in k:sub='IPVA — cálculo contextual';tipo='cálculo contextual'
  elif 'final 5' in k:sub='Calendário de pagamento do IPVA'
  elif k=='ipva 22':sub='IPVA — referência temporal ambígua';conf='média'
  note='IPVA é imposto sobre propriedade de veículo, não benefício trabalhista, gestação ou promoção. Estado, exercício e base tributária não foram informados.'
 elif code=='CARTAO':
  area='Finanças';cluster='Dívidas e cartões';sub='Cálculo de juros de cartão de crédito';tipo='informacional'
  note='A busca pede explicação de como calcular juros de cartão; sem fatura, taxa, dias e modalidade não há resultado numérico.'
 elif code=='ENERGIA':
  area='Energia';cluster='Custos e tarifas';sub='Preço da energia por kWh';tipo='informacional'
  note='Preço de kWh é tarifa elétrica, não juros simples. Valor depende de concessionária, período, bandeira, tributos e classe.'
 else:raise ValueError(code)
 r.update(area_principal=area,cluster=cluster,subcluster=sub,dominio_ou_grandeza=sub,tipo_intencao=tipo,
  intencao_principal={'informacional':'Consultar informação: ','cálculo contextual':'Calcular com contexto: '}[tipo]+sub,
  confianca=conf,revisao_manual='sim',justificativa_curta=note+' (P3 v3.2; homologação editorial pendente.)')
 return r,note

queue,qcols=readcsv(SRC/'p3-v3.1-fila-23965.csv');general,gcols=readcsv(SRC/'fila-geral-p0-p1-p2-p3-v3.1.csv');global98,xcols=readcsv(SRC/'backlog-global-98-com-parecer-v27.csv')
assert len(queue)==23965 and len(general)==52046 and len(global98)==98
indexed={r['id_global']:r for r in general};globids={r['id_global'] for r in global98}
assert len(indexed)==len(general) and len(globids)==98
hist=[k for k in qcols if k.startswith('status_p3_') and k!='status_p3_v1']
remaining=[r for r in queue if r['status_p3_v1']=='FORA_DO_PILOTO' and not any(r[k] for k in hist)]
assert len(remaining)==BASE_REMAIN,('contagem historica',len(remaining))
sel={r['id_global']:match(r) for r in remaining if match(r)}
counts=Counter(sel.values());assert dict(counts)==EXPECTED,(counts,EXPECTED)
assert len(sel)==68 and not (set(sel)&globids)
for r in remaining:
 rid=r['id_global']
 if rid not in sel:continue
 other=indexed.get(rid)
 assert other and r['prioridade']==other['prioridade']=='P3'
 assert (r['Keyword'],r['familia_id'],r['lote'])==(other['Keyword'],other['familia_id'],other['lote'])

oldzip=SRC/'lotes-001-a-030-p3-v3.1.zip'
source={};totalbase=totalctrl=0
with zipfile.ZipFile(oldzip) as za:
 assert len(za.namelist())==30 and za.testzip() is None
 for name in za.namelist():
  rows,cols=zread(za,name)
  for r in rows:
   if r['tipo_registro']=='base':
    totalbase+=1
    if r['id_global'] in sel:
     rid=r['id_global'];assert rid not in source;source[rid]=(name,r)
   else:totalctrl+=1
assert totalbase==294905 and totalctrl==2190 and len(source)==68

selectedq={r['id_global']:r for r in remaining if r['id_global'] in sel}
patches=[];decisions=[];updated={}
for rid,code in sorted(sel.items(),key=lambda x:int(x[0])):
 name,old=source[rid];qr=selectedq[rid]
 assert old['Keyword']==qr['Keyword'] and old['familia_id']==qr['familia_id']
 assert old['lote_id'].lstrip('L0')==qr['lote'].lstrip('L0'),(rid,qr['lote'],old['lote_id'])
 new,note=proposal(old,code);diff=[f for f in old if old[f]!=new[f]]
 assert diff and set(diff)<=ALLOWED,(rid,diff)
 updated[rid]=new
 decisions.append({'id_global':rid,'lote':name,'familia_id':qr['familia_id'],'Keyword':qr['Keyword'],'regra':'P3V32_'+code,
   'parecer_qa':'CLASSIFICADO_COM_RESSALVA' if new['confianca']=='média' else 'CLASSIFICADO_CONTEXTUALMENTE',
   'area_anterior':old['area_principal'],'cluster_anterior':old['cluster'],'subcluster_anterior':old['subcluster'],
   'area_nova':new['area_principal'],'cluster_novo':new['cluster'],'subcluster_novo':new['subcluster'],
   'tipo_anterior':old['tipo_intencao'],'tipo_novo':new['tipo_intencao'],'justificativa':note,'homologacao_editorial':'pendente'})
 patches.append({'id_global':rid,'lote':name,'familia_id':old['familia_id'],'Keyword':old['Keyword'],'regra':'P3V32_'+code,
  'campos_modificados':','.join(diff),'antes_json':json.dumps({f:old[f] for f in diff},ensure_ascii=False,sort_keys=True),
  'depois_json':json.dumps({f:new[f] for f in diff},ensure_ascii=False,sort_keys=True)})

save(OUT/'p3-v3.2-decisoes-68.csv',decisions,list(decisions[0]));save(OUT/'p3-v3.2-patches.csv',patches,list(patches[0]))
# QA sampled across entire selection (fully enumerated)
# Analyze previous review refinements rate strictly as signal, not FP population estimate.
prevprev,pcols=readcsv(SRC/'p3-v3.1-pareceres-36.csv')
byrule=defaultdict(lambda:Counter())
for r in prevprev:byrule[r['regra']][r['parecer_p3_v3_1']]+=1
ruleqa=[]
for rule,cts in sorted(byrule.items()):
 corrected=cts['CORRIGIDO'];sample_size=sum(cts.values())
 ruleqa.append({'regra_v3_0':rule,'registros_revisados':sample_size,'refinamentos_v3_1':corrected,
    'taxa_refinamentos_pct':f'{corrected*100/sample_size:.2f}',
    'interpretacao':'Frequência de refinamento, não estimativa amostral representativa de falsos positivos'})
save(OUT/'p3-v3.2-qa-regras-anteriores.csv',ruleqa,list(ruleqa[0]))

reg=[]
with zipfile.ZipFile(oldzip) as za,zipfile.ZipFile(OUT/'lotes-001-a-030-p3-v3.2.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zb:
 for oldname in za.namelist():
  rows,cols=zread(za,oldname);nbase=nctrl=changed=0;out=[]
  for r in rows:
   nr=updated.get(r['id_global'],r)
   if r['tipo_registro']=='base':nbase+=1
   else:nctrl+=1
   if nr!=r:
    assert r['tipo_registro']=='base' and r['id_global'] in sel
    changed+=1
   out.append(nr)
  zb.writestr(oldname.replace('v3.1','v3.2'),csvbytes(out,cols))
  reg.append({'lote':oldname,'bases':nbase,'controles':nctrl,'patches':changed,'status':'PASSOU'})
assert sum(r['patches'] for r in reg)==68
save(OUT/'p3-v3.2-regressao-30-lotes.csv',reg,list(reg[0]))

bydec={d['id_global']:d for d in decisions}
for rows,cols,dest in [(queue,qcols,'p3-v3.2-fila-23965.csv'),(general,gcols,'fila-geral-p0-p1-p2-p3-v3.2.csv')]:
 assert not set(cols)&set(ADDED)
 out=[]
 for r in rows:
  d=bydec.get(r['id_global']);z=dict(r)
  if d:
   nr=updated[r['id_global']]
   newvals={'status_p3_v3_2':'REVISADO','regra_p3_v3_2':d['regra'],'parecer_p3_v3_2':d['parecer_qa'],
    'justificativa_p3_v3_2':d['justificativa'],'area_final_p3_v3_2':nr['area_principal'],
    'cluster_final_p3_v3_2':nr['cluster'],'subcluster_final_p3_v3_2':nr['subcluster'],
    'tipo_intencao_final_p3_v3_2':nr['tipo_intencao'],'classificacao_alterada_p3_v3_2':'sim'}
  else:newvals=dict.fromkeys(ADDED,'')
  z.update(newvals);out.append(z)
 save(OUT/dest,out,cols+ADDED)
(OUT/'backlog-global-98-com-parecer-v27.csv').write_bytes((SRC/'backlog-global-98-com-parecer-v27.csv').read_bytes())

info={'versao':'P3 v3.2','status':'AUDITORIA_EXECUTADA','total_decisoes':len(decisions),'familias':len({d['familia_id'] for d in decisions}),
 'por_regra':dict(sorted(counts.items())),'lotes':30,'bases':totalbase,'controles':totalctrl,
 'fila_p3':len(queue),'fila_geral':len(general),'p3_fora_dos_pilotos_antes':BASE_REMAIN,
 'p3_fora_dos_pilotos_depois':BASE_REMAIN-len(sel),'p2_pendentes':4660,'global_fora_prioridades':len(global98),
 'qa_regra_anterior':'taxa de refinamento observada, sem estimar falsos positivos da população',
 'homologacao_editorial':'pendente'}
(OUT/'p3-v3.2-resumo.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(info,ensure_ascii=False))
