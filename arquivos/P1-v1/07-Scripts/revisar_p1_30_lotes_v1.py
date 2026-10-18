#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Revisão contextual CONSERVADORA da fila P1 (2557 registros), partindo das versões P0.

Dependências: apenas Python 3 stdlib. NÃO altera originais.
Entrada --root: fila-priorizada-30-lotes-com-p0-revisado.csv e lotes/lote-NNN-revisado-p0-v1.1-barras-v2.csv.
Saída --out: relatórios auditáveis, patches, fila, versões P1 (todos os controles intactos).
O algoritmo só encerra revisão manual quando encontra sinal forte; os demais permanecem abertos.
Não implica aprovação SEO nem revisão humana integral de 2.557 itens.
"""
import argparse, ast, csv, hashlib, json, re, unicodedata, zipfile
from pathlib import Path
from collections import Counter, defaultdict
p=argparse.ArgumentParser()
p.add_argument('--root',default='/mnt/data/p1_work');p.add_argument('--out',default='/mnt/data/p1_work/p1_outputs')
a=p.parse_args(); ROOT=Path(a.root); OUT=Path(a.out); OUT.mkdir(parents=True,exist_ok=True); (OUT/'lotes').mkdir(exist_ok=True)

def read_csv(path):
    with open(path,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def write_csv(path,rows,fields):
    with open(path,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,delimiter=';',fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
def norm(s):
    s=''.join(c for c in unicodedata.normalize('NFKD',s.lower()) if not unicodedata.combining(c))
    return re.sub(r'\s+',' ',s).strip()
def has(t,*patterns):return any(re.search(p,t) for p in patterns)
def cat(code):return C[code]
# Reuse taxonomia já auditada P0 (somente tuplas literais constantes).
src=(ROOT/'07-Scripts/revisar_p0_30_lotes_v1.py').read_text(encoding='utf-8')
C={}
for x in ast.parse(src).body:
    if isinstance(x,ast.Assign) and len(x.targets)==1 and isinstance(x.targets[0],ast.Name):
        try:v=ast.literal_eval(x.value)
        except:continue
        if isinstance(v,tuple) and len(v)==3 and all(isinstance(z,str) for z in v):C[x.targets[0].id]=v
C.update({'MVOL':('Matemática','Geometria','Volume e geometria espacial'),
          'MROOT':('Matemática','Potências e funções','Potências, raízes e logaritmos'),
          'MSTAT':('Matemática','Estatística e probabilidade','Médias e estatística descritiva'),
          'TPER':('Trabalho','Jornada e adicionais','Adicional de periculosidade'),
          'TDSR':('Trabalho','Jornada e adicionais','DSR'),
          'TGES':('Fora de escopo','Saúde','Saúde/gestação'),
          'CMM':('Conversores','Unidades físicas','Área e superfície'),
          'CVOL':('Conversores','Unidades físicas','Volume e capacidade'),
          'CELECT':('Conversores','Eletricidade e eletrônica','Grandezas elétricas'),
          'CBYTE':('Conversores','Dados digitais','Armazenamento digital'),
          'EUTIL':('Energia','Combustíveis','Consumo e autonomia'),
          'EGAST':('Energia','Combustíveis','Custo de viagem'),
          'ELET':('Energia','Consumo elétrico','Consumo em kWh'),
          'CSOLAR':('Energia','Energia solar','Dimensionamento solar'),
          'CPAREDE':('Construção','Metragem','Área aplicada à construção'),
          'CPINT':('Construção','Pintura','Tinta e pintura'),
          'CTIJ':('Construção','Alvenaria','Blocos e tijolos'),
          'CFIN':('Finanças','Crédito','Financiamentos')})
queue=read_csv(ROOT/'fila-priorizada-30-lotes-com-p0-revisado.csv')
assert len(queue)==52046
p1=[q for q in queue if q['prioridade']=='P1']
assert len(p1)==2557 and len(set(q['id_global'] for q in p1))==2557
assert hashlib.sha256('|'.join(sorted(q['id_global'] for q in p1)).encode()).hexdigest()=='257c97e57a5d6a3e7f12028f664eb2e64146457c7086c48ed17def343e2b9de8'
ORIG=['tipo_registro','id_global','lote_id','familia_id','controle_id','Keyword','ocorrencias_origem','areas_origem','qtd_areas','Avg. monthly searches','Mudança em três meses','Mudança YoY','Competition','Competition (indexed value)','Top of page bid (low range)','Top of page bid (high range)']

currency=[('ARS',r'pesos? argentinos?|ars\b'),('CLP',r'pesos? chilenos?|clp\b'),('MXN',r'pesos? mexicanos?|mxn\b'),('UYU',r'pesos? uruguaios?|uyu\b'),('PYG',r'guaranis?|pyg\b'),('GBP',r'libras? esterlinas?|pounds? sterling|gbp\b'),('CHF',r'francos? suicos?|chf\b'),('JPY',r'ienes?|yens?|jpy\b'),('BTC',r'bitcoins?|btc\b'),('EUR',r'euros?|eur\b'),('USD',r'dolares?|usd\b'),('BRL',r'reais|real\b|brl\b'),('GBP',r'libras?\b')]
unit_alias=[('mm',r'milimetros?|mm\b'),('cm',r'centimetros?|cm\b'),('km',r'quilometros?|kms?\b|km\b'),('mi',r'milhas?|miles?\b'),('in',r'polegadas?|inches?\b|inch\b'),('ft',r'pes\b|feet\b|foot\b'),('m',r'metros?\b|m\b'),('kg',r'quilogramas?|quilos?\b|kilos?\b|kg\b'),('mg',r'miligramas?|mg\b'),('g',r'gramas?|g\b'),('lb',r'libras?\b|lbs?\b|pounds?\b'),('l',r'litros?\b'),('ml',r'mililitros?|ml\b'),('°C',r'celsius\b'),('°F',r'fahrenheit\b'),('K',r'kelvin\b'),('bar',r'bar\b'),('psi',r'psi\b'),('kPa',r'kpa\b'),('atm',r'atm\b|atmosferas?\b'),('h',r'horas?\b'),('min',r'minutos?\b'),('s',r'segundos?\b'),('GB',r'gigabytes?|gb\b'),('MB',r'megabytes?|mb\b'),('KB',r'kilobytes?|kb\b')]

def match_units(seg, aliases):
    found=[]
    for code,pattern in aliases:
        for m in re.finditer(r'(?<!\w)(?:'+pattern+r')(?!\w)',seg):found.append((m.start(),m.end(),code))
    found.sort(key=lambda x:(x[0],-(x[1]-x[0])))
    dis=[]
    for y in found:
        if not dis or y[0]>=dis[-1][1]:dis.append(y)
    return dis

def field_updates(t,q):
    """Return classification rule if confidently grounded. Need not label every one resolved."""
    def r(code, intent, why, conf='alta', manual='não', src=None,dst=None):
        c=cat(code)
        d={'area_principal':c[0],'cluster':c[1],'subcluster':c[2],
           'dominio_ou_grandeza':c[2], 'tipo_intencao':intent,
           'confianca':conf,'revisao_manual':manual,
           'unidade_origem':src or '', 'unidade_destino':dst or '',
           'direcao_conversao':f'{src}→{dst}' if src and dst else ''}
        assert intent!='conversão direta' or (src and dst)
        return d,why
    # Includes truncated strings where we avoid trying to guess missing data.
    if has(t,r'\bquanto vale\s*$',r'^converter\s*$',r'^transformar\s*$',r'^qual o valor de\s*$',r'\bsgd to\b',r'\bconverter r 0 00\b'):
        return None,'Consulta truncada, sem objeto ou destino: manter pendência.'
    # Known false positives take precedence over substrings such as 'metro', 'media', 'saldo'.
    if has(t,r'cupom',r'cupons',r'\bifood\b',r'\bdafiti\b',r'\bprimeira compra\b'):
        return r('OCUP','fora de escopo','Cupom/promoção comercial, não cálculo.')
    if has(t,r'whatsapp\s*gb',r'\bwats?app gb\b'):
        return r('OAPP','fora de escopo','GB nomeia aplicativo, não gigabytes de dados.')
    if has(t,r'\bgestac',r'\bgestante',r'gravidez',r'gravida',r'\bparto\b',r'\bfeto\b',r'\bbebe\b',r'\bsexo do bb\b'):
        return r('OSAU','fora de escopo','Consulta gestacional/saúde; não tratar como conversão temporal genérica.')
    if has(t,r'\btjrs\b',r'\btjsp\b',r'\btjrj\b',r'\bcalc judicial\b',r'\bcalculo judicial\b',r'\bcalcul[oa]s? juridic'):
        return r('OJUR','fora de escopo','Ferramenta/tema jurídico, não aritmética genérica.',conf='média',manual='sim')
    # Externally navigational / brand-specific / educational keywords that aren't calculators.
    if has(t,r'\bprocuradoria\b',r'\bconsultar cnis\b',r'\bcnis consultar\b',r'\bbeneficio pelo cpf\b'):
        return r('OSOFT','navegacional/transacional','Busca de serviço público/consulta de cadastro; não operação aritmética.',conf='média',manual='não')
    if has(t,r'\bpreco da vaca\b',r'\bboi gord',r'\barroba do boi\b'):
        return r('OCOM','consulta de preço/mercado','Consulta de commodity/mercado, não converter massa.')
    if has(t,r'\bouro 18\s?k\b',r'\bpreco do ouro\b',r'\bouro por grama\b'):
        return r('OOuro','consulta de preço/mercado','Cotação de metal precioso, não conversor de massa.')
    if has(t,r'\brateio de cursos\b',r'\bcursos rateio\b',r'\brateio cursos\b'):
        return r('OEDU','fora de escopo','Busca por rateio/acesso a cursos, não divisão de contas.')
    if has(t,r'\bcalculadora com bobina\b'):
        return r('OTEC','fora de escopo','Busca por calculadora física como produto.')
    if has(t,r'\b[a-z]*youtube\b',r'\byoutuber?\b') and has(t,r'\b(mp3|mp4|video|conversor|converter)\b'):
        code='CAUD' if 'mp3' in t else 'CVID'
        return r(code,'conversão de arquivo/mídia','Conversão de vídeo/áudio do YouTube; não conversão de frequência Hz.')
    # File formats (not physical quantities). Safe direction where format is explicit.
    if has(t,r'\bpdf\b',r'\bword\b',r'\bdocx?\b',r'\bpptx?\b',r'\bpowerpoint\b',r'\bjpg\b',r'\bpng\b',r'\bjpeg\b',r'\bexcel\b',r'\bmp3\b',r'\bmp4\b',r'\bwav\b',r'\bico\b'):
        if has(t,r'\bmesclar\s+pdf',r'\bjuntar\s+pdf',r'\beditar\s+pdf'):
            return r('OTEC','fora de escopo','Manipulação de PDF sem mudança de formato.')
        if has(t,r'\bplanilhas?\b',r'\bplanilha (?:de|excel|para)\b',r'\bcontrole (?:de )?gastos\b') and not has(t,r'\bconverter\b',r'\bconversao\b',r'\btransformar\b'):
            return r('FBUD','informacional','Planilha financeira/controle de gastos; não converter arquivo.',conf='média',manual='não')
        if has(t,r'\b(pdf|docx?|word|pptx?|powerpoint|jpg|jpeg|png|excel|mp3|mp4|wav|ico)\b') and has(t,r'\bconvers|\btransform|\bpassar|\bformat'):
            out = 'CAUD' if has(t,r'mp3',r'\bwav\b') else ('CVID' if 'mp4' in t else ('CIMG' if has(t,r'\bjpg\b',r'\bpng\b',r'\bjpeg\b',r'\bico\b') and not has(t,r'\bpdf\b',r'\bword\b') else 'CFILE'))
            return r(out,'conversão de arquivo/mídia','Intenção de converter formato de arquivo/mídia explicitada.',conf='alta' if has(t,r'\b(?:para|em)\b') else 'média',manual='não' if has(t,r'\b(?:para|em)\b') else 'sim')
        if has(t,r'\bpdf\b',r'\bword\b',r'\bdocx?\b') and not has(t,r'\bcalcul',r'\bimpost',r'\bjuros'):
            return r('CFILE','ambígua/revisão','Formato isolado/justaposto; falta direção/ação inequívoca.',conf='média',manual='sim')
    # Monetary context, with unambiguous directed pairs only.
    cmatches=match_units(t,currency)
    if has(t,r'\bpesos?\b') and not has(t,r'\bargentino',r'\bchileno',r'\bmexicano',r'\buruguaio',r'\bkg\b',r'\bgram') and has(t,r'\breais?\b',r'\bdolar',r'\beuro',r'\bconvers',r'\bcambio'):
        return r('CFX','ambígua/revisão','Peso sem país de emissão: direção/moeda não inferível.',conf='baixa',manual='sim')
    if (len(cmatches)>=2 and cmatches[0][2]!=cmatches[1][2] and
        not has(t,r'\bfinanciamento\b',r'\bjuros\b',r'\bcdb\b',r'\b(?:preco|valor) da libra\b')):
        a1,b1,ca=cmatches[0];a2,b2,cb=cmatches[1]
        between=t[b1:a2]
        # bare 'x', '/' or juxtaposed doesn't establish the direction.
        if re.search(r'\b(?:para|em|pra|to)\b',between):
            return r('CFX','conversão direta',f'Par de moedas com direcionalidade explícita: {ca}→{cb}.',src=ca,dst=cb)
        if has(t,r'\bquanto\b.*\b(?:vale|equivale|da|sao)\b',r'\bvale\b.*\bquantos\b') and re.search(r'\b(?:em|para)\b',t):
            return r('CFX','conversão direta',f'Equivalência monetária com direção explícita: {ca}→{cb}.',src=ca,dst=cb)
        return r('CFX','ambígua/revisão','Moedas citadas sem preposição direcional: não inferir origem/destino.',conf='média',manual='sim')
    if len(cmatches)>=1 and has(t,r'\bcotac',r'\bcambio\b',r'\bvalor\b',r'\bpreco\b',r'\bhoje\b',r'\bquanto (?:vale|custa)',r'\brate\b') and not has(t,r'\bfinancia'):
        return r('FCOT','cotação atual','Consulta de valor/cotação de moeda, não conversão com duas moedas.')
    if len(cmatches)>=1 and has(t,r'\bconversor\b',r'\bconverter\b',r'\bconversao\b'):
        return r('CFX','navegacional/transacional','Busca de conversor cambial sem duas moedas direcionadas.',conf='média',manual='não')
    # Work and labor; exclude ambiguities like INSS de obra (tax).
    if has(t,r'\binss\b',r'\birrf\b',r'\bimposto de renda\b',r'\birpf\b'):
        if has(t,r'\bsite oficial\b',r'\bmeu inss\b',r'\bconsultar\b',r'\bmeu processo\b'):
            return r('TPREV','navegacional/transacional','Portal ou consulta do INSS, não cálculo da folha.',conf='média',manual='não')
        if has(t,r'\bimovel\b',r'\bobra\b',r'\bconstrucao\b'):
            return r('FTRIB','cálculo contextual','INSS de obra/construção tem contexto tributário próprio.',conf='média',manual='sim')
        if has(t,r'\birpf\b',r'\bimposto de renda\b') and not has(t,r'\bsalario\b',r'\bfolha\b'):
            return r('FTRIB','cálculo direto' if has(t,r'calcul',r'simula') else 'informacional','IRPF é tributo, não álgebra genérica.',conf='média',manual='não')
        if has(t,r'\btabela\b',r'\bal[íi]quota\b',r'\bdesconto\b') and not has(t,r'\bcalcular\b',r'\bcalculo\b',r'\bsimula'):
            return r('TFL','tabela/referência','Tabela de descontos/regras de folha, sem operação explícita.')
        return r('TFL','cálculo direto' if has(t,r'calcul',r'simula',r'\bdesconto\b') else 'informacional','INSS/IRRF pertence a folha e encargos, não geometria/energia.')
    if has(t,r'\bfgts\b'):
        if has(t,r'\bconsult',r'\bcpf\b',r'\btelefone\b',r'\baplicativ',r'\bcaixa app\b'):
            return r('TFGTS','navegacional/transacional','Consulta de conta FGTS ou aplicativo, não cálculo de saldo.')
        return r('TFGTS','cálculo direto' if has(t,r'\bcalcul',r'\bsimula') else 'informacional','FGTS explicitamente trabalhista.',conf='alta',manual='não')
    if has(t,r'\bdecimo terceiro\b',r'\b13\s*(?:o|salario)\b',r'\b13o salario\b'):
        return r('T13','cálculo direto' if has(t,r'calcul',r'simul') else 'informacional','Décimo terceiro é remuneração trabalhista.')
    if has(t,r'\bferias\b',r'\bferias proporcionais\b') and not has(t,r'\bferiado\b'):
        return r('TFER','cálculo direto' if has(t,r'calcul',r'simula') else 'informacional','Férias trabalhistas, não intervalo genérico.')
    if has(t,r'\bhora extra\b',r'\bhoras extras\b'):
        return r('TEXTRA','cálculo direto' if has(t,r'calcul',r'somar',r'\bvalor\b') else 'informacional','Horas extras são jornada/adicionais trabalhistas.')
    if has(t,r'\bdsr\b'):
        return r('TDSR','cálculo direto' if has(t,r'calcul') else 'informacional','Descanso semanal remunerado, jornada trabalhista.')
    if has(t,r'\bpericulosidade\b',r'\binsalubridade\b'):
        return r('TLEG','cálculo direto' if has(t,r'calcul',r'\bpercentual\b') else 'informacional','Adicional/benefício de trabalho; não pintura nem potência.')
    if has(t,r'\bsalario\b',r'\bsalarios\b',r'\bremuneracao\b'):
        if has(t,r'\bdeputado\b',r'\bprofiss',r'\btanatopraxia\b'):
            return r('TREM','informacional','Consulta de salário por profissão/pessoa, sem cálculo.',conf='média',manual='sim')
        if has(t,r'\bhoras?\b',r'\bdias?\b',r'\bproporcional\b'):
            return r('THORA','cálculo direto' if has(t,r'calcul') else 'informacional','Valor proporcional de salário por hora/dia.')
        return r('TREM','cálculo direto' if has(t,r'calcul',r'simula') else 'informacional','Salário/remuneração trabalhista, não área/volume.')
    if has(t,r'\btempo de (?:servico|trabalho)\b',r'\bvalor (?:da )?hora trabalhad',r'\bhoras trabalhadas\b'):
        return r('THORA','cálculo direto' if has(t,r'calcul',r'\bquantas\b') else 'informacional','Cálculo de jornada ou tempo de trabalho.')
    if has(t,r'\bclt\b',r'\bseguro desemprego\b',r'\blicenca paternidade\b',r'\baviso previo\b'):
        code='TRES' if has(t,r'\baviso previo\b') else 'TLEG'
        return r(code,'cálculo contextual' if has(t,r'calcul') else 'informacional','Direito trabalhista explícito.',conf='média',manual='não')
    # Financial investments, loans, inflation. Specific terms first.
    if has(t,r'\bsimulador (?:da )?caixa poupanca\b',r'\bcaixa simulador poupanca\b'):
        return r('FCDI','simulação/projeção','Simulação de rendimento de poupança; não financiamento.')
    if has(t,r'\bfinanciament',r'\bfinanciar\b',r'\bcredito imobiliario\b',r'\bminha casa minha vida\b'):
        return r('FCRED','simulação/projeção' if has(t,r'simul',r'\bparcel',r'calcul') else ('navegacional/transacional' if has(t,r'\bcaixa\b',r'\bbanco\b',r'\bsantander\b') else 'informacional'), 'Financiamento/crédito, mesmo quando ligado a imóvel/construção.')
    if has(t,r'\bemprestim',r'\bemprestimo\b'):
        return r('FLOAN','simulação/projeção' if has(t,r'simul',r'calcul') else 'navegacional/transacional','Empréstimo financeiro/contratação, não conversão de unidade.')
    if has(t,r'\bcdb\b',r'\bcdi\b',r'\bpoupanca\b',r'\btesouro direto\b'):
        return r('FCDI','simulação/projeção' if has(t,r'\brend',r'simul',r'calcul') else 'informacional','Renda fixa/investimentos, não conversão física.',conf='média',manual='não')
    if has(t,r'\bbolsa de valores\b',r'\bacoes\b',r'\bdividendos\b'):
        return r('FSTOCK','informacional','Investimentos em ações/dividendos.',conf='média',manual='não')
    if has(t,r'\bfundos? de investiment',r'\brentabil',r'\brendimento\b'):
        return r('FINV','simulação/projeção' if has(t,r'simul',r'calcul',r'\brend') else 'informacional','Rentabilidade de investimento/carteira.',conf='média',manual='não')
    if has(t,r'\bjuros compost',r'\bjuros simples\b'):
        intent=('informacional' if has(t,r'\bo que\b',r'\bqual\b',r'\bcomo funciona\b') else ('simulação/projeção' if has(t,r'\bsimula',r'\bquanto rende') else 'cálculo direto'))
        return r('FJUROS',intent,'Juros financeiros, distinguindo perguntas conceituais de operações.')
    if has(t,r'\bipca\b',r'\binpc\b',r'\binflacao\b'):
        return r('FIPCA','cálculo direto' if has(t,r'calcul') else 'tabela/referência','Índice de inflação/correção monetária.')
    if has(t,r'\borcamento\b',r'\bplanilha de gastos\b',r'\bcontrole de gastos\b') and not has(t,r'\bobra\b',r'\bmaterial\b'):
        return r('FBUD','informacional','Orçamento financeiro/controle de despesas.',conf='média',manual='não')
    # Academic math. Avoid matching generic words in finance/health contexts.
    if has(t,r'\braiz quadrada\b',r'\braiz cubica\b',r'\bpotencias?\b',r'\bexponencial\b',r'\blogaritm'):
        op='cálculo direto' if has(t,r'\bde\s+\d+',r'\bcalculadora\b',r'\bcalcular\b',r'\bcalculo\b') else 'informacional'
        return r('MROOT',op,'Raiz/potência/logaritmo: conteúdo ou operação matemática.')
    if has(t,r'\bmedia ponderada\b',r'\bmedia aritmetica\b',r'\bmediana\b',r'\bmoda\b',r'\bdesvio padrao\b',r'\bvariancia\b'):
        return r('MSTAT','cálculo direto' if has(t,r'calcul',r'\bcomo fazer\b') else 'informacional','Média/estatística, não valor de combustível ou imposto.')
    if has(t,r'\bprobabil',r'\bpermut',r'\bcombinatori'):
        return r('MPROB','cálculo direto' if has(t,r'calcul') else 'informacional','Probabilidade/combinatória, não porcentagem trabalhista.')
    if has(t,r'\bregra de tres\b',r'\bproporc',r'\bporcentag',r'\bpercentual\b'):
        return r('MPOR','cálculo direto' if has(t,r'calcul') else 'informacional','Raciocínio proporcional/percentual explícito.')
    if has(t,r'\btrigonometr',r'\bradianos\b',r'\bgraus para radianos\b',r'\bseno\b',r'\bcosseno\b'):
        return r('MTRIG','cálculo direto' if has(t,r'calcul',r'\bpara\b') else 'informacional','Ângulos/trigonometria, não temperatura.')
    if has(t,r'\bequac',r'\bsistemas? lineares?\b',r'\bsistema de equacao\b'):
        return r('MALG','cálculo direto' if has(t,r'calcul',r'\bresolver\b') else 'informacional','Equações e sistemas algébricos.')
    if has(t,r'\bprogressao geometrica\b',r'\bprogressao aritmetica\b'):
        return r('MPROG','cálculo direto' if has(t,r'\bsoma\b',r'\bcalcul') else 'informacional','Progressões matemáticas.')
    if has(t,r'\bromanos?\b',r'\bnumeracao romana\b',r'\bbinario\b',r'\bhexadecimal\b'):
        return r('CSYS','conversão direta' if False else ('cálculo direto' if has(t,r'\bconverter\b',r'\bcalculadora\b') else 'tabela/referência'),'Sistema de numeração romano/posicional; sem inventar direção técnica.')
    if has(t,r'\bvolume d[oa] (?:cone|cubo|cilindro|prisma)\b',r'\bformula (?:do )?volume\b',r'\bvolume dos prismas\b'):
        return r('MVOL','cálculo direto' if has(t,r'calcul') else 'informacional','Fórmula ou volume geométrico, não cimento/material de obra.')
    if has(t,r'\barea do (?:triangulo|circulo|retangulo|quadrado)\b',r'\bperimetro\b',r'\bmetros quadrados?\b',r'\bmetro quadrado\b'):
        if has(t,r'\bparede\b',r'\bpintura\b',r'\bpiso\b',r'\btelha\b'):
            return r('CPAREDE','cálculo direto','Área explicitamente aplicada à construção.')
        return r('MGEOM','cálculo direto' if has(t,r'calcul',r'\bquantos\b') else 'informacional','Área/perímetro geométrico sem contexto de obra.')
    # Calendar and dates.
    if has(t,r'\bcalendario\b',r'\bdatas comemorativas\b',r'\bferiado\b',r'\bcarnaval\b',r'\bdia dos pais\b'):
        return r('DFER' if has(t,r'\bferiado\b',r'\bcarnaval\b') else 'DBAS','tabela/referência' if has(t,r'\bferiado\b',r'\bcarnaval\b') else 'informacional','Calendário/data comemorativa, não cálculo de horas trabalhadas.')
    if has(t,r'\bsubtrair horas\b',r'\bcalculadora de tempo horas\b',r'\bhora e minuto\b'):
        return r('DHOR','cálculo direto','Operação com duração (horas/minutos) independente de jornada.')
    # Construction explicit materials.
    if has(t,r'\btelhado\b',r'\bcalha\b',r'\btelha\b'):
        return r('CPAREDE','cálculo contextual' if has(t,r'inclinac') else 'estimativa de quantidade','Geometria/material de telhado aplicado à construção.')
    if has(t,r'\btinta\b',r'\bimpermeabil',r'\bvedapren\b'):
        return r('CPINT','estimativa de quantidade' if has(t,r'\bquant',r'calcul') else 'informacional','Material para pintura/impermeabilização de obra.',conf='média',manual='não')
    if has(t,r'\btijolo\b',r'\bassentam',r'\bcontrapiso\b'):
        return r('CTIJ','estimativa de quantidade','Material/traço de alvenaria.',conf='média',manual='não')
    # Energy and electrical signals.
    if has(t,r'\bgasolina\b',r'\bcombustivel\b',r'\bdiesel\b',r'\bpedagio\b'):
        return r('EGAST' if has(t,r'\bpedagio\b',r'\bcusto\b',r'\bgasto\b',r'\bvalor\b') else 'EUTIL',
                 'estimativa de custo' if has(t,r'\bpedagio\b',r'\bcusto\b',r'\bgasto\b',r'\bvalor\b') else 'estimativa de consumo',
                 'Consumo/custo de combustível, não grandeza monetária de câmbio.',conf='média',manual='não')
    if has(t,r'\benergia solar\b',r'\bpainel solar\b',r'\bfotovoltaic'):
        return r('CSOLAR','dimensionamento','Sistema fotovoltaico, não aplicação financeira.',conf='média',manual='não')
    if has(t,r'\bqueda de tensao\b',r'\bvolts\b',r'\bwatts\b',r'\bpotencia eletrica\b',r'\bkw\b'):
        if has(t,r'\btransformador de energia\b'):
            return r('OTEC','fora de escopo','Transformador de tensão é equipamento físico, não calculadora.')
        return r('CELECT','cálculo contextual' if has(t,r'\bpotencia\b',r'\bwatts\b',r'\bcalculo\b') else 'ambígua/revisão',
                 'Grandezas elétricas podem depender de contexto/fator de potência.',conf='média',manual='sim')
    # Directed unit conversions. Weak pairs remain unresolved.
    umatches=match_units(t,unit_alias)
    if len(umatches)>=2:
        # Restrict mass 'libra' mixing with currency to clear mass units only; exclude time pregnancy above.
        x,y=umatches[0],umatches[1]; src,dst=x[2],y[2]
        if src != dst and has(t,r'\bconvers',r'\btransform',r'\bquantos?\b',r'\bpara\b',r'\bem\b',r'\bfor\b'):
            between=t[x[1]:y[0]]
            if re.search(r'\b(?:em|para|pra|to)\b',between):
                type_map={'cm':'CLEN','mm':'CLEN','km':'CLEN','mi':'CLEN','in':'CLEN','ft':'CLEN','m':'CLEN','kg':'CMASS','mg':'CMASS','g':'CMASS','lb':'CMASS','ml':'CCUL','l':'CCUL','°C':'CTEMP','°F':'CTEMP','K':'CTEMP','bar':'CPRES','psi':'CPRES','kPa':'CPRES','atm':'CPRES','h':'CTIME','min':'CTIME','s':'CTIME','GB':'CBYTE','MB':'CBYTE','KB':'CBYTE'}
                catcode=type_map.get(src)
                if src in ('g','kg','mg','lb') and dst in ('ml','l') or src in ('ml','l') and dst in ('g','kg','mg','lb'):
                    return r('CCUL','cálculo contextual','Massa↔volume culinário depende de ingrediente e densidade.',conf='média',manual='sim')
                if catcode and type_map.get(dst)==catcode and not has(t,r'\bconversor online\b'):
                    if has(t,r'\btabela\b'):
                        return r(catcode,'tabela/referência','Tabela de equivalência unitária solicitada; não operação de valor direto.',conf='alta',manual='não')
                    return r(catcode,'conversão direta',f'Grandezas compatíveis com direção expressa: {src}→{dst}.',src=src,dst=dst)
            else:
                return r('CCON','ambígua/revisão','Duas unidades mencionadas sem direção inequívoca.',conf='média',manual='sim')
    if has(t,r'\bconversor (?:online|de unidades)\b',r'\bconversao de unidades\b',r'\btransformador de unidade\b'):
        return r('CCON','navegacional/transacional','Busca genérica por ferramenta conversora, sem par direcional.',conf='média',manual='não')
    # Padrões suplementares com tipo preciso; não inferir direções nem regras de produto.
    if has(t,r'\bsemanas?\b') and has(t,r'\bmeses?\b'):
        return r('CTIME','cálculo contextual','Semanas↔meses sem referência a gestação depende de definição de mês (calendário/4 semanas).',conf='média',manual='sim')
    if has(t,r'\bconvers',r'\bconverter',r'\btransformac') and has(t,r'\bmedidas?\b',r'\bunidades?\b'):
        return r('CCON','tabela/referência' if has(t,r'\btabela\b') else 'navegacional/transacional','Conversão genérica de medidas sem par de unidades; tabela ou ferramenta conforme redação.',conf='média',manual='não')
    if has(t,r'\bconversor(?: de)? moedas?\b',r'\bconversao de moedas?\b',r'\bconverter moedas?\b',r'\bconverter? moedas?\b',r'\bconversor de moeda\b'):
        return r('CFX','navegacional/transacional','Conversor genérico de moedas sem par dirigido.',conf='média',manual='não')
    if has(t,r'\bconversor de temperatura\b',r'\bconversao de temperatura\b',r'\bconverter de temperatura\b'):
        return r('CTEMP','navegacional/transacional','Busca geral de conversor de temperatura, sem par dirigido.',conf='média',manual='não')
    if has(t,r'\bcolher\b',r'\bcolheres\b',r'\bgramas?\b.*\bml\b',r'\bvolumes? para massas?\b') and has(t,r'\bgramas?\b',r'\bml\b',r'\bquantas?\b'):
        return r('CCUL','cálculo contextual','Medida culinária massa↔volume exige ingrediente/medida padrão.',conf='média',manual='sim')
    if has(t,r'\babrir conta\b',r'\bagencia do bradesco\b',r'\bagencia do banco\b'):
        return r('OSOFT','navegacional/transacional','Abertura/localização de conta bancária, não calculadora.')
    if has(t,r'\bpromocoes?\b',r'\bblack friday\b',r'\bofertas\b',r'\bpreco de tv\b'):
        return r('OCUP','fora de escopo','Busca por promoções de varejo/preços de produtos.')
    if has(t,r'\blua\b') and has(t,r'\bhoje\b',r'\besta\b',r'\btem\b'):
        return r('DBAS','informacional','Consulta lunar/calendário, não cotação financeira.',conf='média',manual='não')
    if has(t,r'\bdia das? maes?\b',r'\bdata natal\b',r'\baniversario\b',r'\bnatal\b',r'\bano novo\b',r'\bdias de semana\b',r'\banos bissextos\b'):
        return r('DBAS','informacional','Data ou referência de calendário.',conf='média',manual='não')
    if has(t,r'\bdias uteis\b',r'\bcalculadora de dias uteis\b'):
        return r('DFER','cálculo direto','Contagem de dias úteis exige calendário/feriados.')
    if has(t,r'\bcalculadora (?:de )?horas?\b',r'\bhoras? subtracao\b',r'\bcontad(?:or|ora) de meses?\b'):
        return r('DHOR' if has(t,r'\bhora') else 'DINT','cálculo direto','Contagem/duração temporal explícita.')
    if has(t,r'\bcalculadora de ir\b',r'\bcalculo do ir\b',r'\bir calculo\b',r'\bcalculadora do igpm\b',r'\bcalculo igpm\b',r'\bcalculadora igpm\b',r'\btaxa selic\b'):
        return r('FTRIB' if has(t,r'\bir\b') else 'FIPCA','cálculo direto' if has(t,r'calcul') else 'tabela/referência','Imposto de renda/índice financeiro sem relação com aritmética genérica.',conf='média',manual='não')
    if has(t,r'\bconsorcio\b',r'\bconsignado\b',r'\bsimulador habitac',r'\bsimulacao habitac',r'\bcaixa simulador imovel\b',r'\bsimulador (?:da )?caixa\b'):
        return r('FCRED','simulação/projeção' if has(t,r'simul') else 'informacional','Crédito/consórcio habitacional ou consignado.',conf='média',manual='não')
    if has(t,r'\bquanto rende\b',r'\brende quanto\b',r'\bquanto .* rende\b',r'\bselic\b',r'\blci\b',r'\blca\b'):
        return r('FINV','simulação/projeção' if has(t,r'\brend') else 'informacional','Projeção ou referência de rendimento de investimento.',conf='média',manual='não')
    if has(t,r'\bsaque aniversario\b',r'\bsaque jam\b',r'\babono salarial\b',r'\baposentadoria\b',r'\bprevidencia social\b',r'\bauxilio doenca\b'):
        return r('TPREV','navegacional/transacional' if has(t,r'\bconsult',r'\bsolicitar\b',r'\btelefone\b') else 'informacional','Benefício previdenciário/FGTS, sem operação aritmética inequívoca.',conf='média',manual='sim')
    if has(t,r'\brescis',r'\bpedido de demissao\b',r'\bjusta causa\b',r'\bdemissao\b',r'\bdesligamento\b',r'\bacordo trabalhista\b'):
        return r('TRES','cálculo contextual' if has(t,r'\bcalcul',r'\bvalor\b') else 'informacional','Rescisão e verbas de desligamento.',conf='média',manual='não')
    if has(t,r'\bhora trabalhada\b',r'\bhorario de trabalho\b',r'\bescalas? [0-9]x[0-9]\b',r'\bhoras? de trabalho\b',r'\b44 h semanais\b',r'\b220 horas mensais\b'):
        return r('TJORN','cálculo direto' if has(t,r'calcul') else 'informacional','Jornada/escala de trabalho em vez de conversão de horas.',conf='média',manual='não')
    if has(t,r'\bfatorial\b',r'\barranjo\b',r'\bcombinacao\b',r'\bmmc\b',r'\bmdc\b',r'\bmultiplos?\b',r'\bdivisores?\b'):
        return r('MPROB' if has(t,r'\bfatorial\b',r'\barranjo\b',r'\bcombinacao\b') else 'MNUM','cálculo direto' if has(t,r'\bde [0-9]+\b',r'\bfazer\b',r'\bcalcul') else 'informacional','Operações de combinatória, divisibilidade ou fatoriais.',conf='média',manual='não')
    if has(t,r'\bbhaskara\b',r'\bdelta\b',r'\bcramer\b',r'\bmetodo da substituicao\b',r'\bpolinomios\b'):
        return r('MALG','cálculo direto' if has(t,r'\bresol',r'\bcalcul') else 'informacional','Álgebra e métodos de resolução de equações.',conf='média',manual='não')
    if has(t,r'\bpa e pg\b',r'\bpa\b.*\bpg\b',r'\bsoma da pa\b',r'\bsoma da pg\b',r'\btermo geral da pa\b',r'\btermo geral da pg\b'):
        return r('MPROG','cálculo direto' if has(t,r'\bsoma\b') else 'informacional','Progressões aritmética/geométrica explícitas.',conf='média',manual='não')
    if has(t,r'\bpitagoras\b',r'\btriangulo retangulo\b',r'\bcircunferencia\b'):
        return r('MGEO3','cálculo direto' if has(t,r'\bcalcular\b') else 'informacional','Geometria plana e relações métricas.',conf='média',manual='não')
    if has(t,r'\braiz de [0-9]+\b',r'\bloga?r?[íi]tm',r'\blog propriedades\b'):
        return r('MROOT','cálculo direto' if has(t,r'\braiz de [0-9]+\b') else 'informacional','Raiz e logaritmo matemático.',conf='média',manual='não')
    if has(t,r'\bnota (?:do |no )?enem\b',r'\bmedia (?:do |no )?enem\b'):
        return r('OEDU','fora de escopo','Notas do ENEM exigem regras educacionais; não média estatística genérica.',conf='média',manual='sim')
    if has(t,r'\bcalculadora escada\b',r'\bcalculadora escadas\b'):
        return r('CPAREDE','cálculo contextual','Escada é dimensionamento construtivo, não geometria abstrata.',conf='média',manual='não')
    if has(t,r'\bkm por litro\b',r'\blitro por km\b',r'\bkwh mes\b',r'\bk wh\b'):
        return r('ELET' if has(t,r'kwh',r'k wh') else 'EUTIL','estimativa de custo' if has(t,r'\bquanto custa\b') else 'estimativa de consumo','Consumo de combustível ou energia elétrica.',conf='média',manual='não')
    return None,'Nenhum padrão contextual inequívoco; preservada classificação original e revisão manual.' 

# Verify each row against original P0 source, preserve all base identities and controls.
base_by_id={}; lot_rows={}; lot_headers={}; lot_index={}
for n in range(1,31):
    lot=f'{n:03d}'; f=ROOT/'lotes'/f'lote-{lot}-revisado-p0-v1.1-barras-v2.csv'
    rows=read_csv(f);lot_rows[lot]=rows;lot_headers[lot]=list(rows[0]);
    controls=[x for x in rows if x['tipo_registro']=='controle'];assert len(controls)==73,(lot,len(controls))
    for j,x in enumerate(rows):
        if x['tipo_registro']=='base':
            assert x['id_global'] not in base_by_id
            base_by_id[x['id_global']]=x;lot_index[x['id_global']]=(lot,j)
assert len(base_by_id)==294905
assert len(set(x['id_global'] for x in p1)-set(base_by_id))==0

updates={}; review=[]; patches=[]; why_counter=Counter()
for order,q in enumerate(p1,1):
    lot,idx=lot_index[q['id_global']];old=lot_rows[lot][idx]
    assert q['lote']==lot and q['Keyword']==old['Keyword']
    txt=norm(old['Keyword']);result,why=field_updates(txt,q)
    new=dict(old)
    if result:
        new.update(result)
        # Do not lower manual scrutiny when rule is uncertain.
        if result['revisao_manual']=='não' and result['confianca'] in ('baixa',):raise AssertionError('Regra fraca fechou revisão')
        new['intencao_principal']=(f'Converter: {new["subcluster"]}' if new['tipo_intencao']=='conversão direta' else
            f'Consultar cotação: {new["subcluster"]}' if new['tipo_intencao']=='cotação atual' else
            f'Simular: {new["subcluster"]}' if new['tipo_intencao']=='simulação/projeção' else
            f'Calcular: {new["subcluster"]}' if new['tipo_intencao']=='cálculo direto' else
            f'Consultar informação: {new["subcluster"]}' if new['tipo_intencao']=='informacional' else
            f'Rever intenção: {new["subcluster"]}' if new['tipo_intencao']=='ambígua/revisão' else
            f'Intenção {new["tipo_intencao"]}: {new["subcluster"]}')
        if any(new[k]!=old[k] for k in new): new['justificativa_curta']='Revisão P1 automatizada: '+why
    changed=[k for k in new if old[k]!=new[k]]
    assert all(new[k]==old[k] for k in ORIG)
    if new['tipo_intencao']=='conversão direta':assert all(new[z] for z in ('unidade_origem','unidade_destino','direcao_conversao'))
    if changed:
        patches.append({'lote':lot,'id_global':q['id_global'],'Keyword':q['Keyword'],
                        'campos_alterados':','.join(changed),
                        'antes_json':json.dumps({k:old[k] for k in changed},ensure_ascii=False),
                        'depois_json':json.dumps({k:new[k] for k in changed},ensure_ascii=False),
                        'justificativa':why})
        updates[q['id_global']]=new
    status='REGRA_CONTEXTO_FORTE' if result and new['revisao_manual']=='não' else 'PENDENTE_SEMANTICA'
    review.append({'ordem':order,'lote':lot,'id_global':q['id_global'],'familia_id':q['familia_id'],
                   'Keyword':q['Keyword'],'volume_ads_patamar':q['Avg. monthly searches'],
                   'status_decisao':status,'regra_identificada':'sim' if result else 'não',
                   'alterado':'sim' if changed else 'não','area_anterior':old['area_principal'],
                   'area_revisada':new['area_principal'],'cluster_anterior':old['cluster'],'cluster_revisado':new['cluster'],
                   'subcluster_anterior':old['subcluster'],'subcluster_revisado':new['subcluster'],
                   'intencao_anterior':old['tipo_intencao'],'intencao_revisada':new['tipo_intencao'],
                   'origem':new['unidade_origem'],'destino':new['unidade_destino'],'direcao':new['direcao_conversao'],
                   'confianca_anterior':old['confianca'],'confianca_revisada':new['confianca'],
                   'revisao_manual_anterior':old['revisao_manual'],'revisao_manual_revisada':new['revisao_manual'],
                   'justificativa':why})
    why_counter[why]+=1

# Protect queue P0/P2/P3; only annotated P1 records affected.
review_by_id={x['id_global']:x for x in review};qnew=[]
for row in queue:
    q=dict(row)
    if q['prioridade']=='P1':
        x=review_by_id[q['id_global']]
        q.update(area=x['area_revisada'],cluster=x['cluster_revisado'],subcluster=x['subcluster_revisado'],
                 tipo_intencao_atual=x['intencao_revisada'],confianca_atual=x['confianca_revisada'],
                 status_revisao='P1_TRIADO_AUTO' if x['status_decisao']=='REGRA_CONTEXTO_FORTE' else 'PENDENTE_VALIDACAO_P1',
                 decisao_final='CORRIGIR' if x['alterado']=='sim' else ('MANTER' if x['status_decisao']=='REGRA_CONTEXTO_FORTE' else ''),
                 observacao_revisor=x['justificativa'])
    qnew.append(q)
assert len(qnew)==len(queue)
for a,b in zip(queue,qnew):
    if a['prioridade']!='P1':assert a==b
write_csv(OUT/'fila-priorizada-30-lotes-com-p0-p1.csv',qnew,list(queue[0]))

# Full CSV versions; all original fields preserved, nonselected rows identical.
file_changed=[];reg_checks=[]
for lot,rows in lot_rows.items():
    mod={k:v for k,v in updates.items() if lot_index[k][0]==lot}
    if not mod:continue
    fresh=[mod.get(r['id_global'],r) if r['tipo_registro']=='base' else r for r in rows]
    f=OUT/'lotes'/f'lote-{lot}-revisado-p0-p1-v1.1-barras-v2.csv'
    write_csv(f,fresh,lot_headers[lot]);reread=read_csv(f)
    assert len(reread)==len(rows)
    assert sum(x['tipo_registro']=='controle' for x in reread)==73
    assert all(o==n for o,n in zip(rows,reread) if o['tipo_registro']=='controle')
    assert all(o==n for o,n in zip(rows,reread) if o['tipo_registro']=='base' and o['id_global'] not in mod)
    assert all(all(o[k]==n[k] for k in ORIG) for o,n in zip(rows,reread))
    assert not any(r['tipo_registro']=='base' and r['tipo_intencao']=='conversão direta' and not all(r[k] for k in ('unidade_origem','unidade_destino','direcao_conversao')) for r in reread)
    file_changed.append(f)
    reg_checks.append({'lote':lot,'registros':len(rows),'controles':73,'controles_inalterados':73,
                       'ads_16_colunas_identicas':True,'linhas_p1_alteradas':len(mod),'demais_linhas_identicas':True,'conversoes_sem_metadados':0})

write_csv(OUT/'revisao-automatizada-2557-p1.csv',review,list(review[0]))
write_csv(OUT/'patches-objetivos-p1.csv',patches,list(patches[0]) if patches else ['lote','id_global','Keyword','campos_alterados','antes_json','depois_json','justificativa'])
pending=[r for r in review if r['status_decisao']=='PENDENTE_SEMANTICA']
write_csv(OUT/'p1-pendencias-validacao.csv',pending,list(review[0]))
write_csv(OUT/'qa-regressao-p1-por-lote.csv',reg_checks,list(reg_checks[0]))
summary={'universo_base':len(base_by_id),'p1_total':len(p1),'p1_familias':len(set(r['familia_id'] for r in p1)),
         'registros_com_regra_forte':sum(x['status_decisao']=='REGRA_CONTEXTO_FORTE' for x in review),
         'registros_pendentes_validacao':len(pending),'registros_alterados':len(patches),
         'mudancas_area':sum(x['area_anterior']!=x['area_revisada'] for x in review),
         'mudancas_tipo_intencao':sum(x['intencao_anterior']!=x['intencao_revisada'] for x in review),
         'novas_conversoes_diretas':sum(x['intencao_revisada']=='conversão direta' and x['intencao_anterior']!='conversão direta' for x in review),
         'lotes_com_patches':len(file_changed),'controles_verificados':sum(r['controles'] for r in reg_checks),
         'p0_inalterado':True,'p2_p3_inalterados':True,'ads_originais_intactos':True}
(OUT/'resumo-p1.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'relatorio-p1.md').write_text(f'''# P1 — triagem contextual conservadora de 2.557 keywords

## Resultado
- Fila P1: **{len(p1)}** registros de **{summary['p1_familias']}** famílias, distribuídos nos 30 lotes.
- Regras contextuais fortes, sem pendência manual: **{summary['registros_com_regra_forte']}**.
- Ainda dependentes de validação semântica/editorial: **{len(pending)}**.
- Registros cujo conteúdo classificatório mudou: **{len(patches)}**.
- Mudanças de área: **{summary['mudancas_area']}**; de tipo de intenção: **{summary['mudancas_tipo_intencao']}**.
- Versões paralelas corrigidas: **{len(file_changed)}** lotes.

## O que foi feito
Cada uma das 2.557 entradas P1 foi submetida a regras contextuais individuais, com marcação de regra, justificativa, antes/depois e preservação de ambiguidades. A decisão foi **automatizada e conservadora**, não equivale à leitura humana independente de todos os termos. Casos sem evidência inequívoca continuam para validação. Essa revisão não autoriza alteração automática em famílias não incluídas em P1.

## Integridade dos dados
- **{sum(x['controles'] for x in reg_checks)} controles** comparados nos {len(file_changed)} lotes com patch; 73 por lote, **0 controles alterados**.
- **16 colunas originais (incluindo Ads), IDs e keywords mantidos** em todos os registros.
- P0/P2/P3 da fila original: idênticos antes/depois, a salvo de recalcular prioridades indevidamente.
- Conversões monetárias/físicas com direção apenas quando origem, destino e preposição tornam inequívoca a relação. Nenhuma conversão direta final pode omitir metadados.
- Arquivos reabertos e comparados; linhas fora do conjunto P1 não foram alteradas.

## Próxima validação necessária
1. Conferir amostra estratificada de regras e exceções, sobretudo câmbio (`peso` sem país), semanas/mês e `gramas em ml` sem ingrediente.
2. Resolver **{len(pending)} pendências** por contexto/produto, sem transformá-las em verdades por regra.
3. Só depois aprovar rótulos como referência para revisão P2. Não inventar demanda multiplicando volumes das variantes de Ads.

## Entregáveis
- `revisao-automatizada-2557-p1.csv`, uma decisão/justificativa por entrada;
- `patches-objetivos-p1.csv`, mudanças pontuais, antes/depois JSON;
- `p1-pendencias-validacao.csv`, itens ainda abertos;
- `fila-priorizada-30-lotes-com-p0-p1.csv`, fila com versões P0 e P1 preservadas;
- `lotes/lote-NNN-revisado-p0-p1-v1.1-barras-v2.csv`, versões paralelas dos lotes modificados;
- `qa-regressao-p1-por-lote.csv` e script reexecutável, dependência Python padrão.
''',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
