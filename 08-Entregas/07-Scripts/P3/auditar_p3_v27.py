#!/usr/bin/env python3
"""P3 v2.7 — revisão de 17 IDs elegíveis e 48 propostas globais B/C.
Reproduz pacotes a partir das quatro fontes v2.6 (somente Python stdlib).
Não altera fontes. Variação conservadora por ID. Executar a partir da raiz
contendo '08-Entregas/P3-v2.7/FONTES-REPRODUCAO/08-Entregas/P3-v2.6/'.
"""
import csv, io, json, pathlib, hashlib, zipfile, collections, re, unicodedata
ROOT=pathlib.Path(__file__).resolve().parents[2]
SRC=ROOT/'08-Entregas/P3-v2.7/FONTES-REPRODUCAO/08-Entregas/P3-v2.6'
OUT=ROOT/'08-Entregas/P3-v2.7'
OUT.mkdir(parents=True,exist_ok=True)
PROTECTED={'tipo_registro','id_global','lote_id','familia_id','controle_id','Keyword'}
ALLOWED={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','dominio_ou_grandeza','confianca','revisao_manual','justificativa_curta'}
CHANGE_ID='190795'

def read_csv(p):
 with p.open(encoding='utf-8-sig',newline='') as f:
  return list(csv.DictReader(f,delimiter=';'))
def getcols(p):
 with p.open(encoding='utf-8-sig',newline='') as f:
  return next(csv.reader(f,delimiter=';'))
def save_csv(p,rows,cols=None):
 p.parent.mkdir(parents=True,exist_ok=True)
 if cols is None:cols=list(rows[0])
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=cols,delimiter=';',lineterminator='\n');w.writeheader();w.writerows(rows)
def zrows(z,name):
 s=z.read(name).decode('utf-8-sig');rr=csv.DictReader(io.StringIO(s),delimiter=';');return list(rr),rr.fieldnames

def normalize(s):return ''.join(c for c in unicodedata.normalize('NFKD',s.lower()) if not unicodedata.combining(c))

