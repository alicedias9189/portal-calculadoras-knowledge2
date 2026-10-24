#!/usr/bin/env python3
# coding: utf-8
"""P3 v2.8: expansão seletiva com validação de escopo antes da aplicação.
Execução reproduzível: colocar este script sob 07-Scripts/P3 e os fontes
no diretório FONTES-REPRODUCAO/08-Entregas/P3-v2.7 do próprio pacote.
A fonte v2.7 é IMUTÁVEL, o destino v2.8 é gerado paralelamente.
Dependências: Python 3.10+ stdlib.
"""
import csv, io, json, zipfile, hashlib, re, unicodedata, collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'08-Entregas/P3-v2.8/FONTES-REPRODUCAO/08-Entregas/P3-v2.7'
OUT=ROOT/'08-Entregas/P3-v2.8';OUT.mkdir(parents=True,exist_ok=True)
ALLOWED={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','dominio_ou_grandeza','confianca','revisao_manual','justificativa_curta'}
HIST_VER=['status_p3_v1_3','status_p3_v1_4','status_p3_v1_5','status_p3_v1_6','status_p3_v1_8','status_p3_v2_0','status_p3_v2_2','status_p3_v2_6']
NEW=['status_p3_v2_8','regra_p3_v2_8','justificativa_p3_v2_8','area_final_p3_v2_8','cluster_final_p3_v2_8','subcluster_final_p3_v2_8','tipo_intencao_final_p3_v2_8','classificacao_alterada_p3_v2_8']

def getcsv(p):
 with p.open(encoding='utf-8-sig',newline='') as f:
  dr=csv.DictReader(f,delimiter=';');return list(dr),dr.fieldnames

def putcsv(p,rows,columns):
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=columns,delimiter=';',lineterminator='\n',extrasaction='ignore');w.writeheader();w.writerows(rows)

def norm(t):return ''.join(c for c in unicodedata.normalize('NFKD',t.lower()) if not unicodedata.combining(c))
def contains(k,s):return bool(re.search(r'\b'+re.escape(s)+r'\b',k))

def assess(r):
 k=norm(r['Keyword']);a=r['area_principal'];c=r['cluster'];sub=r['subcluster'];tipo=r['tipo_intencao']
 # IMPORTANT: never infer a missing original slash or number from removed punctuation.
 # bases explicitly stated; binary "subtração" and decimal comma are excluded unless conversion intent explicit.
 if contains(k,'binario') or contains(k,'binarios'):
  if ('base 36' in k or (('decimal' in k) and ('convers' in k or 'para' in k or 'calculadora binario decimal' in k))) and ('subtracao' not in k):
   if (a!='Conversores' or c!='Sistemas numéricos' or 'bases' not in norm(sub)):
    return ('P3V28_BASES_NUMERICAS','Conversores','Sistemas numéricos','Conversão entre bases numéricas','Sistemas numéricos','conversão contextual','Recurso para conversão entre bases numéricas declaradas; não completar números ausentes.','média')
 if 'fahrenheit' in k and 'celsius' in k and c!='Temperatura':
  return ('P3V28_CELSIUS_FAHRENHEIT','Conversores','Temperatura','Celsius e Fahrenheit','Temperatura','conversão contextual','Ambas as escalas estão explícitas; direção não especificada, não inventar unidade de origem.','alta')
 if 'inss' in k and ('obra' in k or 'construcao civil' in k) and sub!='INSS e regularização de obra':
  intent='informacional' if 'aliquota' in k else ('simulação/projeção' if 'simulacao' in k else 'cálculo contextual')
  return ('P3V28_INSS_OBRA','Construção','Regularização de obra','INSS e regularização de obra','Regularização previdenciária de obra',intent,'INSS da construção civil não é custo solar, áudio, geometria ou área de piso. Valor depende das regras e parâmetros da obra.','média')
 # Automotive financing is not an investment return or a generic electricity/concrete topic.
 if 'financiamento' in k and ('veiculo' in k or 'veiculos' in k or 'carro' in k):
  if ('taxa' in k or 'juros' in k) and 'taxas indevidas' not in k and 'juros compostos' not in k:
   suspect=(a!='Finanças' or c in {'Investimentos','Juros','Correção monetária','Tributos'} or (c=='Crédito' and tipo=='simulação/projeção' and any(k.startswith(x) for x in ('taxa','taxas','qual','menor','melhor'))))
   if suspect:
    intent='informacional'
    if any(k.startswith(x) for x in ('calcular','calculadora','simulador','simulacao')): intent='cálculo contextual'
    return ('P3V28_TAXAS_VEICULOS','Finanças','Crédito e financiamentos','Taxas de financiamento de veículos','Crédito de veículo',intent,'Busca de taxa/juros de financiamento de veículo, não investimento nem simulação sem valores de principal/prazo. Não supor taxas bancárias vigentes.','média')
 # POWER (W) and ENERGY (kWh) cannot be converted without a duration. Explicitly not direct unit conversion.
 if 'kwh' in k and ('watts' in k or 'watt' in k) and ('convers' in k or 'transformar' in k):
  if sub!='Relação entre potência e energia (tempo necessário)':
   return ('P3V28_POTENCIA_ENERGIA','Conversores','Energia, potência e calor','Relação entre potência e energia (tempo necessário)','Energia e potência','conversão contextual','kWh é energia e W é potência; conversão requer intervalo de tempo e não é direta.','alta')
 if 'tempo' in k and ('km h' in k or 'km/h' in k) and ('viagem' in k or 'calcular tempo' in k) and c!='Tempo e velocidade':
  return ('P3V28_TEMPO_VIAGEM','Datas','Tempo e velocidade','Duração de viagem por distância/velocidade','Duração estimada','cálculo contextual','Tempo de viagem requer distância e velocidade; não é adição de datas.','média')
 if 'desvio padrao' in k and ('estatistica' in k or 'matematica' in k) and c not in ('Estatística descritiva','Estatística e probabilidade'):
  return ('P3V28_DESVIO_PADRAO','Matemática','Estatística descritiva','Variância e desvio padrão','Estatística descritiva','informacional','Consulta sobre desvio padrão é estatística, não aritmética básica.','alta')
 return None

