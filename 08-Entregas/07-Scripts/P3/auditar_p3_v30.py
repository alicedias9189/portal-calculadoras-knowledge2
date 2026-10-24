#!/usr/bin/env python3
# coding: utf-8
"""P3 v3.0: expansão conservadora de 36 IDs ELEGÍVEIS, a partir da v2.9.
Executar: python 07-Scripts/P3/auditar_p3_v30.py
Usa apenas a biblioteca padrão. Confere ambas as filas, metadata, escopo, base e controles.
Não edita fontes, controles, dados do Google Ads nem 98 propostas globais.
"""
import csv, io, json, zipfile, collections, hashlib, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'08-Entregas/P3-v3.0/FONTES-REPRODUCAO/08-Entregas/P3-v2.9'
OUT=ROOT/'08-Entregas/P3-v3.0'; OUT.mkdir(parents=True,exist_ok=True)
ALLOWED={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','dominio_ou_grandeza','unidade_origem','unidade_destino','direcao_conversao','confianca','revisao_manual','justificativa_curta'}
ADDED=['status_p3_v3_0','regra_p3_v3_0','parecer_p3_v3_0','justificativa_p3_v3_0','area_final_p3_v3_0','cluster_final_p3_v3_0','subcluster_final_p3_v3_0','tipo_intencao_final_p3_v3_0','classificacao_alterada_p3_v3_0']
# Estes IDs provêm de 36 leituras textuais específicas, sem expansão de regex.
FAMILIES={
 'BASES_OCTAL_DECIMAL': ['32825','34693','35882','38348','128349','195244'],
 'BASES_GENERICA': ['110176'],
 'BASES_HEXA': ['37183'],
 'CAMBIO_PESOS_REAL': ['105024','109352','109353','109476','109488','109489'],
 'VELOCIDADE_INTERNET': ['35782','35783','44136','171606','291863','291868'],
 'TEMPERATURA_CONVERSOR': ['106920','108335','108336','111307'],
 'FINANCIAMENTO_VEICULO': ['174515','183879','275998','45636','57469','273333'],
 'ELETRICIDADE_KWH': ['80806','84147'],
 'MATEMATICA_POTENCIAS': ['82150','149789','207553','207567'],
}
BY_ID={id:rule for rule,ids in FAMILIES.items() for id in ids}
assert len(BY_ID)==36 and len(set(BY_ID))==36

def readcsv(path):
 with path.open(encoding='utf-8-sig',newline='') as f:
  rd=csv.DictReader(f,delimiter=';');return list(rd),list(rd.fieldnames)
def writecsv(path,rows,fields):
 with path.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,delimiter=';',extrasaction='ignore',lineterminator='\n');w.writeheader();w.writerows(rows)
def fromzip(z,name):
 txt=z.read(name).decode('utf-8-sig');r=csv.DictReader(io.StringIO(txt),delimiter=';');return list(r),list(r.fieldnames)
def tozip(rows,fields):
 b=io.StringIO(); w=csv.DictWriter(b,fieldnames=fields,delimiter=';',lineterminator='\n');w.writeheader();w.writerows(rows)
 return ('\ufeff'+b.getvalue()).encode('utf-8')

