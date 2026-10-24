#!/usr/bin/env python3
# coding: utf-8
"""Audita 165 amostras P3 v2.0; corrige falsos positivos conservadores por ID.
Entrada: ZIP da auditoria P3-v2.0 extraído nesta pasta.
Saídas: P3-v2.1 (30 lotes, fila P3, fila geral, decisões, patches, QA).
Usa apenas Python stdlib, não escreve nos arquivos de origem.
"""
import csv, json, re, hashlib, zipfile, io, collections, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[2]
SRC=ROOT/'08-Entregas/P3-v2.1/FONTES-REPRODUCAO/08-Entregas/P3-v2.0'
OUT=ROOT/'08-Entregas/P3-v2.1'
OUT.mkdir(parents=True,exist_ok=True)
WRITE_FIELDS=['area_principal','cluster','subcluster','dominio_ou_grandeza','tipo_intencao','intencao_principal','confianca','revisao_manual','justificativa_curta']
# Não inferir valores, percentual, taxas, direitos ou duração. Só corrige a INTENÇÃO do texto.
fixes={
'15378':('Afastamento e benefícios por incapacidade','informacional','Afastamento pelo INSS não é recolhimento de contribuições.'),
'89477':('Afastamento e benefícios por incapacidade','informacional','Afastamento por doença é consulta sobre benefício/incapacidade, não contribuição.'),
'31756':('Simuladores previdenciários (objetivo não informado)','cálculo contextual','A calculadora da Previdência não especifica se é contribuição, tempo ou benefício.'),
'100020':('Consulta de processo do INSS','navegacional/transacional','Consulta por número de processo é serviço, não cálculo de contribuição.'),
'129039':('Informe de rendimentos de benefícios do INSS','informacional','Declaração anual de rendimentos não é contribuição.'),
'129041':('Informe de rendimentos de benefícios do INSS','informacional','Declaração de rendimentos não é contribuição.'),
'171262':('Revisão de benefícios previdenciários','informacional','Revisão da vida toda envolve revisão de benefício, não cobrança de contribuição.'),
'267405':('Tempo de contribuição e aposentadoria','cálculo contextual','Simulação de tempo de serviço exige histórico e regra aplicável; não é informação genérica.'),
'278229':('Tempo de contribuição e aposentadoria','informacional','Tempo mínimo de contribuição é elegibilidade previdenciária, não valor da contribuição.'),
'50778':('Valores atrasados do INSS (natureza não especificada)','cálculo contextual','Atrasados podem ser benefício retroativo ou recolhimento em atraso; não assumir contribuição.'),
'159198':('Cálculo do INSS no Excel - instruções','informacional','Busca explícita por fórmula no Excel, não pedido de cálculo imediato.'),
'252085':('Equações e radiciação','cálculo contextual','A expressão a resolver não está na keyword: não é cálculo direto com operandos conhecidos.'),
'273182':('Custo efetivo total (CET) de crédito','informacional','CET não é sinônimo de taxa nominal de juros; categoria específica sem taxa real.'),
}

def read_csv_text(text):return list(csv.DictReader(io.StringIO(text),delimiter=';'))
def read(path):
 with path.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def get_fields(path):
 with path.open('r',encoding='utf-8-sig',newline='') as f:return next(csv.reader(f,delimiter=';'))
def write(path,rows,fields):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,delimiter=';',fieldnames=fields,extrasaction='ignore',lineterminator='\n');w.writeheader();w.writerows(rows)
def patch(row):
 id=row['id_global']; sub,tipo,reason=fixes[id]
 # O campo subcluster somente é alterado com evidência específica; manter a categoria ampla já validada.
 r=row.copy();oldsub=r['subcluster']
 r['subcluster']=sub;r['dominio_ou_grandeza']=sub;r['tipo_intencao']=tipo
 r['intencao_principal']=({'informacional':'Consultar informação: ','cálculo contextual':'Calcular com contexto: ','navegacional/transacional':'Localizar serviço: '}[tipo]+sub)
 r['confianca']='média';r['revisao_manual']='sim'
 r['justificativa_curta']=reason+' (P3 v2.1; regra revisada; não constitui homologação editorial).'
 return r,reason