p3,pc=getcsv(SRC/'p3-v2.7-fila-23965.csv')
general,gc=getcsv(SRC/'fila-geral-p0-p1-p2-p3-v2.7.csv')
assert len(p3)==23965 and len(general)==52046
assert not (set(NEW)&set(pc))
gen={r['id_global']:r for r in general}
prior={r['id_global']:r for r in p3}
assert len(gen)==52046 and len(prior)==23965
valid={id:r for id,r in prior.items() if r['prioridade']=='P3' and r['status_p3_v1']=='FORA_DO_PILOTO' and all(not r[f] for f in HIST_VER)}
assert len(valid)==20374,('eligibilidade deve ser recalculada após alterações de fonte',len(valid))
# candidate discovery by queue text; never authorize from words only.
candidates={id for id,r in valid.items() if ('inss' in norm(r['Keyword']) or 'binari' in norm(r['Keyword']) or 'fahrenheit' in norm(r['Keyword']) or 'financiamento' in norm(r['Keyword']) or 'kwh' in norm(r['Keyword']) or 'desvio' in norm(r['Keyword']) or 'km h' in norm(r['Keyword']))}
# Independently read lots, checking 34-column base and 30 lot filenames.
refs={};infiles=[];seen=set();total_base=total_ctrl=0
with zipfile.ZipFile(SRC/'lotes-001-a-030-p3-v2.7.zip') as z:
 assert z.testzip() is None and len(z.namelist())==30
 for fname in z.namelist():
  buf=z.read(fname).decode('utf-8-sig');reader=csv.DictReader(io.StringIO(buf),delimiter=';');ff=reader.fieldnames
  records=[]
  for r in reader:
   records.append(r)
   if r['tipo_registro']=='base':
    total_base+=1;assert r['id_global'] not in seen;seen.add(r['id_global'])
    if r['id_global'] in candidates: refs[r['id_global']]=(fname,r)
   else:total_ctrl+=1
  infiles.append((fname,ff,records))
assert (total_base,total_ctrl)==(294905,2190)
# Strict gate: P3 in both queues, exact id+keyword+family, and exact lot number.
rejections=[];approved=[];mod_byid={};decision_rows=[]
for id in sorted(candidates,key=int):
 queue=valid[id];reg=gen.get(id);lr=refs.get(id)
 fail=[]
 if not reg or reg['prioridade']!='P3':fail.append('NAO_P3_NA_FILA_GERAL')
 if not lr:fail.append('AUSENTE_NOS_LOTES')
 if reg and (reg['Keyword'],reg['familia_id'],reg['lote'])!=(queue['Keyword'],queue['familia_id'],queue['lote']):fail.append('DIVERGENCIA_FILA')
 if lr:
  filename,r=lr
  if (r['Keyword'],r['familia_id'])!=(queue['Keyword'],queue['familia_id']):fail.append('DIVERGENCIA_LOTE')
  if not filename.startswith('lotes/lote-'+queue['lote'].zfill(3)+'-'):fail.append('LOTE_DIVERGENTE')
 if fail:
  rejections.append({'id_global':id,'Keyword':queue['Keyword'],'motivo':'|'.join(fail)});continue
 res=assess(lr[1])
 if not res:continue
 rule,area,cluster,sub,domain,typ,why,confidence=res
 row=lr[1];new=row.copy();new.update({'area_principal':area,'cluster':cluster,'subcluster':sub,'dominio_ou_grandeza':domain,'tipo_intencao':typ,
 'intencao_principal':('Consultar informação: ' if typ=='informacional' else 'Converter com contexto: ' if 'conversão' in typ else 'Calcular com contexto: ' if typ=='cálculo contextual' else 'Simular: ')+sub,
 'confianca':confidence,'revisao_manual':'sim','justificativa_curta':why+' (P3 v2.8, revisão editorial pendente).'} )
 changed=[f for f in ff if f in ALLOWED and row[f]!=new[f]]
 if not changed:continue
 mod_byid[id]=new
 approved.append({'id_global':id,'lote':queue['lote'],'familia_id':queue['familia_id'],'Keyword':queue['Keyword'],'regra':rule,'parecer':'PROPOSTA_TECNICA_COM_RESSALVA','justificativa':why,'campos_modificados':','.join(changed),
 'antes_json':json.dumps({f:row[f] for f in changed},ensure_ascii=False,sort_keys=True),'depois_json':json.dumps({f:new[f] for f in changed},ensure_ascii=False,sort_keys=True)})
