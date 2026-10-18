#!/usr/bin/env python3
# Regras semânticas herdadas da P1, congeladas para reprodutibilidade.
import re,unicodedata

def norm(s):
    s=''.join(c for c in unicodedata.normalize('NFKD',s.lower()) if not unicodedata.combining(c))
    return re.sub(r'\s+',' ',s).strip()

def has(s,*regex):return any(re.search(r,s) for r in regex)

TAX={
 'generic':('Conversores','Conversões gerais','Conversor genérico de unidades'),
 'currency':('Conversores','Moedas e câmbio','Conversão entre moedas'),
 'quote':('Finanças','Câmbio','Cotação atual'),
 'crypto':('Finanças','Criptoativos','Conversão e cotação de criptomoedas'),
 'length':('Conversores','Unidades físicas','Comprimento e distância'),
 'area':('Conversores','Unidades físicas','Área e superfície'),
 'volume':('Conversores','Unidades físicas','Volume e capacidade'),
 'mass':('Conversores','Unidades físicas','Massa e peso'),
 'temp':('Conversores','Unidades físicas','Temperatura'),
 'time':('Conversores','Unidades temporais','Tempo'),
 'pressure':('Conversores','Unidades físicas','Pressão e grandezas mecânicas'),
 'power':('Conversores','Unidades físicas','Energia, potência e calor'),
 'electric':('Conversores','Eletricidade e eletrônica','Grandezas elétricas'),
 'frequency':('Conversores','Eletricidade e eletrônica','Frequência'),
 'bits':('Conversores','Dados digitais','Armazenamento digital'),
 'culinary':('Conversores','Culinária e medidas contextuais','Medidas culinárias'),
 'roman':('Conversores','Sistemas numéricos','Algarismos romanos e bases'),
 'file':('Conversores','Arquivos e documentos','Documentos e PDF'),
 'audio':('Conversores','Áudio','Formatos de áudio'),
 'video':('Conversores','Vídeo','Formatos de vídeo'),
 'image':('Conversores','Imagem','Formatos de imagem'),
 'date':('Datas','Intervalos','Diferença entre datas'),
 'months':('Datas','Operações com datas','Somar/subtrair datas e prazos'),
 'duration':('Datas','Duração','Horas, minutos e duração genérica'),
 'calendar':('Datas','Calendário','Dia da semana e calendário'),
 'holiday':('Datas','Dias úteis','Dias úteis e feriados'),
 'math':('Matemática','Ferramentas matemáticas','Calculadora geral'),
 'arith':('Matemática','Números e operações','Aritmética e operações básicas'),
 'prime':('Matemática','Números e operações','Aritmética e operações básicas'),
 'frac':('Matemática','Números e operações','Frações e decimais'),
 'power_math':('Matemática','Potências e funções','Potências, raízes e logaritmos'),
 'linear':('Matemática','Álgebra','Equações e expressões'),
 'matrix':('Matemática','Álgebra','Equações e expressões'),
 'seq':('Matemática','Álgebra','Progressões e sequências'),
 'geom':('Matemática','Geometria','Área e perímetro'),
 'volume_geom':('Matemática','Geometria','Volume e geometria espacial'),
 'trig':('Matemática','Trigonometria','Trigonometria e geometria angular'),
 'prob':('Matemática','Estatística e probabilidade','Probabilidade e combinatória'),
 'stat':('Matemática','Estatística e probabilidade','Médias e estatística descritiva'),
 'science_math':('Matemática','Ferramentas matemáticas','Calculadora científica'),
 'tax':('Finanças','Tributos','Impostos e Simples Nacional'),
 'interest':('Finanças','Juros','Juros compostos'),
 'interest_simple':('Finanças','Juros','Juros simples'),
 'investment':('Finanças','Investimentos','Rendimento geral'),
 'fixed':('Finanças','Investimentos','CDB, CDI e renda fixa'),
 'treasury':('Finanças','Investimentos','Tesouro Direto'),
 'loan':('Finanças','Crédito','Empréstimos'),
 'finance':('Finanças','Crédito','Financiamentos'),
 'moneytool':('Finanças','Ferramentas financeiras','Calculadora financeira e HP12C'),
 'budget':('Finanças','Planejamento financeiro','Orçamento e reserva'),
 'rate':('Finanças','Correção monetária','Inflação e índices'),
 'debt':('Finanças','Dívidas e cartões','Cartão, dívida e parcelamento'),
 'pricing':('Finanças','Custos e precificação','Precificação de produtos'),
 'payroll':('Trabalho','Remuneração','Salário líquido e bruto'),
 'worktime':('Trabalho','Remuneração','Valor da hora e dias trabalhados'),
 'extrahour':('Trabalho','Jornada e adicionais','Hora extra'),
 'workrights':('Trabalho','Legislação e direitos','Direitos trabalhistas e CLT'),
 'fgts':('Trabalho','FGTS','FGTS e multa rescisória'),
 'workleave':('Trabalho','Afastamentos','Licenças e afastamentos'),
 'workbenefit':('Trabalho','Descontos e benefícios','Vale-transporte e benefícios'),
 'thirteenth':('Trabalho','Décimo terceiro','Décimo terceiro salário'),
 'rescision':('Trabalho','Rescisão','Rescisão trabalhista'),
 'retirement':('Trabalho','Previdência e benefícios','Previdência e benefícios do INSS'),
 'worktool':('Trabalho','Ferramentas trabalhistas','Calculadora trabalhista geral'),
 'wall':('Construção','Metragem','Área aplicada à construção'),
 'waterproof':('Construção','Impermeabilização','Impermeabilização e vedação'),
 'stair':('Construção','Escadas e rampas','Escadas e rampas'),
 'revest':('Construção','Pisos e revestimentos','Pisos e revestimentos'),
 'concrete':('Construção','Concreto','Concreto, cimento, areia e brita'),
 'solar':('Energia','Energia solar','Dimensionamento solar'),
 'energy':('Energia','Aparelhos elétricos','Consumo de aparelhos'),
 'drive':('Energia','Combustíveis','Custo de viagem'),
 'health':('Fora de escopo','Saúde','Saúde/gestação'),
 'animal':('Fora de escopo','Preço de mercado','Commodity pecuária'),
 'fuelprice':('Fora de escopo','Preço de mercado','Combustíveis/preço de mercado'),
 'education':('Fora de escopo','Educação','Cursos e duração'),
 'enem':('Fora de escopo','Educação','Exercícios e notas escolares'),
 'juridic':('Fora de escopo','Jurídico','Cálculos jurídicos'),
 'law':('Fora de escopo','Serviços/software','Consulta navegacional'),
 'software':('Fora de escopo','Software','Sistemas financeiros/software'),
 'app':('Fora de escopo','Aplicativos','WhatsApp GB'),
 'promo':('Fora de escopo','Comércio e promoções','Cupons e promoções'),
 'product':('Fora de escopo','Conteúdo técnico/produto','Consulta técnica não conversível'),
 'navigation':('Fora de escopo','Serviços/software','Consulta navegacional'),
 'out':('Fora de escopo','Consulta ambígua','Finanças/serviço não resolvido'),
}

CUR=[('ARS',r'(?:pesos? argentinos?|ars)'),('CLP',r'(?:pesos? chilenos?|clp)'),('COP',r'(?:pesos? colombianos?|cop)'),('MXN',r'(?:pesos? mexicanos?|mxn)'),('UYU',r'(?:pesos? uruguaios?|uyu)'),('PYG',r'(?:guaranis?|pyg)'),('USD',r'(?:usd|us dollar|dolar(?:es)?(?: americano[s]?)?|dollar[s]?)'),('BRL',r'(?:brl|rea(?:l|is))'),('EUR',r'(?:eur|euro[s]?)'),('GBP',r'(?:gbp|libras?(?: esterlinas?)?)'),('CHF',r'(?:chf|francos? suicos?)'),('JPY',r'(?:jpy|ienes?|yens?)'),('CAD',r'(?:cad|dolar(?:es)? canadenses?)'),('KRW',r'(?:krw|won[s]?)'),('CNY',r'(?:cny|yuan[s]?)'),('AED',r'(?:aed|dirham[s]?)'),('SEK',r'(?:sek|coroas? suecas?)')]

UNITS=[('km/h',r'km\s*/?\s*h|quilometros? por hora'),('m/s',r'm\s*/\s*s|metros? por segundo'),('cm²',r'cm2|centimetros? quadrados?'),('m²',r'm2|metros? quadrados?'),('cm³',r'cm3|centimetros? cubicos?'),('m³',r'm3|metros? cubicos?'),('°F',r'fahrenheit|farenheit|farenheits|firehigh'),('°C',r'celsius'),('kW',r'kw|kilowatt|quilo watt'),('W',r'watts?|w'),('VA',r'va'),('cv',r'cv|cavalos?(?: de potencia)?'),('kV',r'kv'),('Hz',r'hz|hertz'),('rpm',r'rpm'),('psi',r'psi'),('MPa',r'mpa'),('kPa',r'kpa'),('Pa',r'pascal|pa'),('bar',r'bar'),('atm',r'atm|atmosferas?'),('mm',r'mm|milimetros?'),('cm',r'cm|centimetros?'),('km',r'km|quilometros?'),('mi',r'milhas?|miles?'),('in',r'polegadas?|inch(?:es)?|pol'),('ft',r'pes|feet|foot'),('yd',r'jardas?'),('m',r'm|metros?'),('t',r'toneladas?'),('kg',r'kg|quilos?|quilogramas?'),('µg',r'microgramas?'),('mg',r'mg|miligramas?'),('g',r'g|gramas?'),('lb',r'lb|lbs|libras?'),('L',r'litros?|l'),('mL',r'ml|mililitros?'),('gal',r'galoes?'),('GB',r'gb|gigabytes?'),('MB',r'mb|megabytes?'),('s',r'segundos?|s'),('min',r'minutos?'),('ms',r'milissegundos?'),('h',r'horas?'),('dias',r'dias?'),('semanas',r'semanas?'),('meses',r'meses?|mes'),('anos',r'anos?')]