def assess_global(r):
 k=normalize(r['Keyword']);rule=r['regra'];prior=r['faixa_prioridade_global'];notes=[]
 if rule=='P3V22_INSS_DESCONTO_INFO':
  if 'calculadora' in k:
   subtype='Ferramenta para desconto de INSS e IRPF';intent='cálculo contextual';status='REFINAR_PROPOSTA'
   notes.append('Busca pede calculadora de dois tributos; não limitar ao INSS.')
  elif 'consultar' in k:
   subtype='Consulta de descontos previdenciários';intent='navegacional/transacional';status='REFINAR_PROPOSTA'
   notes.append('Ação de consulta a serviço/registro; não cálculo do desconto.')
  elif 'como fazer' in k:
   subtype='Método de cálculo do desconto INSS';intent='informacional';status='MANTER_COM_RESSALVA'
   notes.append('Tutorial/explicação do desconto; valor depende da categoria e período.')
  else:
   subtype='Consulta sobre desconto previdenciário';intent='informacional';status='MANTER_COM_RESSALVA'
   notes.append('Informação sobre desconto em folha; não usar alíquota fixa.')
 elif rule=='P3V22_IRRF_BASE_FINANCAS':
  subtype='IRRF e base de cálculo de aluguel' if 'aluguel' in k else 'Tabela e base de cálculo de IRRF'
  if 'tabela' in k:
   intent='informacional';status='MANTER_COM_RESSALVA';notes.append('Busca por tabela de referência; ano, regime e renda precisam ser identificados.')
  elif any(x in k for x in ['calcular','calculo','calculadora']):
   intent='cálculo contextual';status='REFINAR_PROPOSTA';notes.append('Solicita cálculo ou ferramenta; base tributável, data e situação não foram informadas.')
  else:
   intent='informacional';status='MANTER_COM_RESSALVA';notes.append('Consulta de base/tributação, sem dados para cálculo numérico.')
  if re.search(r'\b(2020|2021|2022|2023|2024|2025|2026)\b',k):
   notes.append('Referência histórica exige tabela do período, sem presumir regras atuais.')
 elif rule=='P3V22_CET_CREDITO':
  subtype='Custo Efetivo Total (CET) de financiamento' if ('financiamento' in k or 'imobili' in k) else 'Custo Efetivo Total (CET) de crédito'
  if 'como calcular' in k:
   intent='informacional';status='MANTER_COM_RESSALVA';notes.append('Pedido de método/instruções, não cálculo numérico executável.')
  elif 'calculadora' in k:
   intent='cálculo contextual';status='REFINAR_PROPOSTA';notes.append('Procura ferramenta; exige encargos, prazo e fluxos para calcular CET.')
  elif any(x in k for x in ['taxa','mensal','anual','juros','cet emprestimo','cet financiamento']):
   intent='informacional';status='MANTER_COM_RESSALVA';notes.append('CET não equivale à taxa nominal; não estimar sem custos/encargos e fluxo contratual.')
  else:
   intent='informacional';status='MANTER_COM_RESSALVA';notes.append('Expressão designa CET, mas não fornece dados para uma operação.')
  if 'caixa' in k or 'banco do brasil' in k:
   notes.append('Instituição citada não implica navegação nem comprova taxa contratual.')
  if '2022' in k:notes.append('Ano histórico preservado; não usar CET contemporâneo.')
 elif rule=='P3V22_TAXA_FINANC_IMOVEL':
  subtype='Taxas de financiamento imobiliário';intent='informacional'
  status='MANTER_COM_RESSALVA';notes.append('Consulta por taxa/comparação, não simulação sem capital e prazo.')
  if any(x in k for x in ['caixa','bradesco','itau','santander','banco central']):
   notes.append('Instituição citada é contexto de consulta; não assumir navegação nem taxa atual.')
  if 'menor' in k or 'melhor' in k:notes.append('Intenção comparativa explícita; fonte/condições da taxa dependem de data e instituição.')
 else:raise AssertionError(('regra inesperada',rule))
 return {'status_tecnico_v27':status,'tipo_intencao_recomendado_v27':intent,'subtipo_recomendado_v27':subtype,
         'fundamentacao_v27':' '.join(notes),'homologacao_editorial_v27':'PENDENTE','aplicacao_lotes_v27':'NAO',
         'destino_v27':'FILA_GLOBAL_NAO_PRIORIZADA','faixa_revisada_v27':prior}

# input source tests
origdec=read_csv(SRC/'p3-v2.6-decisoes-17.csv'); assert len(origdec)==17
backlog=read_csv(SRC/'backlog-global-98-com-parecer-50.csv');assert len(backlog)==98
priority={r['id_global'] for r in read_csv(SRC/'p3-v2.6-fila-23965.csv')}
baseids={r['id_global'] for r in origdec}; assert len(baseids)==17
assert baseids<=priority
assert not {r['id_global'] for r in backlog}&priority
# Review global backlog, preserves previous 50 unchanged, adds v27 only for 48 B/C
newcols=['status_tecnico_v27','tipo_intencao_recomendado_v27','subtipo_recomendado_v27','fundamentacao_v27','homologacao_editorial_v27','aplicacao_lotes_v27','destino_v27','faixa_revisada_v27']
review48=[];all_back=[]
for r in backlog:
 a=r.copy()
 if r['faixa_prioridade_global'] in ('B_MEDIA','C_BAIXA_OU_COMPLEXA'):
  a.update(assess_global(r)); review48.append(a.copy())
 else:
  a.update(dict.fromkeys(newcols,''))
 all_back.append(a)