assert not rejections,('falha da seleção',rejections[:3])
assert 15<=len(approved)<=85,(len(approved),collections.Counter(r['regra'] for r in approved))
putcsv(OUT/'p3-v2.8-decisoes.csv',approved,list(approved[0]))
putcsv(OUT/'p3-v2.8-patches.csv',approved,list(approved[0]))
# QA covers EVERY new decision because this pilot is deliberately small.
review=[]
for d in approved:
  check=dict(d)
  check['qa_critica_p3_v2_8']='MANTER_COM_RESSALVA'
  check['nota_critica']='Regra aplicada com texto de keyword explícito; taxas, regimes, unidades e contextos ausentes não foram inventados. Revisão editorial final pendente.'
  if d['regra']=='P3V28_POTENCIA_ENERGIA':check['nota_critica']='Física dimensional: conversão W ↔ kWh requer duração em horas. Não usar multiplicação de unidade direta.'
  if d['regra']=='P3V28_BASES_NUMERICAS' and 'vírgula' in d['Keyword'].lower(): check['nota_critica']='Número em ponto fixo com vírgula requer parte fracionária; direção de conversão é textual, formato exato pode necessitar revisão.'
  review.append(check)
putcsv(OUT/'p3-v2.8-revisao-qa-integral.csv',review,list(review[0]))
# update full lot zip, never modify controls or protected columns
lot_stats=[]
with zipfile.ZipFile(OUT/'lotes-001-a-030-p3-v2.8.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=5) as zz:
 for fname,fields,rs in infiles:
  out=[];changes=0;ctr=0;b=0
  for r in rs:
   new=mod_byid.get(r['id_global'],r)
   if r['tipo_registro']=='base':b+=1
   else:ctr+=1;assert r is new
   delta={f for f in fields if r[f]!=new[f]};assert not delta or (r['id_global'] in mod_byid and delta<=ALLOWED)
   if delta:changes+=1
   out.append(new)
  output=io.StringIO();writer=csv.DictWriter(output,delimiter=';',fieldnames=fields,lineterminator='\n');writer.writeheader();writer.writerows(out)
  zz.writestr(fname.replace('v2.7','v2.8'),('\ufeff'+output.getvalue()).encode('utf-8'))
  lot_stats.append({'lote':fname,'base':b,'controles':ctr,'alteracoes':changes,'status':'PASSOU'})
assert sum(x['alteracoes'] for x in lot_stats)==len(approved)
putcsv(OUT/'p3-v2.8-regressao-30-lotes.csv',lot_stats,list(lot_stats[0]))
# new queue history only; keep all old values same
for source,dest,expected in [('p3-v2.7-fila-23965.csv','p3-v2.8-fila-23965.csv',23965),('fila-geral-p0-p1-p2-p3-v2.7.csv','fila-geral-p0-p1-p2-p3-v2.8.csv',52046)]:
 old,fields=getcsv(SRC/source);assert len(old)==expected
 for r in old:
  p=mod_byid.get(r['id_global']);q=dict.fromkeys(NEW,'')
  if p:
   res=next(d for d in approved if d['id_global']==r['id_global'])
   q={'status_p3_v2_8':'REVISADO','regra_p3_v2_8':res['regra'],'justificativa_p3_v2_8':res['justificativa'],'area_final_p3_v2_8':p['area_principal'],
      'cluster_final_p3_v2_8':p['cluster'],'subcluster_final_p3_v2_8':p['subcluster'],'tipo_intencao_final_p3_v2_8':p['tipo_intencao'],'classificacao_alterada_p3_v2_8':'sim'}
  r.update(q)
 putcsv(OUT/dest,old,fields+NEW)
# untouched global backlog, compare copied original bytes at packaging stage
counts=collections.Counter(x['regra'] for x in approved)
summary={'versao':'P3 v2.8','alteracoes':len(approved),'regras':dict(counts),'familias':len({x['familia_id'] for x in approved}),
 'qa_integral':len(review),'registros_base':total_base,'controles':total_ctrl,'lotes':len(lot_stats),'fila_P3':23965,'fila_geral':52046,
 'p3_fora_pilotos_reportados_v27':20383,'elegiveis_nao_classificados_reconciliados_v27':len(valid),
 'p3_elegiveis_nao_classificados_v28':len(valid)-len(approved),'divergencia_em_registro_historico':20383-len(valid),
 'p2_pendentes':4660,'propostas_globais_preservadas':98,'escopo':'Somente interseção validada P3; propostas globais bloqueadas','status':'SUJEITO_REGRESSAO_INDEPENDENTE'}
(OUT/'p3-v2.8-resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