dec=read(SRC/'p3-v2.0-decisoes.csv');sample=read(SRC/'p3-v2.0-amostra-qa.csv');sm={r['id_global'] for r in sample};dc={r['id_global']:r for r in dec}
assert len(dec)==272 and len(sample)==165 and len(sm)==165
assert set(fixes).issubset(dc)
basezip=SRC/'lotes-001-a-030-p3-v2.0.zip'
refrows={};infiles={};order=[];all_protected_cols=None
with zipfile.ZipFile(basezip) as z:
 assert len(z.namelist())==30
 for name in z.namelist():
  s=z.read(name).decode('utf-8-sig'); rows=read_csv_text(s)
  field=next(csv.reader(io.StringIO(s),delimiter=';'))
  infiles[name]=(rows,field);order.append(name)
  for r in rows:
   if r['tipo_registro']=='base':
    id=r['id_global'];assert id not in refrows;refrows[id]=(name,r)
assert len(refrows)==294905
for id in fixes:assert id in refrows and refrows[id][1]['Keyword']==dc[id]['Keyword'],id
origids=set(refrows)
patches=[];revised_ids=set();rows_after={}
for id,(name,r) in refrows.items():
 if id in fixes:
  rr,reason=patch(r);changed=[f for f in WRITE_FIELDS if r[f]!=rr[f]]
  assert changed
  rows_after[id]=rr;revised_ids.add(id)
  patches.append(dict(id_global=id,lote=name,familia_id=r['familia_id'],Keyword=r['Keyword'],regra_anterior=dc[id]['regra'],regra_qa='P3V21_REFINAMENTO_SEMANTICO',justificativa=reason,campos_modificados=','.join(changed),antes_json=json.dumps({f:r[f] for f in changed},ensure_ascii=False,sort_keys=True),depois_json=json.dumps({f:rr[f] for f in changed},ensure_ascii=False,sort_keys=True)))
rows_qa=[];all_assess=[];counter=collections.Counter()
for r in dec:
 id=r['id_global'];k=r['Keyword'];rule=r['regra'];in_sample=id in sm
 if id in fixes:
  st='CORRIGIDO';note=fixes[id][2]
 elif rule=='P3V20_CONSUMO_VEICULO':
  st='MANTIDO_COM_RESSALVA';note='Consulta informacional sobre consumo de modelo; valores dependem de ano, versão, combustível, ciclo e fonte. Não é cálculo de consumo com distância/litros fornecidos.'
 elif rule=='P3V20_TAXA_JUROS_INFORME':
  st='MANTIDO_COM_RESSALVA';note='Busca informacional sobre taxa, não simulação com capital/prazo. Valor, modalidade, instituição e data não podem ser presumidos.'
  if 'nubank' in k.lower() and 'poupança' in k.lower(): note+=' Nome comercial/produto citado não verificado; não afirmar existência ou remuneração específica.'
 elif rule=='P3V20_INSS_DOMINIO':
  st='MANTIDO_COM_RESSALVA';note='Área Trabalho/Previdência adequada; cálculo exige regras, ano e categoria do segurado; não usar taxa fixa de INSS.'
 elif rule=='P3V20_SALARIO_MATERNIDADE':
  st='MANTIDO_COM_RESSALVA';note='Área Trabalho e subtema maternidade adequado; direitos/cálculo condicionados a vínculo, datas e regras aplicáveis.'
 elif rule=='P3V20_ALGEBRA_DOMINIO':
  st='MANTIDO_COM_RESSALVA';note='Domínio matemático coerente. Distinguir tutorial ou busca de ferramenta de cálculo com dados efetivamente apresentados.'
 elif rule=='P3V20_MATERIAL_DIDATICO':
  st='MANTIDO';note='Pedido explicitamente por PDF/material didático, não por conversão de arquivo ou cálculo direto.'
 elif rule=='P3V20_ESTATISTICA_DOMINIO':
  st='MANTIDO_COM_RESSALVA';note='Intenção matemática reconhecida; calcular amostra/variância requer dados, e exercícios são informacionais.'
 elif rule=='P3V20_CONVERSAO_ENERGIA':
  st='MANTIDO';note='Unidades Wh e kWh compatíveis com direção explícita; não confundir com potência W/kW.'
 elif rule=='P3V20_IRRF_DOMINIO':
  st='MANTIDO_COM_RESSALVA';note='IRRF em ano histórico requer tabela aplicável e situação tributária; não supor fórmula/percentual.'
 else:raise AssertionError(rule)
 item={**r,'na_amostra_165':'sim' if in_sample else 'não','parecer_qa_p3_v2_1':st,'nota_qa_p3_v2_1':note,'alteracao_no_lote':'sim' if id in fixes else 'não'}
 all_assess.append(item)
 if in_sample:rows_qa.append(item);counter[st]+=1