def proposal(r,rule):
 k=r['Keyword'].lower()
 c={'revisao_manual':'sim','confianca':'alta'}
 note='Revisão semântica P3 v3.0, por ID; homologação editorial pendente.'
 if rule=='BASES_OCTAL_DECIMAL':
  assert 'octal' in k and 'decimal' in k and 'calculadora' in k
  c.update(area_principal='Conversores',cluster='Sistemas numéricos',subcluster='Conversão entre bases numéricas',dominio_ou_grandeza='Sistemas numéricos',tipo_intencao='conversão contextual',intencao_principal='Converter bases: octal e decimal',justificativa_curta='Calculadora de conversão entre decimal e octal, não décimo terceiro salário. '+note)
  # Direção é expressa por "para", e não por simples concatenação.
  if 'decimal para octal' in k:
   c.update(unidade_origem='DEC',unidade_destino='OCT',direcao_conversao='DEC→OCT')
  elif 'octal para decimal' in k:
   c.update(unidade_origem='OCT',unidade_destino='DEC',direcao_conversao='OCT→DEC')
  else:raise AssertionError(k)
 elif rule=='BASES_GENERICA':
  assert k=='converter base numérica'
  c.update(area_principal='Conversores',cluster='Sistemas numéricos',subcluster='Conversão entre bases numéricas',dominio_ou_grandeza='Sistemas numéricos',tipo_intencao='conversão contextual',intencao_principal='Converter: base numérica não especificada',justificativa_curta='Conversão entre bases numéricas, sem bases e valor fornecidos. '+note)
 elif rule=='BASES_HEXA':
  assert k=='calculadora hexadecimal para decimal'
  c.update(area_principal='Conversores',cluster='Sistemas numéricos',subcluster='Conversão entre bases numéricas',dominio_ou_grandeza='Sistemas numéricos',tipo_intencao='conversão contextual',intencao_principal='Converter base: hexadecimal para decimal',unidade_origem='HEX',unidade_destino='DEC',direcao_conversao='HEX→DEC',justificativa_curta='Direção HEX→DEC explícita; não é apenas calculadora científica genérica. '+note)
 elif rule=='CAMBIO_PESOS_REAL':
  assert 'convers' in k and 'peso' in k and 'real' in k
  c.update(area_principal='Conversores',cluster='Moedas e câmbio',subcluster='Conversão entre moedas',dominio_ou_grandeza='Câmbio entre moedas',tipo_intencao='conversão contextual',intencao_principal='Converter moeda: peso latino-americano e real',justificativa_curta='Pesos chileno/colombiano e real são moedas, não densidade. Cotação depende da data; "x" não define direção. '+note)
  # Apenas o par de moedas pode ser inferido; a direção não é declarada.
 elif rule=='VELOCIDADE_INTERNET':
  assert 'velocidade' in k and 'internet' in k
  c.update(area_principal='Tecnologia',cluster='Internet e redes',subcluster='Medição de velocidade da internet',dominio_ou_grandeza='Velocidade de conexão e taxa de dados',tipo_intencao='cálculo contextual',intencao_principal='Medir/calcular velocidade de internet',confianca='média',justificativa_curta='Teste ou cálculo de velocidade de conexão, sem relação com poupança. Pode requerer medição ativa ou tamanho e tempo de transferência. '+note)
 elif rule=='TEMPERATURA_CONVERSOR':
  assert 'temperatura' in k or 'celsius' in k
  c.update(area_principal='Conversores',cluster='Temperatura',subcluster='Conversão de temperatura',dominio_ou_grandeza='Temperatura',tipo_intencao='conversão contextual',intencao_principal='Converter temperatura: escalas não especificadas',confianca='média',justificativa_curta='Busca por conversor de temperatura/Celsius; "Google" não indica câmbio ou arquivo. Escalas e valor ausentes. '+note)
 elif rule=='FINANCIAMENTO_VEICULO':
  assert 'veiculo' in k or 'carro' in k or 'veiculos' in k
  assert 'financiamento' in k or 'juros' in k or 'cdc' in k
  if 'calcular parcela' in k or 'calculo parcela' in k:
   tipo='simulação/projeção';sub='Simulação de parcelas de financiamento de veículos';intro='Simular: parcelas de financiamento de veículos'
  elif 'melhor banco' in k or k.startswith('taxa ') or k.startswith('juros '):
   tipo='informacional';sub='Taxas de financiamento de veículos';intro='Consultar informação: taxas de financiamento de veículos'
  else:
   tipo='informacional';sub='Juros compostos em financiamento de veículos';intro='Consultar informação: juros no financiamento de veículos'
  c.update(area_principal='Finanças',cluster='Crédito e financiamentos',subcluster=sub,dominio_ou_grandeza='Financiamento de veículos',tipo_intencao=tipo,intencao_principal=intro,confianca='média',justificativa_curta='Crédito para veículo, não rendimento de investimento; taxas e prazos não fornecidos e comparação depende de instituição e data. '+note)
 elif rule=='ELETRICIDADE_KWH':
  assert 'quilowatt' in k or 'kwh' in k
  if 'valor' in k:
   sub='Custo de consumo elétrico';tipo='informacional';it='Consultar explicação: custo de energia em kWh';cl='Custo de energia'
  else:
   sub='Energia consumida em kWh';tipo='informacional';it='Consultar explicação: cálculo de energia em kWh';cl='Consumo elétrico'
  c.update(area_principal='Energia',cluster=cl,subcluster=sub,dominio_ou_grandeza='Energia elétrica (kWh)',tipo_intencao=tipo,intencao_principal=it,confianca='média',justificativa_curta='Expressão "quilowatt-hora/kWh" ligada a energia, não operação com datas. Potência (kW), tempo (h) e tarifa precisam ser diferenciados. '+note)
 elif rule=='MATEMATICA_POTENCIAS':
  assert 'potencia' in k or 'potência' in k
  if 'exercicios' in k:
   tipo='informacional';it='Consultar exercícios: propriedades da potenciação';sub='Potenciação e propriedades'
  elif 'como calcular' in k:
   tipo='informacional';it='Consultar método: potenciação de monômios';sub='Potenciação e propriedades'
  else:
   tipo='informacional';it='Consultar conceito: potências e expoentes';sub='Potenciação e propriedades'
  c.update(area_principal='Matemática',cluster='Potências e funções',subcluster=sub,dominio_ou_grandeza='Potenciação algébrica',tipo_intencao=tipo,intencao_principal=it,justificativa_curta='Potenciação matemática (expoentes/monômios), não potência/consumo de aparelhos elétricos. '+note)
 else:raise ValueError(rule)
 return c

