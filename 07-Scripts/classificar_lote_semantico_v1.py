import csv, re, unicodedata, math, os, json
from pathlib import Path
from collections import Counter, defaultdict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion
from sklearn.svm import LinearSVC

import argparse

parser=argparse.ArgumentParser(description='Classifica semanticamente um lote usando lotes aprovados anteriores como treino.')
parser.add_argument('--lote', type=int, required=True, help='Número do lote, ex.: 4')
parser.add_argument('--treino', default='', help='Lotes aprovados para treino, separados por vírgula. Padrão: lote anterior.')
parser.add_argument('--root', default='.', help='Pasta com os arquivos do projeto.')
args=parser.parse_args()
LOT=args.lote
TRAIN_LOTS=[int(x) for x in args.treino.split(',') if x.strip()] or [LOT-1]
ROOT=Path(args.root).resolve()

def read_csv(p):
    with open(p,'r',encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f,delimiter=';'))

def norm(s):
    s=unicodedata.normalize('NFKC',s or '').casefold()
    s=''.join(c for c in unicodedata.normalize('NFKD',s) if not unicodedata.combining(c))
    s=re.sub(r'\s+',' ',s).strip()
    return s

def text_row(r, bars=None):
    kw=(bars or {}).get(r.get('id_global',''),{}).get('keyword_interpretada') or r.get('keyword_interpretada') or r['Keyword']
    areas=' '.join('AREA_'+norm(x).replace(' ','_') for x in (r.get('areas_origem') or '').split('|') if x.strip())
    return norm(kw)+' '+areas

def label(r): return '|||'.join([r['area_principal'],r['cluster'],r['subcluster']])

train=[]
for train_no in TRAIN_LOTS:
    p=ROOT/f'lote-{train_no:03d}-classificado-v1.1-barras-v2.csv'
    train += [r for r in read_csv(p) if r['tipo_registro']=='base']
lot=read_csv(ROOT/f'lote-{LOT:03d}.csv')
base=[r for r in lot if r['tipo_registro']=='base']
ctrl=[r for r in lot if r['tipo_registro']=='controle']
barrows=read_csv(ROOT/'revisao_contextual_barras_v2/mapa-barras-mestre-v2.csv')
bars={r['id_global']:r for r in barrows if r['id_global'] in {x['id_global'] for x in base}}

# Explicit Golden anchors are included as supervised examples.
gold=read_csv(ROOT/'golden-set-v1.1.csv')
for g in gold:
    train.append({
        'id_global':'GOLD-'+g['id'],'Keyword':g['Keyword'],'areas_origem':g['areas_origem'],
        'keyword_interpretada':'','area_principal':g['area_esperada'],'cluster':g['cluster_esperado'],
        'subcluster':g['subcluster_esperado'],'tipo_intencao':g['intencao_esperada']
    })

Xtrain=[text_row(r) for r in train]
y=[label(r) for r in train]

features=FeatureUnion([
    ('char',TfidfVectorizer(analyzer='char_wb',ngram_range=(3,4),min_df=2,max_features=60000,sublinear_tf=True)),
    ('word',TfidfVectorizer(analyzer='word',ngram_range=(1,2),min_df=2,max_features=30000,sublinear_tf=True)),
])
A=features.fit_transform(Xtrain)
clf=LinearSVC(C=2.0,class_weight='balanced')
clf.fit(A,y)

X=[text_row(r,bars) for r in base]
B=features.transform(X)
pred=list(clf.predict(B))
dec=clf.decision_function(B)
part=np.partition(dec,-2,axis=1)
margin=part[:,-1]-part[:,-2]

# Intent conditioned on true/predicted label.
def lt(lab): return ' __LBL_'+re.sub(r'[^a-z0-9]+','_',norm(lab))
ity=[r['tipo_intencao'] for r in train]
Xit=[text_row(r)+lt(label(r)) for r in train]
if_features=FeatureUnion([
    ('char',TfidfVectorizer(analyzer='char_wb',ngram_range=(3,4),min_df=2,max_features=55000,sublinear_tf=True)),
    ('word',TfidfVectorizer(analyzer='word',ngram_range=(1,2),min_df=2,max_features=25000,sublinear_tf=True)),
])
IA=if_features.fit_transform(Xit)
iclf=LinearSVC(C=2.0,class_weight='balanced')
iclf.fit(IA,ity)
IX=[text_row(r,bars)+lt(p) for r,p in zip(base,pred)]
IB=if_features.transform(IX)
ipred=list(iclf.predict(IB))
idec=iclf.decision_function(IB)
ipart=np.partition(idec,-2,axis=1)
imargin=ipart[:,-1]-ipart[:,-2]

