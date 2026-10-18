#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Segunda triagem semântica conservadora dos 8.813 pendentes P2.
Executar: python validar_pendencias_p2_v2.py --base /caminho/lotes-001-a-030-p0-p1-p2-v1.zip --p2 /caminho/p2-validacao-semantica-25050.csv --fila /caminho/fila-30-lotes-p0-p1-p2-v1.csv --out /pasta
Biblioteca padrão Python; preserva todos os dados-fonte, controles, decisões P0/P1;
regras transparentes; status de 'validado' significa confiança heurística, não QA editorial humana.
"""
import argparse, csv, io, re, json, hashlib, collections, zipfile, unicodedata, random
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('--base', default='/mnt/data/p2_work/out/lotes-001-a-030-p0-p1-p2-v1.zip')
parser.add_argument('--p2', default='/mnt/data/p2_work/out/p2-validacao-semantica-25050.csv')
parser.add_argument('--fila', default='/mnt/data/p2_work/out/fila-30-lotes-p0-p1-p2-v1.csv')
parser.add_argument('--out', default='/mnt/data/p2_validation_v2/out')
args=parser.parse_args(); out=Path(args.out);out.mkdir(parents=True,exist_ok=True)

def readcsv(fp):
 with open(fp,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def readzip(z,key):
 with z.open(key) as f:return list(csv.DictReader(io.TextIOWrapper(f,encoding='utf-8-sig',newline=''),delimiter=';'))
def writecsv(fp,rows,fields):
 with open(fp,'w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,delimiter=';',extrasaction='ignore',lineterminator='\n');w.writeheader();w.writerows(rows)
def norm(s):
 return re.sub(r'\s+',' ',''.join(c for c in unicodedata.normalize('NFKD',s.lower()) if not unicodedata.combining(c))).strip()
def yes(t,p):return bool(re.search(p,t))

def result(tax, intent, status, rule, why, fit='ferramenta', origin='',dest=''):
 assert status in ('RESOLVIDO_ALTA','RESOLVIDO_COM_RESSALVA')
 return dict(tax=tax,intent=intent,status=status,rule=rule,why=why,fit=fit,origin=origin,dest=dest)
# taxonomia original P2 v1 complementada por novas classes de alta precisão
TAX={
 'health':('Fora de escopo','Saúde','Saúde/gestação'),
 'coin':('Fora de escopo','Numismática','Moedas e colecionáveis'),
 'product':('Fora de escopo','Comércio','Produtos e compras'),
 'ecommerce':('Fora de escopo','Comércio e promoções','Cupons e ofertas'),
 'bank':('Fora de escopo','Serviços bancários','Abertura de conta e aplicativos'),
 'education':('Fora de escopo','Educação','Materiais escolares e atividades'),
 'geography':('Fora de escopo','Geografia','Localizações e rotas'),
 'agri':('Fora de escopo','Agricultura','Produtividade agropecuária'),
 'fx':('Conversores','Moedas e câmbio','Conversão entre moedas'),
 'quote':('Finanças','Câmbio','Cotação atual'),
 'investment':('Finanças','Investimentos','Rendimento geral'),
 'fixed':('Finanças','Investimentos','CDB, CDI e renda fixa'),
 'loan':('Finanças','Crédito','Empréstimos'),
 'finance':('Finanças','Crédito','Financiamentos'),
 'debt':('Finanças','Dívidas e cartões','Cartão, dívida e parcelamento'),
 'budget':('Finanças','Planejamento financeiro','Orçamento e reserva'),
 'rate':('Finanças','Correção monetária','Inflação e índices'),
 'price':('Finanças','Custos e precificação','Precificação de produtos'),
 'moneytool':('Finanças','Ferramentas financeiras','Calculadora financeira e HP12C'),
 'payroll':('Trabalho','Remuneração','Salário líquido e bruto'),
 'worktime':('Trabalho','Remuneração','Valor da hora e dias trabalhados'),
 'extrahour':('Trabalho','Jornada e adicionais','Hora extra'),
 'rights':('Trabalho','Legislação e direitos','Direitos trabalhistas e CLT'),
 'fgts':('Trabalho','FGTS','FGTS e multa rescisória'),
 'workleave':('Trabalho','Afastamentos','Licenças e afastamentos'),
 'thirteenth':('Trabalho','Décimo terceiro','Décimo terceiro salário'),
 'rescision':('Trabalho','Rescisão','Rescisão trabalhista'),
 'retirement':('Trabalho','Previdência e benefícios','Previdência e benefícios do INSS'),
 'wall':('Construção','Metragem','Área aplicada à construção'),
 'roof':('Construção','Telhados','Telhas, inclinação e cobertura'),
 'concrete':('Construção','Concreto','Concreto, cimento, areia e brita'),
 'revest':('Construção','Pisos e revestimentos','Pisos e revestimentos'),
 'building_cost':('Construção','Custos e orçamento','Orçamento e custo de obra'),
 'electric':('Conversores','Eletricidade e eletrônica','Grandezas elétricas'),
 'energy':('Energia','Aparelhos elétricos','Consumo de aparelhos'),
 'energy_cost':('Energia','Consumo elétrico','Custo do kWh e consumo'),
 'solar':('Energia','Energia solar','Dimensionamento solar'),
 'drive':('Energia','Combustíveis','Custo de viagem'),
 'temp':('Conversores','Unidades físicas','Temperatura'),
 'pressure':('Conversores','Unidades físicas','Pressão e grandezas mecânicas'),
 'mass':('Conversores','Unidades físicas','Massa e peso'),
 'length':('Conversores','Unidades físicas','Comprimento e distância'),
 'area':('Conversores','Unidades físicas','Área e superfície'),
 'volume':('Conversores','Unidades físicas','Volume e capacidade'),
 'speed':('Conversores','Unidades físicas','Velocidade'),
 'frequency':('Conversores','Eletricidade e eletrônica','Frequência'),
 'bits':('Conversores','Dados digitais','Armazenamento digital'),
 'culinary':('Conversores','Culinária e medidas contextuais','Medidas culinárias'),
 'time':('Conversores','Unidades temporais','Tempo'),
 'file':('Conversores','Arquivos e documentos','Documentos e PDF'),
 'video':('Conversores','Vídeo','Formatos de vídeo'),
 'audio':('Conversores','Áudio','Formatos de áudio'),
 'image':('Conversores','Imagem','Formatos de imagem'),
 'numbase':('Conversores','Sistemas numéricos','Bases numéricas'),
 'arith':('Matemática','Números e operações','Aritmética e operações básicas'),
 'frac':('Matemática','Números e operações','Frações e decimais'),
 'algebra':('Matemática','Álgebra','Equações e expressões'),
 'powers':('Matemática','Potências e funções','Potências, raízes e logaritmos'),
 'geometry':('Matemática','Geometria','Área e perímetro'),
 'trig':('Matemática','Trigonometria','Trigonometria e geometria angular'),
 'stats':('Matemática','Estatística e probabilidade','Médias e estatística descritiva'),
 'prob':('Matemática','Estatística e probabilidade','Probabilidade e combinatória'),
 'date':('Datas','Intervalos','Diferença entre datas'),
 'duration':('Datas','Duração','Horas, minutos e duração genérica'),
 'calendar':('Datas','Calendário','Dia da semana e calendário'),
 'holidays':('Datas','Dias úteis','Dias úteis e feriados')
}
# Dimensional vocabulary deliberately avoids generic 'm', 'a', 's', 'g' when unqualified.
UNIT_PAT=[
 ('psi','press',r'(?<![a-z])psi\b'),('bar','press',r'\bbar\b'),('kPa','press',r'(?<![a-z])kpa\b'),('MPa','press',r'(?<![a-z])mpa\b'),('mmHg','press',r'\bmmhg\b'),('atm','press',r'\batm\b|\batmosferas?\b'),('kgf/cm²','press',r'\bkgf\s*/?\s*cm\s*(?:2|²)\b'),
 ('mm','length',r'(?<![a-z])mm\b|\bmilimetros?\b'),('cm','length',r'(?<![a-z])cm\b|\bcentimetros?\b'),('km','length',r'(?<![a-z])km\b|\bquilometros?\b'),('metro','length',r'\bmetros?\b'),('in','length',r'\bpolegadas?\b|\binches?\b|\binch\b'),('ft','length',r'\bfeet\b|\bpes\b'),('mi','length',r'\bmilhas?\b'),('jarda','length',r'\bjardas?\b'),
 ('m²','area',r'\bm\s*(?:2|²)\b|\bmetros? quadrad[oa]s?\b'),('km²','area',r'\bkm\s*(?:2|²)\b|\bquilometros? quadrad[oa]s?\b'),('ha','area',r'\bhectares?\b|\bha\b'),('acre','area',r'\bacres?\b'),('ft²','area',r'\bpes quadrad[oa]s?\b'),('jarda²','area',r'\bjardas? quadrad[oa]s?\b'),('alqueire','area',r'\balqueires?\b'),('tarefa','area',r'\btarefas?\b'),
 ('kg','mass',r'(?<![a-z])kg\b|\bquilos?\b|\bquilogramas?\b'),('g','mass',r'\bgramas?\b'),('mg','mass',r'(?<![a-z])mg\b|\bmiligramas?\b'),('t','mass',r'\btoneladas?\b'),('lb','mass',r'\blbs?\b|\blibras?\b'),('arroba','mass',r'\barrobas?\b'),('dag','mass',r'\bdag\b'),
 ('L','volume',r'\blitros?\b|(?<![a-z])l\b'),('mL','volume',r'(?<![a-z])ml\b|\bmililitros?\b'),('m³','volume',r'\bm\s*(?:3|³)\b|\bmetros? cubicos?\b'),('cm³','volume',r'\bcm\s*(?:3|³)\b|\bcentimetros? cubicos?\b'),('gal','volume',r'\bgaloes?\b|\bgallons?\b'),('quart','volume',r'\bquarts?\b'),('xicara','volume',r'\bxicaras?\b'),
 ('°C','temp',r'\bcelsius\b'),('°F','temp',r'\bfahrenheit\b|\bfarenheits?\b'),('K','temp',r'\bkelvin\b'),
 ('kHz','frequency',r'\bkhz\b'),('MHz','frequency',r'\bmhz\b'),('Hz','frequency',r'\bhz\b|\bhertz\b'),
 ('GB','digital',r'\bgb\b|\bgigabytes?\b'),('MB','digital',r'\bmb\b|\bmegabytes?\b'),('TB','digital',r'\btb\b|\bterabytes?\b'),('KB','digital',r'\bkb\b|\bkilobytes?\b'),('byte','digital',r'\bbytes?\b'),('bit','digital',r'\bbits?\b'),
 ('kW','power',r'\bkw\b|\bkilowatts?\b'),('W','power',r'\bwatts?\b'),('cv','power',r'\bcavalos? vapor\b|\bcv\b'),('hp','power',r'\bhp\b'),('kWh','energy',r'\bkwh\b'),('Wh','energy',r'\bwh\b'),('J','energy',r'\bjoules?\b'),('cal','energy',r'\bcalorias?\b|\bkcal\b'),
 ('V','voltage',r'\bvolts?\b|\bvoltagem\b'),('mA','current',r'(?<![a-z])ma\b|\bmiliamperes?\b'),('A','current',r'\bamperes?\b'),
 ('km/h','speed',r'\bkm\s*/?\s*h\b|\bkmh\b|\bquilometros? por hora\b'),('mph','speed',r'\bmph\b|\bmilhas? por hora\b'),('m/s','speed',r'\bmetros? por segundo\b|\bm\s*/\s*s\b|\bms\b'),('knot','speed',r'\bknots?\b|\bnos?\b'),
 ('dia','time',r'\bdias?\b'),('semana','time',r'\bsemanas?\b'),('mes','time',r'\bmeses?\b'),('ano','time',r'\banos?\b'),('hora','time',r'\bhoras?\b'),('min','time',r'\bminutos?\b'),('s','time',r'\bsegundos?\b')]
# specific units before broad base units; exclude 1000 ml triggering 'L' standalone, etc.
UNIT_PAT_SORT=UNIT_PAT

def parse_units(t):
 result=[]
 for code,dim,pat in UNIT_PAT_SORT:
  for match in re.finditer(pat,t):
   if code=='L' and re.search(r'(?<![a-z])ml\b',t[max(0,match.start()-1):match.end()]): continue
   # Avoid a 'bar' as establishment when no numbers/conversion/counterpart.
   result.append((code,dim,match.start(),match.end()))
 # discard interior matches, favor longer meaningful measurements
 ordered=sorted(result,key=lambda e:(e[2],-(e[3]-e[2]))); keep=[]
 for r in ordered:
  if any(r[2]>=x[2] and r[3]<=x[3] for x in keep):continue
  keep.append(r)
 # second pass overlap (area m2 not length 'm' no conflict, velocity km/h vs km):
 keep=sorted(keep,key=lambda e:e[2]); unique=[]
 for x in keep:
  if x[:2] not in [(a,b) for a,b,_,_ in unique]:unique.append(x)
 return unique

FORMATS=('pdf','doc','docx','xls','xlsx','csv','ods','odt','ppt','pptx','jpg','jpeg','png','heic','webp','svg','mp3','wav','flac','ogg','mp4','mov','avi','mkv','psd','cdr','txt','rtf')
FREG=r'\b(?:'+ '|'.join(FORMATS) + r')\b'
PAT_DIR=r'\b(?:para|em|to|into|a|en)\b|\s*->\s*'
# Currencies with strict textual context
CURRENCIES={
 'USD':r'\b(?:usd|dolar(?:es)? americanos?|dolar(?:es)?(?!\s+(?:australianos?|canadenses?|neozelandeses?))|dollars?)\b',
 'BRL':r'\b(?:brl|reais|real brasileiro)\b|\breal\b',
 'EUR':r'\b(?:eur|euros?)\b|€',
 'GBP':r'\b(?:gbp|libras? esterlinas?|libras? inglesas?)\b',
 'JPY':r'\b(?:jpy|ienes?|yens?)\b',
 'KRW':r'\b(?:krw|wons?)\b',
 'ARS':r'\b(?:ars|pesos? argentinos?)\b',
 'CLP':r'\b(?:clp|pesos? chilenos?)\b',
 'COP':r'\b(?:cop|pesos? colombianos?)\b',
 'MXN':r'\b(?:mxn|pesos? mexicanos?)\b',
 'CAD':r'\b(?:cad|dolares? canadenses?)\b',
 'AUD':r'\b(?:aud|dolares? australianos?)\b',
 'CHF':r'\b(?:chf|francos? suicos?)\b',
 'CNY':r'\b(?:cny|yuans?)\b',
 'INR':r'\b(?:inr|rupias? indianas?)\b',
 'AED':r'\b(?:aed|dirham(?:s)? (?:dos? emirados|emiradense))\b',
 'MAD':r'\b(?:mad|dirham(?:s)? marroquinos?)\b',
 'AOA':r'\b(?:aoa|kwanzas?)\b',
 'ILS':r'\b(?:ils|novo shekel|shekels?)\b',
 'MZN':r'\b(?:mzn|meticais?|metical)\b',
 'EGP':r'\b(?:egp|libras? egipcias?)\b',
}

def classify(e):
 t=norm(e['Keyword']); ar=e['area'];
 # Standalone numeric duration often gestational; do not infer pregnancy.
 if yes(t,r'^\d{1,2}\s+semanas?(?:\s+e\s+\d\s+dias?)?$'):return None
 if len(t)<4 or t in {'quanto custa','como fazer','qual o valor','qual a formula','por mes','calculadora','10 20 30','conversor','qual o valor de','converter online'}:return None
 # Exclusion patterns take precedence over bare homonyms: 'conta', 'peso', 'real', 'libra'.
 if yes(t,r'\b(?:gravidez|gestacao|gestacional|gestante|gravida|ultrassom|feto|prenatal|parto|dpp|idade corrigida|dum\b|recem nascid[oa]|peso ideal|imc|indice de massa corporal)\b'):
  return result('health','informacional','RESOLVIDO_ALTA','saude_contextual','Contexto explícito de gestação/saúde, não conversão temporal genérica.', 'fora de escopo')
 if yes(t,r'\b(?:cupom|promocao|desconto\s+(?:loja|carrefour|amazon|magalu|mercado livre)|black friday|preco[s]?\s+(?:na |do |de )?(?:casas bahia|amazon|carrefour))\b'):
  return result('ecommerce','navegacional/transacional','RESOLVIDO_ALTA','comercio_promocional','Intenção de promoção/compra, não cálculo.', 'fora de escopo')
 if yes(t,r'\b(?:abrir conta|abra sua conta|abertura de conta|fazer transferencia bancaria|deposito de cheque|cartao de debito|conta corrente online|internet banking)\b'):
  return result('bank','navegacional/transacional','RESOLVIDO_ALTA','operacao_bancaria','Operação bancária, não conta aritmética.', 'fora de escopo')
 if yes(t,r'\b(?:ef\d{2}ma\d+|em\d{2}mat\d+|atividades? de|exercicios? de|lista de exercicios|gabarito|apostilas?|ppt|para imprimir|prova de matematica|ensino fundamental|escola|bncc)\b') and not yes(t,r'\b(?:converter|calcular online|calculadora)\b'):
  return result('education','informacional','RESOLVIDO_ALTA','material_escolar','Busca de material didático ou código curricular, sem cálculo solicitado.', 'conteúdo')
 if yes(t,r'\b(?:suv|honda|fiat|corolla|volkswagen|chevrolet|hyundai|toyota|hr v|cr v|s10\s+diesel|uno mille)\b') and not yes(t,r'\b(?:financiar|financiamento|prestacao|simular parcelas)\b'):
  return result('product','informacional','RESOLVIDO_ALTA','veiculo_produto','Modelo de veículo/produto, sem unidade para converter.', 'fora de escopo')
 if yes(t,r'\b(?:distancia entre cidades|rota para|passagem de onibus|cidade de|capital do estado|mapa do|localizacao de|km de .* a (?:sao|rio|cuiaba))\b'):
  return result('geography','informacional','RESOLVIDO_ALTA','consulta_geografica','Consulta geográfica/viagem, não conversão de unidades.', 'fora de escopo')
 # Explicit farming yields: distinguish kg/ha AGRONOMIC PRODUCTIVITY from mass-to-area conversion.
 if yes(t,r'\b(?:plantio|colheita|produtividade|adubo|fertilizante|ureia|sorgo|trigo|soja|milho|aveia|nabo|feno|sementes?)\b') and yes(t,r'\b(?:hectares?|ha\b|arrobas?|sacas?|sacos?|quilos?|kg\b|producao|rendimento)\b'):
  return result('agri','estimativa de produtividade','RESOLVIDO_COM_RESSALVA','rendimento_agricola','Rendimento/agronomia envolve cultura, manejo, solo e região; não fator universal de conversão.', 'fora de escopo')
 # Work calculations (salary/journey/benefits) and explicit rights questions.
 if yes(t,r'\b(?:decimo terceiro|13\s*(?:o|º)?\s*salario|segunda parcela do 13|13 proporcional)\b'):
  return result('thirteenth','informacional' if yes(t,r'\b(?:quando e pago|segunda parcela|data de pagamento)\b') else 'cálculo contextual' if yes(t,r'\b(?:calcul|quanto|valor|parcelas?|proporcional)\b') else 'informacional','RESOLVIDO_COM_RESSALVA','decimo_terceiro','Cálculo ou regra de 13º depende de base remuneratória e meses trabalhados.')
 if yes(t,r'\b(?:rescisao|rescisorio|pedi demissao|pedindo conta|fui demitid[oa]|mandad[oa] embora|aviso previo|multa rescisoria|acerto salarial|calculo desligamento|sai do trabalho quando)\b'):
  return result('rescision','cálculo contextual' if yes(t,r'\b(?:quanto|calcul|recebo|valor|simul)\b') else 'informacional','RESOLVIDO_COM_RESSALVA','rescisao_trabalhista','Regime e verbas trabalhistas dependem de dados contratuais e datas.')
 if yes(t,r'\b(?:fgts|saque aniversario|multa de 40 porcento)\b'):
  return result('fgts','cálculo contextual' if yes(t,r'\b(?:calcul|quanto|valor|saldo|porcentagem|simul)\b') else 'informacional','RESOLVIDO_COM_RESSALVA','fgts_saques','FGTS depende de saldo, data, legislação e modalidade.')
 if yes(t,r'\b(?:licenca paternidade|licenca maternidade|insalubridade|periculosidade|clt|direitos dos trabalhadores|direitos do trabalhador)\b'):
  return result('rights','informacional','RESOLVIDO_ALTA','direitos_trabalhistas','Informação de legislação e direitos; sem cálculo universal.', 'conteúdo')
 if yes(t,r'\b(?:hora extra|horas extras|dsr|adicional noturno|calcular minhas horas|horas noturnas|horas trabalhadas|carga horaria semanal|valor hora|valor da hora trabalhada)\b'):
  tax='extrahour' if yes(t,r'\b(?:extras?|noturn|dsr)\b') else 'worktime'
  return result(tax,'cálculo contextual','RESOLVIDO_COM_RESSALVA','jornada_trabalho','Jornada e remuneração dependem de escala, salário e regras aplicáveis.')
 if yes(t,r'\b(?:salario liquido|salario bruto|desconto em folha|reajuste salarial|dissidio|adiantamento salarial|quanto eu ganho por dia|quanto ganho por hora|calculo do ir na fonte|calcular iss|calcular inss|calculadora salario|valor do salario)\b'):
  return result('payroll','cálculo contextual','RESOLVIDO_COM_RESSALVA','folha_remuneracao','Base salarial, período e alíquotas precisam ser informados.')
 if yes(t,r'\b(?:aposentar|aposentadoria|fator previdenciario|inss aposentadoria|previdenciaria)\b'):
  return result('retirement','cálculo contextual' if yes(t,r'\b(?:calcul|simul|quanto|tempo)\b') else 'informacional','RESOLVIDO_COM_RESSALVA','previdencia','Previdência depende de regras vigentes e histórico contributivo.')
 # Construction calculator and information, avoid broad words 'massa', 'piso' in other domains.
 if yes(t,r'\b(?:telhad[oa]s?|telhas?|cumeeira|cobertura metalica|telha fibrocimento|telha sanduiche)\b') and yes(t,r'\b(?:inclinacao|caimento|quantidade|quantas|quantos|calcul|preco|orcamento|metro[s]? quadrad[oa]s?|m2\b|cobrir)\b'):
  return result('roof','estimativa de quantidade' if yes(t,r'\b(?:quantas|quantos|quantidade|cobrir|calculadora)\b') else 'cálculo contextual','RESOLVIDO_COM_RESSALVA','cobertura_telhas','Inclinação, dimensões, recobrimento e modelo da telha variam conforme projeto.')
 if yes(t,r'\b(?:argamassa|rejunte|porcelanato|contrapiso|piso ceramico|assentar tijolo)\b') and yes(t,r'\b(?:m2|metros? quadrad|calcul|quantos|quanto|rende|cobertura|traco|saco|consumo)\b'):
  return result('revest','estimativa de quantidade','RESOLVIDO_COM_RESSALVA','revestimento','Consumo depende de espessura, perdas e produto.')
 if yes(t,r'\b(?:concreto|viga|sapata|cimento|brita|fundacao|tijolo|bloco ceramico|muro)\b') and yes(t,r'\b(?:quantos|quanto|calcul|volume|area|metros?|sacos?|traco|orcam|preco|custa)\b'):
  return result('concrete','estimativa de quantidade','RESOLVIDO_COM_RESSALVA','material_construcao','Depende de dimensões, especificação do material e margens de perda.')
 if yes(t,r'\b(?:custo de construir|custa construir|quanto custa para construir|preco de pedreiro|orcamento de obra|construir uma casa|construir um sobrado|preco m2 telhado|mao de obra por m2)\b'):
  return result('building_cost','estimativa de custo','RESOLVIDO_COM_RESSALVA','custo_obra','Preço depende de região, materiais e projeto.')
 # Energy/transport-specific calculations never direct cross-dimensional conversion.
 if yes(t,r'\b(?:consumo de gasolina|gasolina para viagem|km por litro|litros? por 100 km|km\/l|kml|consumo de combustivel|quanto gasto de gasolina|alcool e gasolina|reembolso km|milhas por galao|\bmpg\b)\b'):
  return result('drive','estimativa de consumo','RESOLVIDO_COM_RESSALVA','consumo_combustivel','Consumo/custo depende de veículo, percurso, preços e rendimento.')
 if yes(t,r'\b(?:energia solar|painel solar|placa solar|fotovoltaic[oa]|geracao solar)\b') and yes(t,r'\b(?:calcul|simul|dimension|geracao|potencia|kw\b|kwh\b|preco|custo)\b'):
  return result('solar','estimativa de custo' if yes(t,r'\b(?:preco|custa|custo)\b') else 'dimensionamento','RESOLVIDO_COM_RESSALVA','solar_dimensionamento','Usa irradiação, perdas, demanda e dados técnicos.')
 if yes(t,r'\b(?:queda de tensao|disjuntor|instalacao eletrica|\bvolt\b.*\bwatt\b|\bwatt\b.*\bvolt\b|\bkw\b.*\bamp\b|\bamp\b.*\bkw\b)\b'):
  return result('electric','cálculo contextual','RESOLVIDO_COM_RESSALVA','potencia_eletrotecnica','Grandezas elétricas distintas exigem dados de corrente, tensão, fator de potência e circuito.')
 if yes(t,r'\b(?:valor do kwh|preco do quilowatt|custo da energia|tarifa de energia|conta de luz|quanto custa o kwh|economia de energia)\b'):
  return result('energy_cost','estimativa de custo','RESOLVIDO_COM_RESSALVA','tarifa_consumo','Tarifa depende de distribuidora, localidade, data e faixa de consumo.')
 # File formats. Distinguish educational PDF from file transformation.
 formats=[(m.group(),m.start(),m.end()) for m in re.finditer(FREG,t)]
 if len(formats)>=2 and yes(t,r'\b(?:converter|conversao|conversor|transformar|passar|mudar|de\b.*\bpara|\bto\b|\bem\b)'):
  a,b=formats[0][0].upper(),formats[1][0].upper()
  if a!=b and not yes(t,r'\b(?:exercicios|questoes|apostila|lista de|atividades|gabarito|teoria)\b'):
   typ='audio' if a in ('MP3','WAV','FLAC','OGG') or b in ('MP3','WAV','FLAC','OGG') else 'video' if a in ('MP4','MOV','AVI','MKV') or b in ('MP4','MOV','AVI','MKV') else 'image' if a in ('JPG','JPEG','PNG','HEIC','WEBP','SVG','PSD','CDR') or b in ('JPG','JPEG','PNG','HEIC','WEBP','SVG','PSD','CDR') else 'file'
   return result(typ,'conversão de arquivo/mídia','RESOLVIDO_ALTA','formatos_arquivo_direcionais','Formatos distintos e intenção de transformação explícitos.', 'ferramenta',a,b)
 if len(formats)==1 and yes(t,r'\b(?:converter|conversor|transformar|passar|mudar formato|arquivo|documento)\b'):
  return result('file','conversão de arquivo/mídia','RESOLVIDO_COM_RESSALVA','arquivo_destino_ausente','Tipo de arquivo referido, mas par completo não especificado.')
 if yes(t,r'\b(?:converter video|conversor de video|converter imagem|conversor de audio|conversor de imagem|mudar formato de arquivo|site para converter video)\b'):
  typ='video' if 'video' in t else 'audio' if 'audio' in t else 'image' if 'imagem' in t else 'file'
  return result(typ,'conversão de arquivo/mídia','RESOLVIDO_COM_RESSALVA','conversor_arquivo_generico','Busca de ferramenta de arquivo; formatos de entrada e saída precisam ser selecionados.')
 # Electrical bill amounts are not currency-exchange queries.
 if yes(t,r'\b(?:kwh|quilowatt.?hora|kw\s*h)\b') and yes(t,r'\b(?:reais|real|r\$|quanto custa|preco|valor|tarifa|conta de luz)\b'):
  return result('energy_cost','estimativa de custo','RESOLVIDO_COM_RESSALVA','kwh_valor_tarifario','Energia consumida x tarifa variável (R$/kWh); não converter kWh em moeda diretamente.')
 # Currency usage in arithmetic contexts is not a foreign-exchange conversion.
 if yes(t,r'\b(?:porcentagem|percentual|percentagem)\b') and yes(t,r'\b(?:reais|real)\b'):
  return result('price','cálculo contextual','RESOLVIDO_COM_RESSALVA','porcentagem_monetaria','Percentual financeiro precisa de base de cálculo, não taxa de câmbio.')
 if yes(t,r'\b(?:moeda chinesa|moeda chilena|moeda colombiana|moeda venezuelana|moeda tailandesa)\b') and yes(t,r'\b(?:real|reais|cambio|converter|cotacao|conversao)\b'):
  return result('fx','cálculo contextual','RESOLVIDO_COM_RESSALVA','moeda_nacional_sem_codigo','Moeda nacional mencionada, mas código/nome específico e direção precisam ser validados.')
 if yes(t,r'\b(?:bushel)\b') and yes(t,r'\b(?:soja|milho|trigo|kg|quilos?|sacas?)\b'):
  return result('agri','cálculo contextual','RESOLVIDO_COM_RESSALVA','bushel_por_cultura','Bushel é volume; conversão em massa depende da cultura e da convenção comercial.')
 # Numismatic collectible value is not an exchange rate.
 if yes(t,r'\b(?:moeda\s+(?:de\s+)?(?:um|1|2|5|10|25|50|100)\s+(?:reais?|centavos?|euros?)|moeda\s+(?:de\s+)?\d+(?:[.,]\d+)?\s+euros?|moeda.*(?:beija flor|comemorativ|25 anos|40 anos|50 anos|raridade|colecion))\b') and yes(t,r'\b(?:moeda|numismat)\b'):
  return result('coin','consulta de preço/mercado','RESOLVIDO_ALTA','moeda_colecionavel','Valor de peça monetária/colecionável, não par cambial.', 'fora de escopo')
 # Unqualified pound becomes sterling only in currency-pair queries, never physical mass.
 if yes(t,r'\blibras?\b') and yes(t,r'\b(?:euros?|dolares?|usd|eur|moeda|cambio|cotacao)\b') and not yes(t,r'\b(?:peso corporal|kg|quilos?|gramas?|massa)\b'):
  if yes(t,r'\b(?:euros?|dolares?|usd|eur)\b') and yes(t,r'\b(?:converter|conversor|transformar|cambio|cotacao|para|em)\b'):
   cash=[(m.start(),'GBP') for m in re.finditer(r'\blibras?\b',t)]
   for code,pat in [('EUR',r'\beuros?\b|\beur\b'),('USD',r'\bdolares?\b|\busd\b')]:
    cash.extend((m.start(),code) for m in re.finditer(pat,t))
   cash.sort();seq=list(dict.fromkeys(c for _,c in cash))
   if len(seq)==2:
    return result('fx','conversão direta','RESOLVIDO_COM_RESSALVA','libra_cambio_contextual','Libra interpretada como GBP pelo contexto cambial; confirmar moeda caso haja ambiguidade.', 'ferramenta',seq[0],seq[1])
 # Currency: reject financial words used outside FX and insufficient word 'peso' or 'libra'.
 if not yes(t,r'\b(?:peso corporal|peso ideal|peso da|peso de|massa de|quilograma|quilos?|kg\b|peso do)\b'):
  currencies=[]
  for k,p in CURRENCIES.items():
   m=re.search(p,t)
   if m:currencies.append((m.start(),m.end(),k))
  currencies.sort(key=lambda x:x[0]);currency_codes=list(dict.fromkeys(k for _,_,k in currencies))
  if len(currency_codes)==2 and yes(t,r'\b(?:converter|conversao|conversor|transformar|cambiar|cotacao|cambio|valor|para|em|a\b|to\b|en\b|moeda|quantos|quanto)\b'):
   if not yes(t,r'\b(?:valor da moeda de|moeda antiga|moeda rara|colecion|numismatic|valor da moeda do banco central|mais valorizada do mundo)\b'):
    direct=bool(yes(t[currencies[0][1]:currencies[1][0]],r'\b(?:para|em|to|a|en)\b|[\->]+'))
    return result('fx','conversão direta' if direct else 'cálculo contextual','RESOLVIDO_ALTA' if direct else 'RESOLVIDO_COM_RESSALVA','par_moedas_nomeadas','Par monetário explícito; taxas de câmbio exigem fonte e data.', 'ferramenta', currency_codes[0] if direct else '',currency_codes[1] if direct else '')
  if len(currency_codes)==1 and yes(t,r'\b(?:converter|cotacao|cambio|conversor|taxa de cambio|transformar|cambiar|valor de|moeda)\b'):
   if yes(t,r'\b(?:hoje|atual|valor|cotacao|quanto vale|preco)\b'):
    return result('quote','cotação atual','RESOLVIDO_COM_RESSALVA','cotacao_moeda_unica','Moeda explícita mas par de referência/mercado precisa ser informado.')
   return result('fx','cálculo contextual','RESOLVIDO_COM_RESSALVA','cambio_destino_ausente','Uma moeda explícita; par de conversão não identificado.')
 # Unit parsen: numeric and explicit pair = conversion; ambiguous without direction => with caveat.
 # By requiring <=2 distinct compatible units, no conversion between incompatible dimensions.
 units=parse_units(t)
 primary=[u for u in units if u[1] not in ('time',)]
 dims={x[1] for x in primary};codes=[]
 for u in primary:
  if u[0] not in codes:codes.append(u[0])
 if len(primary)>=2 and len(codes)==2 and len(dims)==1 and not yes(t,r'\b(?:custa|consumo|preco|taxa de|peso ideal|altura de pessoas|tabela nutricional|numa receita|\bdia\s+mmhg|\bmg\s+zs\b)\b'):
  dimension=next(iter(dims));taxonomy={'press':'pressure','length':'length','area':'area','mass':'mass','volume':'volume','temp':'temp','frequency':'frequency','digital':'bits','power':'electric','energy':'electric','voltage':'electric','current':'electric','speed':'speed'}[dimension]
  if 'alqueire' in codes or 'tarefa' in codes or 'xicara' in codes:
   return result('area' if dimension=='area' else 'culinary','cálculo contextual','RESOLVIDO_COM_RESSALVA','medida_regional','Medida regional ou culinária exige padrão local/recipiente.')
  if dimension=='digital' and (('bit' in codes) ^ ('byte' in codes)):
   return result('bits','conversão direta' if yes(t,PAT_DIR) else 'cálculo contextual','RESOLVIDO_COM_RESSALVA','bits_bytes','Base decimal versus binária, precisão e capitalização devem ser especificadas.')
  # text '500 kg em arroba' is direct, '110 psi bar' no direction => caveat
  sorted_units=sorted([u for u in primary if u[0] in codes],key=lambda x:x[2]);explicit=bool(yes(t[sorted_units[0][3]:sorted_units[1][2]],r'\b(?:para|em|to|into|en)\b')) if len(sorted_units)>=2 else False
  return result(taxonomy,'conversão direta' if explicit else 'cálculo contextual','RESOLVIDO_ALTA' if explicit else 'RESOLVIDO_COM_RESSALVA','par_unidades_fisicas','Duas unidades físicas compatíveis identificadas; direção explícita.' if explicit else 'Par compatível, mas direção não explicitada.', 'ferramenta',codes[0] if explicit else '',codes[1] if explicit else '')
 if len(codes)==1 and yes(t,r'\b(?:celsius|fahrenheit|kelvin)\b') and yes(t,r'\b(?:calcular|converter|quantos|transformar|graus)\b'):
  return result('temp','cálculo contextual','RESOLVIDO_COM_RESSALVA','escala_temperatura','Escala presente, falta escala/valor de destino.')
 # Explicit compound time, units not present in physical list.
 if yes(t,r'\b(?:calculadora de horas|contador de dias horas|somar minutos e segundos|contar semanas|converter semanas em meses|quantos dias tem um mes)\b'):
  return result('duration','cálculo contextual','RESOLVIDO_COM_RESSALVA','duracao_composta','Duração temporal exige período de referência ou convenção de calendário.')
 if yes(t,r'\b(?:prazo em dias|dias corridos|somar dias|diferen[cç]a entre datas|data de hoje mais|contador de meses de namoro|quantos dias para meu aniversario)\b'):
  return result('date','cálculo contextual','RESOLVIDO_COM_RESSALVA','prazos_datas','Cálculos de datas exigem data inicial e/ou final.')
 if yes(t,r'\b(?:anos bissextos?|sexta feira santa|feriados?)\b'):
  return result('calendar','informacional','RESOLVIDO_ALTA','calendario','Consulta de calendário ou feriados; não conversão de medida.', 'conteúdo')
 # Finance: strict, proper nouns without action get caveat.
 if yes(t,r'\b(?:cdb|cdi|lci|lca|tesouro direto|selic|rentabilidade de fundo|fundo de investimento)\b'):
  return result('fixed','simulação/projeção' if yes(t,r'\b(?:calcul|simul|quanto rende|rendimento|rentabilidade)\b') else 'informacional','RESOLVIDO_COM_RESSALVA','renda_fixa','Rentabilidade/índice dependem de período, taxa, tributação e instituição.')
 if yes(t,r'\b(?:dividendos?|mercado pago rende|poupanca rende|investir para receber|rendimento mensal|payback|taxa interna de retorno|\btir\b|\bvpl\b|valor presente)\b'):
  return result('investment','informacional' if yes(t,r'^(?:o que e|qual o significado|definicao|formula)\b') else 'simulação/projeção','RESOLVIDO_COM_RESSALVA','rentabilidade','Cálculo de investimento exige hipóteses, aportes e periodicidade.')
 if yes(t,r'\b(?:financiar|financiamento|consignado|prestacao fixa|prestacoes?|prestacao|credito imobiliario|parcela de carro|parcelas de veiculo|simulador (?:santander|itau|banco|omni|caixa))\b'):
  return result('finance' if yes(t,r'\b(?:financi|veiculo|carro|imobili)\b') else 'loan','simulação/projeção','RESOLVIDO_COM_RESSALVA','credito_simulacao','Parcelas dependem de CET, juros, prazo e entrada.')
 if yes(t,r'\b(?:emprestimos?|emprestimo|cheque especial|taxa bancaria|taxas bancarias|parcela[dr]?\b|parcelado\b|cartao de credito|dividas?)\b'):
  return result('loan' if yes(t,r'\b(?:emprest|cheque especial|taxas? banc)\b') else 'debt','simulação/projeção','RESOLVIDO_COM_RESSALVA','emprestimos_dividas','Juros e condições dependem de valor, prazo e credor.')
 if yes(t,r'\b(?:organizar contas|controle de despesas|gastos mensais|despesa mensal|orcamento familiar|reserva de emergencia|planejamento financeiro)\b'):
  return result('budget','cálculo contextual','RESOLVIDO_COM_RESSALVA','orcamento','Ferramenta de orçamento exige receitas, despesas e períodos.')
 if yes(t,r'\b(?:calculo da inflacao|correcao monetaria|reajuste de aluguel|calculadora igpm|\bigpm\b|\bipca\b)\b'):
  return result('rate','cálculo contextual','RESOLVIDO_COM_RESSALVA','indices_inflacao','Reajuste depende do índice e do período.')
 # Digital/electrical common shorthand with explicit 'para' missing from legacy classifier
 if yes(t,r'\b(?:binario para decimal|decimal para binario|hexadecimal para decimal|decimal para hexadecimal|binario decimal|conversor binario)\b'):
  return result('numbase','conversão direta' if yes(t,r'\bpara\b') else 'cálculo contextual','RESOLVIDO_ALTA' if yes(t,r'\bpara\b') else 'RESOLVIDO_COM_RESSALVA','base_numerica','Conversão de bases numéricas, direção explícita apenas quando nomeada.')
 if yes(t,r'\b(?:calculo do disjuntor|calcular disjuntor|transformar w em kw|\bma\s+para\s+a\b)\b'):
  return result('electric','cálculo contextual','RESOLVIDO_COM_RESSALVA','eletrica_parametros','Circuito e unidade elétrica exigem validação técnica.')
 # Distinguish mathematical topics without pretending a solved expression.
 mathmap=[('powers',r'\b(?:logaritm|radiciacao|potenciac|expoentes?|raiz quadrada|equacao exponencial)\b'),('prob',r'\b(?:permutac|arranjo|combinatoria|probabilidade|espaco amostral|eventos dependentes|eventos independentes)\b'),('stats',r'\b(?:media aritmetica|desvio padrao|variancia|mediana|moda estatistica)\b'),('trig',r'\b(?:pitagoras|seno|cosseno|tangente|trigonometria)\b'),('algebra',r'\b(?:equacao|sistema linear|sistemas lineares|incognita|metodo da substituicao|fatoracao|trinomio|algebr)\b'),('frac',r'\b(?:fracoes?|porcentagem|percentual)\b'),('geometry',r'\b(?:area do trapezio|area do triangulo|perimetro|geometria)\b'),('arith',r'\b(?:divisores|multiplos|numero primo|mmc\b|mdc\b)\b')]
 for tax,pat in mathmap:
  if yes(t,pat):
   if yes(t,r'\b(?:poupanca|bancos?|capital|rendimento|investir|dividendos|tesouro|salario)\b'):return None
   op=bool(yes(t,r'\b(?:calculadora|resolver|resolva|calcule|calcular|quanto e|online)\b'))
   return result(tax,'cálculo contextual' if op else 'informacional','RESOLVIDO_COM_RESSALVA' if op else 'RESOLVIDO_ALTA','tema_matematico','Tópico matemático identificável; parâmetros necessários.' if op else 'Consulta informacional, sem operação especificada.', 'ferramenta' if op else 'conteúdo')
 return None

PROTECTED={'tipo_registro','id_global','lote_id','familia_id','controle_id','Keyword','ocorrencias_origem','areas_origem','qtd_areas','Avg. monthly searches','Mudança em três meses','Mudança YoY','Competition','Competition (indexed value)','Top of page bid (low range)','Top of page bid (high range)','keyword_interpretada','reconstrucao_barra_status','tipos_reconstrucao_barra','confianca_reconstrucao_barra','observacao_reconstrucao_barra'}
original=readcsv(args.p2);pending=[r for r in original if r['status_p2']=='PENDENTE_CONTEXTUAL'];assert len(original)==25050 and len(pending)==8813
before_queue=readcsv(args.fila);assert len(before_queue)==len({x['id_global'] for x in before_queue})
z=zipfile.ZipFile(args.base)
base_rows={};byid={};total_ctl=0
for k in range(1,31):
 name=f'lotes/lote-{k:03d}-p0-p1-p2-v1.csv';rr=readzip(z,name);base_rows[k]=rr
 for r in rr:
  if r['tipo_registro']=='controle':total_ctl+=1
  elif r['tipo_registro']=='base':
   ident=r['id_global'];assert ident not in byid;byid[ident]=(k,r)
assert len(byid)==294905 and total_ctl==2190
D=[]; PATCH=[]; counter=collections.Counter();rules=collections.Counter()
for e in original:
 d={**e,'regra_p2_v2':'nao_pendente_p2_v1','status_p2_v2':'MANTIDO_P2_V1','justificativa_p2_v2':'Decisão P2 anterior preservada.','adequacao_portal_p2_v2':e['adequacao_portal_p2'],'area_final_p2_v2':e['area_final_p2'],'cluster_final_p2_v2':e['cluster_final_p2'],'subcluster_final_p2_v2':e['subcluster_final_p2'],'tipo_intencao_final_p2_v2':e['tipo_intencao_final_p2'],'unidade_origem_final_p2_v2':e['unidade_origem_final_p2'],'unidade_destino_final_p2_v2':e['unidade_destino_final_p2'],'classificacao_alterada_p2_v2':'não'}
 if e['status_p2']=='PENDENTE_CONTEXTUAL':
  c=classify(e);k,b=byid[e['id_global']]
  assert b['Keyword']==e['Keyword']
  if c:
   tax=c['tax'];assert tax in TAX
   area,cluster,sub=TAX[tax]
   d.update(regra_p2_v2=c['rule'],status_p2_v2=c['status'],justificativa_p2_v2=c['why'],adequacao_portal_p2_v2=c['fit'],area_final_p2_v2=area,cluster_final_p2_v2=cluster,subcluster_final_p2_v2=sub,tipo_intencao_final_p2_v2=c['intent'],unidade_origem_final_p2_v2=c['origin'],unidade_destino_final_p2_v2=c['dest'])
   original_row=b.copy()
   updates={'area_principal':area,'cluster':cluster,'subcluster':sub,'tipo_intencao':c['intent'],'intencao_principal':('Converter: ' if c['intent']=='conversão direta' else 'Consultar: ' if c['intent'] in ('informacional','cotação atual','navegacional/transacional') else 'Calcular: ')+sub,'confianca':'alta' if c['status']=='RESOLVIDO_ALTA' else 'média','revisao_manual':'não' if c['status']=='RESOLVIDO_ALTA' else 'sim','justificativa_curta':('P2-v2 '+c['rule']+': '+c['why'])[:450]}
   if c['origin'] and c['dest'] and c['intent'] in ('conversão direta','conversão de arquivo/mídia'):
    updates.update(unidade_origem=c['origin'],unidade_destino=c['dest'],direcao_conversao=c['origin']+' → '+c['dest'])
   else:updates.update(unidade_origem='',unidade_destino='',direcao_conversao='')
   for f,value in updates.items():b[f]=value
   if b!=original_row:
    changes={f:{'antes':original_row[f],'depois':b[f]} for f in b if b[f]!=original_row[f]}
    PATCH.append({'id_global':e['id_global'],'lote':e['lote'],'Keyword':e['Keyword'],'regra_p2_v2':c['rule'],'status_p2_v2':c['status'],'antes_area':original_row['area_principal'],'depois_area':b['area_principal'],'antes_intencao':original_row['tipo_intencao'],'depois_intencao':b['tipo_intencao'],'campos_alterados':' | '.join(changes),'diff_json':json.dumps(changes,ensure_ascii=False)})
    d['classificacao_alterada_p2_v2']='sim'
  else:
   d.update(regra_p2_v2='evidencia_insuficiente_v2',status_p2_v2='PENDENTE_REAL',justificativa_p2_v2='Contexto ainda insuficiente ou potencialmente múltiplo; não inferir direção, unidade nem operação.',adequacao_portal_p2_v2='indeterminado')
 counter[d['status_p2_v2']]+=1;rules[d['regra_p2_v2']]+=1;D.append(d)
# Queue: change only P2 entries resolved in this pass.
update={d['id_global']:d for d in D if d['status_p2_v2'] in ('RESOLVIDO_ALTA','RESOLVIDO_COM_RESSALVA')}
queue=[]
for r in before_queue:
 rr=r.copy();d=update.get(r['id_global'])
 if d:
  rr.update(status_revisao='REVISADO_P2_V2_REGRA' if d['status_p2_v2']=='RESOLVIDO_ALTA' else 'P2_V2_RESSALVA',decisao_final='CORRIGIR' if d['classificacao_alterada_p2_v2']=='sim' else 'MANTER_REGRA',observacao_revisor=('P2-v2 '+d['regra_p2_v2']+': '+d['justificativa_p2_v2'])[:800],area=d['area_final_p2_v2'],cluster=d['cluster_final_p2_v2'],subcluster=d['subcluster_final_p2_v2'],tipo_intencao_atual=d['tipo_intencao_final_p2_v2'],confianca_atual='alta' if d['status_p2_v2']=='RESOLVIDO_ALTA' else 'média')
 queue.append(rr)
# Independent regression: compare each row with P2 v1 source, no other ids touched.
protected_hash_before=hashlib.sha256();protected_hash_after=hashlib.sha256();reg=[];unchanged_count=0;modified=0
allowed=set(update)
for k in range(1,31):
 source=readzip(z,f'lotes/lote-{k:03d}-p0-p1-p2-v1.csv');new=base_rows[k]; assert len(source)==len(new)
 cnt=collections.Counter()
 for a,b in zip(source,new):
  assert a['id_global']==b['id_global'] and a['tipo_registro']==b['tipo_registro']
  assert all(a[f]==b[f] for f in PROTECTED),(k,a['id_global'],'coluna protegida')
  for f in sorted(PROTECTED):
   protected_hash_before.update((a[f]+'\x1f').encode('utf-8'));protected_hash_after.update((b[f]+'\x1f').encode('utf-8'))
  if a['tipo_registro']=='controle':cnt['controle']+=1;assert a==b
  else:
   cnt['base']+=1
   if a['id_global'] not in allowed:assert a==b,(k,a['id_global'],'fora do escopo');unchanged_count+=1
   elif a!=b:cnt['alterado']+=1;modified+=1
 reg.append({'lote':f'L{k:03d}','base':cnt['base'],'controles':cnt['controle'],'mudancas_p2_v2':cnt['alterado'],'sem_mudanca':len(new)-cnt['alterado'],'status':'PASSOU'})
assert len(PATCH)==modified and protected_hash_before.digest()==protected_hash_after.digest()
assert sum(int(x['base']) for x in reg)==294905 and sum(int(x['controles']) for x in reg)==2190
assert sum(counter[x] for x in ('RESOLVIDO_ALTA','RESOLVIDO_COM_RESSALVA','PENDENTE_REAL'))==8813
assert len(D)==25050
# QA: deterministic stratified sample per resolved rule and 500 unresolved for human queue, with source+result.
rng=random.Random(20261017);grouped=collections.defaultdict(list)
for d in D:
 if d['status_p2_v2']!='MANTIDO_P2_V1':grouped[(d['regra_p2_v2'],d['status_p2_v2'])].append(d)
sample=[]
for (rule,status),rr in sorted(grouped.items(),key=lambda x:(-len(x[1]),x[0])):
 n=min(len(rr),max(5,round(len(rr)*.04))) if status!='PENDENTE_REAL' else min(len(rr),80)
 for r in rng.sample(rr,n):
  sample.append({f:r.get(f,'') for f in ['id_global','lote','Keyword','regra_p2','regra_p2_v2','status_p2_v2','area','area_final_p2_v2','tipo_intencao_atual','tipo_intencao_final_p2_v2','justificativa_p2_v2']})
writecsv(out/'p2-v2-decisoes-25050.csv',D,list(D[0]))
writecsv(out/'p2-v2-pendencias-reais.csv',[d for d in D if d['status_p2_v2']=='PENDENTE_REAL'],list(D[0]))
writecsv(out/'p2-v2-ressalvas.csv',[d for d in D if d['status_p2_v2']=='RESOLVIDO_COM_RESSALVA'],list(D[0]))
writecsv(out/'p2-v2-patches.csv',PATCH,list(PATCH[0]))
writecsv(out/'p2-v2-amostra-auditoria.csv',sample,list(sample[0]))
writecsv(out/'fila-30-lotes-p0-p1-p2-v2.csv',queue,list(queue[0]))
writecsv(out/'p2-v2-regressao-30-lotes.csv',reg,list(reg[0]))
with zipfile.ZipFile(out/'lotes-001-a-030-p0-p1-p2-v2.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as zz:
 for k,rs in base_rows.items():
  stream=io.StringIO(newline='');w=csv.DictWriter(stream,fieldnames=list(rs[0]),delimiter=';',lineterminator='\n');w.writeheader();w.writerows(rs)
  zz.writestr(f'lotes/lote-{k:03d}-p0-p1-p2-v2.csv','\ufeff'+stream.getvalue())
summary={'data_execucao':'2026-10-17','universo_p2':len(D),'fila_pendente_anterior':len(pending),'classificacoes_v2':dict(counter),'qtd_regras_p2_v2':dict(rules),'qtd_patches':modified,'registros_base':294905,'controles':2190,'hash_sha256_colunas_protegidas':protected_hash_before.hexdigest(),'metodo':'segunda passada de regras contextuais conservadoras; requer controle editorial amostral; ressalvas sao operacoes parametrizadas'}
(out/'resumo-p2-v2.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
md=f'''# P2 — Validação contextual complementar v2

## Escopo
- Universo P2: {len(D):,} palavras-chave; pendências anteriores: {len(pending):,}.
- Resolvidas por regras de maior confiança: {counter['RESOLVIDO_ALTA']:,}.
- Reclassificadas com ressalvas de operação: {counter['RESOLVIDO_COM_RESSALVA']:,}.
- Pendências contextuais remanescentes: {counter['PENDENTE_REAL']:,}.
- Registros com atualização analítica: {modified:,}.
- Registros P2 já classificados na v1 preservados nesta rodada: {counter['MANTIDO_P2_V1']:,}.

## Integridade e auditabilidade
- Registros-base preservados: 294.905; controles preservados: 2.190.
- Todos os 30 lotes passaram na comparação fonte x saída.
- P0, P1 e campos protegidos de Ads, rastreamento e reconstrução de barras inalterados.
- SHA256 dos campos protegidos: `{protected_hash_before.hexdigest()}`.
- Scripts reutilizáveis não dependem de bibliotecas externas para reclassificação e regressão.

## Limites do resultado
A classificação é feita por regras textuais verificáveis, com regras de exceção; não equivale a leitura humana individual de 8.813 keywords. `RESOLVIDO_ALTA` indica confiança na regra, e não aprovação editorial final. Uma ressalva pode exigir valor, país, moeda, sentido, densidade, material, data, convenção, taxa, ou outro parâmetro. Não criar parâmetros de conversão imaginados. Os casos insuficientes continuam pendentes.

## Arquivos
`p2-v2-decisoes-25050.csv`: toda P2 e rastreabilidade; `p2-v2-pendencias-reais.csv`: restante para revisão; `p2-v2-ressalvas.csv`: casos classificados com dependências; `p2-v2-patches.csv`: diffs por registro; `p2-v2-regressao-30-lotes.csv`: testes; `fila-30-lotes-p0-p1-p2-v2.csv`: fila geral; `.zip`: 30 lotes revisados; `p2-v2-amostra-auditoria.csv`: amostra estratificada das regras. A planilha `.xlsx` resume os resultados e inclui uma amostra, enquanto os CSVs preservam todas as colunas e linhas.
'''
(out/'relatorio-validacao-p2-v2.md').write_text(md,encoding='utf-8')
print(json.dumps(summary,indent=2,ensure_ascii=False))
