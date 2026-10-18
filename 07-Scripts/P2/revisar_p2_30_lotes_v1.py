#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P2: revisão contextual conservadora das 25.050 keywords dos 30 lotes.
Requisitos: Python 3.10+; arquivos ZIP originais P0/P1 v2; p2_classificador_base.py.
Uso: python revisar_p2_30_lotes_v1.py --base /caminho/zip-lotes --qa /caminho/zip-auditoria --out /caminho/saida
Nenhuma consulta externa ou IA; regras inspecionáveis; não decide ambiguidades sem evidência.
"""
import argparse,csv,io,re,collections,zipfile,json,hashlib,unicodedata,random,sys
from pathlib import Path
from p2_classificador_base import classify as legacy, norm, TAX
P=argparse.ArgumentParser();P.add_argument('--base',default='/mnt/data/files/lotes-001-a-030-p0-p1-v2.zip');P.add_argument('--qa',default='/mnt/data/files/p1-v2-auditoria-relatorios-scripts.zip');P.add_argument('--out',default='/mnt/data/p2_work/out'); args=P.parse_args()
out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
base=zipfile.ZipFile(args.base);prior=zipfile.ZipFile(args.qa)
def read(z,name):return list(csv.DictReader(io.TextIOWrapper(z.open(name),encoding='utf-8-sig',newline=''),delimiter=';'))
def csvout(name,rows,cols):
 with (out/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=cols,delimiter=';',extrasaction='ignore');w.writeheader();w.writerows(rows)
def rx(t,pattern):return bool(re.search(pattern,t))
def set_result(c,klass,intent,rule,reason,status='VALIDADO',org='',dst='',fit='ferramenta',conf='alta'):
 c.update(classe=klass,intent=intent,rule=rule,reason=reason,status=status,origin=org,dest=dst,fit=fit,manual=('sim' if status=='PENDENTE_CONTEXTUAL' else 'não'),confidence=conf);return c
def tentative(c,reason,rule='sem_evidencia'):
 return set_result(c,None,None,rule,reason,'PENDENTE_CONTEXTUAL',fit='indeterminado',conf='baixa')
def reserve(c,klass,intent,rule,reason,fit='ferramenta'):
 return set_result(c,klass,intent,rule,reason,'VALIDADO_COM_RESSALVA',fit=fit,conf='média')
# Sanity: representation > number. Avoid effects of '/' stripped in source; never restore unobserved direction.
SOURCE_FIELDS=['tipo_registro','id_global','lote_id','familia_id','controle_id','Keyword','ocorrencias_origem','areas_origem','qtd_areas','Avg. monthly searches','Mudança em três meses','Mudança YoY','Competition','Competition (indexed value)','Top of page bid (low range)','Top of page bid (high range)']
PROTECTED={'tipo_registro','id_global','lote_id','familia_id','controle_id','Keyword','ocorrencias_origem','areas_origem','qtd_areas','Avg. monthly searches','Mudança em três meses','Mudança YoY','Competition','Competition (indexed value)','Top of page bid (low range)','Top of page bid (high range)','keyword_interpretada','reconstrucao_barra_status','tipos_reconstrucao_barra','confianca_reconstrucao_barra','observacao_reconstrucao_barra'}
# Original taxon labels in P1 are preserved through TAX; additions are kept explicit.
TAX=dict(TAX)
TAX.update({'price_collectible':('Fora de escopo','Numismática','Valor de moedas colecionáveis'), 'spreadsheet':('Fora de escopo','Software e planilhas','Excel e fórmulas'), 'vehicle':('Fora de escopo','Veículos','Consulta de veículo e produto'), 'nutrition':('Fora de escopo','Saúde','Nutrição e saúde'), 'solar_calc':('Energia','Energia solar','Dimensionamento solar'), 'geographic':('Fora de escopo','Geografia','Consulta geográfica'), 'work_info':('Trabalho','Legislação e direitos','Direitos trabalhistas e CLT'), 'crypto_price':('Finanças','Criptoativos','Conversão e cotação de criptomoedas'), 'historical_fx':('Finanças','Câmbio','Cotação histórica'), 'clock':('Datas','Duração','Horas, minutos e duração genérica')})
# Unit recognition: restrict to real engineering units and word boundaries.
UNITS=[('km/h','velocidade',r'km\s*/?\s*h\b|quilometros? por hora'),('m/s','velocidade',r'\bm\s*/\s*s\b|metros? por segundo'),('mph','velocidade',r'\bmph\b|milhas? por hora'),('m²','area',r'\bm\s*(?:2|²)\b|\bmetros? quadrad[oa]s?\b'),('cm²','area',r'\bcm\s*(?:2|²)\b|\bcentimetros? quadrad[oa]s?\b'),('ha','area',r'\bhectares?\b|\bha\b'),('acre','area',r'\bacres?\b'),('m³','volume',r'\bm\s*(?:3|³)\b|\bmetros? cubicos?\b'),('cm³','volume',r'\bcm\s*(?:3|³)\b|\bcentimetros? cubicos?\b'),('°F','temperatura',r'\bfahrenheit\b|\bfarenheit\b'),('°C','temperatura',r'\bcelsius\b'),('K','temperatura',r'\bkelvin\b'),('kWh','energia',r'\bkwh\b|\bquilowatt.?hora\b'),('Wh','energia',r'\bwh\b|\bwatt.?hora\b'),('kW','potencia',r'\bkw\b|\bkilowatts?\b'),('W','potencia',r'\bwatts?\b'),('cv','potencia',r'\bcavalos? vapor\b|\bcavalos? de potencia\b|\bcv\b'),('VA','potencia_aparente',r'\bkva\b|\bva\b'),('kV','tensao',r'\bkv\b|\bquilovolts?\b'),('V','tensao',r'\bvolts?\b|\bvoltagem\b'),('A','corrente',r'\bamperes?\b|\bamp\b|\bampere\b'),('Hz','frequencia',r'\bhz\b|\bhertz\b'),('rpm','frequencia_rotacao',r'\brpm\b'),('psi','pressao',r'(?<![a-z])psi\b'),('MPa','pressao',r'\bmpa\b'),('kPa','pressao',r'\bkpa\b'),('bar','pressao',r'\bbar\b'),('atm','pressao',r'\batm\b|\batmosferas?\b'),('mm','comprimento',r'(?<![a-z])mm\b|\bmilimetros?\b'),('cm','comprimento',r'(?<![a-z])cm\b|\bcentimetros?\b'),('km','comprimento',r'(?<![a-z])km\b|\bquilometros?\b'),('mi','comprimento',r'\bmilhas?\b'),('in','comprimento',r'\bpolegadas?\b|\binch(?:es)?\b'),('ft','comprimento',r'\bpes\b|\bfeet\b'),('m','comprimento',r'\bmetros?\b'),('t','massa',r'\btoneladas?\b'),('kg','massa',r'(?<![a-z])kg\b|\bquilos?\b|\bquilogramas?\b'),('µg','massa',r'\bmicrogramas?\b'),('mg','massa',r'(?<![a-z])mg\b|\bmiligramas?\b'),('g','massa',r'\bgramas?\b'),('lb','massa',r'\blbs?\b|\blibras? massa\b|\blibras?\b'),('L','volume',r'\blitros?\b'),('mL','volume',r'(?<![a-z])ml\b|\bmililitros?\b'),('gal','volume',r'\bgaloes?\b'),('GB','digital_byte',r'\bgb\b|\bgigabytes?\b'),('MB','digital_byte',r'\bmb\b|\bmegabytes?\b'),('TB','digital_byte',r'\btb\b|\bterabytes?\b'),('bit','digital_bit',r'\bbits?\b'),('byte','digital_byte',r'\bbytes?\b'),('ms','tempo',r'\bmilissegundos?\b'),('s','tempo',r'\bsegundos?\b'),('min','tempo',r'\bminutos?\b'),('h','tempo',r'\bhoras?\b'),('dia','tempo',r'\bdias?\b'),('semana','tempo',r'\bsemanas?\b'),('mes','tempo',r'\bmeses?\b'),('ano','tempo',r'\banos?\b')]
DEPS={'area':'area','volume':'volume','massa':'mass','comprimento':'length','pressao':'pressure','velocidade':'length','temperatura':'temp','tempo':'time','digital_byte':'bits','potencia':'power','energia':'power','tensao':'electric','corrente':'electric','potencia_aparente':'electric','frequencia':'frequency','frequencia_rotacao':'frequency'}
# currency units robustly separated; only explicit named pairs directional.
CUR=[('ARS',r'\b(?:peso[s]? argentino[s]?|ars)\b'),('CLP',r'\b(?:peso[s]? chileno[s]?|clp)\b'),('COP',r'\b(?:peso[s]? colombiano[s]?|cop)\b'),('MXN',r'\b(?:peso[s]? mexicano[s]?|mxn)\b'),('UYU',r'\b(?:peso[s]? uruguaio[s]?|uyu)\b'),('PYG',r'\b(?:guarani[s]?|pyg)\b'),('USD',r'\b(?:usd|d[oó]lar(?:es)?|dollar[s]?)\b'),('BRL',r'\b(?:brl|real|reais)\b'),('EUR',r'\b(?:eur|euro[s]?)\b'),('GBP',r'\b(?:gbp|libra[s]?(?: esterlinas?)?)\b'),('CHF',r'\b(?:chf|francos? suicos?)\b'),('JPY',r'\b(?:jpy|ienes?|yens?)\b'),('CAD',r'\b(?:cad|dolares? canadenses?)\b'),('CNY',r'\b(?:cny|yuans?)\b'),('KRW',r'\b(?:krw|wons?)\b'),('RUB',r'\b(?:rub|rublos?)\b'),('INR',r'\b(?:inr|rupias? indianas?)\b'),('MZN',r'\b(?:mzn|meticais?|metical)\b'),('BRL',r'\b(?:r\$)\b')]
AMBI_BASE= {'como converter','qual o valor de','corresponde a','como calcular','calcular on line','calculador virtual','calcule online','calculadora gratis','calculadora online','quanto fica','conta exata'}
# Extra safeguards applied before broad inherited P1 rules.
def classify_p2(e):
 t=norm(e['Keyword']); c=legacy({**e,'area_revisada':e['area_principal']})
 # Never silently change reconstruction semantics. Very short/underspecified forms are unresolved.
 if not t or t in AMBI_BASE or len(t)<3:return tentative(c,'Expressão genérica ou incompleta: faltam elementos para uma operação específica.','curto_ou_ambigua')
 # Distinct contexts that were erroneously interpreted as conversion, money or mathematics.
 if rx(t,r'\b(?:hr\s?v|cr\s?v|suv|suvs|honda|fiat|volkswagen|chevrolet|toyota|hyundai|carro[s]? a venda|veiculo[s]? usado[s]?|moto[s]? a venda|celular[s]? usado[s]?)\b') and not rx(t,r'\b(?:financiar|financiamento|emprestimo|parcelas?|entrada de|consumo de combustivel)\b'):
  return set_result(c,'vehicle','informacional','veiculo_produto','Busca por marca/modelo ou comércio automotivo, não conversor de unidade. ',fit='fora de escopo')
 if rx(t,r'\b(?:moeda\s+(?:de\s+)?(?:1|5|10|25|50)\s+(?:centavos?|real)|moeda\s+(?:de\s+)?1\s+real|moedas? antigas?|moeda comemorativa|moeda rara|colecionador|numismatica)\b') and rx(t,r'\b(?:valor|vale|preco|custa|raridade|colecao)\b'):
  return set_result(c,'price_collectible','consulta de preço/mercado','numismatica','Valor de moeda física colecionável, não taxa de câmbio.',fit='fora de escopo')
 if rx(t,r'\b(?:gestac(?:ao|ional)|gravidez|gravida|gestante|ultrassom|ultrasonografia|morfol[oó]gico|bebe|fet(?:o|al)|parto|sexagem|prenatal|obstetr|dpp|cesarea|maternidade|pre natal|licenca maternidade|contracao de treinamento|exame de glicose|teste de farmacia)\b'):
  return set_result(c,'health','fora de escopo','gestacao_prioritaria','Contexto explícito de gestação/saúde, não converter mês de calendário automaticamente.',fit='fora de escopo')
 if rx(t,r'\b(?:excel|planilhas?|word|powerpoint)\b') and rx(t,r'\b(?:formula|funcao|arredondar|somar|soma|celula|piv[oô]|macro|gr[aá]fico|baixar|modelo|tabela dinamica)\b') and not rx(t,r'\b(?:converter|transformar|conversor|passar)\b.*\b(?:pdf|csv|xlsx|xls|docx|pptx|jpg|png)\b'):
  return set_result(c,'spreadsheet','informacional','planilhas_operacoes','Busca por recurso/fórmula de planilha, não conversão de formato.',fit='conteúdo')
 if rx(t,r'\b(?:exercicios?|atividades?|prova[s]?|gabarito|lista de|resumo[s]?|teoria|definicao|conceito|questoes?|aula[s]?|educacao infantil|ensino medio|apostila[s]?)\b') and rx(t,r'\b(?:pdf|doc|docx|word)\b') and not rx(t,r'\b(?:converter|conversor|transformar)\b'):
  # Educational PDF/download is not a conversion request.
  if rx(t,r'\b(?:raiz|logarit|fracao|numeros|potenci|area|circunferencia|combinatori|probabilid|trigonomet|algebra|bhaskara|matematic|somar|subtrair|equac|express)'):
   return set_result(c,'math','informacional','educacao_pdf','Material didático de matemática em arquivo, não conversão de PDF.',fit='conteúdo')
  return tentative(c,'Material didático em arquivo, sem certeza quanto à disciplina ou ferramenta.','material_didatico')
 if rx(t,r'\b(?:nota[s]?|peso)\b.*\b(?:prouni|enem|vestibular|faculdade|prova|avaliacao|media escolar)\b') or rx(t,r'\b(?:prouni|enem|vestibular)\b.*\b(?:peso|nota|media)\b'):
  return set_result(c,'enem','informacional','educacao_notas','Nota escolar/ponderação, não peso físico nem moeda estrangeira.',fit='conteúdo')
 if rx(t,r'\b(?:cronograma|pedagogia|engenharia civil|materiais de construcao)\b') and rx(t,r'\b(?:media para passar|nota de corte|vestibular)\b'):
  return set_result(c,'enem','informacional','notas_universidade','Nota de corte educacional, não cálculo de área nem material.',fit='conteúdo')
 if rx(t,r'\b(?:preco|valor|cotacao)\b.*\b(?:ouro|grama do ouro|combustivel|diesel|gasolina|etanol|soja|arroz|milho)\b') and not rx(t,r'\b(?:converter|conversao)\b'):
  return set_result(c,'animal' if rx(t,r'boi|bezerro|arroba do boi') else 'fuelprice' if rx(t,r'gasolina|diesel|etanol|combustivel') else 'rate','cotação atual','preco_mercado','Consulta de preço de commodity/mercado, não multiplicador fixo.',fit='conteúdo')
 if rx(t,r'\b(?:agravada|pregao|cnpj|cpf|oficio|advogado|tributario|jurisprudencia)\b') and not rx(t,r'\bcalcul|simul'):
  return set_result(c,'juridic','informacional','juridico_geral','Termo jurídico não operacional.',fit='fora de escopo')
 # FX historical; no live conversion of archival prices.
 if rx(t,r'\b(?:dolar|usd|euro|libra|real|brl|peso argentino|taxa de cambio|cotacao)\b') and rx(t,r'\b(?:em|de|do|no|para|ano)\s+(?:19\d{2}|20(?:0\d|1\d|2[0-6]))\b|\bhistoric[oa]\b') and not rx(t,r'\b(?:converter|conversao)\b'):
  return set_result(c,'historical_fx','cotação histórica','cambio_historico','Cotação cambial de período histórico, não cotação atual.',fit='conteúdo')
 if rx(t,r'\b(?:bitcoin|btc|ethereum|eth|criptomoed|criptoativo|binance|coingecko)\b'):
  intent='cotação atual' if rx(t,r'preco|cotac|quanto vale|valor|price') else 'informacional'
  if rx(t,r'\b(?:converter|conversao|para reais|para dolar)\b'):
   return reserve(c,'crypto_price','cálculo contextual','cripto_dinamico','Conversão de criptoativo requer ativo, contraparte, rede/cotação e horário.','ferramenta')
  return set_result(c,'crypto_price',intent,'cripto_consulta','Consulta informacional/mercado de criptoativo, não unidade física.',fit='conteúdo')
 # Physical money must not be mistaken for force/mass, and education/business is distinct.
 if rx(t,r'\b(?:libra forca|libras? forca|lbf|pounds? per square|libra peso)\b'):
  return reserve(c,'pressure','cálculo contextual','libra_fisica','Libra de força/massa física não é GBP; solicitar dimensão e unidade destino.')
 if rx(t,r'\b(?:trabalhar|trabalho|jornada|carga horaria|escala)\b') and rx(t,r'\b(?:horas?|dias?|semana)\b'):
  return reserve(c,'worktime','cálculo contextual' if rx(t,r'calcul|quanto|valor|salario') else 'informacional','horas_trabalhadas','Horas de trabalho/jornada não são automaticamente conversão de duração.',fit='conteúdo')
 if rx(t,r'\blibras?\b') and rx(t,r'\b(?:kg|quilos?|gramas?|massa|peso corporal|conversao de peso|quilogramas?)\b'):
  return reserve(c,'mass','cálculo contextual','libra_massa','Libra como unidade de massa por contexto de quilogramas/gramas; não GBP.')
 # Currency pair interpreter: require recognised codes on both ends, never guess for unspecific "peso".
 found=[]
 for code,pat in CUR:
  for m in re.finditer(pat,t):
   if not any(not(m.end()<=a or m.start()>=b) for a,b,_ in found):found.append((m.start(),m.end(),code))
 found.sort()
 if len(found)>=2 and rx(t,r'\b(?:dolar|dollar|usd|euro|eur|brl|real|reais|peso|ars|clp|mxn|gbp|libra|franco|jpy|yen|rub|rublo|inr|rupia|metical|chf)\b'):
  left,right=found[0],found[1]
  # 'real' in informal speech requires explicit monetary cue or another named currency.
  if left[2]!=right[2]:
   cn=t[left[1]:right[0]]
   if re.search(r'\b(?:para|em|to|en|a)\b',cn) and not rx(cn,r'\b(?:x|vs|versus|e)\b'):
    if not rx(t,r'\b(?:qual pais|de qual pais|historia|origem da moeda)\b'):
     return set_result(c,'currency','conversão direta','cambio_par_explicito','Par de códigos cambiais e direção linguística explícitos.',org=left[2],dst=right[2])
   return reserve(c,'currency','cálculo contextual','cambio_par_bidir','Dois códigos cambiais reconhecidos; não presumir direção.')
 if rx(t,r'\b(?:pesos?)\b') and rx(t,r'\b(?:moeda|cambio|converter|conversao|reais|dolar|euro)\b') and not rx(t,r'\b(?:argentin|chilen|colombi|mexican|uruguai)'):
  return reserve(c,'currency','cálculo contextual','peso_pais_ausente','Peso sem país emissor; origem/destino só se resolvem após escolher moeda.')
 # Legal / employment queries where original P1 fallback might say a direct arithmetic calculation.
 if rx(t,r'\b(?:clt|trabalhista|empregador|rescisao|fgts|inss|irrf|seguro desemprego|aviso previo|ferias|salario|remuneracao|jornada|hora extra|adicional noturno|vale transporte|descanso semanal)\b'):
  if rx(t,r'\b(?:descontado do salario base|qual a lei|o que e|quantos dias|quem tem direito|prazo|limite|carga horaria|horario da|como funciona|quando recebo|quando posso|legisla[cç]ao|tabela|artigo|forma de pagamento)\b'):
   return set_result(c,'work_info','informacional','regra_trabalhista','Pergunta de regra/prazo trabalhista, não cálculo direto.',fit='conteúdo')
  if rx(t,r'\b(?:calcular|calculo|calculadora|simular|simulacao|quanto recebo|valor a receber|valor da hora)\b'):
   key='rescision' if rx(t,r'rescisao|aviso previo') else 'fgts' if 'fgts' in t else 'thirteenth' if rx(t,r'decimo terceiro|13 salario') else 'worktime' if rx(t,r'hora extra|valor da hora|horas trabalhadas') else 'payroll'
   return reserve(c,key,'cálculo contextual','trabalho_contextual','Cálculo depende de regime, período, salário-base, alíquotas e legislação aplicável.')
  if c.get('classe') not in ('fgts','rescision','payroll','workrights','worktime','workbenefit','extrahour','workleave','retirement','thirteenth'):
   return reserve(c,'work_info','informacional','trabalho_informativo','Assunto trabalhista sem operação determinística identificada.',fit='conteúdo')
 # File operation: only if explicit in query and supported file tokens.
 formats=['pdf','png','jpg','jpeg','gif','mp3','mp4','xls','xlsx','csv','ppt','pptx','doc','docx','dwg','svg','ico','epub','zip','rar','webp','wav','avi','heic','ofx']
 fm=[(m.start(),m.end(),m.group()) for name in formats for m in re.finditer(r'\b'+name+r'\b',t)]
 fm.sort(key=lambda x:x[0]);fmt=[x[2] for x in fm]
 file_intent=rx(t,r'\b(?:converter|conversor|conversao|transformar|converter? online|passar|salvar|exportar|gerar|de .* para)\b')
 if fm and (file_intent or rx(t,r'\b(?:youtube|imagem|video|audio)\b.*\b(?:mp3|mp4|jpg|pdf)\b')):
  if len(set(fmt))>=2:
   # Format pair not automatically actual direction absent a clear connector.
   if rx(t,r'\b(?:para|em|to)\b'):
    return set_result(c,'file','conversão de arquivo/mídia','formato_direcional','Formatos de origem e destino explicitados; conversão de arquivo.',fit='ferramenta')
   return reserve(c,'file','conversão de arquivo/mídia','formato_bidir','Dois formatos reconhecidos; pode faltar direção ou operação específica.')
  if len(fmt)==1 and rx(t,r'\b(?:converter|conversor|conversao|transformar|passar)\b'):
   return reserve(c,'file','conversão de arquivo/mídia','formato_incompleto','Formato citado, mas origem/destino ou operação não estão completos.')
 if 'pdf' in fmt and not file_intent:return set_result(c,'file','informacional','pdf_referencia','PDF citado como documento/referência, não há pedido de conversão.',fit='conteúdo')
 # Physical units, with explicit dimension checking and grammatical direction.
 matches=[]
 for label,dim,pat in UNITS:
  for m in re.finditer(pat,t):
   # Do not treat 'valor de 5 anos' as converter without context; handled by rules below.
   if not any(m.start()<a[1] and m.end()>a[0] for a in matches):matches.append((m.start(),m.end(),label,dim))
 matches.sort()
 # Particular standalone units often need a target, never infer it.
 if len(matches)>=2 and rx(t,r'\b(?:converter|conversao|conversor|passar|transformar|quantos?|quantas?|equivale|sao|em|para|por|x)\b'):
  left,right=matches[:2];dims={left[3],right[3]};org,dst=left[2],right[2]
  # Explicit non-equivalent dimensional pairs: require physical parameters.
  if len(dims)>1:
   if dims=={'massa','volume'}:return reserve(c,'culinary','cálculo contextual','densidade_fisica','Massa↔volume exige densidade/ingrediente; não é conversão universal.')
   if dims & {'tensao','corrente','potencia','potencia_aparente'} and dims <= {'tensao','corrente','potencia','potencia_aparente'}:return reserve(c,'electric','cálculo contextual','potencia_eletrica','Entre V, A, VA e W são necessárias corrente/tensão e, quando aplicável, fator de potência.')
   if dims == {'energia','potencia'}:return reserve(c,'power','cálculo contextual','energia_potencia','kWh↔kW requer duração; não converter diretamente.')
   if dims == {'area','volume'}:return reserve(c,'wall','cálculo contextual','area_volume','Área↔volume exige espessura/altura; não é fator universal.')
   if dims == {'area','comprimento'}:return reserve(c,'area','cálculo contextual','area_comprimento','Comprimento↔área exige largura ou geometria; não é conversão direta.')
   if dims=={'digital_byte','digital_bit'}:return reserve(c,'bits','cálculo contextual','bits_bytes','A relação bit/byte é fixa mas prefixos e contexto de velocidade/armazenamento precisam ser identificados.')
   return tentative(c,'Unidades de dimensões diferentes; falta relação física explícita e/ou texto pode não representar uma conversão.','dimensoes_incompativeis')
  if org==dst:return reserve(c,DEPS.get(left[3],'generic'),'informacional','mesma_unidade','Mesma unidade repetida; não assumir conversão útil.')
  if left[3]=='tempo' and {org,dst}&{'mes','semana'} and not {org,dst}<={'dia','semana','h','min','s','ms'}:
   return reserve(c,'time','cálculo contextual','semana_mes','Semanas e meses exigem definição de mês, gestacional ou civil; não fator fixo universal.')
  connector=t[left[1]:right[0]]
  directional=bool(re.search(r'\b(?:para|em|to|en)\b',connector)) and not rx(connector,r'\b(?:x|vs|versus|e)\b')
  if rx(t,r'\bquantos?\s+'+re.escape(right[2])+r'\b.*\btem\b'):
   directional=False # Cannot assume same direction in flipped question
  if directional:
   return set_result(c,DEPS.get(left[3],'generic'),'conversão direta','unidades_compativeis_direcao','Duas unidades da mesma dimensão com relação direcional explícita.',org=org,dst=dst)
  return reserve(c,DEPS.get(left[3],'generic'),'cálculo contextual','unidades_compativeis_bidir','Par de unidades compatíveis, mas sentido não explicitado; exigir seleção.')
 # prioritize context of date and time that is actually dates not converter
 if rx(t,r'\b(?:quantos dias faltam|entre duas datas|calcular prazo|diferen[cç]a entre datas|somar dias a data|dias uteis)\b'):
  return reserve(c,'date','cálculo contextual','data_parametros','Cálculo de datas requer data inicial/final e convenção de dias úteis.')
 if rx(t,r'\b(?:quantas semanas|quantos meses|semanas em meses|meses em semanas)\b') and not rx(t,r'gesta|gravidez|bebe'):
  return reserve(c,'time','cálculo contextual','meses_temporais','Conversão temporal depende de calendário versus mês de duração média.')
 # Mathematical educational query versus calculator endpoint.
 if rx(t,r'\b(?:exercicios?|atividades?|questoes?|aula[s]?|teoria|exemplos?|conceito[s]?|resumo[s]?|livro|escola|ensino|enem|ano escolar|gabarito|lista|5 ano|6 ano|7 ano|8 ano|9 ano)\b'):
  if rx(t,r'\b(?:fracao|fracoes|expressao|express[oõ]es|potencia|potenciacao|radicia[cç]ao|raiz|logaritmo|combinatoria|permutacao|probabilidade|geometria|volume|area|media|matematica|bhaskara|circunferencia|pitagoras|trigonometria|equacao|soma|subtracao|divisao|multiplicacao)\b'):
   key='prob' if rx(t,r'probabilidade|permutacao|combinatoria|arranjo') else 'power_math' if rx(t,r'raiz|logarit|potencia|radicia') else 'geom' if rx(t,r'circunferencia|geometr|pitagoras|triangulo|area') else 'frac' if rx(t,r'frac') else 'math'
   return set_result(c,key,'informacional','ensino_nao_calculadora','Consulta educacional/didática sem pedido operacional inequívoco.',fit='conteúdo')
 # Financial simulation with missing params.
 if rx(t,r'\b(?:investimento|aplicar dinheiro|tesouro direto|cdb|cdi|juros compostos|juros simples|parcelamento|financiamento|emprestimo)\b'):
  if rx(t,r'\b(?:simular|simulacao|simulador|calculadora|calcular)\b'):
   key='loan' if rx(t,r'emprestimo|credito pessoal') else 'finance' if 'financiamento' in t else 'interest' if 'juros' in t else 'investment'
   return reserve(c,key,'simulação/projeção','simulacao_parametrica','Taxa, prazo, valor/índice e calendário dependem dos dados do usuário.')
 # Clean, conservative inherited classifications: guard known unreliable rules.
 rule=c.get('rule',''); status=c['status']; klass=c.get('classe'); intent=c.get('intent')
 if status=='PENDENTE_CONTEXTUAL':
  # Targeted extra cases safely recoverable.
  if rx(t,r'\b(?:permutacao|fatorial|mdc|mmc|mediana|amplitude|bhaskara|equacao de segundo grau|equacao de 2 grau|regra de tres|raiz cubica)\b'):
   key='prob' if 'permutac' in t else 'stat' if rx(t,r'mediana|amplitude') else 'linear' if 'equac' in t or 'bhaskara' in t else 'prime' if rx(t,r'mdc|mmc|fatorial') else 'frac' if 'regra de tres' in t else 'power_math'
   return reserve(c,key,'cálculo contextual' if rx(t,r'calcul|quanto|resultado') else 'informacional','matematica_especifica','Objeto matemático identificável; parâmetros/expressão podem não constar.',fit='ferramenta' if rx(t,r'calcul|quanto|resultado') else 'conteúdo')
  if rx(t,r'\b(?:carga horaria|banco de horas|folga|descanso semanal|escala 6x1|escala 12x36)\b'):
   return set_result(c,'workrights','informacional','jornada_regras','Consulta de regra de jornada e descanso; não converter horas para moeda.',fit='conteúdo')
  if rx(t,r'\b(?:dolares?|dolar|euro|libra esterlina|peso[s]? argentin[oa]s?)\b') and rx(t,r'\b(?:cambio|convert|cotacao|para|em real|em reais)\b'):
   return reserve(c,'currency','cálculo contextual','cambio_par_incompleto','Moeda/serviço de câmbio identificado, mas par ou direção pode estar incompleto.')
  return tentative(c,'Não há contexto suficiente para garantir classificação sem revisão contextual adicional.','contexto_ainda_insuficiente')
 # Guard false positives from P1 broad fallbacks.
 if rule in {'cambio_direcional','unidades_direcionais'}:
  return tentative(c,'Regra herdada de direção sem verificação dimensional/monetária P2 suficiente.','direcao_nao_verificada')
 if rule=='conversao_arquivo':
  return tentative(c,'Arquivo/formato detectado por regra ampla, mas não houve pedido explícito verificado.','arquivo_amplo')
 if rule in {'moeda_isolada','cotacao_moeda','moeda_sem_par','peso_sem_pais','cotacao_generica'}:
  # Currency terms may be false positives (real-world usage of real, weight, force pounds).
  if rx(t,r'\b(?:realidade|mundo real|vida real|saldo real|peso corporal|peso ideal|massa corporal|libra forca|libra peso)\b') or rx(t,r'\b(?:moeda do real|valor real de|custo real de)\b'):
   return tentative(c,'Ambiguidade lexical: palavra ligada a moeda pode significar outra grandeza.','falso_positivo_cambio')
  # historical query checked above; remaining quote may be historic with date not caught.
  if rx(t,r'\b(?:19\d\d|20\d\d|colecion|antiga|comemorativa)\b'):
   return reserve(c,'quote','informacional','cotacao_data_ambigua','Pode ser cotação antiga, numismática ou valor comparativo: requer contexto.',fit='conteúdo')
  if rx(t,r'\b(?:converter|conversor|cambio|cotacao|dolar|usd|eur|euro|libra esterlina|peso argentino|peso chileno|peso mexicano|preco moeda)\b'):
   return reserve(c,'currency' if rx(t,r'convert|cambio|conversor') else 'quote','cálculo contextual' if rx(t,r'convert|cambio|conversor') else 'cotação atual','cambio_contexto','Intenção cambial provável, mas origem/destino ou cotação não estão completamente explicitados.',fit='ferramenta' if rx(t,r'convert|cambio|conversor') else 'conteúdo')
  return tentative(c,'Termo monetário isolado sem evidência cambial inequívoca.','termo_monetario_solto')
 if rule in {'unidades_bidirecionais','grandeza_sem_par','unidade_isolada'}:
  if rx(t,r'\b(?:tabela de medidas|conversao|converter|conversor|quanto[s]?|medida[s]?|equivale|para| em )\b'):
   return reserve(c,klass,intent,'unidade_contextual','Unidade física mencionada; parâmetros/par ou sentido não totalmente especificados.')
  return tentative(c,'Unidade mencionada sem pedido de conversão suficiente.','unidade_solitaria')
 if rule in {'semanas_meses_contextuais','culinaria_sem_ingrediente','densidade_obrigatoria','eletrica_contextual','colher_volume'}:
  return reserve(c,klass,intent,rule,c['reason'])
 if rule=='calculadora_generica':
  return reserve(c,klass,intent,rule,c['reason'])
 # Generic context often means a named family, not an operative conversion; maintain qualified.
 if rule=='conversor_generico':
  return reserve(c,'generic','cálculo contextual','conversor_sem_par','Conversor genérico sem unidade/par suficiente: solicitar seleção.')
 # Decisive topic signals only. Low-risk informational categories preserve fit.
 if rule in {'educacao_enem','saude_gestacao','planejamento_financeiro','direito_trabalhista','beneficio_previdenciario','mercado_pecuario','vale_a_pena','marca_produto','juridico','salario_profissao','educacao','numeracao','previdencia_servico'}:
  return c
 if rule in {'geometria_plana','probabilidade','potencias_logaritmos','estatistica','fracoes_decimais','sequencias_matematicas','aritmetica_numeros','algebra','trigonometria'} and rx(t,r'\b(?:exercicios?|atividade|exemplo[s]?|lista|teoria|formulas?|resumo|conceito)\b'):
  return set_result(c,klass,'informacional','matematica_didatica','Conteúdo educativo, não ferramenta calculadora operacional.',fit='conteúdo')
 if rule=='divida_tributaria' and not rx(t,r'\b(?:parcela|parcelamento|parcelar|mei|das|sefaz|pgfn|receita federal|iptu|icms|tributo|divida|negocia)\b'):
  return tentative(c,'Correspondência herdada de tributos sem pistas lexicais tributárias reais.','tributos_sem_contexto')
 if rule=='trigonometria' and rx(t,r'\b(?:converter|conversao|transformar)\b.*\b(?:graus?|radianos?)\b'):
  return reserve(c,'trig','cálculo contextual','angulo_conversao','Conversão angular clara, embora unidade/direção exatas precisem ser verificadas.')
 if rule in {'financiamento','rescisao','juros_financeiros','fgts','jornada_trabalho','jornada_adicionais','investimentos'} and intent in {'cálculo direto','simulação/projeção','cálculo contextual'}:
  return reserve(c,klass,'cálculo contextual' if rule not in {'financiamento','investimentos'} else 'simulação/projeção','parametros_dinamicos','Cálculo dependente de data, regras, taxas e parâmetros definidos pelo usuário.')
 # For broad inherited evidence, mark qualified rather than certain.
 if rule in {'conversao_arquivo','transformador_produto','medidas_culinarias','grandeza_fisica'}:
  return reserve(c,klass,intent,'revisao_ampla',c.get('reason','Necessário contexto adicional.'))
 # Structural low-risk signals. Retain inherited rule; report that this is not independent human review.
 return c

q=read(prior,'fila-30-lotes-p0-p1-v2.csv');assert len(q)==52046
p2=[x for x in q if x['prioridade']=='P2'];assert len(p2)==25050
ids={x['id_global'] for x in p2};assert len(ids)==25050
# Index base without modifying anything yet.
base_rows={};byid={}
for k in range(1,31):
 name=f'lotes/lote-{k:03d}-p0-p1-v2.csv';r=read(base,name);base_rows[k]=r
 for row in r:
  if row['tipo_registro']=='base':
   ident=row['id_global'];assert ident not in byid;byid[ident]=(k,row)
assert len(byid)==294905
assert ids <= set(byid)
assert sum(sum(x['tipo_registro']=='controle' for x in rows) for rows in base_rows.values())==2190
assert len({row['id_global'] for row in q})==len(q)
DEC=[]; PATCH=[];cross=collections.Counter()
for e in p2:
 k,original=byid[e['id_global']]
 assert original['Keyword']==e['Keyword'] and original['lote_id']==f'L{k:03d}'
 old=original.copy();c=classify_p2({**e,**original})
 status=c['status'];classname=c.get('classe')
 d={**e,'regra_p2':c['rule'],'status_p2':status,'justificativa_p2':c['reason'],'adequacao_portal_p2':c['fit'], 'confianca_p2':c['confidence'], 'area_final_p2':TAX[classname][0] if classname else old['area_principal'],'cluster_final_p2':TAX[classname][1] if classname else old['cluster'],'subcluster_final_p2':TAX[classname][2] if classname else old['subcluster'],'tipo_intencao_final_p2':c['intent'] or old['tipo_intencao'],'unidade_origem_final_p2':c['origin'],'unidade_destino_final_p2':c['dest'],'classificacao_alterada_p2':'não'}
 if status!='PENDENTE_CONTEXTUAL':
  it=c['intent']
  title=(('Converter: ' if it=='conversão direta' else 'Consultar informação: ' if it in ('informacional','tabela/referência') else 'Simular: ' if it=='simulação/projeção' else 'Calcular: ' if it in ('cálculo direto','cálculo contextual') else 'Consultar: ')+d['subcluster_final_p2'])
  updates={'area_principal':d['area_final_p2'],'cluster':d['cluster_final_p2'],'subcluster':d['subcluster_final_p2'],'tipo_intencao':d['tipo_intencao_final_p2'],'intencao_principal':title,'confianca':c['confidence'],'revisao_manual':'não','justificativa_curta':('P2 '+c['rule']+': '+c['reason'])[:450]}
  # Only set directional metadata for explicit compatible direct conversion.
  if c['intent']=='conversão direta' and c['origin'] and c['dest'] and c['origin']!=c['dest']:
   updates.update(unidade_origem=c['origin'],unidade_destino=c['dest'],direcao_conversao=c['origin']+' → '+c['dest'])
  else:
   updates.update(unidade_origem='',unidade_destino='',direcao_conversao='')
  for col,v in updates.items(): original[col]=v
  if any(original[col]!=old[col] for col in original):
   d['classificacao_alterada_p2']='sim'
   cols={key:{'antes':old[key],'depois':original[key]} for key in original if original[key]!=old[key]}
   PATCH.append({'id_global':e['id_global'],'lote':e['lote'],'Keyword':e['Keyword'],'status_p2':status,'regra_p2':c['rule'],'antes_area':old['area_principal'],'depois_area':original['area_principal'],'antes_intencao':old['tipo_intencao'],'depois_intencao':original['tipo_intencao'],'campos_alterados':' | '.join(cols.keys()),'diff_json':json.dumps(cols,ensure_ascii=False)})
 if status=='PENDENTE_CONTEXTUAL':
  assert original==old
 cross[(status,c['rule'])]+=1
 DEC.append(d)
# Queue only P2 reviewed, preserve P0 and P1 statuses/decisions.
idx={d['id_global']:d for d in DEC}
for e in q:
 if e['id_global'] not in idx:continue
 d=idx[e['id_global']];e['status_revisao']={'VALIDADO':'REVISADO_P2_REGRA','VALIDADO_COM_RESSALVA':'P2_RESSALVA','PENDENTE_CONTEXTUAL':'P2_PENDENTE'}[d['status_p2']]
 e['decisao_final']='CORRIGIR' if d['classificacao_alterada_p2']=='sim' else ('MANTER_REGRA' if d['status_p2']!='PENDENTE_CONTEXTUAL' else 'MANTER_PENDENTE')
 e['observacao_revisor']=('P2 '+d['regra_p2']+': '+d['justificativa_p2'])[:800]
 if d['status_p2']!='PENDENTE_CONTEXTUAL':
  e['area']=d['area_final_p2'];e['cluster']=d['cluster_final_p2'];e['subcluster']=d['subcluster_final_p2'];e['tipo_intencao_atual']=d['tipo_intencao_final_p2'];e['confianca_atual']=d['confianca_p2']
# Regression: unchanged rows byte-identical logical fields and controls.
qarep=[];c_all=collections.Counter();source_hash=hashlib.sha256();result_hash=hashlib.sha256()
for k in range(1,31):
 name=f'lotes/lote-{k:03d}-p0-p1-v2.csv';ref=read(base,name);current=base_rows[k]
 assert len(ref)==len(current)
 delta=0;base_ct=0;ctl_ct=0;unchanged=0
 for a,b in zip(ref,current):
  assert all(a[f]==b[f] for f in PROTECTED),'Protected values altered'
  source_hash.update(('\x1e'.join(a[f] for f in SOURCE_FIELDS)+'\n').encode())
  result_hash.update(('\x1e'.join(b[f] for f in SOURCE_FIELDS)+'\n').encode())
  if a['tipo_registro']=='controle':ctl_ct+=1;assert a==b
  else:base_ct+=1
  if a['id_global'] not in ids:assert a==b,'non-P2 changed';unchanged+=1
  elif a!=b:delta+=1
 assert sum(d['lote']==f'{k:03d}' and d['classificacao_alterada_p2']=='sim' for d in DEC)==delta
 c_all['base']+=base_ct;c_all['controles']+=ctl_ct;c_all['alteracoes']+=delta
 qarep.append({'lote':f'L{k:03d}','base':base_ct,'controles':ctl_ct,'nao_p2_preservados':unchanged,'p2_alterados':delta,'status':'PASSOU'})
assert source_hash.hexdigest()==result_hash.hexdigest();assert c_all['base']==294905 and c_all['controles']==2190
assert c_all['alteracoes']==len(PATCH)
status=collections.Counter(d['status_p2'] for d in DEC)
print('TOTAL',len(DEC),'STATUS',dict(status),'PATCH',len(PATCH),'regressao',dict(c_all))
# Independent verifiable audit rows and original field schema.
cols=list(DEC[0].keys());csvout('p2-validacao-semantica-25050.csv',DEC,cols)
csvout('p2-pendencias.csv',[d for d in DEC if d['status_p2']=='PENDENTE_CONTEXTUAL'],cols)
csvout('p2-ressalvas.csv',[d for d in DEC if d['status_p2']=='VALIDADO_COM_RESSALVA'],cols)
csvout('p2-patches.csv',PATCH,list(PATCH[0]) if PATCH else ['id_global'])
csvout('fila-30-lotes-p0-p1-p2-v1.csv',q,list(q[0]))
csvout('qa-regressao-30-lotes-p2.csv',qarep,list(qarep[0]))
# output ZIP immutable originals unchanged (new separate namespace)
with zipfile.ZipFile(out/'lotes-001-a-030-p0-p1-p2-v1.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for k,rs in base_rows.items():
  name=f'lotes/lote-{k:03d}-p0-p1-p2-v1.csv';s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=list(rs[0]),delimiter=';',lineterminator='\n');w.writeheader();w.writerows(rs);z.writestr(name,'\ufeff'+s.getvalue())
summary={'origem':'P0 + P1 v2','total_p2':len(DEC),'status':dict(status),'alteracoes':len(PATCH),'registros_base':c_all['base'],'controles':c_all['controles'],'hash_colunas_protegidas':source_hash.hexdigest(),'regras':dict(collections.Counter(d['regra_p2'] for d in DEC)),'validacao':'regras contextuais automatizadas, nao revisao humana independente'}
(out/'resumo-p2-v1.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
md=f'''# Auditoria P2 — triagem contextual e validação determinística

- P2 original: **{len(DEC):,}** keywords nos 30 lotes.
- Validadas por regra: **{status['VALIDADO']:,}**.
- Com ressalvas operacionais/contextuais: **{status['VALIDADO_COM_RESSALVA']:,}**.
- Ainda pendentes por evidência insuficiente: **{status['PENDENTE_CONTEXTUAL']:,}**.
- Registros com campos analíticos alterados: **{len(PATCH):,}**.
- Base preservada: **{c_all['base']:,}** keywords; controles preservados: **{c_all['controles']:,}**.
- Assinatura SHA256 de todas as colunas protegidas antes/depois: `{source_hash.hexdigest()}`.

## Método e limitações

Análise feita por regras de linguagem e contexto, não por leitura humana independente de 25 mil termos. Os estados VALIDADO e COM_RESSALVA refletem apenas confiança das regras e **não equivalem a aprovação editorial definitiva**. Casos incertos permanecem na fila `p2-pendencias.csv`; ajustes são propostos somente quando há evidência textual, sem adivinhar parâmetros, moeda, unidade ou direção. As classificações P0 e P1, os 2.190 controles, todos os dados Ads e colunas de reconstrução de barras foram preservados. Nunca se deve aplicar taxa fixa para converter massa↔volume, comprimento↔área, V↔W, nem tratar menções a PDF didático como conversão de arquivos.

## Pistas de regressão e reexecução

`qa-regressao-30-lotes-p2.csv` contém os 30 lotes com status PASSOU; `p2-patches.csv` apresenta os campos antes/depois; `resumo-p2-v1.json` discrimina regras, decisões e SHA256. Os scripts executáveis `revisar_p2_30_lotes_v1.py` e `p2_classificador_base.py` reproduzem a trilha a partir dos ZIPs P0/P1 v2, e `gerar_planilha_p2_v1.py` gera a planilha. A base original não foi sobrescrita.

## Escopo

P2 não implica revisão independente de P0/P1 nem P3. A validação é uma etapa de triagem e saneamento com controles de integridade. A próxima passada útil é revisão amostral estratificada por regra de maior volume e revisão contextual manual de pendências, antes de usar as decisões como taxonomia de produção.
'''
(out/'relatorio-p2-v1.md').write_text(md,encoding='utf-8')
# Sample stratified QA of category status/rules
sample=[];by=collections.defaultdict(list)
for d in DEC:by[(d['regra_p2'],d['status_p2'])].append(d)
rng=random.Random(20261017)
for ky,items in sorted(by.items(),key=lambda x:-len(x[1])):
 for row in rng.sample(items,min(5,len(items))): sample.append({key:row[key] for key in ['id_global','Keyword','area','area_final_p2','tipo_intencao_atual','tipo_intencao_final_p2','status_p2','regra_p2','justificativa_p2']})
csvout('amostra-estratificada-p2.csv',sample,list(sample[0]))