def tokens(regex_list,t):
    matches=[]
    for c,rx in regex_list:
        for m in re.finditer(r'(?<![a-z])(?:'+rx+r')(?!\w)',t):matches.append((m.start(),m.end(),c))
    matches.sort(key=lambda x:(x[0],-(x[1]-x[0])))
    result=[]
    for x in matches:
        if not any(not(x[1]<=v[0] or x[0]>=v[1]) for v in result):result.append(x)
    return sorted(result)

def classify(entry):
    t=norm(entry['Keyword']); toks=tokens(CUR,t); units=tokens(UNITS,t)
    cls={'classe':None,'intent':None,'status':'VALIDADO','rule':'','reason':'', 'origin':'','dest':'', 'manual':'não','confidence':'alta', 'fit':'ferramenta'}
    def apply(klass,intent,reason,rule,status='VALIDADO',origin='',dest='',fit='ferramenta',conf='alta'):
        cls.update(classe=klass,intent=intent,reason=reason,rule=rule,status=status,origin=origin,dest=dest,fit=fit,manual=('sim' if status=='PENDENTE_CONTEXTUAL' else 'não'),confidence=conf)
    def tentative(why):
        cls.update(status='PENDENTE_CONTEXTUAL',reason=why,rule='contexto_insuficiente',fit='depende contexto',manual='sim',confidence='baixa')
    # Curated contextual overrides: inspectable keywords previously falling through.
    precise={
       'calculadora gps':(None,None,'GPS pode ser guia da previdência ou localização; sem contexto não presumir.'),
       'artigo 29':(None,None,'Número de artigo sem código/lei, contexto indeterminado.'),
       'artigo 482':('workrights','informacional','Artigo 482 da CLT: justa causa, informação jurídica trabalhista.'),
       'multa do artigo 477':('rescision','informacional','Multa por atraso na quitação de rescisão (art. 477 da CLT).'),
       'lei do domestico':('workrights','informacional','Legislação trabalhista específica dos empregados domésticos.'),
       'legislacao do empregado domestico':('workrights','informacional','Direitos de trabalhador doméstico.'),
       'formula matematica financeira':('interest','informacional','Fórmulas de matemática financeira; conteúdo educacional.'),
       'formula de volume':('volume_geom','informacional','Fórmula geométrica para calcular o volume.'),
       'formula do volume':('volume_geom','informacional','Fórmula geométrica de volume.'),
       'formula da esfera':('volume_geom','informacional','Fórmula de volume de esfera.'),
       'calculadora de semanas':('time','cálculo contextual','Conversor/contagem de semanas genérico; exigir unidade ou datas.'),
       'calcular minutos':('duration','cálculo direto','Operação com minutos e tempo de duração.'),
       'calculo da hora':(None,None,'Hora pode ser horário, jornada ou custo; falta informação.'),
       'calcular pj':('payroll','cálculo contextual','Valor de remuneração como pessoa jurídica, exigindo impostos e custos.'),
       'renda variavel':('investment','informacional','Investimento em renda variável; não folha trabalhista.'),
       'credito construcao':('finance','simulação/projeção','Crédito destinado à construção de imóveis.'),
       'revisao vida toda':('retirement','informacional','Revisão de aposentadoria; não energia ou matemática.'),
       'revisao da vida toda':('retirement','informacional','Revisão de aposentadoria; não energia ou matemática.'),
       'calculadora juros banco central':('interest','cálculo contextual','Calculadora de taxas bancárias, sujeita a período e indexador.'),
       'calculo juros banco central':('interest','cálculo contextual','Cálculo de juros em simulador Bacen; requer taxa e período.'),
       'ipva atrasado da multa':('tax','cálculo contextual','Multa/IPVA em atraso; cálculo tributário por UF e período.'),
       'multa e ipva':('tax','informacional','Multas de veículo e imposto IPVA, não folha trabalhista.'),
       'alvara prefeitura':('navigation','navegacional/transacional','Serviço municipal de licenciamento/consulta.'),
       'alvara da prefeitura':('navigation','navegacional/transacional','Serviço municipal de licenciamento/consulta.'),
       'alvara de funcionamento prefeitura':('navigation','navegacional/transacional','Licenciamento municipal de estabelecimento.'),
       'prefeitura alvara':('navigation','navegacional/transacional','Serviço municipal de licenciamento/consulta.'),
       'prefeitura alvara de funcionamento':('navigation','navegacional/transacional','Serviço municipal de licenciamento/consulta.'),
       'simulacao nubank':('loan','simulação/projeção','Simulação bancária; falta especificar modalidade do produto.'),
       'simulador santander':('loan','simulação/projeção','Simulador bancário sem modalidade específica.'),
       'simulacao santander':('loan','simulação/projeção','Simulador bancário sem modalidade específica.'),
       'simulador banco do brasil':('loan','simulação/projeção','Simulador bancário sem modalidade específica.'),
       'simulador do banco do brasil':('loan','simulação/projeção','Simulador bancário sem modalidade específica.'),
       'simulador bv':('finance','simulação/projeção','Simulação de financiamento, exigir modalidade e parâmetros.'),
       'simulacao da honda':('finance','simulação/projeção','Simulação de financiamento veicular Honda, não cálculo geral.'),
       'caixa economica federal simulador':('finance','simulação/projeção','Simulador da Caixa sem produto explícito: selecionar modalidade.'),
       'carro zero sem entrada':('finance','informacional','Oferta/condições de financiamento de veículos.'),
       'comprar carro com nome sujo':('loan','informacional','Consulta sobre obtenção de crédito para veículo.'),
       'dinheiro emprestado na hora para negativado':('loan','navegacional/transacional','Consulta comercial de empréstimo para negativados.'),
       'refinanciar carro':('loan','simulação/projeção','Refinanciamento com garantia de veículo.'),
       'refinanciar veiculo':('loan','simulação/projeção','Refinanciamento com garantia de veículo.'),
       'santander veiculos':('finance','navegacional/transacional','Produto bancário/financiamento de veículos.'),
       'banco hyundai':('finance','navegacional/transacional','Produto bancário da montadora Hyundai.'),
       'bv financeira carros para negativados':('loan','navegacional/transacional','Busca de crédito automotivo para negativados.'),
       'proposta habitacional caixa':('finance','navegacional/transacional','Proposta de financiamento habitacional.'),
       'taxa equivalente':('interest','cálculo direto','Equivalência de taxas em matemática financeira.'),
       'melhor banco para render dinheiro':('investment','informacional','Comparação de investimento/rendimentos bancários.'),
       'desconto salarial':('payroll','cálculo contextual','Desconto em folha de pagamento.'),
       'calculadora de preco':('pricing','cálculo contextual','Cálculo de preço/margem/custo do produto.'),
       'calculo trabalhista online gratis':('worktool','cálculo contextual','Ferramenta trabalhista online.'),
       'calculos exatos trabalhista':('worktool','navegacional/transacional','Busca de serviço/marca de cálculos trabalhistas.'),
       'calculo exato para aluguel':('rate','cálculo contextual','Reajuste de aluguel, requer índice e datas.'),
       'calculos exatos aluguel':('rate','navegacional/transacional','Nome de ferramenta de correção de aluguel.'),
       'parcelas do 13':('thirteenth','cálculo contextual','Parcelas do 13º dependem da base e datas.'),
       'conta exata':(None,None,'Nome genérico de ferramenta ou cálculo sem operação.'),
       'calculadora de hora':('duration','cálculo direto','Calculadora de duração em horas.'),
       'calculadora de horas':('duration','cálculo direto','Calculadora de duração em horas.'),
       'conversor de tempo':('time','cálculo contextual','Conversor temporal exige par de unidades.'),
       'conversor de hora':('time','cálculo contextual','Conversor temporal exige par de unidades.'),
       'conversor de horas':('time','cálculo contextual','Conversor temporal exige par de unidades.'),
       'conversor de horario':('time','cálculo contextual','Conversor de horário requer fuso/formato.'),
       'calculador de dias':('date','cálculo contextual','Contagem de dias exige datas inicial e final.'),
       'calcula prazo':('months','cálculo contextual','Cálculo de prazo exige data-base, unidade e calendário.'),
       'calcular prazo':('months','cálculo contextual','Cálculo de prazo exige data-base, unidade e calendário.'),
       'distancia entre dois enderecos':('out','informacional','Distância por rotas é geolocalização, não data/calendário.'),
       'passagem de onibus mais barato':('out','informacional','Pesquisa comercial de passagem, não cálculo.'),
       'educacao fisica quantos anos':('education','informacional','Duração de curso superior, não conversão de anos.'),
       'terapia ocupacional quantos anos':('education','informacional','Duração de graduação, não conversão de anos.'),
       'bombeiro civil ganha quanto':('payroll','informacional','Pesquisa salarial de profissão.'),
       'revisao vida toda stf':('retirement','informacional','Assunto previdenciário/jurisprudência.'),
       'mauricio godinho delgado':('out','informacional','Busca por pessoa/autor de direito trabalhista.'),
       'alqueires em metros':('area','cálculo contextual','Alqueire tem padrões regionais; indicar hectare/m² e localidade.'),
       'quantos hectares tem um alqueire':('area','cálculo contextual','Alqueire depende da região; unidade não única.'),
       'calculadora queda de tensao':('electric','cálculo contextual','Queda de tensão depende de circuito, condutor e corrente.'),
       'calculo de queda de tensao':('electric','cálculo contextual','Cálculo elétrico de queda de tensão.'),
       'volts e watts':('electric','cálculo contextual','Grandezas V e W distintas; corrente e dados da carga exigidos.'),
       'volts para watts':('electric','cálculo contextual','V→W não é conversão simples; precisa de corrente/carga.'),
       'kgf para newton':('power','conversão direta','Conversão de força kgf→N com gravidade padrão.'),
       'kn para kgf':('power','conversão direta','Grandezas de força kN→kgf, adotando gravidade padrão.'),
       'graus em fahrenheit':('temp','cálculo contextual','Escala de origem não indicada, não assumir Celsius.'),
       'graus fahrenheit':('temp','informacional','Indica escala Fahrenheit sem origem de conversão.'),
       'graus para fahrenheit':('temp','cálculo contextual','Falta escala de origem; não presumir Celsius.'),
       'grau fahrenheit':('temp','informacional','Termo Fahrenheit sem par de conversão.'),
       'graus farenheits':('temp','informacional','Fahrenheit mencionado sem escala de origem.'),
       '58 fahrenheit':('temp','cálculo contextual','Medida em °F sem temperatura de destino.'),
       'c fahrenheit':('temp','cálculo contextual','Celsius e Fahrenheit identificáveis; definir lado de origem.'),
       'c celsius':('temp','informacional','Celsius sem par de conversão.'),
       'f para celsius':('temp','conversão direta','Símbolo F→C, escalas Fahrenheit→Celsius.'),
       'kmh para ms':('length','conversão direta','Velocidade km/h→m/s explicitada.'),
       'km h para ms':('length','conversão direta','Velocidade km/h→m/s explicitada.'),
       '3milhas em km':('length','conversão direta','Milhas→km explicitado na consulta.'),
       '32mm em polegada':('length','conversão direta','Milímetros→polegadas explícito.'),
       '10mm em polegada':('length','conversão direta','Milímetros→polegadas explícito.'),
       '16mm em polegada':('length','conversão direta','Milímetros→polegadas explícito.'),
       '20mm em polegadas':('length','conversão direta','Milímetros→polegadas explícito.'),
       '25mm em polegadas':('length','conversão direta','Milímetros→polegadas explícito.'),
       '40mm em polegadas':('length','conversão direta','Milímetros→polegadas explícito.'),
       '50mm em polegadas':('length','conversão direta','Milímetros→polegadas explícito.'),
       '500 mil wons em reais':('currency','conversão direta','Moeda sul-coreana KRW→BRL explícita.'),
       '1000 ml e 1 litro':('volume','informacional','Equivalência já expressa; não multiplicar volumes Ads.'),
       '100 milhas por hora em km':('length','cálculo contextual','Velocidade mph exige destino em km/h, não km puro.'),
       'milhas por hora para km h':('length','conversão direta','Velocidade mph→km/h; ambas são velocidades.'),
       'dias em anos':('time','cálculo contextual','Ano pode ser civil ou de 365/365,25 dias.'),
       'quantos dias tem um mes':('time','cálculo contextual','Mês civil varia de 28 a 31 dias.'),
       'km ml':(None,None,'km e mL misturam distância/volume; talvez consumo de veículo, falta contexto.'),
       'g hz':(None,None,'Grama e hertz são dimensões incompatíveis; termo provavelmente truncado.'),
       'm hz':(None,None,'Metro e hertz são dimensões distintas; falta contexto de onda.'),
       'gal[oõ]es de agua 20 litros':('product','informacional','Recipiente de água com capacidade de 20L, não conversão.'),
       'como somar horas em excel':('duration','cálculo direto','Soma de horas em planilha Excel, não conversão de arquivo.'),
       'como saber se um numero e primo':('prime','informacional','Verificação de primalidade matematicamente definida.'),
       'expoente fracionario':('power_math','informacional','Expoente fracionário em álgebra.'),
       'expoentes negativos':('power_math','informacional','Potenciação com expoente negativo.'),
       '3elevado a 5':('power_math','cálculo direto','3^5 é operação numérica explícita.'),
       '2elevado a 6':('power_math','cálculo direto','2^6 é operação numérica explícita.'),
       'sistemalinear':('linear','informacional','Sistema linear (grafia sem espaço).'),
       'trinomios quadrados perfeitos':('linear','informacional','Identidades algébricas, não conversor.'),
       'razao aurea':('geom','informacional','Proporção áurea, conteúdo matemático.'),
       'hp 50g':('moneytool','informacional','Modelo de calculadora científica, não ação de cálculo.'),
       'tabela de polegada':('length','tabela/referência','Tabela de medidas em polegadas, sem operação direcional.'),
       'tabelas polegadas':('length','tabela/referência','Tabela de medidas em polegadas.'),
       'tabela milimetro polegada':('length','tabela/referência','Tabela milímetros/polegadas sem origem direcional.'),
       'tabela milimetros polegadas':('length','tabela/referência','Tabela de equivalência de medidas lineares.'),
       'segundo':('time','informacional','Unidade temporal isolada.'),
       'quantas semanas':(None,None,'Pergunta isolada sem intervalo/gestação/objeto a contar.'),
       'moeda ca':(None,None,'Moeda “ca” pode significar código truncado; não inferir moeda.'),
       'quantos meses tem':(None,None,'Período ausente; não inferir data de referência.'),
    }
    precise.update({
       'conversao de dolar':('currency','cálculo contextual','Conversão de USD sem destino especificado.'),
       'calculadora online financeira':('moneytool','cálculo contextual','Calculadora financeira genérica, precisa definir operação.'),
       'calculadoras online':('math','cálculo contextual','Portal de calculadoras sem ferramenta específica.'),
       'calcular on line':('math','cálculo contextual','Busca genérica de cálculo, sem operação específica.'),
       'calc ule online':('math','cálculo contextual','Busca de ferramenta de cálculo.'),
       'calculadora gratis':('math','cálculo contextual','Calculadora genérica online.'),
       'contador de semanas':('time','cálculo contextual','Contador de semanas exige data de origem/destino.'),
       'meses x semanas':('time','cálculo contextual','Par de unidades, calendário/convenção são necessários.'),
       'semanas e meses':('time','cálculo contextual','Conversão contextual meses↔semanas.'),
       'semanas em meses':('time','cálculo contextual','Conversão semana→mês requer convenção de mês.'),
       'tabela de conversao':('generic','tabela/referência','Tabela genérica sem grandeza especificada.'),
       'conversor de energia':('power','cálculo contextual','Conversor energético genérico, requer pares de unidades.'),
       'conversor de pressao':('pressure','cálculo contextual','Conversor de pressão genérico, requer pares de unidades.'),
       'conversor de torque':('pressure','cálculo contextual','Conversor de torque genérico, requer unidades.'),
       'conversores de torque':('pressure','cálculo contextual','Conversores de torque genéricos, requer unidades.'),
       'medidas de capacidade':('volume','informacional','Conceito de capacidade/volume, sem valor a converter.'),
       'medidas de temperatura':('temp','informacional','Termo geral de temperatura e escalas.'),
       'grandeza e medida':('generic','informacional','Conteúdo educacional de grandezas e medidas.'),
       'inversores de frequencia':('product','informacional','Equipamento industrial inversor de frequência.'),
       'caixa economica imoveis':('finance','navegacional/transacional','Financiamento/imóveis da Caixa.'),
       'itau imoveis':('finance','navegacional/transacional','Produtos imobiliários do Itaú.'),
       'veiculo itau':('finance','navegacional/transacional','Financiamento de veículos pelo Itaú.'),
       'preco da bezerra nelore':('animal','cotação atual','Preço de mercado pecuário.'),
       'fgt':(None,None,'Fundo de Garantia abreviado incorretamente? Sem confirmação de que seja FGTS.'),
       'calculo de fgt':(None,None,'Sigla FGT ambígua; não assumir FGTS automaticamente.'),
       'como calcular fgt':(None,None,'FGT sem S pode ser erro de digitação; confirmar intenção.'),
       'calculo de decimo':('thirteenth','cálculo contextual','Provável décimo terceiro, conferir base e vínculo.'),
       'calculo certo':(None,None,'Nome genérico de serviço/ferramenta sem cálculo específico.'),
       'notacao':(None,None,'Notação matemática, científica ou musical; domínio insuficiente.'),
       'expoente negativo':('power_math','informacional','Potências com expoente negativo.'),
       'convert ermoeda':('currency','cálculo contextual','Conversão monetária; termo separado incorretamente.'),
       'convertermoeda':('currency','cálculo contextual','Conversão monetária digitada sem espaço.'),
       'dolarhoje':('quote','cotação atual','Cotação atual do dólar, grafia sem espaço.'),
       'megabit':('bits','informacional','Grandeza digital isolada, sem direção de conversão.'),
       'mpeg mp3':('audio','cálculo contextual','Dois formatos de mídia sem direção inequívoca.'),
       'ms para segundos':('time','conversão direta','Milissegundos→segundos (ms→s) explícito.'),
       'ms para minutos':('time','conversão direta','Milissegundos→minutos (ms→min) explícito.'),
       'quantos ms tem um segundo':('time','conversão direta','Segundos→milissegundos com origem explícita.'),
       'horas minutos e segundos':('duration','cálculo contextual','Operações com duração de tempo; exigir tipo de cálculo.'),
       'horas minutos segundos':('duration','cálculo contextual','Duração em horas, minutos e segundos.'),
       'calc ulos':('math','cálculo contextual','Consulta genérica a operações.'),
       'calculados':(None,None,'Palavra sem operação, consulta genérica/errada.'),
       'calcular bebidas para festa':('out','estimativa de quantidade','Planejamento de bebidas para evento, fora das áreas atuais.'),
       'celsius fa':('temp','cálculo contextual','Celsius/Fahrenheit, grafia parcial sem direção.'),
       'kilo watt':('power','informacional','Unidade de potência kW isolada.'),
       '1k g':(None,None,'Texto possivelmente 1 kg ou notação numérica; sem certeza.'),
       'b5p211':(None,None,'Código de produto ou título financeiro sem contexto.'),
       'a voz':('out','informacional','Expressão isolada sem intenção de cálculo.'),
       'a vult':(None,None,'Expressão truncada/possivelmente erro de digitação.'),
       'ef05ma07':('out','informacional','Código curricular BNCC, não calculadora.'),
       'psc men sm ec103':('retirement','informacional','Siglas de cálculo previdenciário, sem operação explícita.'),
       'daycambio':('quote','navegacional/transacional','Nome/serviço de câmbio; busca de prestador.'),
       'atlas cambios':('quote','navegacional/transacional','Nome comercial de casa de câmbio.'),
       'e calcula':('math','cálculo contextual','Expressão genérica.'),
       'ecalculos':('juridic','navegacional/transacional','Ferramenta denominada eCálculos; pode ser consulta judicial.'),
       'resolvendo sistemas':('linear','informacional','Solução de sistemas de equações.'),
       'calculadora gratis':('math','cálculo contextual','Ferramenta genérica.'),
       'dias em anos':('time','cálculo contextual','Período civil anual pode ter 365 ou 366 dias.'),
       'converter dias em anos e meses':('time','cálculo contextual','Dois destinos temporais; precisa de convenção e data.'),
       'quantos ms tem um segundo':('time','conversão direta','1 segundo = 1000 milissegundos.'),
       'quanto euros vale um real':('currency','conversão direta','Conversão de 1 BRL para EUR (ordem invertida na pergunta).'),
       'quanto reais vale um dolar':('currency','conversão direta','Conversão de 1 USD para BRL (ordem invertida na pergunta).'),
       'moeda do japao em real':('currency','conversão direta','Iene japonês para reais.'),
       'moeda do japao para real':('currency','conversão direta','Iene japonês para reais.'),
       'moeda japao para real':('currency','conversão direta','Iene japonês para reais.'),
       'moeda chinesa para real':('currency','conversão direta','Yuan chinês para reais.'),
       'moeda aed':('quote','informacional','Código AED dos dirhams emiradenses, sem taxa de destino.'),
       'calcule online':('math','cálculo contextual','Ferramenta genérica sem operação informada.'),
       'galões de agua 20 litros':('product','informacional','Recipiente de água com volume 20L; não conversão galão↔litro.'),
       'galoes de agua 20 litros':('product','informacional','Embalagem com volume fixo, não conversão física.'),
       'como somar horas excel':('duration','cálculo direto','Soma de durações usando planilha, não conversão de arquivo.'),
       'kv':('electric','informacional','kV: quilovolt, unidade de tensão; sem pedido de cálculo.'),
       'ien e real':('currency','cálculo contextual','Par JPY/BRL sem origem direcionada.'),
       'moeda peso':(None,None,'Peso sem país; moeda não identificável.'),
       'peso moeda':(None,None,'Moeda peso sem país; impossível identificar código e taxa.'),
       'peso real':('currency','cálculo contextual','Peso sem país e sem direção; seleção necessária.'),
       'conversor de peso':(None,None,'Pode ser peso massa ou peso moeda; falta contexto.'),
       'conversor de voltagem':('electric','informacional','Ferramenta/equipamento de tensão sem parâmetros de corrente.'),
       'conversor de voltagens':('electric','informacional','Equipamento de transformação de tensão, não conversão aritmética.'),
       'conversor de horario':('time','cálculo contextual','Conversor de horário genérico; requer fuso ou formato.'),
       'dolar converter':('currency','cálculo contextual','Moeda USD com destino ausente.'),
       'converter dollar':('currency','cálculo contextual','Moeda USD com destino não informado.'),
       'convertor de dolar':('currency','cálculo contextual','Conversor monetário USD com destino não informado.'),
       'dolar calcular':('currency','cálculo contextual','Cálculo com USD sem destino.'),
       'calculadora euro':('currency','cálculo contextual','Calculadora EUR sem moeda de destino.'),
       'dollar en peso':('currency','cálculo contextual','USD→peso sem país; selecionar moeda peso.'),
       'moedas em euros':('currency','cálculo contextual','Moeda de origem não informada; destino EUR.'),
       'moeda chinesa para real':('currency','conversão direta','CNY→BRL explícito por nacionalidade.'),
    })
    if t in precise:
        klass,intent,reason=precise[t]
        if klass is None:tentative(reason)
        else:
            orig,dest='', ''
            direct={'kgf para newton':('kgf','N'),'kn para kgf':('kN','kgf'),'f para celsius':('°F','°C'),'kmh para ms':('km/h','m/s'),'km h para ms':('km/h','m/s'),'3milhas em km':('mi','km'),'32mm em polegada':('mm','in'),'10mm em polegada':('mm','in'),'16mm em polegada':('mm','in'),'20mm em polegadas':('mm','in'),'25mm em polegadas':('mm','in'),'40mm em polegadas':('mm','in'),'50mm em polegadas':('mm','in'),'500 mil wons em reais':('KRW','BRL'),'milhas por hora para km h':('mi/h','km/h')}
            direct.update({'ms para segundos':('ms','s'),'ms para minutos':('ms','min'),'quantos ms tem um segundo':('s','ms'),'quanto euros vale um real':('BRL','EUR'),'quanto reais vale um dolar':('USD','BRL'),'moeda do japao em real':('JPY','BRL'),'moeda do japao para real':('JPY','BRL'),'moeda japao para real':('JPY','BRL'),'moeda chinesa para real':('CNY','BRL')})
            if intent=='conversão direta':orig,dest=direct[t]
            ctx=('VALIDADO_COM_RESSALVA' if intent in ('cálculo contextual',) else 'VALIDADO')
            apply(klass,intent,reason,'curadoria_excecao_especifica',status=ctx,origin=orig,dest=dest,fit='conteúdo' if intent=='informacional' else 'ferramenta',conf='média' if ctx!='VALIDADO' else 'alta')
        return cls
    # Priority 1: precise semantic blockers and non-calculator topics.
    AMBIGUOUS_EXACT={"como converter","qual o valor de","corresponde a","como calcular","calcular on line","calculador virtual","calcule online","calculadora gratis","calculadora online","quanto fica","conta exata","calculos exatos aluguel","calculos exatos trabalhista","fgt","kv","ms","notacao","horas minutos e segundos","horas minutos segundos","meses x semanas","semanas e meses","semanas em meses","tabela de conversao","conversor de voltagem","conversor de voltagens","conversor de energia","conversor de horario","conversor de tempo","conversor de hora","conversor de horas","conversor de peso","converter r 0 00","converter em pdf a","a voz","a vult","b5p211","conversao de dolar","conversor de pressao","conversores de torque","conversor de torque","calculadora gps","artigo 29","artigo 482"}
    if t in AMBIGUOUS_EXACT:

        tentative('Expressão genérica, truncada ou sem objeto suficiente para atribuir uma operação específica.');return cls
    if has(t,r'gestacao|gestante|fetal|sexagem|morfologico|gravidez|bebe[s]?\b|contrac(?:a|o)es?|tampao mucoso|com quantas semanas estou|^com quantas semanas$|morfol[óo]gico|dpp\b'):
        apply('health','fora de escopo','Busca sobre gestação ou saúde; não representa conversão temporal comum.','saude_gestacao',fit='fora de escopo');return cls
    if has(t,r'\benem\b|\bnota do enem\b'):
        apply('enem','informacional','Notas do ENEM dependem de regras de avaliação/ponderação; não são média aritmética universal.','educacao_enem',fit='conteúdo');return cls
    if has(t,r'faculdade.*quantos anos|quantos anos de faculdade|\bcurso de rateio\b|rateiodeconcursos|\brateio\b'):
        apply('education','informacional','Busca educacional/cursos, não uma calculadora temporal ou financeira.','educacao',fit='fora de escopo');return cls
    if has(t,r'calculo juridico|calculo judicial|calculos aasp|aasp calcul|dr calc|tjrs|tjrj|tjsp|tjmg|cadej|\bsumula\b|\btribunal\b'):
        apply('juridic','navegacional/transacional' if has(t,r'login|dr calc|ferramenta|aasp|tj') else 'informacional','Ferramenta ou norma jurídica específica; não usar como cálculo matemático comum.','juridico',fit='fora de escopo');return cls
    if has(t,r'\bgbwhatsapp\b|alexmods|\bgb whatsapp\b|\bnetflix\b|\bpower pivot\b|\bmon[s]? jonas\b|\bd paulo evaristo\b|\bliturgia\b|santos festas juninas|fotos? do dias das maes|\bterma dos laranjais\b|therma dos laranjais|\bmarques casa de concha\b|\bbook friday\b|\bclube uol\b|\bbattlefield\b|shin megami tensei|street fighter|\bvolvo\b|\bwr\s?v\b|\bhr\s?v\b|\bv rod\b|\bshell v power\b|\bblade 250\b|\bfiat\b|\bkabum\b|\bzapay\b|\bsimparic\b|\bsuvinil\b|\bvedacit\b|\bvedapren\b'):
        if 'suvinil' in t:apply('product','informacional','Simulador de cores de marca, não calculadora de materiais.','marca_produto',fit='fora de escopo')
        elif 'vedacit' in t or 'vedapren' in t:apply('waterproof','informacional','Produto de obra/impermeabilização, consulta informacional.','obra_produto',fit='conteúdo')
        else:apply('product','informacional','Consulta de aplicativo, marca, produto ou conteúdo sem intenção de cálculo.','marca_produto',fit='fora de escopo')
        return cls
    if has(t,r'\bvale a pena\b'):
        apply('product','informacional','Pedido de opinião sobre produto/serviço, não é cálculo de benefício ou desconto.','vale_a_pena',fit='fora de escopo');return cls
    if has(t,r'\bpecuaria\b|\bnovilha\b|\bcepea\b|arroba (?:da )?(?:vaca|boi)|boi cepea|preco (?:do )?(?:gado|bezerro|bezerra|vaca)|preco da arroba|\bpreco arroba\b|\barrobaboi\b|\barroba bovina\b'):
        apply('animal','cotação atual','Preço de mercado pecuário; arroba é unidade citada, mas a intenção é acompanhar preços.','mercado_pecuario',fit='fora de escopo');return cls
    if has(t,r'\bquerosene\b|\bpreco do etanol\b|\bpreco da gasolina\b'):
        apply('fuelprice','cotação atual','Consulta de preço de combustível, não cálculo de consumo.','mercado_combustiveis',fit='fora de escopo');return cls
    if has(t,r'\bformato\b.*\bpdf\b') and not has(t,r'converter|conversao|conversor'):
        apply('file','informacional','Conteúdo sobre formato de arquivo sem operação explícita.','arquivo_info',fit='conteúdo');return cls
    if has(t,r'\bleitor de pdf\b|\bgbwhatsapp\b|\bdownload\b'):
        apply('navigation','navegacional/transacional','Busca de aplicativo/visualizador, não conversão de arquivo.','aplicativo_navegacao',fit='fora de escopo');return cls
    if has(t,r'\bservico\b.*\bprevidencia\b|telefone (?:da )?previdencia|numero da previdencia|\bmeu cnis\b|\bcnis\b|\bprevidencia social\b.*\btelefone\b|\bsaque jam\b|\bconsulta\b.*\bempregador\b|\btelefone 135\b'):
        apply('retirement','navegacional/transacional','Consulta de canal, extrato ou serviço previdenciário/FGTS, não cálculo.','previdencia_servico',fit='conteúdo');return cls
    if has(t,r'\bcasamento folga\b|\bfolga (?:de |para |no )?casamento\b|\blicenca parental\b|\btrabalhando sem carteira\b|\bempregadas? domesticas?\b|\bleis? (?:do|para o) trabalhador\b|\bdireito trabalhista\b|\bequiparacao salarial\b|\bdispensa discriminatoria\b|\bsair da empresa\b|\bquebra de contrato\b|\bclt\b|\bhora in itinere\b'):
        apply('workrights','informacional','Direito/regra trabalhista; informação jurídica, não operação direta.','direito_trabalhista',fit='conteúdo');return cls
    if has(t,r'\bbpc\b|\bbolsa familia\b|\bauxilio doenca\b|\bbeneficio por incapacidade\b|\baposentad|\babono salarial\b|\brevisao da vida toda\b|\bprevidencia\b|\babono pecuniario\b|\b13\b.*aposentado'):
        klass='thirteenth' if has(t,r'^13|\b13\b|decimo terceiro') and has(t,r'aposentad') else 'retirement'
        apply(klass,'simulação/projeção' if has(t,r'\bsimulador\b') else 'informacional','Benefício previdenciário/legislação; cálculo condicionado a regras próprias quando solicitado.','beneficio_previdenciario',fit='conteúdo');return cls
    if has(t,r'\bticket\b|\bsodexo\b|\balelo\b|\bcartao vr\b|\bvale refeicao\b|\bvale alimentacao\b|\bvales?\b.*\balimentacao\b|\bcartao refeicao\b|\bcartao estudante\b'):
        if 'cartao estudante' in t:
            apply('navigation','informacional','Cartão de transporte estudantil/local, não benefício trabalhista.','transporte_local',fit='fora de escopo')
        else:apply('workbenefit','informacional','Benefício de alimentação/refeição ou produto de cartão, sem operação.','beneficios_trabalho',fit='conteúdo')
        return cls
    if has(t,r'\bquanto ganha\b|\bquanto um\b.*\bganha\b|\bquanto ganha\b|\bsalario de (?:um )?(?:deputado|tecnico|policial)|\bsalario de deputado\b|\bdeputado estadual salario\b|\btanatopraxia salario\b|\bmedia salarial\b|\btecnico de enfermagem quanto ganha\b|\bbiomedicina quanto ganha\b|\bauxiliar de enfermagem quanto ganha\b'):
        apply('payroll','informacional','Pesquisa salarial de profissão/cargo, não uma operação aritmética.','salario_profissao',fit='conteúdo');return cls
    if has(t,r'\bfgts\b|\bfgtsonline\b|\bfunda de garantia\b|^fgt\b|\bsaque jam\b'):
        apply('fgts','navegacional/transacional' if has(t,r'\bonline\b|\bconsultar\b|\bsaque\b') else ('cálculo direto' if has(t,r'\bcalcul|como calcular') else 'informacional'),'Termo de FGTS/saldo/multa trabalhista.','fgts');return cls
    if has(t,r'\b13\s*(?:salario|parcela|aposentados?)\b|\bparcela 13\b|\bdecimo terceiro\b|\b13 aposentad|\b13 para os aposentados\b'):
        apply('thirteenth','cálculo contextual' if 'parcela' in t else 'informacional','Parcela ou direito ao décimo terceiro salário.','decimo_terceiro',fit='conteúdo');return cls
    if has(t,r'\bdesconto salarial\b|\bdescontos salariais\b|\bbruto ou liquido\b|\bvalor liquido e bruto\b'):
        apply('payroll','cálculo contextual' if has(t,r'calcul|descontos') else 'informacional','Salário bruto/líquido e descontos de folha sujeitos a regras.','salario_desconto');return cls
    if has(t,r'\bhoras? extra\b|\bhora noturn|\bvalor adicional noturno\b'):
        apply('extrahour','cálculo contextual' if has(t,r'calcul|valor|100') else 'informacional','Jornada e adicionais sujeitos a percentual/jornada.','jornada_adicionais');return cls
    if has(t,r'\btempo servico\b|\btempo de servico\b|\bdia trabalhado\b|\bdia de trabalho\b|\bvalor hora trabalho\b|\bdescontar? 2\b|funcionario falta'):
        apply('worktime','cálculo contextual' if has(t,r'calcul|dia|valor') else 'informacional','Tempo ou proporção de trabalho, não diferença de datas genérica.','jornada_trabalho');return cls
    if has(t,r'\bplr\b|\btrct\b|\bacordo entre as partes\b|\bacordo mutuo\b|\brescisao\b'):
        apply('rescision','informacional' if has(t,r'\bo que\b|\bacordo\b') else 'cálculo contextual','Verbas e direitos de desligamento/trabalho.','rescisao',fit='conteúdo');return cls
    if has(t,r'\btrabalhist\b|calculadora trabalhista'):
        apply('worktool','cálculo contextual' if has(t,r'\bcalcul') else 'informacional','Ferramenta geral de cálculos trabalhistas.','calculadora_trabalhista');return cls
    if has(t,r'\bgps\b'):
        if has(t,r'\bcalcul|em atraso'):
            apply('retirement','cálculo contextual','GPS em atraso: guia de Previdência, juros e regras próprias.','guia_previdenciaria',status='VALIDADO_COM_RESSALVA');return cls
        tentative('GPS isolado pode ser localização ou Guia da Previdência Social; falta contexto.');return cls
    # Explicit construction and domain-specific real-world needs.
    if has(t,r'\bescada\b|\bpiso[s]? para escada\b'):
        apply('stair','cálculo contextual' if has(t,r'calcul') else 'informacional','Escada/etapas e dimensões de construção.','escada_construcao');return cls
    if has(t,r'\bmetro cubico\b|\bmetros cubicos\b|\bm3\b') and has(t,r'\bcalcular\b|\bcomo calcular\b'):
        apply('volume_geom','cálculo direto','Cálculo geométrico de volume sem contexto de insumos.','geometria_volume');return cls
    if has(t,r'\bparede\b|\breboco\b|\brebocar\b|\bborracha liquida\b|\bimpermeabil'):
        klass='waterproof' if has(t,r'borracha|impermeabil') else 'concrete'
        apply(klass,'informacional' if has(t,r'borracha|material') else 'estimativa de quantidade','Material/revestimento de parede na construção.','material_obra',fit='conteúdo');return cls
    if has(t,r'\bpisos?\b|\bpintura\b') and not has(t,r'\bsalarial\b'):
        apply('revest','estimativa de quantidade' if has(t,r'quant|calcul') else 'informacional','Pisos/revestimentos são insumos de construção.','pisos_obra');return cls
    if has(t,r'\broi\b'):
        apply('investment','cálculo direto' if has(t,r'\bcalcul') else 'informacional','ROI é retorno sobre investimento e não consumo energético.','roi_investimento',fit='conteúdo' if not has(t,r'calcul') else 'ferramenta');return cls
    if has(t,r'\binversor\b'):
        apply('solar' if has(t,r'\bplaca solar\b|\bsolar\b') else 'product', 'dimensionamento' if 'solar' in t else 'informacional','Inversor solar é dimensionamento elétrico; inversor de frequência genérico é equipamento.','inversor_contexto',fit='ferramenta' if 'solar' in t else 'conteúdo');return cls
    if has(t,r'\btransformador\b.*\b(?:110|220)\b'):
        apply('electric','informacional','Transformador 110↔220 é equipamento físico; não conversão aritmética entre tensões.','transformador_produto',fit='fora de escopo');return cls
    if has(t,r'\bvoltagem\b|\bvoltagens\b'):
        tentative('Voltagem isolada: pode envolver medição, transformador ou tensão; faltam parâmetros.');return cls
    if has(t,r'\bgal[oõ]es? de?\s*(?:5|20)\s*litros\b|\bgaloes?\s*20\s*litros\b|\bgal[oõ]es?\s*5\s*litros\b'):
        apply('product','informacional','Consulta a recipientes com capacidade declarada, não unidade galão↔litro.','embalagem_galao',fit='fora de escopo');return cls
    if has(t,r'\bviagem de carro\b'):
        apply('drive','cálculo contextual','Custo de viagem de carro exige distância/consumo e preço do combustível.','viagem_automovel');return cls
    # Finance: explicit brands and government interactions vs calculations.
    if has(t,r'\bimovel\b|\bimobiliario\b|\bhabitacao\b|\bsbpe\b|\bfiname\b|\bbndes\b|\bfinanciad|\bfinanciamento\b|\brefinancia\b'):
        apply('finance','simulação/projeção' if has(t,r'\bsimula|\bfinancia\b') else 'navegacional/transacional' if has(t,r'banco|caixa|santander|itau|cef|bndes|finame|siopi|sbpe|credito') else 'informacional','Financiamento imobiliário/veicular ou linha de crédito, com parâmetros da instituição.','financiamento');return cls
    if has(t,r'\bempresta\b|\bemprestimo\b|\bcredi[tc]as\b|\bcrefaz\b|\bagiota\b|\bnegativad\b|\bportabilidade\b.*\btroco\b'):
        apply('loan','simulação/projeção' if has(t,r'\bsimula|portabilidade') else 'navegacional/transacional','Crédito/contratação e empréstimo, não conversão de grandezas.','credito',fit='ferramenta' if has(t,r'simula') else 'conteúdo');return cls
    if has(t,r'\bparcelament|\bparcelar\b|\bparcelado\b|\bdivida mei\b|\biptu\b|\bicms\b|\bsefaz\b|\breceita federal\b|\bmei\b|\bdas\b'):
        klass='tax' if has(t,r'\biptu\b|\bicms\b|\bsefaz\b|\breceita federal\b|\bmei\b|\bdas\b|\bsimples nacional\b') else 'debt'
        apply(klass,'navegacional/transacional' if has(t,r'\bnegoci|parcelar|parcelamento|receita federal|sefaz') else 'informacional','Dívida/parcelamento tributário exige regras do órgão credor.','divida_tributaria',fit='conteúdo');return cls
    if has(t,r'\bjuros?\b|\bjuro simples\b|\bmontante\b') and not has(t,r'\bjuros banco central\b|\btaxa do di\b'):
        klass='interest_simple' if has(t,r'\bjuro simples\b|\bjuros simples\b') and not has(t,r'compostos?') else 'interest'
        apply(klass,'informacional' if has(t,r'\bformula\b|\bfórmula\b|simples juro composto') else 'cálculo direto' if has(t,r'\bcalcul') else 'informacional','Juros/montante são funções financeiras, não salário nem trabalho.','juros_financeiros');return cls
    if has(t,r'\bincc\b|\bigpm\b|\bcorr[eç]ao de valores\b|\batualizar um valor\b|\bvalores atualizados\b|\bcorrecao\b'):
        apply('rate','cálculo contextual' if has(t,r'\bcalcul|atualizar|correcao') else 'informacional','Correção monetária depende de índice e datas.','correcao_monetaria',status='VALIDADO_COM_RESSALVA');return cls
    if has(t,r'\bcontabil\b|\bcontabilidade\b'):
        apply('budget','informacional','Contabilidade ou conta contábil não é calculadora de conversão.','contabilidade',fit='conteúdo');return cls
    if has(t,r'\bplanejamento financeiro\b|\bplanilha\b|\borganiza[cç]ao financeira\b|\bcontrol[e]? (?:de )?gastos\b|\bguardar dinheiro\b|\bjuntar dinheiro\b|\bcomo juntar\b|\bcontas a pagar\b'):
        apply('budget','informacional','Planejamento financeiro/planilha, não conversão de moeda ou consumo elétrico.','planejamento_financeiro',fit='conteúdo');return cls
    if has(t,r'\bcalculadora de preco\b|\bprecificacao\b'):
        apply('pricing','cálculo contextual','Calculadora de preço de venda/custo, com margem e impostos configuráveis.','preco_venda');return cls
    if has(t,r'\binvestimento\b|\binvestimentos\b|\brenda fixa\b|\btesouro\b|\btitulos publicos\b|\bdi\b|\bcd[i|b]\b'):
        klass='treasury' if has(t,r'\btesouro\b|\btitulos publicos\b') else 'fixed' if has(t,r'renda fixa|\bcd[i|b]\b|\btaxa do di\b') else 'investment'
        apply(klass,'simulação/projeção' if has(t,r'\bsimula|\bcalculadora\b') else 'informacional','Aplicação/retorno financeiro, sem operação de conversão física.','investimentos',fit='ferramenta' if has(t,r'\bsimula|\bcalculadora\b') else 'conteúdo');return cls
    if has(t,r'\bcalculadora (?:financeira|hp)\b|\bhp ?12c\b|\bhp\s?50g\b|\bhp prime\b|\bemulator\b'):
        apply('moneytool','cálculo direto' if has(t,r'\bcalculadora\b|\bemulator\b') else 'informacional','Calculadora financeira ou produto de calculadora, não matemática geral.','calculadora_financeira',fit='conteúdo' if has(t,r'\bhp ?50g|hp prime\b') else 'ferramenta');return cls
    if has(t,r'\bdolar(?:es)?\b|\bdollars?\b|\beuros?\b|\bienes?\b|\breal\b|\bbrl\b|\busd\b|\bars\b|\bclp\b|\bchf\b|\bcad\b|\bkrw\b|\bsek\b|\baed\b|\bpeso\b|\bpesos\b|\blibra\b|\bguarani\b|\bmoeda[s]?\b|\bcambio\b|\bmoeda\b|\bcotacao\b|\bvalor da moeda\b|\bexchange\b|\bcurrency converter\b|\bwise conversor\b|\bconversor de dinheiro\b|\bconversor dinheiro\b|\bconverter dinheiro\b|\bbacen\b|\bbanco central (?:taxa|cotacao|cotacoes)\b'):
        # Never assume a country for bare 'peso', or numeric direction for juxtaposition.
        curr=tokens(CUR,t)
        if has(t,r'\bpesos?\b') and not has(t,r'\b(?:argentin[oa]s?|chilen[oa]s?|colombian[oa]s?|mexican[oa]s?|uruguai[oa]s?)\b'):
            if len([c for _,_,c in curr if c!='BRL'])==0:
                if has(t,r'\bmoeda\b'):
                    tentative('Moeda “peso” sem país emissor: não se sabe o código de moeda e, portanto, a taxa.');return cls
                apply('currency','cálculo contextual','“Peso(s)” não identifica o país; a calculadora precisa solicitar a moeda específica.','peso_sem_pais',status='VALIDADO_COM_RESSALVA',conf='média');return cls
        if has(t,r'\bpreco\b|\bvalor\b|\bquanto (?:ta|esta|esta valendo|vale|custa|custo)\b|\bhoje\b|\btaxa\b|\bcotacao\b|\bbacen\b|\bbanco central\b|\buol\b') and not has(t,r'\bconvert|\bconversor\b|\bconversao\b|\bpara\b|\bem\b'):
            apply('quote','cotação atual','Consulta ao preço/taxa atual, não cálculo de direção de conversão.','cotacao_moeda',fit='conteúdo');return cls
        if len(curr)>=2:
            left,right=curr[0],curr[1]
            org=dst=''
            connector=t[left[1]:right[0]]
            # Direction only when a strong grammatical connector appears between the two explicit currency tokens.
            if re.search(r'\b(?:para|em|to|en|a)\b',connector) and not re.search(r'\b(?:x|versus|vs|e)\b',connector):org,dst=left[2],right[2]
            elif 'quanto' in t and re.search(r'\bvale\b|\bequivale\b',t):org,dst=left[2],right[2]
            # "valor em real do peso argentino" is inverse despite surface order
            if has(t,r'\bvalor em real (?:do|da) peso argentino\b'):org,dst='ARS','BRL'
            # "um peso argentino vale quantos reais" is explicit directional
            if org and dst and org!=dst:
                apply('currency','conversão direta','Origem/destino explicitados pela relação linguística entre moedas.','cambio_direcional',origin=org,dest=dst);return cls
            if len({x[2] for x in curr})<2:
                apply('quote','informacional','Mesma moeda expressa em nomes/códigos equivalentes; não existe par cambial.','moeda_equivalente',fit='conteúdo');return cls
            apply('currency','cálculo contextual','Par cambial identificável, mas sem direção inequívoca: ferramenta deve permitir selecionar origem/destino.','cambio_bidirecional',status='VALIDADO_COM_RESSALVA',conf='média');return cls
        if len(curr)==1:
            if has(t,r'\b(?:convert|conversor|conversao)\b'):
                apply('currency','cálculo contextual','Moeda identificada, porém falta contraparte/destino; solicitar antes do cálculo.','moeda_sem_par',status='VALIDADO_COM_RESSALVA',conf='média');return cls
            if has(t,r'^\d+[\.,\d]*\s*(?:dolar|dollar|euros?|usd|cad|brl|real|yen|won|pesos?)\b'):
                apply('currency','cálculo contextual','Valor expresso em moeda sem unidade de destino; solicitar segunda moeda.','valor_moeda_sem_destino',status='VALIDADO_COM_RESSALVA',conf='média');return cls
            apply('quote','cotação atual' if has(t,r'valor|preco|hoje|moeda|quanto|cotacao') else 'informacional','Moeda isolada: não inferir conversão direcional.','moeda_isolada',fit='conteúdo',conf='média');return cls
        if has(t,r'\bconversor\b|\bconverter\b|\bconversao\b|\bcambio\b|\bwise\b'):
            apply('currency','cálculo contextual','Ferramenta de câmbio genérica sem par definido.','conversor_moeda_generico',status='VALIDADO_COM_RESSALVA',conf='média');return cls
        apply('quote','cotação atual','Cotação, taxa ou preço de mercado cambial genérico.','cotacao_generica',fit='conteúdo',conf='média');return cls
    # Converters for files. Direction can be read from syntax or user may select source.
    fmt={'pdf','png','jpg','jpeg','gif','mp3','mp4','xls','xlsx','csv','ppt','powerpoint','word','dwg','cdr','ico','epub','mobi','rar','zip','ofx','excel','mpeg','wav','avi'}
    filetok=[x for x in t.split() if x in fmt]
    if filetok or has(t,r'\barquivos?\b|\bimagem\b|\baudio\b|\bvideo\b|\byoutube\b|\bmusica\b|\bconvert\s+io\b|\bclip convert\b|\bconvertor\b'):
        if has(t,r'\bimobiliario\b|\bcambio\b'):pass
        elif has(t,r'\bconverter pdf em pdf\b'):
            tentative('Mesmo formato PDF na origem e destino; pode significar otimização, OCR ou outro processo.');return cls
        elif has(t,r'\bpower pivot\b'):pass
        elif has(t,r'\bconvert io\b|\bclip convert\b|\bconvertor\b'):
            apply('file','navegacional/transacional','Busca de plataforma específica, não necessariamente uma operação indicada.','servico_conversao',fit='conteúdo');return cls
        elif has(t,r'\bconvert(?:er|or)?\b|\bconversor\b|\bpara\b|\bem\b|\bimagem\b|\baudio\b|\bvideo\b|\byoutube\b|\bmusica\b|\bpdf\b|\bpng\b|\bjpe?g\b'):
            kind='audio' if 'mp3' in t or 'wav' in t or 'mpeg' in t and 'mp4' not in t else 'video' if 'mp4' in t or 'avi' in t else 'image' if ('jpg' in t or 'jpeg' in t or 'gif' in t or 'png' in t or 'ico' in t) and not has(t,r'\bpdf\b|\bexcel\b|\bword\b|\bppt\b|\bpowerpoint\b') else 'file'
            apply(kind,'conversão de arquivo/mídia','Conversão/formato de arquivo ou mídia: não confundir com unidades monetárias.','conversao_arquivo',status='VALIDADO_COM_RESSALVA' if len(filetok)<2 else 'VALIDADO',conf='média' if len(filetok)<2 else 'alta');return cls
    # Calendar and durations before generic units to avoid false positives.
    if has(t,r'\bferiado\b|\bferiados\b|\bcalendario\b|\bdias das maes\b|\bdatas comemorativas\b'):
        apply('holiday','tabela/referência','Busca de feriados/agenda, não duração matemática.','calendario',fit='conteúdo');return cls
    if has(t,r'\bmes de agosto\b|\bcontador de mes\b|\bcalculadora de (?:m[eê]s|mes)\b|\bcalcular meses\b'):
        apply('months','cálculo contextual','Contagem de meses exige datas ou período inicial e final.','datas_meses',status='VALIDADO_COM_RESSALVA');return cls
    if has(t,r'\bha quanto tempo ou a quanto tempo\b|\ba quanto tempo ou ha quanto tempo\b|\ba quanto tempo ou ha quanto tempo\b'):
        apply('out','informacional','Dúvida ortográfica entre “há” e “a”, não operação com datas.','duvida_gramatical',fit='fora de escopo');return cls
    if has(t,r'\bquanto tempo\b|\bcalcular horas e minutos\b|\bcontar horas\b|\bsomar horas\b|\bcalculadora de horas\b'):
        apply('duration','cálculo direto' if has(t,r'\bcalcul|\bcontar\b|\bsomar\b') else 'informacional','Duração/horas; não é conversão de moeda.','duracao');return cls
    if has(t,r'\bha quanto tempo\b|\ba quanto tempo\b'):
        apply('out','informacional','Consulta gramatical entre “há” e “a”; não cálculo de datas.','gramatica',fit='fora de escopo');return cls
    if has(t,r'\bhorario de almoco\b|\bdias vai ser o enem\b'):
        apply('calendar','informacional','Consulta de agenda/horário, não cálculo de duração.','agenda_informacional',fit='conteúdo');return cls
    if has(t,r'\bquantos meses\b|\bquantas semanas\b|\bsemanas\b.*\bmeses\b|\bmeses\b.*\bsemanas\b'):
        if has(t,r'\bquantos meses tem\b|\bquantos meses sao\b') and not has(t,r'\bsemanas\b'):
            tentative('“Quantos meses tem” carece de período de referência.');return cls
        apply('time','cálculo contextual','Conversão semana↔mês depende de convenção: calendário, média astronômica ou semana gestacional.','semanas_meses_contextuais',status='VALIDADO_COM_RESSALVA',conf='média');return cls
    # Mathematics: explicit fields, not math words in payroll/salary contexts.
    if has(t,r'\bnumeros? primos?\b|\bfator(?:acao|es) primos\b|\bmdc\b|\bmaximo divisor comum\b|\bnumeros? compostos?\b|\bdividendo\b|\bdivisor\b|\bquociente\b'):
        apply('prime','informacional' if has(t,r'\bo que\b|\bquais\b|\btodos\b|\bde 1 a\b|\bcomo fazer\b|\bpropriedades\b') else 'cálculo direto','Teoria de números e divisibilidade, não preço de mercado.','aritmetica_numeros');return cls
    if has(t,r'\bpa\b|\bpg\b|\bprogress[oa]es\b|\bprogressao\b|\bsequencias?\b|\bfibonacci\b|\btermo geral\b'):
        apply('seq','cálculo direto' if has(t,r'\bsoma\b|\btermo geral\b|\bcalcul') else 'informacional','Progressão, soma/termo de PA ou PG.','sequencias_matematicas');return cls
    if has(t,r'\bmatriz\b|\bmatrizes\b|\bdeterminante\b|\bsistemas? lineares\b|\bequac\b|\bfatoracao de polinomio\b|\btrinomio\b|\bmetodo substituicao\b|\bsolvendo sistemas\b'):
        apply('linear','cálculo direto' if has(t,r'\bdeterminante\b|\bmatriz calculator\b|\bresolv|\bfatoracao\b') else 'informacional','Álgebra linear/polinomial, não fórmula de preço.','algebra');return cls
    if has(t,r'\bintegral\b|\blimite\b|\bteorema fundamental do calculo\b'):
        apply('science_math','cálculo direto' if has(t,r'\bcalcul|\bintegral\b|\blimite\b') else 'informacional','Cálculo diferencial/integral.','calculo_superior');return cls
    if has(t,r'\btriangul|\bretangul|\bcirculo\b|\bcirculos\b|\bcircunferencia\b|\bquadrado\b|\blosango\b|\bparalelogramo\b|\bcateto\b|\bhipotenusa\b|\bdiagonal quadrado\b|\bgeometria plana\b|\bfiguras? planas?\b|\bteorema pitagoras\b'):
        apply('geom','cálculo direto' if has(t,r'\bcalcul|\barea\b|\bhipotenusa\b|\bdiagonal\b') else 'informacional','Geometria plana/área/perímetro.','geometria_plana');return cls
    if has(t,r'\bvolume (?:(?:de |da |do )?(?:um |uma )?)?(?:cone|cubo|pir[aâ]mide|esfera)\b|\bvolume cone\b|\bformula do volume\b|\btronco de piramide\b|\bformula da esfera\b'):
        apply('volume_geom','cálculo direto' if has(t,r'\bcalcul|\bvolume\b') else 'informacional','Volume de sólido geométrico, não metrologia de líquido.','solidos_geometricos');return cls
    if has(t,r'\bcombinac|\barranjo\b|\bespaco amostral\b|\bprobabilidade\b'):
        apply('prob','cálculo direto' if has(t,r'\bcombina[cç]|\barranjos?\b') else 'informacional','Combinatória e probabilidade.','probabilidade');return cls
    if has(t,r'\bmedia\b|\bmedias\b|\bdesvio medio\b|\bmoda\b|\bvariancia\b'):
        if has(t,r'\bsalaria[l]?\b'):apply('payroll','informacional','Média salarial de mercado/categoria profissional.','salario_profissao',fit='conteúdo')
        else:apply('stat','cálculo direto' if has(t,r'\bcalcul|\bdesvio medio\b') else 'informacional','Conceito/cálculo de estatística descritiva.','estatistica')
        return cls
    if has(t,r'\bfraca|\bfracao|\bfracoes\b|\bnumeros? decima(?:l|is)\b|\barredondamento\b|\bnotacao cientifica\b'):
        apply('frac','cálculo direto' if has(t,r'\bcomo resolver\b|\bcomo dividir\b|\boperacoes\b') else 'informacional','Frações, notação decimal/arredondamento.','fracoes_decimais');return cls
    if has(t,r'\blog\b|\bln\b|\blogaritm\b|\bexponent|\bpotenci|\belevado a\b|\braizes quadradas\b|\braiz\b|\bpotencias?\b'):
        apply('power_math','cálculo direto' if has(t,r'\belevado a\b|\bcalcul|\braizes quadradas exatas\b') else 'informacional','Potências/expoentes/logaritmos/raízes.','potencias_logaritmos');return cls
    if has(t,r'\btrigonome|\bsen\b|\bcos\b|\btg\b|\barctan\b|\barcsen\b|\bradianos?\b|\bangulos?\b|\bgraus?\b.*\bradiano\b'):
        apply('trig','cálculo direto' if has(t,r'\bcalcul|\bpara\b') else 'informacional','Trigonometria e unidades angulares.','trigonometria');return cls
    if has(t,r'\bnumeracao romana\b|\bnumeros arabicos\b|\bnumero em algarismo\b'):
        apply('roman','informacional','Representação de números e bases numéricas.','numeracao',fit='conteúdo');return cls
    if has(t,r'\bcalculadora\b|\bcalculador\b|\bcalcular\b|\bcalculo\b|\bcalculos\b') and entry['area_revisada']=='Matemática':
        apply('math','cálculo direto','Calculadora matemática geral, sem operação específica na consulta.','calculadora_generica',status='VALIDADO_COM_RESSALVA',conf='média');return cls
    # Cooking contextual; explicit utensil-to-volume does not require a density.
    if has(t,r'\bcolher\b|\bxicara\b|\bgrama[s]? em ml\b|\bgrama[s]? para ml\b'):
        if has(t,r'\bcolher\b') and ('ml' in t) and not has(t,r'\bgrama|\bmg\b'):
            apply('culinary','cálculo contextual','Colher culinária↔volume usa padrão de utensílio configurável; não exige densidade.','colher_volume',status='VALIDADO_COM_RESSALVA',conf='média');return cls
        if has(t,r'\bfarinha\b'):
            apply('culinary','cálculo contextual','Conversão culinária massa↔volume depende do ingrediente e da padronização da xícara/colher.','culinaria_ingrediente',status='VALIDADO_COM_RESSALVA',conf='média');return cls
        apply('culinary','cálculo contextual','Conversão culinária massa↔volume precisa do ingrediente/densidade ou padrão da medida.','culinaria_sem_ingrediente',status='VALIDADO_COM_RESSALVA',conf='média');return cls
    # Technical physical unit matching; avoid assuming any direction from 'x', 'e', whitespace.
    us=tokens(UNITS,t)
    if len(us)>=2:
        # Product/grammar false positives caught above. Generic converter intent first.
        left,right=us[0],us[1]
        UL={left[2],right[2]}
        klass='time' if UL&{'s','min','ms','h','dias','semanas','meses','anos'} and UL<={'s','min','ms','h','dias','semanas','meses','anos'} else 'temp' if UL&{'°C','°F'} else 'pressure' if UL&{'psi','bar','MPa','Pa','kPa','atm'} else 'electric' if UL&{'VA','kV'} else 'power' if UL&{'W','kW','cv'} else 'frequency' if UL&{'rpm','Hz'} else 'area' if UL&{'m²','cm²'} else 'volume' if UL&{'m³','cm³','L','mL','gal'} else 'mass' if UL&{'t','kg','µg','mg','g','lb'} else 'bits' if UL&{'MB','GB'} else 'length'
        connector=t[left[1]:right[0]]
        org=dst=''
        if has(connector,r'\b(?:para|em|to|en|a)\b') and not has(connector,r'\b(?:x|vs|e|versus)\b'):org,dst=left[2],right[2]
        if has(t,r'\bquantos?\b|\bquantas?\b|\bequivale\b') and org=='':
            # "quantos ml tem um litro" is reversed text order.
            if has(t,r'quantos?\s+ml\s+te[mn]\b.*\blitro'):
                org,dst='L','mL'
        if UL&{'VA','kV'} and UL&{'W','kW'}:
            apply('electric','cálculo contextual','Volt-ampère/tensão↔watts exige fator de potência, corrente ou parâmetros da carga.','eletrica_contextual',status='VALIDADO_COM_RESSALVA',conf='média');return cls
        if has(t,r'\bvolts?\b') and has(t,r'watts?'):
            apply('electric','cálculo contextual','V↔W exigem corrente/potência, não são a mesma dimensão.','eletrica_dimensional',status='VALIDADO_COM_RESSALVA',conf='média');return cls
        if org and dst and org!=dst and ({org,dst} & {'g','kg','mg','µg'}) and ({org,dst} & {'mL','L'}):
            apply('culinary','cálculo contextual','Massa↔volume depende do ingrediente/densidade; não converter diretamente.','densidade_obrigatoria',status='VALIDADO_COM_RESSALVA',conf='média');return cls
        if org and dst and org!=dst:
            apply(klass,'conversão direta','Origem/destino explicitados e unidades compatíveis, sem direção presumida.','unidades_direcionais',origin=org,dest=dst);return cls
        if left[2]!=right[2]:
            apply(klass,'cálculo contextual','Duas unidades reconhecidas, sem direção inequívoca: conversor pode solicitar lado de origem.','unidades_bidirecionais',status='VALIDADO_COM_RESSALVA',conf='média');return cls
    if has(t,r'\bmetros cubicos?\b|\bmetro cubico\b'):
        apply('volume','informacional','Grandeza física volume mencionada sem pedido de conversão explícita.','unidade_isolada',fit='conteúdo');return cls
    if has(t,r'\bgramas?\b|\bmililitro\b|\bmicrogramas?\b|\bkilogramas?\b|\blb\b|\bquilos\b|\btoneladas\b|\barroba em kg\b|\bgal[oõ]es?\b'):
        if has(t,r'\barroba em kg\b'):
            apply('mass','conversão direta','Conversão massa arroba→kg explícita; tratar arroba padrão conforme contexto (pecuário Brasil).','arroba_kg',status='VALIDADO_COM_RESSALVA',origin='arroba',dest='kg');return cls
        apply('mass' if not has(t,r'\bgal[oõ]es?\b') else 'volume','informacional','Unidade mencionada sem direção/par completo de conversão.','grandeza_sem_par',fit='conteúdo',conf='média');return cls
    if has(t,r'\bpressao\b|\btorque\b'):
        apply('pressure','cálculo contextual','Grandeza pressão/torque requer unidade e operação selecionada.','grandeza_fisica',status='VALIDADO_COM_RESSALVA',conf='média');return cls
    if has(t,r'\bconversor\b|\bconverter\b|\bconversao\b'):
        apply('generic','cálculo contextual','Intenção de converter explícita, mas par/unidade incompletos na expressão.','conversor_generico',status='VALIDADO_COM_RESSALVA',conf='média');return cls
    # No adequate evidence: must not fabricate, maintain manual review.
    tentative('Ainda não há contexto suficiente para resolver a classificação com segurança; preservada a rotulagem anterior.');return cls