assert len(review48)==48 and len([r for r in review48 if r['faixa_prioridade_global']=='B_MEDIA'])==30
save_csv(OUT/'global-v27-pareceres-48.csv',review48,list(backlog[0])+newcols)
save_csv(OUT/'backlog-global-98-com-parecer-v27.csv',all_back,list(backlog[0])+newcols)
# P3 review/one conservative correction of too narrow 'piso do INSS'
review17=[]
for r in origdec:
 a=r.copy();k=normalize(r['Keyword'])
 if r['id_global']==CHANGE_ID:
  a.update({'parecer_critico_v27':'REFINAMENTO_SEMANTICO','fundamentacao_v27':'"Piso do INSS" não especifica se é piso de benefício, contribuição ou outra referência previdenciária. Evitar subtipo exclusivo de benefício.','homologacao_editorial_v27':'PENDENTE','alteracao_no_lote_v27':'SIM'})
 elif r['id_global']=='72576':
  a.update({'parecer_critico_v27':'MANTIDO_COM_RESSALVA','fundamentacao_v27':'Expressão "quantos anos de INSS pago" não permite fixar regra de aposentadoria; tempo de contribuição e idade continuam condicionais.','homologacao_editorial_v27':'PENDENTE','alteracao_no_lote_v27':'NAO'})
 else:
  a.update({'parecer_critico_v27':'MANTIDO_COM_RESSALVA','fundamentacao_v27':'Área e intenção coerentes. Não concluir elegibilidade, valor ou direito sem período, vínculo e condições aplicáveis.','homologacao_editorial_v27':'PENDENTE','alteracao_no_lote_v27':'NAO'})
 review17.append(a)