p3,cols3=readcsv(SRC/'p3-v2.9-fila-23965.csv'); gen,colsg=readcsv(SRC/'fila-geral-p0-p1-p2-p3-v2.9.csv')
assert len(p3)==23965 and len(gen)==52046
idx3={r['id_global']:r for r in p3};idxg={r['id_global']:r for r in gen}
assert len(idx3)==len(p3) and len(idxg)==len(gen)
statuscols=[x for x in cols3 if x.startswith('status_p3_')]
def pending(row):
 return row['status_p3_v1']=='FORA_DO_PILOTO' and not any(row[x] for x in statuscols if x!='status_p3_v1')
assert sum(pending(r) for r in p3)==20308
for id,rule in BY_ID.items():
 assert id in idx3 and id in idxg,('fora do escopo',id)
 a,b=idx3[id],idxg[id]
 assert a['prioridade']==b['prioridade']=='P3' and pending(a) and pending(b),(id,'já pilotado')
 assert (a['Keyword'],a['familia_id'],a['lote'])==(b['Keyword'],b['familia_id'],b['lote']),(id,'metadados divergentes')
 assert rule in FAMILIES

# 30 lotes, fonte única para os valores antes/depois; controle estrito de escopo
infiles=[];bases=controls=0;found={}
with zipfile.ZipFile(SRC/'lotes-001-a-030-p3-v2.9.zip') as za:
 assert za.testzip() is None and len(za.namelist())==30
 for name in za.namelist():
  rows,fields=fromzip(za,name); infiles.append((name,rows,fields))
  for row in rows:
   if row['tipo_registro']=='base':
    bases+=1
    id=row['id_global']
    if id in BY_ID:
     assert id not in found and row['Keyword']==idx3[id]['Keyword'] and row['familia_id']==idx3[id]['familia_id'],id
     assert row['lote_id'].lstrip('L0')==idx3[id]['lote'].lstrip('0'),(id,row['lote_id'],idx3[id]['lote'])
     found[id]=(name,row)
   else:controls+=1
assert (bases,controls)==(294905,2190) and set(found)==set(BY_ID)

proposed={}; patches=[]; decisions=[];qa=[]
for id in sorted(BY_ID,key=int):
 rule=BY_ID[id];fname,old=found[id]; new=dict(old);new.update(proposal(old,rule))
 changed=[f for f in old if old[f]!=new[f]]
 assert changed and set(changed)<=ALLOWED,(id,changed)
 proposed[id]=new
 note=proposal(old,rule)['justificativa_curta']
 item={'id_global':id,'lote':idx3[id]['lote'],'familia_id':old['familia_id'],'Keyword':old['Keyword'],'regra':'P3V30_'+rule,'justificativa':note,'confianca_proposta':new['confianca'],'area_anterior':old['area_principal'],'cluster_anterior':old['cluster'],'subcluster_anterior':old['subcluster'],'tipo_anterior':old['tipo_intencao'],'area_proposta':new['area_principal'],'cluster_proposto':new['cluster'],'subcluster_proposto':new['subcluster'],'tipo_proposto':new['tipo_intencao'],'revisao_editorial_final':'pendente'}
 decisions.append(item)
 qa.append({'id_global':id,'Keyword':old['Keyword'],'regra':item['regra'],'parecer_tecnico':'PROPOSTA_COM_RESSALVA' if new['confianca']=='média' else 'PROPOSTA_CLARA','risco_residual':('Termo incompleto; não preencher variáveis ausentes nem simular preços/taxas reais.' if new['confianca']=='média' else 'Validar taxonomia final editorialmente.'),'validacao_de_escopo':'AUTORIZADO_P3'})
 patches.append({'id_global':id,'lote':fname,'familia_id':old['familia_id'],'Keyword':old['Keyword'],'regra':item['regra'],'campos_modificados':','.join(changed),'antes_json':json.dumps({f:old[f] for f in changed},sort_keys=True,ensure_ascii=False),'depois_json':json.dumps({f:new[f] for f in changed},sort_keys=True,ensure_ascii=False)})