# exact Golden lookup, because Golden controls are drift anchors.
gold_lookup={norm(g['Keyword']):('|||'.join([g['area_esperada'],g['cluster_esperado'],g['subcluster_esperado']]),g['intencao_esperada']) for g in gold}
for i,r in enumerate(base):
    k=norm((bars.get(r['id_global']) or {}).get('keyword_interpretada') or r['Keyword'])
    if k in gold_lookup:
        pred[i],ipred[i]=gold_lookup[k]

# targeted context rules inherited from R01-R26.
def L(a,c,s):return '|||'.join([a,c,s])
for i,r in enumerate(base):
    kw=(bars.get(r['id_global']) or {}).get('keyword_interpretada') or r['Keyword']
    t=norm(kw)
    # Labor high-specificity
    if re.search(r'\b(rescisao|rescisorio|rescisoria|acerto trabalhista|demissao|demitid)\b',t):
        pred[i]=L('Trabalho','Rescisão','Rescisão trabalhista')
    if re.search(r'\b(ferias)\b',t) and not re.search(r'\b(viagem|hotel|turismo)\b',t):
        pred[i]=L('Trabalho','Férias','Férias e férias proporcionais')
    if re.search(r'\b(decimo terceiro|13 salario|13o salario|13º)\b',t):
        pred[i]=L('Trabalho','Décimo terceiro','Décimo terceiro salário')
    if re.search(r'\bfgts\b',t):
        pred[i]=L('Trabalho','FGTS','FGTS e multa rescisória')
    if re.search(r'\b(dsr|descanso semanal remunerado)\b',t):
        pred[i]=L('Trabalho','Jornada e adicionais','DSR')
    if re.search(r'\b(12x36|12/36|6x1|6/1|banco de horas|jornada|carga horaria|turno)\b',t) and re.search(r'\b(trabalho|trabalh|escala|jornada|turno|horas?)\b',t):
        pred[i]=L('Trabalho','Jornada e adicionais','Escalas e jornada')
    if re.search(r'\b(seguro desemprego|seguro-desemprego)\b',t):
        pred[i]=L('Trabalho','Benefícios e desligamento','Seguro-desemprego')
    if re.search(r'\b(pis|pasep)\b',t) and not re.search(r'\b(piso|pisos)\b',t):
        pred[i]=L('Trabalho','Benefícios e desligamento','PIS/PASEP')
    if re.search(r'\b(aposentadoria|dataprev|beneficio inss|beneficio do inss|auxilio doenca|auxilio-doenca)\b',t):
        pred[i]=L('Trabalho','Previdência e benefícios','Previdência e benefícios do INSS')
    # Savings/finance
    if re.search(r'\b(poupanca|caderneta)\b',t) and re.search(r'\b(rende|rendimento|rentabilidade|remuneracao|quanto rende)\b',t):
        pred[i]=L('Finanças','Investimentos','Poupança')
    if re.search(r'\b(cdb|cdi|lci|lca)\b',t):
        pred[i]=L('Finanças','Investimentos','CDB, CDI e renda fixa')
    # Currency quote vs conversion
    currency=bool(re.search(r'\b(dolar|euro|libra|iene|yuan|peso|franco|real|reais|usd|eur|gbp)\b',t))
    quote=bool(re.search(r'\b(hoje|hj|cotacao|valor atual|agora|tempo real|variacao|historico)\b',t))
    conv=bool(re.search(r'\b(converter|conversor|transformar|trocar| para | em )\b',t))
    if currency and quote:
        pred[i]=L('Finanças','Câmbio','Cotação atual'); ipred[i]='cotação atual'
    elif currency and conv and not quote:
        if not re.search(r'\b(preco|salario|rendimento|investimento)\b',t):
            pred[i]=L('Conversores','Moedas e câmbio','Conversão entre moedas')
    # construction
    if re.search(r'\b(tijolo|bloco|telha|argamassa|reboco|concreto|cimento|brita|tinta|impermeabil|parede|fachada)\b',t):
        if re.search(r'\b(quant|m2|metro quadrado|calcular|calculadora|rendimento|cobertura|tra[cç]o)\b',t):
            if 'tijol' in t or 'bloco' in t: pred[i]=L('Construção','Alvenaria','Blocos e tijolos')
            elif 'telha' in t: pred[i]=L('Construção','Telhados','Telhados e coberturas')
            elif 'tinta' in t: pred[i]=L('Construção','Pintura','Tinta e pintura')
            elif 'impermeabil' in t: pred[i]=L('Construção','Impermeabilização','Impermeabilização e vedação')
            elif re.search(r'\b(concreto|cimento|brita)\b',t): pred[i]=L('Construção','Concreto','Concreto, cimento, areia e brita')
            elif re.search(r'\b(argamassa|reboco)\b',t): pred[i]=L('Construção','Argamassa e revestimento','Argamassa, reboco e assentamento')
    # solar/appliances/energy
    if re.search(r'\b(energia solar|fotovoltaic|painel solar|placa solar)\b',t):
        if re.search(r'\b(dimension|quantas placas|quantos paineis|calculo solar)\b',t): pred[i]=L('Energia','Energia solar','Dimensionamento solar')
        elif re.search(r'\b(custo|preco|valor|payback|economia|viabilidade)\b',t): pred[i]=L('Energia','Energia solar','Custo e viabilidade solar')
    if re.search(r'\b(microondas|air fryer|airfryer|chuveiro|geladeira|forno|cafeteira|secador|aspirador)\b',t) and re.search(r'\b(consum|gasta|kwh|quilowatt|potencia|watts?)\b',t):
        pred[i]=L('Energia','Aparelhos elétricos','Consumo de aparelhos')
    # Fuel market/news
    if re.search(r'\b(gasolina|etanol|diesel|petrobras|combustivel)\b',t) and re.search(r'\b(preco|valor|subiu|aument|hoje|semana)\b',t) and not re.search(r'\b(km|litros?|consumo|viagem)\b',t):
        pred[i]=L('Fora de escopo','Preço de mercado','Combustíveis/preço de mercado'); ipred[i]='consulta de preço/mercado'
    # PDF content vs conversion
    if 'pdf' in t and re.search(r'\b(converter|transformar|passar|para pdf|pdf para|juntar|colocar)\b',t):
        pred[i]=L('Conversores','Arquivos e documentos','Documentos e PDF'); ipred[i]='conversão de arquivo/mídia'
    # fractions/bar reconstructions
    if r['id_global'] in bars:
        bi=bars[r['id_global']]['keyword_interpretada']; bt=norm(bi)
        if re.search(r'\bpolegada',bt) and re.search(r'\bmm\b|milimet',bt): pred[i]=L('Conversores','Unidades físicas','Comprimento e distância'); ipred[i]='conversão direta'
        if re.search(r'\b(ferias|salario minimo)\b',bt) and re.search(r'\b1/3\b',bt): pred[i]=L('Trabalho','Férias','Férias e férias proporcionais')
        if re.search(r'\b(aposentadoria|regra de pontos)\b',bt) and '85/95' in bt: pred[i]=L('Trabalho','Previdência e benefícios','Previdência e benefícios do INSS')
        if re.search(r'\b\d+/\d+\b',bt) and 'porcentagem' in bt: pred[i]=L('Matemática','Números e operações','Frações e decimais'); ipred[i]='cálculo direto'

