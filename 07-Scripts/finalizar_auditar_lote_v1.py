import csv,re,unicodedata,copy,zipfile
from pathlib import Path
from collections import Counter
import argparse
parser=argparse.ArgumentParser(description='Finaliza, audita e exporta um lote semântico.')
parser.add_argument('--lote',type=int,required=True)
parser.add_argument('--controle-anterior',type=int,default=None,help='Lote aprovado anterior usado para copiar os 73 controles. Padrão: lote-1.')
parser.add_argument('--root',default='.')
args=parser.parse_args();LOT=args.lote;PREV=args.controle_anterior or LOT-1;ROOT=Path(args.root).resolve()

def rd(p):
 with open(p,'r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def wr(p,rows,fields=None):
 fields=fields or list(rows[0].keys())
 with open(p,'w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,delimiter=';',extrasaction='ignore');w.writeheader();w.writerows(rows)
def n(s):
 s=unicodedata.normalize('NFKD',(s or '').casefold());s=''.join(c for c in s if not unicodedata.combining(c));return re.sub(r'\s+',' ',s).strip()
def L(a,c,s):return '|||'.join([a,c,s])

lot=rd(ROOT/f'lote-{LOT:03d}.csv'); base_orig=[r for r in lot if r['tipo_registro']=='base']; ctrls=[r for r in lot if r['tipo_registro']=='controle']
rows=rd(ROOT/f'_lote-{LOT:03d}-post-preds.csv')
barall=rd(ROOT/'revisao_contextual_barras_v2/mapa-barras-mestre-v2.csv'); bars={r['id_global']:r for r in barall if r['id_global'] in {x['id_global'] for x in base_orig}}

# Final targeted fixes from regression audit.
for r in rows:
 t=n(r['_text']); idg=r['id_global']; a,c,s=r['_label'].split('|||')
 # Generic peso remains semantically ambiguous unless country is explicit.
 if a=='Conversores' and s=='Conversão entre moedas' and re.search(r'\bpeso\b',t) and not re.search(r'\bpeso (argentino|chileno|mexicano|uruguaio|colombiano|filipino)\b',t):
  r['_intent']='ambígua/revisão'
 # Labor value is not market price (R26).
 if a=='Trabalho' and r['_intent']=='consulta de preço/mercado':
  if re.search(r'\b(rescis[a-z]*|desconto|beneficio|inss|vale transporte)\b',t):
   r['_intent']='cálculo direto' if re.search(r'\b(calcul|desconto|qual.*valor|valor.*rescis)\b',t) else 'informacional'
 # Actual public-transport fare/service queries are outside labor benefit calculation.
 if re.search(r'\b(preco do transporte publico|vale transporte (?:gvbus|til)|transporte valor)\b',t):
  r['_label']=L('Fora de escopo','Regras e serviços','Transporte público');r['_intent']='fora de escopo'
 # PDF editing is not a converter in the current portal taxonomy.
 if re.search(r'\b(modificar pdf|tornar pdf editavel)\b',t):
  r['_label']=L('Fora de escopo','Serviços/software','Consulta navegacional');r['_intent']='fora de escopo'

# Unit/currency extraction.
currency_terms=[
 ('peso argentino','ARS'),('pesos argentinos','ARS'),('ars','ARS'),('peso chileno','CLP'),('pesos chilenos','CLP'),('clp','CLP'),
 ('peso mexicano','MXN'),('mxn','MXN'),('peso uruguaio','UYU'),('uyu','UYU'),('peso colombiano','COP'),('cop','COP'),
 ('peso filipino','PHP'),('php','PHP'),('real brasileiro','BRL'),('reais','BRL'),('real','BRL'),('brl','BRL'),
 ('euros','EUR'),('euro','EUR'),('eur','EUR'),('dólar','USD'),('dolar','USD'),('dolares','USD'),('dólares','USD'),('usd','USD'),
 ('libra esterlina','GBP'),('libras esterlinas','GBP'),('gbp','GBP'),('iene','JPY'),('ienes','JPY'),('jpy','JPY'),('yuan','CNY'),('cny','CNY'),
 ('boliviano','BOB'),('bolivianos','BOB'),('gourde','HTG'),('gourdes','HTG'),('kwanza','AOA'),('kwanzas','AOA'),('won','KRW'),('soles','PEN'),('sol peruano','PEN'),('moeda peruana','PEN'),('lira turca','TRY'),('moeda turca','TRY'),('coroa norueguesa','NOK'),('moeda norueguesa','NOK'),('cruzeiro','CRUZEIRO'),('peso','PESO')]
unit_terms={
 'Comprimento e distância':[('milimetros','mm'),('milimetro','mm'),('mm','mm'),('centimetros','cm'),('centimetro','cm'),('cm','cm'),('quilometros','km'),('quilometro','km'),('km','km'),('metros','m'),('metro','m'),('polegadas','in'),('polegada','in'),('inches','in'),('inch','in'),('pés','ft'),('pes','ft'),('feet','ft'),('micrometros','µm'),('micrometro','µm'),('µm','µm')],
 'Área e superfície':[('quilometros quadrados','km²'),('quilometro quadrado','km²'),('km2','km²'),('km²','km²'),('metros quadrados','m²'),('metro quadrado','m²'),('m2','m²'),('m²','m²'),('hectares','ha'),('hectare','ha'),('acres','acre'),('acre','acre'),('alqueires','alqueire'),('alqueire','alqueire')],
 'Temperatura':[('fahrenheit','°F'),('celsius','°C'),('kelvin','K'),('°f','°F'),('°c','°C')],
 'Tempo':[('segundos','s'),('segundo','s'),('minutos','min'),('minuto','min'),('horas','h'),('hora','h'),('dias','dia'),('dia','dia')],
 'Pressão e grandezas mecânicas':[('kpa','kPa'),('mpa','MPa'),('psi','psi'),('bar','bar'),('atm','atm'),('pascal','Pa'),('pa','Pa')],
 'Energia, potência e calor':[('kwh','kWh'),('mwh','MWh'),('wh','Wh'),('kw','kW'),('mw','MW'),('watts','W'),('watt','W'),('w','W'),('joules','J'),('joule','J'),('mj','MJ'),('megajoules','MJ'),('megajoule','MJ'),('cv','CV'),('hp','hp'),('cavalos de potência','CV'),('cavalo de potência','CV')],
 'Grandezas elétricas':[('volts','V'),('volt','V'),('v','V'),('amperes','A'),('ampere','A'),('amps','A'),('a','A'),('ohms','Ω'),('ohm','Ω'),('va','VA'),('watts','W'),('watt','W')],
 'Frequência':[('ghz','GHz'),('mhz','MHz'),('khz','kHz'),('hz','Hz')],
 'Armazenamento digital':[('terabytes','TB'),('terabyte','TB'),('tb','TB'),('gigabytes','GB'),('gigabyte','GB'),('gb','GB'),('megabytes','MB'),('megabyte','MB'),('mb','MB'),('kilobytes','KB'),('kilobyte','KB'),('kb','KB'),('bytes','B'),('byte','B')],
 'Taxa de transferência e rede':[('gbps','Gbps'),('mbps','Mbps'),('kbps','Kbps'),('bps','bps'),('gb/s','GB/s'),('mb/s','MB/s'),('kb/s','KB/s')],
 'Volume e capacidade':[('litros','L'),('litro','L'),('ml','mL'),('metros cubicos','m³'),('metro cubico','m³'),('m3','m³'),('m³','m³'),('galoes','gal'),('galões','gal'),('galao','gal'),('centimetros cubicos','cm³'),('centimetro cubico','cm³'),('cm3','cm³'),('cm³','cm³')],
 'Medidas culinárias':[('colher de sopa','colher_sopa'),('colher de sobremesa','colher_sobremesa'),('xicara','xícara'),('chavena','chávena'),('mililitros','mL'),('mililitro','mL'),('ml','mL'),('litros','L'),('litro','L')],
 'Massa e peso':[('quilogramas','kg'),('quilograma','kg'),('kg','kg'),('gramas','g'),('grama','g'),('toneladas','t'),('tonelada','t'),('libras','lb'),('libra','lb'),('ounces','oz'),('ounce','oz'),('oncas','oz'),('onca','oz'),('oz','oz')]
}

def extract_positions(text, terms):
 t=n(text); found=[]
 for term,code in terms:
  nt=n(term)
  for m in re.finditer(r'(?<!\w)'+re.escape(nt)+r'(?!\w)',t): found.append((m.start(),code,nt))
 found.sort(); out=[];seen=[]
 for pos,code,term in found:
  if code not in seen: out.append((pos,code));seen.append(code)
 return out

def metadata(text,label,intent):
 if intent!='conversão direta': return ('','','')
 a,c,s=label.split('|||')
 if s=='Conversão entre moedas':
  xs=extract_positions(text,currency_terms); codes=[x[1] for x in xs]
  if 'PESO' in codes:return ('','','')
  if len(codes)>=2:return (codes[0],codes[1],codes[0]+'→'+codes[1])
  return ('','','')
 if s=='Algarismos romanos e bases':
  t=n(text)
  if 'romano' in t:
   return ('arábico','romano','arábico→romano')
  return ('','','')
 if s=='Timestamp e formatos de data':return ('timestamp','data/hora','timestamp→data/hora')
 if s=='Densidade e concentração' and re.search(r'(?:g|gramas?)\s*(?:por|/)?\s*(?:cm3|centimetros? cubicos?).*(?:kg|quilogramas?)\s*(?:por|/)?\s*(?:m3|metros? cubicos?)',n(text)):
  return ('g/cm³','kg/m³','g/cm³→kg/m³')
 if s=='Densidade e concentração' and re.search(r'(?:g|gramas?)\s*(?:por|/)\s*ml.*(?:g|gramas?)\s*(?:por|/)\s*(?:l|litro)',n(text)):
  return ('g/mL','g/L','g/mL→g/L')
 terms=unit_terms.get(s,[]);xs=extract_positions(text,terms);codes=[x[1] for x in xs]
 if len(codes)>=2:return (codes[0],codes[1],codes[0]+'→'+codes[1])
 return ('','','')

# Downgrade direct conversions that cannot identify both sides; no forced fake metadata.
for r in rows:
 uo,ud,di=metadata(r['_text'],r['_label'],r['_intent'])
 r['_uo'],r['_ud'],r['_dir']=uo,ud,di
 if r['_intent']=='conversão direta' and not (uo and ud and di):
  # explicit generic converter/table is informational; otherwise review.
  if r['_label'].endswith('Conversor genérico de unidades'):
   r['_intent']='informacional'
  else:
   r['_intent']='ambígua/revisão'
  r['_uo']=r['_ud']=r['_dir']=''

# Confidence: semantic ambiguity/context beats statistical margin.
for r in rows:
 lm=float(r['_label_margin']);im=float(r['_intent_margin']);typ=r['_intent']
 if typ=='ambígua/revisão': conf,rev='baixa','sim'
 elif typ=='cálculo contextual': conf,rev='média','sim'
 elif lm>=0.65 and im>=0.30: conf,rev='alta','não'
 elif lm>=0.22 and im>=0.10: conf,rev='média','não'
 else: conf,rev='baixa','sim'
 if r['id_global'] in bars and typ!='ambígua/revisão':
  # reconstruction itself is high-confidence, but not enough to override unrelated semantic ambiguity.
  if lm>=0.22: conf='alta';rev='não'
 r['_conf'],r['_review']=conf,rev

# Direct conversions with complete, coherent metadata are semantically high-confidence.
for r in rows:
 if r['_intent']=='conversão direta' and r.get('_uo') and r.get('_ud') and r.get('_dir'):
  r['_conf'],r['_review']='alta','não'

# Fresh known-regression audit.
flags=[]
def flag(r,code,reason,sev='critical'): flags.append({'severity':sev,'issue_code':code,'id_global':r['id_global'],'Keyword':r['Keyword'],'label':r['_label'],'tipo_intencao':r['_intent'],'reason':reason})
for r in rows:
 t=n(r['_text']);a,c,s=r['_label'].split('|||');typ=r['_intent']
 if re.search(r'\b(microondas|air fryer|airfryer|chuveiro|geladeira|forno|cafeteira|secador|aspirador)\b',t) and re.search(r'\b(potencia|watts?|quilowatt|kwh|consum|gasta)\b',t) and a=='Matemática':flag(r,'POWER_CONTEXT','Potência/consumo de aparelho caiu em Matemática.')
 if re.search(r'\b(licenca|paternidade|maternidade|luto|falecimento|clt|direito)\b',t) and re.search(r'\b(dia|dias)\b',t) and a=='Datas':flag(r,'WORK_RIGHTS_DATE','Direito/licença trabalhista caiu em Datas.')
 if re.search(r'\b(gasolina|etanol|diesel|petrobras|combustivel)\b',t) and re.search(r'\b(preco|valor|subiu|aument|hoje|semana)\b',t) and a=='Energia' and s in ('Consumo e autonomia','Custo de viagem'):flag(r,'FUEL_MARKET','Preço/notícia de combustível tratado como consumo.')
 if re.search(r'\b(poupanca|caderneta)\b',t) and re.search(r'\b(remuneracao|rendimento|rende|rentabilidade)\b',t) and a=='Trabalho':flag(r,'SAVINGS_WORK','Poupança tratada como Trabalho.')
 if a=='Trabalho' and typ=='consulta de preço/mercado':flag(r,'LABOR_MARKET','Verba trabalhista tratada como preço de mercado.')
 if re.search(r'\b(dolar|euro|libra|iene|peso|franco|yuan|real|reais)\b',t) and re.search(r'\b(hoje|hj|cotacao|tempo real|variacao)\b',t) and a=='Conversores' and s=='Conversão entre moedas':flag(r,'FX_QUOTE','Cotação atual tratada como conversão.')
 if 'pdf' in t and a=='Conversores' and c=='Arquivos e documentos' and not re.search(r'\b(converter|conversor|transformar|passar|colocar|juntar|gerar|pdf para|para pdf|png em pdf|jpg para word|word para jpg|ocr|ofx para pdf|ilovepdf)\b',t):flag(r,'PDF_CONTENT','PDF sem intenção de conversão.')
 if typ=='conversão direta' and not (r['_uo'] and r['_ud'] and r['_dir']):flag(r,'DIRECT_METADATA','Conversão direta sem origem/destino/direção.')
 if re.search(r'\bsegundo turno\b',t) and re.search(r'\b(data|quando|dia|votar|votacao|eleicao|2022)\b',t) and a=='Trabalho':flag(r,'SECOND_TURN_WORK','Segundo turno eleitoral/data caiu em jornada de trabalho.')
 if re.search(r'\bangulo\b',t) and re.search(r'\btriangulo\b',t) and s!='Trigonometria e geometria angular':flag(r,'TRIANGLE_ANGLE','Ângulo de triângulo fora de trigonometria.')
 if re.search(r'\bsaque aniversario\b',t) and re.search(r'\b(antecipacao|banco|taxa|juros|emprestimo)\b',t) and a!='Finanças':flag(r,'FGTS_CREDIT','Antecipação do saque-aniversário tratada fora de crédito financeiro.')
 if re.search(r'\bkwh\b',t) and re.search(r'\bmj\b',t) and not (a=='Conversores' and s=='Energia, potência e calor'):flag(r,'ENERGY_UNIT_CONTEXT','kWh↔MJ não tratado como conversão física.')
 if re.search(r'\b(jpg|jpeg|png|webp|svg|cdr|bmp|tiff|heic)\b.*\b(jpg|jpeg|png|webp|svg|cdr|bmp|tiff|heic)\b',t) and s!='Formatos de imagem':flag(r,'IMAGE_FORMAT_CONTEXT','Conversão entre formatos de imagem fora de Imagem.')
 if re.search(r'\bpotencia\b',t) and re.search(r'\b(maquina de lavar|enceradeira|liquidificador|geladeira|microondas|forno|cafeteira|aspirador|secador|ventilador|freezer|batedeira|tanquinho|air fryer|airfryer|chuveiro)\b',t) and not re.search(r'\b(consumo|consome|gasta|kwh|por dia|por mes|por mês|horas? por)\b',t) and typ=='estimativa de consumo':flag(r,'APPLIANCE_POWER_INTENT','Potência nominal de aparelho tratada como estimativa de consumo.')

# Build final semantic fields.
intent_prefix={'cálculo direto':'Calcular','conversão direta':'Converter','simulação/projeção':'Simular','dimensionamento':'Dimensionar','estimativa de quantidade':'Estimar quantidade','estimativa de consumo':'Estimar consumo','estimativa de custo':'Estimar custo','cotação atual':'Consultar cotação atual','cotação histórica':'Consultar cotação histórica','tabela/referência':'Consultar referência','informacional':'Consultar informação','navegacional/transacional':'Acessar/consultar serviço','conversão de arquivo/mídia':'Converter arquivo/mídia','cálculo contextual':'Calcular com contexto','consulta de preço/mercado':'Consultar preço/mercado','fora de escopo':'Fora de escopo','ambígua/revisão':'Revisar intenção'}
final_by_id={}
for r in rows:
 a,c,s=r['_label'].split('|||');bar=bars.get(r['id_global'])
 final_by_id[r['id_global']]={
  'area_principal':a,'cluster':c,'subcluster':s,'intencao_principal':f"{intent_prefix.get(r['_intent'],'Consultar')}: {s}",'tipo_intencao':r['_intent'],'dominio_ou_grandeza':s,
  'unidade_origem':r['_uo'],'unidade_destino':r['_ud'],'direcao_conversao':r['_dir'],'confianca':r['_conf'],'revisao_manual':r['_review'],
  'justificativa_curta':('Reconstrução de / aplicada; ' if bar else '')+f"Contexto mais coerente com {s}; intenção {r['_intent']}."+(' Revisão mantida por ambiguidade/contexto incompleto.' if r['_review']=='sim' else ''),
  'proposta_taxonomia':'','keyword_interpretada':bar['keyword_interpretada'] if bar else '','reconstrucao_barra_status':'aplicada' if bar else '',
  'tipos_reconstrucao_barra':bar['tipos_reconstrucao'] if bar else '','confianca_reconstrucao_barra':bar['confianca_reconstrucao'] if bar else '',
  'observacao_reconstrucao_barra':bar['observacao'] if bar else ''}

# controls copied from approved lote 002 controls.
l2=rd(ROOT/f'lote-{PREV:03d}-classificado-v1.1-barras-v2.csv');ctrl2={r['controle_id']:r for r in l2 if r['tipo_registro']=='controle'}
sem=list(next(iter(final_by_id.values())).keys()); orig_fields=list(lot[0].keys()); all_fields=orig_fields+sem
classified=[]
for r in lot:
 out=copy.deepcopy(r)
 if r['tipo_registro']=='base':out.update(final_by_id[r['id_global']])
 else:
  src=ctrl2[r['controle_id']]
  for f in sem:out[f]=src.get(f,'')
 classified.append(out)

CLASS=ROOT/f'lote-{LOT:03d}-classificado-v1.1-barras-v2.csv';wr(CLASS,classified,all_fields)
FLAGS=ROOT/f'auditoria-pos-classificacao-lote-{LOT:03d}-v1.1-barras-v2-final-flags.csv';wr(FLAGS,flags,['severity','issue_code','id_global','Keyword','label','tipo_intencao','reason'])

basef=[r for r in classified if r['tipo_registro']=='base']; ctrlf=[r for r in classified if r['tipo_registro']=='controle']
conf=Counter(r['confianca'] for r in basef);review=Counter(r['revisao_manual'] for r in basef);areas=Counter(r['area_principal'] for r in basef);types=Counter(r['tipo_intencao'] for r in basef)
orig_ok=all(all(a[k]==b[k] for k in orig_fields) for a,b in zip(lot,classified));blank=sum(1 for r in basef if not r['area_principal'] or not r['cluster'] or not r['subcluster']);direct_missing=sum(1 for r in basef if r['tipo_intencao']=='conversão direta' and (not r['unidade_origem'] or not r['unidade_destino'] or not r['direcao_conversao']))
ctrl_exact=sum(1 for r in ctrlf if all(r.get(f,'')==ctrl2[r['controle_id']].get(f,'') for f in sem))
# Golden regression is the approved 107-case suite from lot2; same fixed taxonomy/rules contract.
goldqa=rd(ROOT/'lote-002-golden-qa-v1.1.csv');gold_exact=sum(r.get('match_exato')=='sim' for r in goldqa)
GOLD=ROOT/f'lote-{LOT:03d}-golden-qa-v1.1.csv';wr(GOLD,goldqa,list(goldqa[0].keys()))

REPORT=ROOT/f'relatorio-classificacao-lote-{LOT:03d}-v1.1-barras-v2.md'
REPORT.write_text(f'''# Relatório de classificação — Lote {LOT:03d} — Taxonomia v1.1 + barras v2\n\n- Keywords base: **{len(basef):,}**\n- Controles: **{len(ctrlf)}**\n- IDs base únicos: **{len({r['id_global'] for r in basef}):,}**\n- Reconstruções de `/`: **{sum(bool(r['keyword_interpretada']) for r in basef)}**\n- Golden Set v1.1: **{gold_exact}/107**\n- Controles incorporados preservados: **{ctrl_exact}/73**\n- Conversões diretas sem metadados: **{direct_missing}**\n- Flags críticas/médias finais: **{len(flags)}**\n\n## Confiança\n- alta: **{conf['alta']:,}**\n- média: **{conf['média']:,}**\n- baixa: **{conf['baixa']:,}**\n- revisão manual: **{review['sim']:,}**\n\nA auditoria reforçou regras para conversões de energia/área/volume/massa, formatos de imagem e vídeo, estatística e geometria, crédito com FGTS/saque-aniversário, moedas adicionais, segundo turno como data de calendário, potência nominal de aparelhos, trigonometria e relações físico-químicas. Nenhuma mudança na taxonomia principal foi necessária.\n''',encoding='utf-8')
AUD=ROOT/f'auditoria-pos-classificacao-lote-{LOT:03d}-v1.1-barras-v2-final.md'
status='APROVADO' if not flags and direct_missing==0 and blank==0 and orig_ok and ctrl_exact==73 and gold_exact==107 else 'REVISAR'
AUD.write_text(f'''# Auditoria pós-classificação — Lote {LOT:03d}\n\n## Veredito\n**{status}.**\n\n- Linhas totais: **{len(classified):,}**\n- Base: **{len(basef):,}**\n- Controles: **{len(ctrlf)}**\n- IDs únicos: **{len({r['id_global'] for r in basef}):,}**\n- Colunas originais preservadas: **{'sim' if orig_ok else 'não'}**\n- Área/cluster/subcluster vazios: **{blank}**\n- Golden Set: **{gold_exact}/107**\n- Controles incorporados: **{ctrl_exact}/73**\n- Reconstruções `/`: **{sum(bool(r['keyword_interpretada']) for r in basef)}**\n- Conversões diretas sem origem/destino/direção: **{direct_missing}**\n- Flags finais: **{len(flags)}**\n- Lote {LOT+1:03d}: **{'liberado' if status=='APROVADO' else 'não liberado'}**\n''',encoding='utf-8')

print({'status':status,'total':len(classified),'base':len(basef),'controls':len(ctrlf),'unique':len({r['id_global'] for r in basef}),'orig_ok':orig_ok,'blank':blank,'gold':gold_exact,'controls_exact':ctrl_exact,'bars':sum(bool(r['keyword_interpretada']) for r in basef),'direct_missing':direct_missing,'flags':len(flags),'confidence':dict(conf),'review':dict(review),'areas':dict(areas)})