writecsv(OUT/'p3-v3.0-decisoes.csv',decisions,list(decisions[0]))
writecsv(OUT/'p3-v3.0-revisao-qa-36.csv',qa,list(qa[0]))
writecsv(OUT/'p3-v3.0-patches.csv',patches,list(patches[0]))

reg=[]
with zipfile.ZipFile(OUT/'lotes-001-a-030-p3-v3.0.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zb:
 for oldname,rows,fields in infiles:
  altered=0;ctrl=base=0;out=[]
  for row in rows:
   if row['tipo_registro']=='base':base+=1
   else:ctrl+=1
   new=proposed.get(row['id_global'],row)
   if new!=row:altered+=1;assert row['tipo_registro']=='base'
   out.append(new)
  zb.writestr(oldname.replace('v2.9','v3.0'),tozip(out,fields))
  reg.append({'lote':oldname,'base':base,'controles':ctrl,'patches':altered,'status':'PASSOU'})
assert sum(int(r['patches']) for r in reg)==len(BY_ID)
writecsv(OUT/'p3-v3.0-regressao-30-lotes.csv',reg,list(reg[0]))

# Entradas antigas são copiadas campo a campo; APENAS novas colunas no fim
assert not(set(ADDED)&set(cols3)) and not(set(ADDED)&set(colsg))
for rows,columns,filename,expected in [(p3,cols3,'p3-v3.0-fila-23965.csv',23965),(gen,colsg,'fila-geral-p0-p1-p2-p3-v3.0.csv',52046)]:
 assert len(rows)==expected
 processed=[]
 for r in rows:
  id=r['id_global'];record=dict(r)
  if id in proposed:
   old=found[id][1];new=proposed[id]
   v={'status_p3_v3_0':'REVISADO','regra_p3_v3_0':'P3V30_'+BY_ID[id],'parecer_p3_v3_0':'PROPOSTA_COM_RESSALVA' if new['confianca']=='média' else 'PROPOSTA_CLARA','justificativa_p3_v3_0':new['justificativa_curta'],'area_final_p3_v3_0':new['area_principal'],'cluster_final_p3_v3_0':new['cluster'],'subcluster_final_p3_v3_0':new['subcluster'],'tipo_intencao_final_p3_v3_0':new['tipo_intencao'],'classificacao_alterada_p3_v3_0':'sim'}
  else:v=dict.fromkeys(ADDED,'')
  record.update(v);processed.append(record)
 writecsv(OUT/filename,processed,columns+ADDED)

# Quarentena global permanece byte a byte idêntica
srcglob=SRC/'backlog-global-98-com-parecer-v27.csv'; assert srcglob.exists()
(OUT/srcglob.name).write_bytes(srcglob.read_bytes())

tests=[]
def test(title,condition,actual):
 assert condition,title;tests.append({'teste':title,'resultado':actual,'status':'PASSOU'})
test('Exatamente 36 IDs exclusivos',len(BY_ID)==36 and len(set(BY_ID))==36,str(len(BY_ID)))
test('Interseção com fila P3 e fila geral',all(id in idx3 and id in idxg for id in BY_ID),'36/36')
test('Somente P3 fora dos pilotos',all(pending(idx3[id]) and pending(idxg[id]) for id in BY_ID),'36/36')
with srcglob.open(encoding='utf-8-sig',newline='') as f: globalids={r['id_global'] for r in csv.DictReader(f,delimiter=';')}
test('98 IDs globais bloqueados',len(globalids)==98 and not(globalids&set(BY_ID)),'98 bloqueados')
p2=[r for r in gen if r['prioridade']=='P2']
test('P2 não alterada',not any(r['id_global'] in BY_ID for r in p2),'zero P2')
test('IDs repetidos bloqueados',len(BY_ID)==len(set(BY_ID)),'sem repetição')
test('Volume base e controles',bases==294905 and controls==2190,'294905 + 2190')
writecsv(OUT/'p3-v3.0-testes-escopo.csv',tests,list(tests[0]))
summary={'versao':'P3 v3.0','novos_ajustes':len(BY_ID),'familias':len({r['familia_id'] for r in decisions}),'regras':dict(collections.Counter(r['regra'] for r in decisions)),'fora_do_piloto_antes':20308,'fora_do_piloto_depois':20308-len(BY_ID),'P2_pendentes':4660,'globais_separados':98,'base':bases,'controles':controls,'lotes':30,'elegibilidade':'intersecao das filas P3 e geral + metadados + status FORA_DO_PILOTO sem revisao posterior','homologacao':'pendente'}
(OUT/'p3-v3.0-resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