assert len(rows_qa)==165
fields_all=list(all_assess[0]);write(OUT/'p3-v2.1-pareceres-272.csv',all_assess,fields_all)
write(OUT/'p3-v2.1-revisao-amostra-165.csv',rows_qa,fields_all)
write(OUT/'p3-v2.1-patches.csv',sorted(patches,key=lambda x:int(x['id_global'])),list(patches[0]))
# Escreve lotes corrigidos e compara contra fonte linha a linha, incluindo controles.
regress=[];counter_types=collections.Counter();lock_keys=('tipo_registro','id_global','lote_id','familia_id','controle_id','Keyword')
with zipfile.ZipFile(OUT/'lotes-001-a-030-p3-v2.1.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zz:
 for srcname in order:
  original,fields=infiles[srcname]; updated=[]; controls=0;modified=0;basecount=0;bad=0
  for r in original:
   id=r['id_global'];nr=rows_after.get(id,r)
   if r['tipo_registro']=='base':basecount+=1
   else:controls+=1
   if id in revised_ids and r['tipo_registro']=='base':modified+=1
   for f in fields:
    if nr[f]!=r[f] and not (id in revised_ids and f in WRITE_FIELDS):bad+=1
   updated.append(nr)
  assert bad==0,(srcname,bad)
  b=io.StringIO();w=csv.DictWriter(b,delimiter=';',fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(updated)
  # BOM padronizado como origem
  outname=srcname.replace('v2.0','v2.1');zz.writestr(outname,('\ufeff'+b.getvalue()).encode('utf-8'))
  regress.append({'lote':srcname,'base':basecount,'controles':controls,'alteracoes_autorizadas':modified,'alteracoes_indevidas':bad,'status':'PASSOU'})
assert sum(int(x['base']) for x in regress)==294905
assert sum(int(x['controles']) for x in regress)==2190
assert sum(int(x['alteracoes_autorizadas']) for x in regress)==len(fixes)
write(OUT/'p3-v2.1-regressao-30-lotes.csv',regress,list(regress[0]))
assessment_by_id={q['id_global']:q for q in all_assess}
# Fila P3 e fila geral — preservar todas as colunas prévias intactas.
newcols=['status_p3_v2_1','parecer_p3_v2_1','nota_qa_p3_v2_1','area_final_p3_v2_1','cluster_final_p3_v2_1','subcluster_final_p3_v2_1','tipo_intencao_final_p3_v2_1','classificacao_alterada_p3_v2_1']
for filename,newname in [('p3-v2.0-fila-23965.csv','p3-v2.1-fila-23965.csv'),('fila-geral-p0-p1-p2-p3-v2.0.csv','fila-geral-p0-p1-p2-p3-v2.1.csv')]:
 fields=get_fields(SRC/filename);assert len(fields)>=149 and not any(f in fields for f in newcols)
 aa=read(SRC/filename);updates=0
 for r in aa:
  id=r['id_global'];rv=rows_after.get(id)
  q=dict.fromkeys(newcols,'')
  if id in dc:
   old=refrows[id][1];new=rv or old
   q={'status_p3_v2_1':'REVISADO' if id in fixes else 'PRESERVADO', 'parecer_p3_v2_1':assessment_by_id[id]['parecer_qa_p3_v2_1'], 'nota_qa_p3_v2_1':assessment_by_id[id]['nota_qa_p3_v2_1'],'area_final_p3_v2_1':new['area_principal'],'cluster_final_p3_v2_1':new['cluster'],'subcluster_final_p3_v2_1':new['subcluster'],'tipo_intencao_final_p3_v2_1':new['tipo_intencao'],'classificacao_alterada_p3_v2_1':'sim' if id in fixes else 'não'}
   if id in fixes:updates+=1
  r.update(q)
 assert updates==len(fixes),(filename,updates)
 write(OUT/newname,aa,fields+newcols)
assert counter['CORRIGIDO']==len(fixes)-1,dict(counter) # CET não incluído na amostra
summary={'versao':'P3 v2.1','amostra_revisada':165,'universo_auditado':272,'patches':len(fixes),'patches_amostra':len(fixes)-1,'patch_extra_amostra':'273182 (CET)','pareceres_amostra':dict(counter),'base':294905,'controles':2190,'lotes':30,'P3_fora_dos_pilotos':20400,'P2_pendentes':4660,'criterio':'revisão contextual e regras por ID; não homologação editorial','status':'PASSOU'}
(OUT/'p3-v2.1-resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