extra17=['parecer_critico_v27','fundamentacao_v27','homologacao_editorial_v27','alteracao_no_lote_v27']
save_csv(OUT/'p3-v2.7-revisao-critica-17.csv',review17,list(origdec[0])+extra17)
# load base ZIP to immutable copies, patch only id
srczip=SRC/'lotes-001-a-030-p3-v2.6.zip'
changedids=set();patches=[];reg=[];new_by_id={};base_count=ctrl_count=0
with zipfile.ZipFile(srczip) as za, zipfile.ZipFile(OUT/'lotes-001-a-030-p3-v2.7.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=5) as zb:
 for name in za.namelist():
  rows,fields=zrows(za,name);nb=nc=patchcount=0
  for r in rows:
   if r['tipo_registro']=='base':nb+=1
   else:nc+=1
   if r['id_global'] != CHANGE_ID:continue
   assert r['tipo_registro']=='base' and r['Keyword']=='novo piso do inss'
   nr=r.copy();sub='Piso previdenciário (natureza a confirmar)'
   nr['subcluster']=sub
   nr['intencao_principal']='Consultar informação: '+sub
   nr['confianca']='baixa'
   nr['revisao_manual']='sim'
   nr['justificativa_curta']='Consulta genérica sobre piso do INSS; não especifica se se refere a benefícios ou contribuições. (P3 v2.7; revisão contextual, não homologação.)'
   changed=[f for f in fields if r[f]!=nr[f]]
   assert changed and set(changed)<=ALLOWED
   patches.append({'id_global':r['id_global'],'lote':name,'familia_id':r['familia_id'],'Keyword':r['Keyword'], 'motivo':'Evitar presumir piso de benefício em consulta genérica ao piso do INSS', 'campos_modificados':','.join(changed),'antes_json':json.dumps({f:r[f] for f in changed},ensure_ascii=False,sort_keys=True),'depois_json':json.dumps({f:nr[f] for f in changed},ensure_ascii=False,sort_keys=True)})
   r.update(nr); changedids.add(r['id_global']);patchcount+=1;new_by_id[r['id_global']]=nr
  outname=name.replace('v2.6','v2.7')
  stream=io.StringIO();ww=csv.DictWriter(stream,fieldnames=fields,delimiter=';',lineterminator='\n');ww.writeheader();ww.writerows(rows)
  zb.writestr(outname,('\ufeff'+stream.getvalue()).encode('utf-8'))
  reg.append({'lote':name,'base':nb,'controles':nc,'alteracoes':patchcount,'status':'PASSOU'})
  base_count+=nb;ctrl_count+=nc
assert len(changedids)==1 and base_count==294905 and ctrl_count==2190
save_csv(OUT/'p3-v2.7-patches.csv',patches)
save_csv(OUT/'p3-v2.7-regressao-30-lotes.csv',reg)
# add audit columns only to queues, preserving all original columns/rows
auditcols=['status_p3_v2_7','parecer_p3_v2_7','nota_qa_p3_v2_7','area_final_p3_v2_7','subcluster_final_p3_v2_7','tipo_intencao_final_p3_v2_7','classificacao_alterada_p3_v2_7']
rev={r['id_global']:r for r in review17}
for inp,outname,expected in [('p3-v2.6-fila-23965.csv','p3-v2.7-fila-23965.csv',23965),('fila-geral-p0-p1-p2-p3-v2.6.csv','fila-geral-p0-p1-p2-p3-v2.7.csv',52046)]:
 records=read_csv(SRC/inp);assert len(records)==expected
 cols=list(records[0]);assert not set(cols)&set(auditcols)
 for r in records:
  rid=r['id_global'];extra=dict.fromkeys(auditcols,'')
  if rid in rev:
   q=rev[rid];extra.update({'status_p3_v2_7':'REVISADO', 'parecer_p3_v2_7':q['parecer_critico_v27'],'nota_qa_p3_v2_7':q['fundamentacao_v27'], 'classificacao_alterada_p3_v2_7':'sim' if rid==CHANGE_ID else 'não'})
   if rid==CHANGE_ID:
    nr=new_by_id[rid];extra.update({'area_final_p3_v2_7':nr['area_principal'],'subcluster_final_p3_v2_7':nr['subcluster'],'tipo_intencao_final_p3_v2_7':nr['tipo_intencao']})
  r.update(extra)
 save_csv(OUT/outname,records,cols+auditcols)
# independent audit: read back both ZIPs/queues, patch exact before/after
changed=set();hb=hashlib.sha256();ha=hashlib.sha256();test_rows=[]
with zipfile.ZipFile(srczip) as za,zipfile.ZipFile(OUT/'lotes-001-a-030-p3-v2.7.zip') as zb:
 assert len(za.namelist())==len(zb.namelist())==30
 for old in za.namelist():
  x,fields=zrows(za,old);y,fields2=zrows(zb,old.replace('v2.6','v2.7'))
  assert fields==fields2 and len(x)==len(y)
  a=b=c=0
  for p,q in zip(x,y):
   assert p['id_global']==q['id_global'] and p['tipo_registro']==q['tipo_registro']
   if p['tipo_registro']=='base':a+=1
   else:b+=1
   dif={f for f in fields if p[f]!=q[f]}
   if dif:
    assert p['id_global']==CHANGE_ID and dif<=ALLOWED
    patch=patches[0];assert dif==set(patch['campos_modificados'].split(','))
    assert json.loads(patch['antes_json'])=={f:p[f] for f in dif}
    assert json.loads(patch['depois_json'])=={f:q[f] for f in dif}
    changed.add(p['id_global']);c+=1
   for f in fields:
    if f not in ALLOWED:
     hb.update((f+'\0'+p[f]+'\x1e').encode())
     ha.update((f+'\0'+q[f]+'\x1e').encode())
  test_rows.append({'lote':old,'base':a,'controles':b,'mudancas_conferidas':c,'protegidos':'OK','status':'PASSOU'})
assert changed=={CHANGE_ID} and hb.hexdigest()==ha.hexdigest() and sum(int(x['controles']) for x in test_rows)==2190
save_csv(OUT/'p3-v2.7-regressao-independente.csv',test_rows)
for inname,outname,expected in [('p3-v2.6-fila-23965.csv','p3-v2.7-fila-23965.csv',23965),('fila-geral-p0-p1-p2-p3-v2.6.csv','fila-geral-p0-p1-p2-p3-v2.7.csv',52046)]:
 before=read_csv(SRC/inname);after=read_csv(OUT/outname)
 assert len(before)==len(after)==expected
 for x,y in zip(before,after):
  assert x['id_global']==y['id_global'] and all(x[k]==y[k] for k in x)
# summaries
summary={'versao':'P3 v2.7','p3_revisados':17,'p3_patches':1,'p3_mantidos_com_ressalva':16,'globais_revisados':48,'globais_B':30,'globais_C':18,'globais_aplicados':0,'lotes':30,'registros_base':294905,'controles':2190,'p3_fora_pilotos':20383,'p2_pendentes':4660,'sha256_colunas_protegidas':hb.hexdigest(),'status':'PASSOU'}
(OUT/'p3-v2.7-resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
