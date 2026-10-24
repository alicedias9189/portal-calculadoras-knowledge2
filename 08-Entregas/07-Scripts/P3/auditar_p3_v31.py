#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Revisão crítica P3 v3.1. Executar a partir de qualquer pasta:
python 07-Scripts/P3/auditar_p3_v31.py
Usa fontes integralmente incluídas nesta entrega. Python stdlib.
Somente 8 refinamentos por ID, todos estritamente contidos nas 36 decisões da v3.0.
"""
from pathlib import Path
import csv,io,zipfile,json,collections,hashlib
ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'08-Entregas/P3-v3.1/FONTES-REPRODUCAO/08-Entregas/P3-v3.0'
OUT=ROOT/'08-Entregas/P3-v3.1';OUT.mkdir(parents=True,exist_ok=True)
ALLOWED={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','dominio_ou_grandeza','unidade_origem','unidade_destino','direcao_conversao','confianca','revisao_manual','justificativa_curta'}
ADDED=['status_p3_v3_1','parecer_p3_v3_1','justificativa_p3_v3_1','area_final_p3_v3_1','cluster_final_p3_v3_1','subcluster_final_p3_v3_1','tipo_intencao_final_p3_v3_1','classificacao_alterada_p3_v3_1']
NET={'35782','35783','44136','171606','291863','291868'}
FIN={'174515','183879'}
FIXED=NET|FIN
assert len(FIXED)==8

def read_csv(path):
 with path.open(encoding='utf-8-sig',newline='') as f:
  rd=csv.DictReader(f,delimiter=';');return list(rd),list(rd.fieldnames)
def read_zip_csv(z,name):
 with io.StringIO(z.read(name).decode('utf-8-sig')) as f:
  rd=csv.DictReader(f,delimiter=';');return list(rd),list(rd.fieldnames)
def dump_csv(rows,fields):
 b=io.StringIO();w=csv.DictWriter(b,delimiter=';',fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows);return ('\ufeff'+b.getvalue()).encode('utf-8')
def write_csv(path,rows,fields):
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_bytes(dump_csv(rows,fields))

def proposal(old):
 rid=old['id_global'];r=old.copy()
 if rid in NET:
  assert 'internet' in old['Keyword'].lower() and 'velocidade' in old['Keyword'].lower()
  r.update(subcluster='Velocidade da internet — teste ou cálculo não especificado',
   intencao_principal='Verificar ou calcular velocidade de internet (método não informado)',
   confianca='média',revisao_manual='sim',
   justificativa_curta='A busca não distingue teste ativo de conexão e cálculo com dados de transferência. Não presumir disponibilidade de medição real. P3 v3.1; revisão editorial ainda pendente.')
  return r,'REFINAR_METODO_INTERNET','A keyword não informa se o usuário quer teste de velocidade ou calculadora com tamanho/tempo de arquivo.'
 if rid=='174515':
  assert old['Keyword']=='juros compostos financiamento veiculo'
  r.update(subcluster='Juros compostos em financiamento de veículos',
   intencao_principal='Consultar explicação: juros compostos em financiamento de veículos',
   justificativa_curta='O termo juros compostos identifica tema de cálculo de encargos, não taxa anunciada. Em financiamento, distinguir método de amortização, CET e taxa nominal. P3 v3.1; homologação pendente.',revisao_manual='sim')
  return r,'REFINAR_JUROS_COMPOSTOS_VEICULO','Juros compostos não é sinônimo de busca por melhor taxa divulgada.'
 if rid=='183879':
  assert old['Keyword']=='melhor banco para financiamento veiculo'
  r.update(subcluster='Comparação de instituições para financiamento de veículos',
   intencao_principal='Comparar instituições de financiamento de veículos',
   justificativa_curta='Melhor banco envolve critérios de comparação (CET, prazos, condições e instituição) e não apenas taxas. Nenhuma instituição é recomendada pela keyword. P3 v3.1; homologação pendente.',revisao_manual='sim')
  return r,'REFINAR_COMPARACAO_BANCOS_VEICULO','Busca por comparação de bancos, com critérios não especificados.'
 raise AssertionError(rid)

def assessment(d):
 id=d['id_global'];k=d['Keyword'];rule=d['regra']
 if id in FIXED:
  n= 'Internet: método de verificação indefinido.' if id in NET else ('Crédito: juros compostos não significa cotação de taxa.' if id=='174515' else 'Crédito: comparação de bancos não equivale apenas a juros.')
  return 'CORRIGIDO',n
 if rule in ['P3V30_BASES_OCTAL_DECIMAL','P3V30_BASES_HEXA']:
  return 'MANTIDO_COM_RESSALVA','Par de bases e direção para explícitos; não inferir operando a converter.'
 if rule=='P3V30_BASES_GENERICA':
  return 'MANTIDO_COM_RESSALVA','Bases numéricas e valor ainda não definidos.'
 if rule=='P3V30_CAMBIO_PESOS_REAL':
  return 'MANTIDO_COM_RESSALVA','Peso chileno/colombiano e real identificados; quando falta PARA, manter direção vazia e não inventar cotação.'
 if rule=='P3V30_TEMPERATURA_CONVERSOR':
  return 'MANTIDO_COM_RESSALVA','Domínio temperatura correto; Google/online pode indicar busca de ferramenta, e faltam escalas ou valor.'
 if rule=='P3V30_FINANCIAMENTO_VEICULO':
  return 'MANTIDO_COM_RESSALVA','Parcelas são simuláveis somente com valor, juros, prazo e sistema de amortização; taxa não deve ser inventada.'
 if rule=='P3V30_ELETRICIDADE_KWH':
  return 'MANTIDO_COM_RESSALVA','kWh é energia; potência (kW), duração (h) e tarifa (R$/kWh) são coisas diferentes.'
 if rule=='P3V30_MATEMATICA_POTENCIAS':
  return 'MANTIDO_COM_RESSALVA','Potenciação matemática, não elétrica; distinguir pedido de conceito, exercício e cálculo com operandos.'
 raise AssertionError((id,rule))

p3,p3cols=read_csv(SRC/'p3-v3.0-fila-23965.csv'); general,gcols=read_csv(SRC/'fila-geral-p0-p1-p2-p3-v3.0.csv');dec,dcols=read_csv(SRC/'p3-v3.0-decisoes.csv')
assert len(p3)==23965 and len(general)==52046 and len(dec)==36
idxp={r['id_global']:r for r in p3};idxg={r['id_global']:r for r in general};ixd={r['id_global']:r for r in dec}
assert len(idxp)==len(p3) and len(idxg)==len(general) and len(ixd)==36
assert FIXED.issubset(ixd)
for rid in ixd:
 assert rid in idxp and rid in idxg,(rid,'fora da fila P3')
 assert idxp[rid]['prioridade']==idxg[rid]['prioridade']=='P3'
 assert idxp[rid]['status_p3_v3_0']==idxg[rid]['status_p3_v3_0']=='REVISADO'
 assert idxp[rid]['Keyword']==idxg[rid]['Keyword']==ixd[rid]['Keyword']
 assert idxp[rid]['familia_id']==idxg[rid]['familia_id']==ixd[rid]['familia_id']

# Read 30 lots of v3.0, preserving every input row and protected value
infiles=[];refrows={};bases=controls=0
with zipfile.ZipFile(SRC/'lotes-001-a-030-p3-v3.0.zip') as za:
 assert za.testzip() is None and len(za.namelist())==30
 for name in za.namelist():
  rows,fields=read_zip_csv(za,name);infiles.append((name,rows,fields))
  for row in rows:
   if row['tipo_registro']=='base':
    bases+=1
    if row['id_global'] in ixd:
     rid=row['id_global'];assert rid not in refrows;assert row['Keyword']==ixd[rid]['Keyword'];assert row['familia_id']==ixd[rid]['familia_id']
     assert row['lote_id'].lstrip('L0')==ixd[rid]['lote'].lstrip('0')
     refrows[rid]=(name,row)
   else:controls+=1
assert bases==294905 and controls==2190 and set(refrows)==set(ixd)
# Global quarantine must not overlap revised IDs.
glob,glcols=read_csv(SRC/'backlog-global-98-com-parecer-v27.csv');gids={r['id_global'] for r in glob}
assert len(glob)==len(gids)==98 and not (gids & set(ixd))

patched={};patches=[];review=[]
for d in dec:
 rid=d['id_global'];name,old=refrows[rid]
 status,note=assessment(d)
 nr=old
 if rid in FIXED:
  nr,rule,why=proposal(old)
  fields=[f for f in old if old[f]!=nr[f]]
  assert fields and set(fields)<=ALLOWED,(rid,fields)
  patched[rid]=nr
  patches.append({'id_global':rid,'lote':name,'familia_id':old['familia_id'],'Keyword':old['Keyword'],
   'regra_qa':rule,'motivo':why,'campos_modificados':','.join(fields),
   'antes_json':json.dumps({f:old[f] for f in fields},ensure_ascii=False,sort_keys=True),
   'depois_json':json.dumps({f:nr[f] for f in fields},ensure_ascii=False,sort_keys=True)})
 review.append({**d,'parecer_p3_v3_1':status,'nota_critica_p3_v3_1':note,'mudou_p3_v3_1':'sim' if rid in FIXED else 'não',
  'subcluster_v3_0':old['subcluster'],'subcluster_v3_1':nr['subcluster'],
  'tipo_v3_0':old['tipo_intencao'],'tipo_v3_1':nr['tipo_intencao'],'editorial_final':'pendente'})
assert len(patches)==8 and len(review)==36
write_csv(OUT/'p3-v3.1-pareceres-36.csv',review,list(review[0]))
write_csv(OUT/'p3-v3.1-patches.csv',sorted(patches,key=lambda r:int(r['id_global'])),list(patches[0]))

reg=[]
with zipfile.ZipFile(OUT/'lotes-001-a-030-p3-v3.1.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zb:
 for oldname,rows,fields in infiles:
  changed=0;updated=[];nbase=nctrl=0
  for old in rows:
   new=patched.get(old['id_global'],old)
   if old['tipo_registro']=='base':nbase+=1
   else:nctrl+=1
   if new!=old:
    changed+=1; assert old['tipo_registro']=='base' and old['id_global'] in FIXED
   updated.append(new)
  zb.writestr(oldname.replace('v3.0','v3.1'),dump_csv(updated,fields))
  reg.append({'lote':oldname,'bases':nbase,'controles':nctrl,'patches':changed,'status':'PASSOU'})
assert sum(r['patches'] for r in reg)==8
write_csv(OUT/'p3-v3.1-regressao-30-lotes.csv',reg,list(reg[0]))

# Preserve entire old queue columns and append new metadata.
assert not set(ADDED).intersection(p3cols) and not set(ADDED).intersection(gcols)
for rows,cols,outname in [(p3,p3cols,'p3-v3.1-fila-23965.csv'),(general,gcols,'fila-geral-p0-p1-p2-p3-v3.1.csv')]:
 out=[]
 byrev={r['id_global']:r for r in review}
 for r in rows:
  nr=dict(r);rid=r['id_global'];new=patched.get(rid)
  if rid in ixd:
   dest=new or refrows[rid][1];qa=byrev[rid]
   vals={'status_p3_v3_1':'REVISADO' if rid in FIXED else 'PRESERVADO',
    'parecer_p3_v3_1':qa['parecer_p3_v3_1'],'justificativa_p3_v3_1':qa['nota_critica_p3_v3_1'],
    'area_final_p3_v3_1':dest['area_principal'],'cluster_final_p3_v3_1':dest['cluster'],
    'subcluster_final_p3_v3_1':dest['subcluster'],'tipo_intencao_final_p3_v3_1':dest['tipo_intencao'],
    'classificacao_alterada_p3_v3_1':'sim' if rid in FIXED else 'não'}
  else: vals=dict.fromkeys(ADDED,'')
  nr.update(vals);out.append(nr)
 write_csv(OUT/outname,out,cols+ADDED)
# Exact bytes for 98 global entries (no changes)
(OUT/'backlog-global-98-com-parecer-v27.csv').write_bytes((SRC/'backlog-global-98-com-parecer-v27.csv').read_bytes())
qa_summary=collections.Counter(x['parecer_p3_v3_1'] for x in review)
info={'versao':'P3 v3.1','auditoria_de_registros':36,'patches':8,'mantidos_com_ressalvas':qa_summary['MANTIDO_COM_RESSALVA'],
 'pareceres':dict(qa_summary),'regras_refinadas':dict(collections.Counter(x['regra_qa'] for x in patches)),
 'lotes':30,'bases':bases,'controles':controls,'fila_p3':len(p3),'fila_geral':len(general),
 'pendencias_p3_fora_dos_pilotos':20272,'pendencias_p2':4660,'quarentena_global':98,
 'escopo':'revisão de 36 decisões já classificadas; sem nova expansão','homologacao_editorial':'pendente'}
(OUT/'p3-v3.1-resumo.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(info,ensure_ascii=False))
