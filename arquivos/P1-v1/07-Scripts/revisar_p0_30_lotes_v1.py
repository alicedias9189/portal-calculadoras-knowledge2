#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Revisão semântica conservadora das 474 keywords P0 (sinalizadas, não todo o acervo).
Entradas: fila priorizada CSV, lotes classificados originais, lote 001 saneado,
          ZIP aprovado do lote 003.
Saídas: diff auditável, decisão individual, versões corrigidas dos lotes envolvidos,
        fila P0 residual e relatório. Nunca altera os originais.
Uso: python3 revisar_p0_30_lotes_v1.py --root /mnt/data
"""
import argparse, csv, hashlib, json, re, zipfile
from pathlib import Path
from collections import Counter, defaultdict

ap=argparse.ArgumentParser(); ap.add_argument('--root',default='/mnt/data'); args=ap.parse_args()
ROOT=Path(args.root); OUT=ROOT/'revisao-p0-30-lotes'; OUT.mkdir(exist_ok=True)
SRC=ROOT/'saneamento-revisao-30-lotes'

def read_csv(path):
    with path.open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f,delimiter=';'))
def write_csv(path,rows,keys):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,delimiter=';',fieldnames=keys,extrasaction='ignore');w.writeheader();w.writerows(rows)

queue=read_csv(SRC/'fila-revisao-priorizada-30-lotes.csv')
p0=sorted((r for r in queue if r['prioridade']=='P0'),key=lambda a:(a['area'],a['cluster'],a['Keyword']))
assert len(p0)==474 and len({x['id_global'] for x in p0})==474
assert hashlib.sha256('|'.join(x['id_global'] for x in p0).encode()).hexdigest()=='2d6ad7da68c28fcb7ae934c259589f812f943e17a543806082ff890b25935d0d', 'Fila P0 mudou; revisar índice de decisões antes de aplicar.'
for idx,r in enumerate(p0,1):r['_ordem']=idx

# Triplas sempre existentes no vocabulário classificado; nenhuma categoria inventada.
MCAL=('Matemática','Ferramentas matemáticas','Calculadora geral')
MALG=('Matemática','Álgebra','Equações e expressões')
MNUM=('Matemática','Números e operações','Aritmética e operações básicas')
MFRAC=('Matemática','Números e operações','Frações e decimais')
MPOR=('Matemática','Porcentagem e proporções','Porcentagem e variação percentual')
MPROP=('Matemática','Porcentagem e proporções','Regra de três e proporções')
MSTAT=('Matemática','Estatística e probabilidade','Médias e estatística descritiva')
MPROB=('Matemática','Estatística e probabilidade','Probabilidade e combinatória')
MGEOM=('Matemática','Geometria','Área e perímetro')
MGEO3=('Matemática','Geometria','Relações métricas, semelhança e circunferência')
MTRIG=('Matemática','Trigonometria','Trigonometria e geometria angular')
MROOT=('Matemática','Potências e funções','Potências, raízes e logaritmos')
MPROG=('Matemática','Álgebra','Progressões e sequências')
MSYS=('Matemática','Sistemas numéricos','Representação numérica')
CCON=('Conversores','Conversões gerais','Conversor genérico de unidades')
CFX=('Conversores','Moedas e câmbio','Conversão entre moedas')
CFILE=('Conversores','Arquivos e documentos','Documentos e PDF')
CIMG=('Conversores','Imagem','Formatos de imagem')
CAUD=('Conversores','Áudio','Formatos de áudio')
CVID=('Conversores','Vídeo','Formatos de vídeo')
CTEMP=('Conversores','Unidades físicas','Temperatura')
CLEN=('Conversores','Unidades físicas','Comprimento e distância')
CMASS=('Conversores','Unidades físicas','Massa e peso')
CPRES=('Conversores','Unidades físicas','Pressão e grandezas mecânicas')
CPOWER=('Conversores','Unidades físicas','Energia, potência e calor')
CTIME=('Conversores','Unidades temporais','Tempo')
CSYS=('Conversores','Sistemas numéricos','Algarismos romanos e bases')
CCUL=('Conversores','Culinária e medidas contextuais','Medidas culinárias')
DBAS=('Datas','Calendário','Dia da semana e calendário')
DFER=('Datas','Dias úteis','Dias úteis e feriados')
DHOR=('Datas','Duração','Horas, minutos e duração genérica')
DINT=('Datas','Intervalos','Diferença entre datas')
DADD=('Datas','Operações com datas','Somar/subtrair datas e prazos')
FCOT=('Finanças','Câmbio','Cotação atual')
FINV=('Finanças','Investimentos','Rendimento geral')
FCDI=('Finanças','Investimentos','CDB, CDI e renda fixa')
FSTOCK=('Finanças','Investimentos','Ações e dividendos')
FCRED=('Finanças','Crédito','Financiamentos')
FLOAN=('Finanças','Crédito','Empréstimos')
FJUROS=('Finanças','Juros','Juros compostos')
FIPCA=('Finanças','Correção monetária','Inflação e índices')
FHP=('Finanças','Ferramentas financeiras','Calculadora financeira e HP12C')
FTRIB=('Finanças','Tributos','Impostos e Simples Nacional')
FBUD=('Finanças','Planejamento financeiro','Orçamento e reserva')
TFL=('Trabalho','Folha e encargos','INSS e IRRF')
TRES=('Trabalho','Rescisão','Rescisão trabalhista')
T13=('Trabalho','Décimo terceiro','Décimo terceiro salário')
TFER=('Trabalho','Férias','Férias e férias proporcionais')
TJORN=('Trabalho','Jornada e adicionais','Escalas e jornada')
TEXTRA=('Trabalho','Jornada e adicionais','Hora extra')
TNOT=('Trabalho','Jornada e adicionais','Adicional noturno')
TREM=('Trabalho','Remuneração','Salário líquido e bruto')
THORA=('Trabalho','Remuneração','Valor da hora e dias trabalhados')
TFGTS=('Trabalho','FGTS','FGTS e multa rescisória')
TPREV=('Trabalho','Previdência e benefícios','Previdência e benefícios do INSS')
TBENE=('Trabalho','Descontos e benefícios','Vale-transporte e benefícios')
TLEG=('Trabalho','Legislação e direitos','Direitos trabalhistas e CLT')
TAFAST=('Trabalho','Afastamentos','Licenças e afastamentos')
CMET=('Construção','Metragem','Área aplicada à construção')
OAMB=('Fora de escopo','Consulta ambígua','Finanças/serviço não resolvido')
OCUP=('Fora de escopo','Comércio e promoções','Cupons e promoções')
OAPP=('Fora de escopo','Aplicativos','WhatsApp GB')
OSAU=('Fora de escopo','Saúde','Saúde/gestação')
OTEC=('Fora de escopo','Conteúdo técnico/produto','Consulta técnica não conversível')
OSOFT=('Fora de escopo','Serviços/software','Consulta navegacional')
OOuro=('Fora de escopo','Preço de mercado','Ouro e moedas')
OCOM=('Fora de escopo','Preço de mercado','Commodity pecuária')
OJUR=('Fora de escopo','Jurídico','Cálculos jurídicos')
OEDU=('Fora de escopo','Educação','Exercícios e notas escolares')
OEVENT=('Fora de escopo','Conteúdo/comércio','Datas comemorativas')

# Regra de cobertura: cada um dos 474 recebe decisão individual. Primeiro rótulo
# conservador; sobreposições explícitas refinam o resultado. No modo default não
# alteramos confiança nem revisão_manual, portanto não escondemos dúvidas.
reviews={i:{'status':'AMBIGUIDADE_PRESERVADA' if r['tipo_intencao_atual']=='ambígua/revisão' else 'CONFIRMADO_SEM_ALTERACAO',
            'motivo':'A consulta não fornece contexto suficiente para fixar intenção, variável ou direção.' if r['tipo_intencao_atual']=='ambígua/revisão' else 'Intenção e domínio plausíveis após conferência contextual; classificação preservada.',
            'updates':{}} for i,r in enumerate(p0,1)}

def parse(spec):
    if isinstance(spec,int):return [spec]
    if isinstance(spec,(list,tuple,set)):
        return [int(i) for i in spec]
    out=[]
    for item in spec.replace(' ','').split(','):
        if not item:continue
        if '-' in item:
            a,b=map(int,item.split('-'));out.extend(range(a,b+1))
        else:out.append(int(item))
    return out

def set_review(indices, cat=None, intent=None, conf=None, manual=None,why='',status=None,src=None,dst=None):
    for i in parse(indices):
        assert 1<=i<=474
        r=p0[i-1]
        u=dict(reviews[i]['updates'])
        if cat:
            u.update(zip(['area_principal','cluster','subcluster'],cat))
            u['dominio_ou_grandeza']=cat[2]
        if intent:u['tipo_intencao']=intent
        if conf:u['confianca']=conf
        if manual:u['revisao_manual']=manual
        if src or dst:
            assert src and dst
            u.update(unidade_origem=src,unidade_destino=dst,direcao_conversao=f'{src}→{dst}')
            u['tipo_intencao']='conversão direta'
        elif intent and intent!='conversão direta':
            u.update(unidade_origem='',unidade_destino='',direcao_conversao='')
        reviews[i]={'status':status or ('CORRIGIDO' if u else 'CONFIRMADO_SEM_ALTERACAO'),
                    'motivo':why or 'Revisão contextual baseada na redação explícita da keyword.',
                    'updates':u}

# Construção e documentos
set_review(2,TFL,'cálculo direto','alta','não','Cálculo INSS é operação de folha/encargos, não metragem de obra.')
set_review(4,OCUP,'fora de escopo','alta','não','Cupom de loja não é cálculo de telhado.')
set_review(9,OTEC,'fora de escopo','alta','não','Juntar PDFs é mesclagem, sem mudança de formato.')
set_review('5-8,10-14',None,'conversão de arquivo/mídia','alta','não','Transformação explícita de arquivo; não converter termos em unidades físicas.')
set_review(6,CFILE,'ambígua/revisão','baixa','sim','PDA pode ser um dispositivo/erro de digitação de PDF/A: não presumir formato.')
set_review('15-16',CTIME,'cálculo contextual','média','sim','Semanas em meses dependem da convenção de mês civil e podem se referir a gestação.')
set_review(18,OCOM,'consulta de preço/mercado','média','sim','Arroba do boi sugere commodity, mas a consulta sem verbo não especifica preço/peso.')
set_review('20,44',FCRED,'simulação/projeção','média','não','Simulador da Caixa é crédito/financiamento; não conversão de unidade.')
set_review('22-24,28,30-31',CCON,'navegacional/transacional','média','não','Busca genérica por ferramenta de conversão, sem origem/destino.')
set_review(25,CFILE,'navegacional/transacional','média','não','Conversor de PDF: formato geral, sem direção explícita.')
set_review(26,CFX,'navegacional/transacional','média','não','Conversor de dólar sem moeda destino informada.')
set_review(27,CVID,'navegacional/transacional','média','não','Busca por ferramenta MP4, sem formato de entrada especificado.')
set_review(29,CFILE,'ambígua/revisão','baixa','sim','PDF/A isolado não explicita origem ou operação.')
set_review(32,CFX,'ambígua/revisão','baixa','sim','Par USD/BRL sem direção inequívoca.')
set_review(34,OTEC,'fora de escopo','alta','não','Inversor de frequência é equipamento, não conversão Hz/kHz.')
set_review(35,CPOWER,'tabela/referência','média','não','Megawatt é unidade, sem operação de conversão.')
set_review('36-38,41-42',OSAU,'fora de escopo','alta','não','Consulta de semanas/meses de gestação pertence a saúde.')
set_review(39,CIMG,'conversão de arquivo/mídia','alta','não','PNG para ICO tem origem/destino de arquivo explícitos.')
set_review(43,CFX,'ambígua/revisão','baixa','sim','SGD to está truncado: moeda destino não aparece.')
set_review('45-47',OAMB,'ambígua/revisão','baixa','sim','Verbo transformar sem objeto impede classificar a operação.')
set_review(48,OTEC,'fora de escopo','alta','não','Ventilador de mesa é produto, não unidade de medida.')
set_review(49,OAPP,'fora de escopo','alta','não','WhatsApp GB é aplicativo, não gigabyte.')
set_review(51,CMASS,'tabela/referência','média','não','Miligrama isolado é unidade de massa, sem direção.')
set_review(52,CMASS,conf='alta',manual='não',why='Miligramas para gramas: conversão explícita.',src='mg',dst='g')
set_review(53,OOuro,'consulta de preço/mercado','alta','não','Valor de ouro 18K por grama é preço de commodity.')
set_review(54,CMASS,'ambígua/revisão','baixa','sim','Pound kilo sem preposição exige revisão da direção.')
set_review(55,FCRED,'simulação/projeção','alta','não','Simulador de financiamento de imóvel é domínio financeiro.')
set_review(56,CPRES,'ambígua/revisão','média','sim','BAR e PSI são pressão; sem seta explícita não preencher direção.')
set_review('57-60,186',CAUD,'conversão de arquivo/mídia','alta','não','MP3 é formato de áudio de saída explícito.')
set_review(61,CMASS,conf='alta',manual='não',why='Grama para miligrama explícito.',src='g',dst='mg')
set_review('62-63',CLEN,conf='alta',manual='não',why='Milha para quilômetro explícito.',src='mi',dst='km')
set_review('64,68-70',CFX,'ambígua/revisão','média','sim','Par real/dólar sem preposição; não assumir direção.')
set_review(65,CFX,'ambígua/revisão','média','sim','Guarani/real sem preposição; falta direção.')
set_review(66,CCON,'navegacional/transacional','média','não','Conversão online é busca por ferramenta genérica.')
set_review(67,CLEN,'ambígua/revisão','média','sim','Polegadas/cm sem preposição explícita.')
set_review('71-73',CFILE,'conversão de arquivo/mídia','alta','não','JPG↔PDF explicitamente com preposição/direção.')

# Moedas: distinguir ferramenta genérica, taxa/cotação e conversão direcionada.
set_review('75,77-79,81-89,91-93,96-98,102-105,108-109,113,117-118,122-123,138-139',CFX,'navegacional/transacional','média','não','Consulta por ferramenta/categoria de câmbio sem par direcional; não inventar metadados.')
set_review('116,118,122,153',FCOT,'cotação atual','média','não','Consulta da moeda/cotação atual, não conversão unitária.')
set_review('124,125-126,128,130,137,142-146,148,150,152',CFX,'ambígua/revisão','média','sim','Par de moedas sem direção inequívoca ou peso sem país; manter revisão.')
set_review('100-101,111,120-121,129,131-133',CFX,'ambígua/revisão','média','sim','Pares monetários sem seta inequívoca; não inferir origem/destino a partir da ordem isolada.')
set_review('140-141',CFX,conf='alta',manual='não',why='Peso argentino para real com direção explícita.',src='ARS',dst='BRL')
set_review(74,CFX,conf='alta',manual='não',why='1 EUR em BRL é conversão explícita.',src='EUR',dst='BRL')
set_review(76,CFX,conf='alta',manual='não',why='BRL para dólar explícito.',src='BRL',dst='USD')
set_review(80,CFX,conf='alta',manual='não',why='Dólar para real explícito.',src='USD',dst='BRL')
set_review(90,CFX,'ambígua/revisão','média','sim','Dólar/real sem preposição; a palavra conversor não explicita direção.')
set_review(94,CFX,conf='alta',manual='não',why='Guarani em real explícito.',src='PYG',dst='BRL')
set_review('99,106-107,114-115',CFX,conf='alta',manual='não',why='Peso argentino em/para real explícito.',src='ARS',dst='BRL')
set_review('110,112',CFX,conf='alta',manual='não',why='Guarani em real explícito.',src='PYG',dst='BRL')
set_review('127,131-133',CFX,conf='alta',manual='não',why='Franco suíço em/para real explícito.',src='CHF',dst='BRL')
set_review(134,CFX,conf='alta',manual='não',why='Iene em/para real explícito.',src='JPY',dst='BRL')
set_review(135,CMASS,conf='alta',manual='não',why='Libra para quilograma é massa, não câmbio.',src='lb',dst='kg')
set_review(136,CFX,conf='alta',manual='não',why='Libra esterlina para real explícito.',src='GBP',dst='BRL')
set_review(147,CFX,conf='alta',manual='não',why='Peso mexicano em real explícito.',src='MXN',dst='BRL')
set_review('149,151',CFX,conf='alta',manual='não',why='Real em/para peso argentino explícito.',src='BRL',dst='ARS')
set_review(154,CFX,conf='alta',manual='não',why='Iene para real explícito.',src='JPY',dst='BRL')

# Números e grandezas.
set_review('155-157',CSYS,'tabela/referência','média','não','Numeração romana sem valor indica referência/sistema, não operação direta.')
set_review('158-159,172-176',CLEN,conf='alta',manual='não',why='Milha para quilômetro explícito.',src='mi',dst='km')
set_review('160-162',MGEOM,'cálculo direto','média','sim','Calcular metros quadrados é área, não conversão; aplicação obra não declarada.')
set_review('163',CLEN,conf='alta',manual='não',why='Centímetros em polegadas explícito.',src='cm',dst='in')
set_review(164,CFX,'ambígua/revisão','média','sim','Converter para dólares sem moeda de origem.')
set_review(165,CLEN,conf='alta',manual='não',why='Polegadas em cm explícito.',src='in',dst='cm')
set_review(166,CTEMP,'tabela/referência','média','não','Graus Celsius sem valor ou moeda destino é referência de temperatura.')
set_review(167,CMASS,conf='alta',manual='não',why='Lbs for kg com direção explícita.',src='lb',dst='kg')
set_review('169-171,179',CLEN,'ambígua/revisão','média','sim','Par de unidades sem relação direcional inequívoca.')
set_review('177-178',CLEN,conf='alta',manual='não',why='Polegadas para mm explícito.',src='in',dst='mm')
set_review(181,CFX,'ambígua/revisão','baixa','sim','Libra pode designar GBP ou massa; valor não esclarece contexto.')
set_review(182,CTIME,'cálculo contextual','média','sim','Semanas em mês depende de mês civil, convenção ou gestação.')
set_review(183,DHOR,'cálculo direto','alta','não','Somar horas é operação temporal, não conversão genérica.')
set_review('184-185,188',CVID,'navegacional/transacional','média','não','Ferramenta genérica de áudio/vídeo sem direção de formato.')
set_review(187,CFX,'navegacional/transacional','média','não','Converter dólar abreviatura sem destino.')
set_review(189,CLEN,conf='alta',manual='não',why='Polegada em cm explícito.',src='in',dst='cm')

# Datas; buscas lunares não são taxa de câmbio.
set_review('190,197-198,260-263',DBAS,'informacional','alta','não','Fase da lua atual é consulta de calendário/astronomia, não mercado financeiro.')
set_review('194-196,209-213',DFER,'informacional','média','sim','Feriado depende do calendário/município em certos casos; não inferir localização.')
set_review(200,OEVENT,'fora de escopo','alta','não','Texto de Dia das Mães é conteúdo comemorativo, não operação com datas.')
set_review('214,216',FCRED,'simulação/projeção','alta','não','Simulador habitacional da Caixa é financiamento.')
set_review(215,CTIME,'tabela/referência','alta','não','Semanas em ano são referência de tempo; resposta depende do calendário.')
set_review('217-218',CTIME,'cálculo contextual','média','sim','Semanas em meses depende de convenção e eventual contexto gestacional.')
set_review(219,DINT,'navegacional/transacional','média','não','Calculadora de datas é ferramenta; sem operação única.')
set_review('220-222,224',DHOR,'cálculo direto','alta','não','Cálculo de horas/horário deve usar duração, não diferença de datas.')
set_review('225-226',DBAS,'informacional','alta','não','Pergunta por Dia dos Pais busca data comemorativa.')
set_review(228,TEXTRA,'informacional','alta','não','Como calcular horas extras é jornada trabalhista.')
set_review(229,MPOR,'cálculo direto','alta','não','Porcentagem é matemática, não operação com datas.')
set_review(230,FJUROS,'ambígua/revisão','média','sim','Juros sem indicação simples/composto: assunto financeiro, fórmula não determinada.')

# Energia false positives e finanças gerais.
set_review(231,OTEC,'fora de escopo','alta','não','Nome de pessoa não é calculadora de consumo elétrico.')
set_review('232-233,236,259,305',FCRED,'simulação/projeção','alta','não','Financiamento de veículos/imóveis é crédito, não energia ou câmbio.')
set_review(235,FCRED,'navegacional/transacional','média','não','Refinanciamento de banco pertence a crédito.')
set_review(246,FSTOCK,'informacional','média','não','Ticker RBRR11 é ativo/FII, não cálculo de empréstimo.')
set_review(252,OAMB,'ambígua/revisão','baixa','sim','Quanto ganha sem profissão ou sujeito não permite definir remuneração.')
set_review(253,CFX,conf='alta',manual='não',why='1 USD em BRL sugere cotação unitária direcionada.',src='USD',dst='BRL')
set_review('254-255',CFX,'ambígua/revisão','média','sim','Euro/real com palavra conversão sem preposição de direção.')
set_review('264-266',FCOT,'ambígua/revisão','média','sim','Preço em dólar pode ser preço de produto expresso em USD, não cotação cambial.')
set_review('269,277',FCOT,'ambígua/revisão','média','sim','Valor em/ou da moeda sem referência suficiente a cotação versus preço.')
set_review('274-275,278',OOuro,'consulta de preço/mercado','alta','não','Valor em dinheiro por grama de ouro é mercado de commodity.')
set_review(281,FHP,'navegacional/transacional','alta','não','HP12C online é calculadora financeira, não cálculo específico.')
set_review('282,303',TBENE,'informacional','alta','não','VR/Ticket alimentação são benefícios trabalhistas, não investimento.')
set_review(283,OTEC,'fora de escopo','média','não','Bolsa Família é benefício social, não investimento nem previdência INSS.')
set_review(284,OSOFT,'fora de escopo','alta','não','Busca por agências bancárias é serviço/navegação, não cálculo.')
set_review(285,FHP,'navegacional/transacional','média','não','HP12C genérica é ferramenta financeira sem fórmula alvo.')
set_review('286-287,301-302',FCDI,'cotação atual','alta','não','Taxa CDI hoje é indicador atual, não simulação de rendimento.')
set_review('288',FLOAN,'informacional','média','não','Crédito consignado é modalidade de empréstimo.')
set_review('289-290,293,297,299',FCRED,'simulação/projeção','média','não','Financiamento bancário ou de veículo/imóvel, não investimento.')
set_review(295,FTRIB,'ambígua/revisão','média','sim','Parcelar MEI pode ser parcelamento de tributos ou crédito, não projeção de investimento.')
set_review('296,364-365,394',OTEC,'fora de escopo','média','não','Salário de profissão sem operação de cálculo é pesquisa de carreira/mercado.')
set_review(306,FJUROS,'informacional','alta','não','Fórmula de juros compostos é conteúdo de referência, não simulação.')
set_review(307,FHP,'navegacional/transacional','alta','não','HP12C é ferramenta específica, não conteúdo genérico de juros.')
set_review(309,FSTOCK,'informacional','média','não','KNCR11 é ticker de ativo/FII.')
set_review('310-311,314-315',FCRED,'simulação/projeção','média','não','Financiamento de automóvel/imóvel não é tributo.')
set_review('312-313,337',TREM,'informacional','alta','não','Salário mínimo nacional não é imposto ou cotação financeira.')

# Fora de escopo ou navegacional financeiro.
set_review(320,FCRED,'informacional','média','não','Minha Casa Minha Vida/CAIXA é programa de financiamento habitacional.')
set_review('321-322',FCRED,'navegacional/transacional','média','não','Consulta por agência/linha de crédito habitacional ou empréstimo.')
set_review(323,FCDI,'navegacional/transacional','média','não','Ferramenta para CDI é investimento, não serviço irresolvido.')
set_review(324,FIPCA,'informacional','alta','não','Correção monetária pertence a Finanças.')
set_review('325-326',OCUP,'fora de escopo','alta','não','Cupons de varejo são promoções, não calculadora.')
set_review('327-328',TFL,'informacional','alta','não','Desconto INSS é operação de folha trabalhista.')
set_review(330,FCOT,'cotação atual','média','não','Dólar do dia com grafia abreviada é taxa cambial.')
set_review(331,CFX,'ambígua/revisão','média','sim','Dólares para real: país da moeda dólar não informado; não fixar USD automaticamente.')
set_review(332,FCRED,'simulação/projeção','alta','não','Simulador Caixa Econômica remete a crédito, não fora de escopo.')
set_review(333,FCOT,'cotação atual','alta','não','Valor do dólar hoje é cotação.')
set_review(334,FCRED,'navegacional/transacional','média','não','Refinanciamento em banco é crédito.')
set_review(338,CTIME,'cálculo contextual','média','sim','Semanas em meses ambíguo quanto a mês civil/gestação; não presumir saúde.')

# Matemática: referencial informacional vs calculadora; deslocar termos fora do assunto.
set_review(347,FBUD,'informacional','média','não','Planilha de controle financeiro pessoal é organização financeira, não estatística.')
set_review('348-349,406',MGEOM,'informacional','alta','não','Áreas de figuras planas são geometria.')
set_review(350,MPROB,'informacional','média','não','Arranjo é tópico de combinatória.')
set_review('351,368,370-371',MALG,'tabela/referência','alta','não','Fórmula de Bhaskara é equações, não ferramenta genérica.')
set_review(353,MCAL,'navegacional/transacional','média','não','Calculadora online genérica é ferramenta.')
set_review(359,OEDU,'fora de escopo','média','sim','Nota ENEM pode ser simulador educacional, fora das sete áreas; escolha de produto pendente.')
set_review('361-362',MSTAT,'ambígua/revisão','média','sim','Desvio padrão sem verbo pode ser definição, fórmula ou calculadora.')
set_review(363,OSOFT,'navegacional/transacional','baixa','sim','Drcalc parece aplicativo/serviço específico; referência externa não verificada.')
set_review(366,MALG,'cálculo direto','alta','não','Fatorar é operação algébrica.')
set_review(367,MPROB,'cálculo direto','média','não','Fatorial representa operação matemática definida.')
set_review(369,MROOT,'informacional','alta','não','Funções logarítmicas são conteúdo matemático.')
set_review(372,FJUROS,'informacional','alta','não','Fórmula de juros compostos é finanças.')
set_review(373,FHP,'navegacional/transacional','alta','não','HP12C online é calculadora financeira.')
set_review('374-375',MROOT,'informacional','média','não','Logaritmo isolado é assunto matemático; sem operandos.')
set_review(376,MNUM,'informacional','média','não','MMC e MDC são operações aritméticas, mas a busca isolada não dá operandos.')
set_review(378,MSTAT,'informacional','média','não','Médias ponderadas é assunto de estatística, sem valores.')
set_review(379,MSYS,'tabela/referência','média','não','Numeração decimal é representação numérica.')
set_review('380-387,418',MNUM,'informacional','alta','não','Números primos sem valores são conceito/explicação, não cálculo genérico.')
set_review('388-391,392',MPROB,'informacional','média','não','Permutação/probabilidade são conceitos de combinatória.')
set_review(393,MPROG,'informacional','alta','não','Progressão aritmética é tópico de álgebra.')
set_review(396,MPROP,'informacional','alta','não','Razões e proporções são conteúdo matemático.')
set_review(397,MPROG,'informacional','alta','não','Sequências numéricas são conteúdo de progressões.')
set_review(398,MSYS,'informacional','alta','não','Sistemas de numeração são representação numérica.')
set_review('399-400',MTRIG,'tabela/referência','alta','não','Tabela trigonométrica corresponde a seno/cosseno/tangente.')
set_review('401-405',MGEO3,'informacional','alta','não','Teorema de Pitágoras e triângulo retângulo são geometria.')
set_review('407-409',FJUROS,'informacional','alta','não','Fórmulas de juros compostos não são geometria.')
set_review('410-411,420',MGEO3,'informacional','alta','não','Relações métricas do triângulo pertencem à geometria.')
set_review(412,OJUR,'fora de escopo','média','sim','TJD/tribunal e cálculo judicial têm escopo jurídico, fora das sete áreas.')
set_review(414,CSYS,conf='alta',manual='não',why='Número em romanos explicita destino romano.',src='arábico',dst='romano')

# Trabalho e seus falsos positivos.
set_review(421,TFER,'informacional','alta','não','Abono pecuniário é conversão de férias em pecúnia.')
set_review(422,TNOT,'cálculo direto','alta','não','Adicional noturno é jornada trabalhista.')
set_review(423,FCOT,'cotação atual','alta','não','Valor do euro é cotação cambial, não benefício.')
set_review(424,TREM,'informacional','alta','não','Adiantamento de salário não é décimo terceiro.')
set_review('428,449',THORA,'cálculo contextual','média','sim','Cálculo de hora sem contexto permite duração ou remuneração por hora.')
set_review('429-430,464',TRES,'cálculo direto','alta','não','Rescisão trabalhista explícita.')
set_review('431,445',OJUR,'fora de escopo','alta','não','Cálculo jurídico genérico é escopo judicial, não trabalhista específico.')
set_review(432,FTRIB,'cálculo direto','média','não','Imposto de renda sem menção ao salário é tributo geral, não exclusivamente IRRF folha.')
set_review(433,TPREV,'informacional','alta','não','CNIS é serviço/registro previdenciário.')
set_review(434,TFL,'informacional','alta','não','Desconto INSS é encargo sobre folha.')
set_review(435,TPREV,'navegacional/transacional','alta','não','Meu INSS do gov.br é serviço previdenciário.')
set_review(438,TFER,'informacional','alta','não','Abono pecuniário é férias.')
set_review(439,TAFAST,'informacional','alta','não','Atestado médico pode justificar afastamento trabalhista.')
set_review(441,MFRAC,'informacional','alta','não','Mínimo denominador comum é fração matemática, não férias.')
set_review(442,TFER,'informacional','alta','não','O que é abono pecuniário é pergunta sobre férias.')
set_review(446,TLEG,'informacional','alta','não','CLT é legislação trabalhista, não horas trabalhadas.')
set_review(447,OAMB,'ambígua/revisão','baixa','sim','Palavra geral isolada não tem assunto identificável.')
set_review(448,TEXTRA,'informacional','alta','não','Horas extraordinárias são horas extras.')
set_review(449,THORA,'informacional','média','sim','Trabalho por hora: remuneração provável, mas contexto pouco específico.')
set_review(450,TEXTRA,'cálculo direto','alta','não','Calcular horas extras explícito.')
set_review(451,FLOAN,'informacional','média','sim','Empréstimo FGTS é crédito antecipado, não saque de saldo FGTS.')
set_review('452-453',OTEC,'fora de escopo','alta','não','Procuradoria-Geral da República é instituição, não benefício.')
set_review('454-457',TPREV,'simulação/projeção','alta','não','Simulador de aposentadoria INSS envolve projeção previdenciária.')
set_review(458,TEXTRA,'cálculo direto','alta','não','Cálculo de horas extras é jornada.')
set_review(459,TJORN,'cálculo direto','média','não','Hora trabalhada cálculo é jornada, sem salário explícito.')
set_review(462,THORA,'informacional','média','não','Trabalho por hora remete a remuneração/jornada, não rescisão.')
set_review(465,FCRED,'informacional','alta','não','Carro financiado sem entrada é produto de financiamento.')
set_review(466,FCRED,'informacional','média','não','FIES é financiamento educacional, não rescisão.')
set_review(467,TREM,'informacional','alta','não','Quanto ganha jovem aprendiz é remuneração/legalidade.')
set_review(468,TFGTS,'cálculo direto','média','não','Multa rescisória tem relação com FGTS.')
set_review(469,TPREV,'informacional','alta','não','Pensionista é benefício previdenciário, não rescisão.')
set_review(470,TPREV,'informacional','alta','não','Revisão da vida toda é benefício previdenciário.')
set_review('471-473',TFGTS,'informacional','alta','não','Fundo de garantia é FGTS, não tempo de serviço isolado.')
set_review(474,OOuro,'consulta de preço/mercado','alta','não','Valor do grama de ouro é commodity, não tempo de serviço.')

# Ajustes de exceções e cautelas após revisão das regras.
set_review(43,CFX,'ambígua/revisão','baixa','sim','SGD to está incompleto e não especifica moeda destino.')
set_review(170,CLEN,'ambígua/revisão','média','sim','Milha/km justapostos não indicam direção.')
set_review(171,CLEN,'ambígua/revisão','média','sim','Milha por km não especifica a operação desejada.')

# Segunda passada: validação dos itens que estavam com classe plausível, mas baixa
# confiança automática, e correção de exceções sem direção ou domínio errado.
set_review('17,33',CTEMP,'ambígua/revisão','média','sim','Fahrenheit com valor, mas sem temperatura de destino.')
set_review(19,CFX,'ambígua/revisão','média','sim','CAD e BRL são moedas; não há de/para explícito.')
set_review(21,OAMB,'ambígua/revisão','baixa','sim','Consulta truncada/possível marca de câmbio; intenção não identificável.')
set_review(40,OAMB,'ambígua/revisão','baixa','sim','Quanto vale sem objeto definido.')
set_review(95,CFX,'ambígua/revisão','média','sim','Guarani/real sem direção explícita.')
set_review(119,CFX,'ambígua/revisão','média','sim','Dólar em rea está truncado: destino provavelmente real, mas requer conferência.')
set_review(173,CLEN,'ambígua/revisão','média','sim','Milhas quilômetros justapostos sem indicação inequívoca da direção.')
set_review(180,CLEN,conf='alta',manual='não',why='Polegada para milímetro tem direção explícita.',src='in',dst='mm')
set_review('191-193',DBAS,'informacional','alta','não','Calendário de ano/mês é consulta clara de calendário.')
set_review(199,DBAS,'informacional','alta','não','Dia dos Pais é data comemorativa.')
set_review('202-208',DBAS,'tabela/referência','alta','não','Calendário do mês não equivale a calculadora de dias úteis.')
set_review(223,DINT,'cálculo direto','alta','não','Contador de datas opera sobre intervalo entre datas.')
set_review(227,DFER,'cálculo direto','alta','não','Dias úteis exigem regra de feriados, não soma genérica de data.')
set_review(234,FIPCA,'cálculo direto','alta','não','Calculadora IPCA é cálculo financeiro de correção monetária.')
set_review(237,FCRED,'simulação/projeção','média','não','Simulador Caixa com grafia abreviada é simulação de crédito.')
set_review(238,FCRED,'informacional','média','sim','Casa financiada pela Caixa pode se referir a imóvel anunciado ou crédito.')
set_review(239,FLOAN,'informacional','alta','não','Empréstimo com garantia de imóvel é modalidade de crédito.')
set_review(240,FLOAN,'navegacional/transacional','alta','não','Busca por contratar empréstimo online.')
set_review(241,FLOAN,'simulação/projeção','alta','não','Simulação de empréstimo é modelagem de crédito.')
set_review('242-244',FCRED,'simulação/projeção','alta','não','Financiamento imobiliário/CAIXA é crédito.')
set_review(245,FCRED,'simulação/projeção','alta','não','Minha Casa Minha Vida/CAIXA simulação é financiamento.')
set_review(247,FCRED,'navegacional/transacional','alta','não','Financiamento de veículo Santander: busca específica de produto.')
set_review(248,FLOAN,'simulação/projeção','alta','não','Simulador de empréstimos é crédito.')
set_review(249,FCRED,'ambígua/revisão','média','sim','Simulação Caixa sem menção a financiamento específico exige contexto.')
set_review('250-251',FCRED,'simulação/projeção','alta','não','Simulação explícita de financiamento habitacional.')
set_review('256-258,267-268,270-273,276,279',FCOT,'cotação atual','alta','não','Consulta por valor/cotação cambial do momento.')
set_review(280,FJUROS,'ambígua/revisão','média','sim','Cálculos de juros sem taxa, prazo ou distinção entre simples/compostos.')
set_review('291-292,298,300',FINV,'simulação/projeção','alta','não','Simulação de investimento é projeção de rendimento.')
set_review(294,FJUROS,'simulação/projeção','alta','não','Calcular juros compostos é simulação financeira.')
set_review(304,FJUROS,'cálculo direto','alta','não','Calcular juros compostos tem domínio explícito.')
set_review(308,FJUROS,'ambígua/revisão','média','sim','Calculadora de juros sem modalidade simples/composta.')
set_review('316-319',OCUP,'fora de escopo','alta','não','Cupons promocionais de varejo não são calculadoras.')
set_review(335,OAMB,'ambígua/revisão','baixa','sim','Rateio isolado pode ser divisão de despesas ou termo educacional.')
set_review(336,FCOT,'cotação atual','alta','não','Dólar do dia é cotação, não preço de commodity.')
set_review('339-344',OSAU,'fora de escopo','alta','não','Busca contextual de gestação/saúde não é conversor de unidade genérico.')
set_review(341,CTIME,'cálculo contextual','média','sim','Semanas em um mês sem gestação explícita dependem do calendário.')
set_review(345,OTEC,'fora de escopo','alta','não','Editar PDF é manipulação sem mudança de formato.')
set_review(346,MPROB,'informacional','alta','não','Análise combinatória é conteúdo matemático.')
set_review(357,MCAL,'ambígua/revisão','média','sim','Cálculos exatos sem grandeza ou operador específico.')
set_review(358,MTRIG,'informacional','alta','não','Ciclo trigonométrico é assunto de trigonometria.')
set_review(360,MCAL,'ambígua/revisão','média','sim','Cálculos exatos sem entrada específica.')
set_review(377,MSTAT,'cálculo direto','alta','não','Média ponderada é operação estatística bem definida.')
set_review(413,('Matemática','Geometria','Volume e geometria espacial'),'cálculo direto','alta','não','Volume do cone é geometria espacial.')
set_review('415-416',None,'cálculo direto','alta','não','Regra de três/percentagem com calculadora explícita.')
set_review(417,MPOR,'informacional','alta','não','Percentagens sem operandos são tema de porcentagem.')
set_review(419,MROOT,'informacional','alta','não','Raiz quadrada isolada é assunto matemático.')
set_review(425,T13,'cálculo direto','alta','não','Décimo terceiro salário explicitamente calculado.')
set_review('426-427',TFGTS,'navegacional/transacional','alta','não','Consulta FGTS pelo CPF é serviço oficial, não cálculo.')
set_review(437,TPREV,'informacional','média','sim','Previdenciária isolada: benefício ou previdência privada não distinguíveis.')
set_review(440,TFER,'cálculo direto','alta','não','Calcular férias é operação trabalhista.')
set_review('443-444',TJORN,'cálculo direto','alta','não','Calculadora de horas trabalhadas é jornada.')
set_review('460-461',OAMB,'ambígua/revisão','baixa','sim','Meu benefício sem contexto pode ser INSS, benefício social ou trabalhista.')
set_review(463,TRES,'cálculo contextual','média','não','Acerto trabalhista refere-se a cálculo de verbas rescisórias.')

set_review(56,CPRES,conf='alta',manual='não',why='Bar para psi indica conversão de pressão inequívoca.',src='bar',dst='psi')
set_review(129,CFX,conf='alta',manual='não',why='Franco suíço para real especifica origem e destino.',src='CHF',dst='BRL')

# Identidade original e leitura dos trinta lotes. L003 está no ZIP aprovado.
input_by_lot={}
for n in range(1,31):
    if n==1:path=SRC/'lote-001-saneado-v1.1-barras-v2.csv';rows=read_csv(path)
    elif n==3:
        with zipfile.ZipFile(ROOT/'lote-003-v1.1-barras-v2-aprovado.zip') as z:
            matches=[x for x in z.namelist() if x.endswith('lote-003-classificado-v1.1-barras-v2.csv')]
            assert len(matches)==1
            rows=list(csv.DictReader(z.read(matches[0]).decode('utf-8-sig').splitlines(),delimiter=';'))
    else:rows=read_csv(ROOT/f'lote-{n:03d}-classificado-v1.1-barras-v2.csv')
    input_by_lot[n]=rows
by_id={}
for n,rows in input_by_lot.items():
    for r in rows:
        if r['tipo_registro']=='base':
            assert r['id_global'] not in by_id
            by_id[r['id_global']]=(n,r)

assert sum(len([x for x in rows if x['tipo_registro']=='base']) for rows in input_by_lot.values())==294905
patch_rows=[];audit=[]; new_base_rows=[]
original_keys=['tipo_registro','id_global','lote_id','familia_id','controle_id','Keyword',
               'ocorrencias_origem','areas_origem','qtd_areas','Avg. monthly searches',
               'Mudança em três meses','Mudança YoY','Competition','Competition (indexed value)',
               'Top of page bid (low range)','Top of page bid (high range)']
for i,q in enumerate(p0,1):
    n,actual=by_id[q['id_global']];assert n==int(q['lote']) and actual['Keyword']==q['Keyword'],(i,actual['Keyword'],q['Keyword'])
    rule=reviews[i];old=actual.copy();new=actual.copy();new.update(rule['updates'])
    changed={k:(old.get(k,''),new.get(k,'')) for k in new if old.get(k,'')!=new.get(k,'')}
    if changed:
        new['intencao_principal'] = (
            f'Converter: {new["subcluster"]}' if new['tipo_intencao']=='conversão direta' else
            f'Consultar cotação: {new["subcluster"]}' if new['tipo_intencao']=='cotação atual' else
            f'Simular: {new["subcluster"]}' if new['tipo_intencao']=='simulação/projeção' else
            f'Calcular: {new["subcluster"]}' if new['tipo_intencao']=='cálculo direto' else
            f'Consultar informação: {new["subcluster"]}' if new['tipo_intencao']=='informacional' else
            f'Rever intenção: {new["subcluster"]}' if new['tipo_intencao']=='ambígua/revisão' else
            f'Intenção {new["tipo_intencao"]}: {new["subcluster"]}')
        new['justificativa_curta']='Revisão P0: '+rule['motivo']
        assert all(old[k]==new[k] for k in original_keys)
        if new['tipo_intencao']=='conversão direta':assert new['unidade_origem'] and new['unidade_destino'] and new['direcao_conversao']
        patch_rows.append({'lote':f'{n:03d}','id_global':q['id_global'],'Keyword':q['Keyword'],
                          'campos_alterados':','.join(k for k in new if old[k]!=new[k]),
                          'antes_json':json.dumps({k:old[k] for k in new if old[k]!=new[k]},ensure_ascii=False),
                          'depois_json':json.dumps({k:new[k] for k in new if old[k]!=new[k]},ensure_ascii=False),
                          'justificativa':rule['motivo']})
    elif rule['status']=='CORRIGIDO':rule['status']='VALIDADO_SEM_MUDANCA'
    if new['tipo_intencao']=='conversão direta':assert all(new[k] for k in ['unidade_origem','unidade_destino','direcao_conversao'])
    # Arquivo individual mostra decisão mesmo para as 474 revisões que não exigem edição.
    audit.append({'ordem':i,'lote':f'{n:03d}','id_global':q['id_global'],'familia_id':q['familia_id'],
                  'Keyword':q['Keyword'],'volume_ads_patamar':q['Avg. monthly searches'],
                  'status_decisao':rule['status'],'alterado':'sim' if changed else 'não',
                  'area_anterior':old['area_principal'],'area_revisada':new['area_principal'],
                  'cluster_anterior':old['cluster'],'cluster_revisado':new['cluster'],
                  'subcluster_anterior':old['subcluster'],'subcluster_revisado':new['subcluster'],
                  'intencao_anterior':old['tipo_intencao'],'intencao_revisada':new['tipo_intencao'],
                  'origem':new['unidade_origem'],'destino':new['unidade_destino'],'direcao':new['direcao_conversao'],
                  'confianca_anterior':old['confianca'],'confianca_revisada':new['confianca'],
                  'revisao_manual_anterior':old['revisao_manual'],'revisao_manual_revisada':new['revisao_manual'],
                  'justificativa':rule['motivo']})
    new_base_rows.append((n,new))

# Reaplica somente os registros P0 alterados no lote correspondente. Preserva
# controles, todas as colunas originais e linhas base não selecionadas.
updated_by_id={r['id_global']:r for n,r in new_base_rows}
files_changed=[]
for n,rows in input_by_lot.items():
    changed_here={p['id_global'] for p in patch_rows if int(p['lote'])==n}
    if not changed_here:continue
    outrows=[]
    for original in rows:
        row=updated_by_id.get(original['id_global'],original) if original['tipo_registro']=='base' else original
        assert all(original[k]==row[k] for k in original_keys)
        if original['tipo_registro']=='controle' or original['id_global'] not in changed_here:assert row==original
        outrows.append(row)
    outf=OUT/f'lote-{n:03d}-revisado-p0-v1.1-barras-v2.csv'
    write_csv(outf,outrows,list(rows[0]))
    reread=read_csv(outf)
    assert len(reread)==len(rows) and sum(x['tipo_registro']=='controle' for x in reread)==73
    assert all(x['tipo_registro']!='controle' or x==y for x,y in zip(reread,rows))
    assert not any(x['tipo_registro']=='base' and x['tipo_intencao']=='conversão direta' and not (x['unidade_origem'] and x['unidade_destino'] and x['direcao_conversao']) for x in reread)
    files_changed.append(outf)

write_csv(OUT/'revisao-individual-474-p0.csv',audit,list(audit[0]))
write_csv(OUT/'correcoes-objetivas-p0.csv',patch_rows,list(patch_rows[0]))
remaining=[x for x in audit if x['revisao_manual_revisada']=='sim']
write_csv(OUT/'p0-ambiguidades-remanescentes.csv',remaining,list(audit[0]))
# Exporta a fila completa mantendo P1-P3 inalterados; P0 revisado por ID.
p0_by_id={x['id_global']:x for x in audit};qnew=[]
for q in queue:
    r=dict(q)
    if r['prioridade']=='P0':
        d=p0_by_id[r['id_global']]
        r['area']=d['area_revisada'];r['cluster']=d['cluster_revisado'];r['subcluster']=d['subcluster_revisado']
        r['tipo_intencao_atual']=d['intencao_revisada'];r['confianca_atual']=d['confianca_revisada']
        r['status_revisao']='REVISADO_P0' if d['revisao_manual_revisada']=='não' else 'PENDENTE_AMBIGUIDADE_P0'
        r['decisao_final']='CORRIGIR' if d['alterado']=='sim' else 'MANTER'
        r['observacao_revisor']=d['justificativa']
    qnew.append(r)
write_csv(OUT/'fila-priorizada-30-lotes-com-p0-revisado.csv',qnew,list(qnew[0]))

cnt=Counter(x['status_decisao'] for x in audit)
byarea=Counter(x['area_revisada'] for x in audit)
review_before=sum(x['revisao_manual_anterior']=='sim' for x in audit)
review_after=sum(x['revisao_manual_revisada']=='sim' for x in audit)
assert review_before==474
assert len(audit)==474 and len({x['id_global'] for x in audit})==474
assert len(files_changed)>0
summary={'p0_revisadas':len(audit),'p0_alteradas':sum(x['alterado']=='sim' for x in audit),
         'p0_pendentes_contexto':review_after,'p0_resolvidas':474-review_after,
         'mudancas_de_area':sum(x['area_anterior']!=x['area_revisada'] for x in audit),
         'mudancas_de_intencao':sum(x['intencao_anterior']!=x['intencao_revisada'] for x in audit),
         'conversoes_diretas':sum(x['intencao_revisada']=='conversão direta' for x in audit),
         'lotes_com_correcao':len(files_changed),'linhas_acervo_preservadas':294905,
         'controle_lotes_preservado':73,'statuses':dict(cnt),'areas':dict(byarea)}
(OUT/'resumo-revisao-p0.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
report=f'''# Revisão semântica individual das 474 keywords prioritárias (P0)

## Resumo

- Keywords P0 examinadas: **474/474**, distribuídas entre **{len(set(x['familia_id'] for x in audit))} famílias**.
- Registros com alteração de algum campo: **{summary['p0_alteradas']}**.
- Mudanças de área: **{summary['mudancas_de_area']}**; mudanças de tipo de intenção: **{summary['mudancas_de_intencao']}**.
- Revisões P0 esclarecidas (sem necessidade de revisão manual adicional): **{summary['p0_resolvidas']}**.
- Ambiguidades/decisões P0 ainda abertas: **{review_after}**.
- Lotes com arquivo de versão corrigida: **{len(files_changed)}**.
- Keywords base no acervo: **294.905**; preservadas colunas Ads, IDs e controles de cada lote modificado.

## Critérios

1. Não inferir moeda de origem/destino quando um par não informa direção, ainda que a expressão contenha `conversão`.
2. Conversão direta explicitamente direcionada recebe origem e destino; sem isso não forçar `conversão direta`.
3. Identificar falsos positivos interáreas: INSS/CLT→Trabalho; financiamento→Finanças; lua/calendário→Datas; ouro e cupons→Fora de escopo; geometria→Matemática.
4. Correção de categorias não implica criação automática de páginas. Termos genéricos mantêm decisão editorial em aberto quando necessário.
5. Revisão P0 é pontual: **nenhuma mudança foi propagada automaticamente a todos os integrantes das famílias** sem examinar suas exceções.
6. As planilhas do Google Ads informam faixas/agrupamentos de volume, **não somar volumes de variantes próximas**.

## Controle de regressão

- Todos os lotes revisados foram exportados como **versões paralelas**, sem sobrescrever os originais.
- Cada arquivo reaberto mantém o mesmo número de linhas, **73 controles byte a byte em conteúdo tabular** e as 16 colunas originais inalteradas.
- Não foram criadas conversões diretas sem unidade de origem/destino/direção.
- Golden Set anterior não foi retrainado; 107/107 é validação histórica do pipeline, não teste independente de qualidade desta revisão P0.

## Ambiguidades estratégicas ou semânticas que restam

- Par de moedas sem `de/para` e `peso` sem país de emissão.
- Busca genérica `quanto vale` sem objeto, marcas/serviços pouco identificáveis e consultas truncadas.
- Semanas para meses quando mês civil versus gestação muda a interpretação.
- Fórmulas/termos matemáticos sem verbo; intenção pode ser informativa ou operacional.
- Consulta por salários profissionais e domínios de saúde/educação, que exigem definição de escopo do portal.

## Entregáveis

- `revisao-individual-474-p0.csv`: decisão e justificativa individual, inclusive termos sem alteração.
- `correcoes-objetivas-p0.csv`: patch explícito de campos, antes/depois, por ID global.
- `p0-ambiguidades-remanescentes.csv`: apenas casos que continuam marcados para revisão.
- `fila-priorizada-30-lotes-com-p0-revisado.csv`: fila global anterior, status P0 atualizado e P1–P3 preservados.
- `lote-NNN-revisado-p0-v1.1-barras-v2.csv`: versões paralelas somente dos lotes com correção.
- `revisar_p0_30_lotes_v1.py`: pipeline reexecutável com cobertura por SHA dos 474 IDs.

**Importante:** não é correto afirmar que a revisão de 52 mil keywords foi concluída. Esta etapa é apenas P0. Antes de aplicar correções a todas as famílias, precisamos analisar casos semelhantes de P1/P2 e testar regressões semânticas ampliadas.
'''
(OUT/'relatorio-revisao-p0.md').write_text(report,encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