for i,r in enumerate(base):
    t=norm((bars.get(r['id_global']) or {}).get('keyword_interpretada') or r['Keyword'])
    a,c,s=pred[i].split('|||')
    if a=='Conversores' and re.search(r'\b(para| to | em )\b',t) and s not in ('Conversor genérico de unidades',):
        if s not in ('Documentos e PDF',): ipred[i]='conversão direta'
    if a=='Finanças' and c=='Câmbio': ipred[i]='cotação atual' if 'histor' not in t else 'cotação histórica'
    if a=='Trabalho':
        if re.search(r'\b(calcular|calculadora|calculo|simular|simulador|quanto vou|quanto da|quanto dá|valor da rescisao|valor rescisao)\b',t): ipred[i]='cálculo direto'
        elif re.search(r'\b(consultar|consulta|onde vejo|como saber|tem direito|quem tem direito|quando)\b',t): ipred[i]='informacional'
    if a=='Matemática' and re.search(r'\b(calcular|calculadora|quanto e|quanto é|resolva|achar)\b',t): ipred[i]='cálculo direto'
    if a=='Construção' and re.search(r'\b(quantas|quantos|quantidade|calcular|calculadora)\b',t): ipred[i]='estimativa de quantidade'
    if a=='Energia' and s=='Consumo de aparelhos': ipred[i]='estimativa de consumo'
    if a=='Energia' and s=='Dimensionamento solar': ipred[i]='dimensionamento' if 'pdf' not in t else 'informacional'
    if a=='Energia' and s=='Custo e viabilidade solar': ipred[i]='estimativa de custo'
    if a=='Fora de escopo' and c!='Preço de mercado': ipred[i]='fora de escopo'

out=[]
for i,r in enumerate(base):
    out.append({**r,'_label':pred[i],'_intent':ipred[i],'_label_margin':float(margin[i]),'_intent_margin':float(imargin[i]),'_text':((bars.get(r['id_global']) or {}).get('keyword_interpretada') or r['Keyword'])})
with open(ROOT/f'_lote-{LOT:03d}-stage-preds.csv','w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(out[0].keys()),delimiter=';');w.writeheader();w.writerows(out)
print('lote',LOT,'treinos',TRAIN_LOTS,'train',len(train),'base',len(base),'labels',len(set(y)),'bars',len(bars))
print('areas',Counter(x['_label'].split('|||')[0] for x in out))
print('intent',Counter(x['_intent'] for x in out))
print('low label margins',sum(x['_label_margin']<0.25 for x in out),'low intent',sum(x['_intent_margin']<0.15 for x in out))
