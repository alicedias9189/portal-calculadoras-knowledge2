#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P2 v4: revisão contextual conservadora por padrões/famílias e QA 30 lotes.
Entradas imutáveis: ZIP de lotes v3 + ZIP de auditoria v3. Saída paralela v4.
Somente biblioteca padrão. --preview apresenta regras/alertas sem gravar nada.
"""
import argparse, csv, hashlib, io, json, re, unicodedata, zipfile
from collections import Counter, defaultdict
from pathlib import Path

SAFE_FIELDS=['tipo_registro','id_global','lote_id','familia_id','controle_id','Keyword','ocorrencias_origem','areas_origem','qtd_areas','Avg. monthly searches','Mudança em três meses','Mudança YoY','Competition','Competition (indexed value)','Top of page bid (low range)','Top of page bid (high range)','keyword_interpretada','reconstrucao_barra_status','tipos_reconstrucao_barra','confianca_reconstrucao_barra','observacao_reconstrucao_barra']
EDIT_FIELDS=['area_principal','cluster','subcluster','tipo_intencao','intencao_principal','confianca','revisao_manual','justificativa_curta','unidade_origem','unidade_destino','direcao_conversao']
ADD_FIELDS=['regra_p2_v4','status_p2_v4','justificativa_p2_v4','area_final_p2_v4','cluster_final_p2_v4','subcluster_final_p2_v4','tipo_intencao_final_p2_v4','unidade_origem_final_p2_v4','unidade_destino_final_p2_v4','classificacao_alterada_p2_v4']


def norm(s):
    s=''.join(c for c in unicodedata.normalize('NFKD',(s or '').casefold()) if not unicodedata.combining(c))
    return re.sub(r'\s+',' ',s).strip()
def hit(s,regex):return re.search(regex,s) is not None

def decided(rule, area, cluster, sub, intent, reason, status='ALTA', src='', dst=''):
    return {'regra':rule,'area':area,'cluster':cluster,'sub':sub,'intent':intent,'reason':reason,'status':status,'src':src,'dst':dst}

# Aliases longos primeiro e limites de tokens; unidades dimensionais com preposições explícitas.
UNIT_ALIASES={
    'milimetros':'mm','milimetro':'mm','mm':'mm','centimetros':'cm','centimetro':'cm','cm':'cm','quilometros':'km','quilometro':'km','kms':'km','km':'km','metros':'m','metro':'m','m':'m',
    'micrometros':'um','micrometro':'um','nanometros':'nm','nanometro':'nm','polegadas':'in','polegada':'in','inches':'in','inch':'in','pulgadas':'in','pes':'ft','pe':'ft','feet':'ft','foot':'ft','ft':'ft','jardas':'yd','jarda':'yd','yards':'yd','yd':'yd','milhas':'mi','milha':'mi','miles':'mi',
    'miligramas':'mg','miligrama':'mg','mg':'mg','microgramas':'ug','micrograma':'ug','ug':'ug','quilogramas':'kg','quilograma':'kg','quilos':'kg','quilo':'kg','kg':'kg','gramas':'g','grama':'g','gr':'g','g':'g','toneladas':'t','tonelada':'t','ton':'t','libras':'lb','libra':'lb','lbs':'lb','lb':'lb','ounces':'oz','ounce':'oz','oncas':'oz','onca':'oz','oz':'oz','stone':'st',
    'mililitros':'ml','mililitro':'ml','ml':'ml','litros':'l','litro':'l','litres':'l','liter':'l','l':'l','galones':'gal','galoes':'gal','galao':'gal','gallons':'gal','gallon':'gal','gal':'gal','quarts':'qt','quart':'qt','quartos':'qt','quarto':'qt','pints':'pt','pint':'pt',
    'megahertz':'mhz','mhz':'mhz','gigahertz':'ghz','ghz':'ghz','quilohertz':'khz','kilohertz':'khz','khz':'khz','hertz':'hz','hz':'hz','terahertz':'thz','thz':'thz',
    'microamperes':'ua','microampere':'ua','ua':'ua','miliamperes':'ma','miliampere':'ma','ma':'ma','amperes':'a','ampere':'a','amps':'a',
    'milivolts':'mv','milivolt':'mv','mv':'mv','quilovolts':'kv','quilovolt':'kv','kv':'kv','volts':'v','volt':'v','v':'v',
    'kilowatts':'kw','quilowatts':'kw','quilowatt':'kw','kw':'kw','megawatts':'mw','megawatt':'mw','mw':'mw','gigawatts':'gw','gigawatt':'gw','gw':'gw','watts':'w','watt':'w','w':'w',
    'terabytes':'tb','terabyte':'tb','tb':'tb','gigabytes':'gb','gigabyte':'gb','gb':'gb','megabytes':'mb','megabyte':'mb','mb':'mb','kilobytes':'kb','kilobyte':'kb','quilobytes':'kb','kb':'kb','bytes':'byte','byte':'byte',
    'psi':'psi','bars':'bar','bar':'bar','pascals':'pa','pascal':'pa','pa':'pa','kilopascals':'kpa','quilopascal':'kpa','kpa':'kpa','atm':'atm',
    'fahrenheit':'f','celsius':'c','kelvin':'k','rankine':'r',
    'joules':'j','joule':'j','j':'j','quilojoules':'kj','kj':'kj','eletronvolts':'ev','eletronvolt':'ev','ev':'ev','quilowatts hora':'kwh','kilowatt hora':'kwh','kwh':'kwh',
    'hectares':'ha','hectare':'ha','ha':'ha','acres':'acre','acre':'acre', 'm2':'m2','cm2':'cm2','mm2':'mm2','km2':'km2','ft2':'ft2','m3':'m3','cm3':'cm3',
    'minutos':'min','minuto':'min','min':'min','segundos':'s','segundo':'s','seg':'s','s':'s','horas':'h','hora':'h','h':'h','dias':'dia','dia':'dia','semanas':'semana','semana':'semana',
}
DIMENSIONS={
'comprimento':set('nm um mm cm m km in ft yd mi'.split()),
'massa':set('ug mg g kg t lb oz st'.split()),
'volume':set('ml l gal qt pt m3 cm3'.split()),
'frequencia':set('hz khz mhz ghz thz'.split()),
'corrente':set('ua ma a'.split()),
'voltagem':set('mv v kv'.split()),
'potencia':set('w kw mw gw'.split()),
'dados digitais':set('byte kb mb gb tb'.split()),
'pressao':set('pa kpa bar psi atm'.split()),
'temperatura':set('c f k r'.split()),
'energia':set('j kj ev kwh'.split()),
'area':set('mm2 cm2 m2 km2 ha acre ft2'.split()),
'tempo':set('s min h dia semana'.split()),
}
UNIT_PARTS=sorted(UNIT_ALIASES,key=len,reverse=True)
UNIT_REGEX='(?:'+'|'.join(re.escape(x) for x in UNIT_PARTS)+')'
CURRENCY={'euros':'EUR','euro':'EUR','eur':'EUR','dolares':'USD','dolar':'USD','usd':'USD','reais':'BRL','real':'BRL','brl':'BRL','francos suicos':'CHF','franco suico':'CHF','chf':'CHF','wones':'KRW','won':'KRW','krw':'KRW','iene':'JPY','ienes':'JPY','jpy':'JPY','bolivares':'VES','bolivar':'VES'}
CURRENCY_RE='(?:'+'|'.join(re.escape(x) for x in sorted(CURRENCY,key=len,reverse=True))+')'

def decide(keyword):
    t=norm(keyword).replace('²','2').replace('³','3')
    # Famílias sem sinal seguro: não adivinhar gravidez, temperatura alvo ou finalidade do aparelho.
    if hit(t,r'^\d{1,2}\s*semanas?\s+e\s+\d\s*dias?$'):return None
    if hit(t,r'^\d+\s*(?:v|a)\s+\d+\s*(?:v|a)$'):return None
    if hit(t,r'\b(?:compra|venda|loj[ao]|preco|produto|promo[cç]ao)\b') and not hit(t,r'\b(?:converter|calculadora|calcular)\b'):return None
    # Arquivos: exigir dois formatos e preposição; não interpretar PDF de exercícios como arquivo a converter.
    if not hit(t,r'\b(?:exercicios?|apostila|atividade|questoes?)\b'):
        fm=re.search(r'\b(pdf|jpg|jpeg|png|bmp|gif|webp|doc|docx|xls|xlsx|csv|mp3|mp4|wav|avi|mov|webm|txt)\s+(?:para|em|to)\s+(pdf|jpg|jpeg|png|bmp|gif|webp|doc|docx|xls|xlsx|csv|mp3|mp4|wav|avi|mov|webm|txt)\b',t)
        if fm and fm.group(1)!=fm.group(2):
            return decided('arquivo_formatos_explicitos','Conversores','Arquivos e documentos','Conversão de formatos','conversão de arquivo/mídia','Dois formatos e sentido de conversão explícitos.',src=fm.group(1).upper(),dst=fm.group(2).upper())
    # Cotação e rendimento são questões financeiras; não converter moeda em rendimento.
    if hit(t,r'\b(?:quanto\s+(?:que\s+)?rende|rende\s+quanto|rendimento\s+de|quanto\s+renderia)\b') and hit(t,r'\b(?:nubank|caixinha|poupanca|cdi|cdb|investimento|fundo|fii|milhao|milhoes|reais|real|r\$|por mes|ao mes)\b'):
        return decided('simulacao_rendimento','Finanças','Investimentos','Simulação de rendimento','cálculo contextual','Rendimento requer prazo, taxa, tributos e produto; não presumir taxa.',status='RESSALVA')
    if hit(t,r'\b(?:quantos?\s+km\s+(?:faz|roda)|km\s+por\s+litro|litros?\s+de\s+gasolina\s+faz\s+quantos?|calcular\s+(?:consumo|gasto)\s+(?:de\s+)?(?:combustivel|gasolina))\b'):
        return decided('consumo_combustivel','Automóveis','Combustíveis','Consumo e autonomia','cálculo contextual','Consumo/autonomia exige distância, consumo médio, volume ou preço conforme consulta.',status='RESSALVA')
    if hit(t,r'\b(?:arredondar|arredondamento)\b') and not hit(t,r'\b(?:excel|formula|funcao|significa|definicao|o que e|como|quando|javascript|java|ceil|floor|typescript|python)\b'):
        return decided('calculadora_arredondar','Matemática','Arredondamento','Arredondamento de números','cálculo contextual','Arredondamento requer valor, casas decimais e modo.',status='RESSALVA')
    if hit(t,r'\b(?:fatorar|fatoracao)\b') and hit(t,r'\b(?:expressoes?|polinomios?|equacoes?|online|algebric[ao]s?)\b') and not hit(t,r'\b(?:como fazer|passo a passo|definicao|formula|exercicio|o que e)\b'):
        return decided('fatoracao_algebrica','Matemática','Álgebra','Fatoração algébrica','cálculo contextual','Fatoração exige expressão algébrica fornecida pelo usuário.',status='RESSALVA')
    if hit(t,r'\b(?:calculadora\s+(?:de\s+)?(?:segundos?\s+e\s+minutos?|horas?\s+e\s+minutos?|data\s+e\s+hora)|somador\s+de\s+horas?|subtra[cç]ao\s+de\s+horas?|subtrair\s+minutos|contador\s+datas)\b') and not hit(t,r'\b(?:diferenca\s+ao|como|significa)\b'):
        return decided('calculadora_intervalos_tempo','Datas','Cálculos de tempo','Somar e subtrair intervalos','cálculo contextual','Operação de tempo reconhecível; solicitar durações/datas.',status='RESSALVA')
    if hit(t,r'\b(?:ano\s+bissexto|anos\s+bissextos|anos\s+bisiestos|como\s+saber\s+se\s+o\s+ano\s+e\s+bissexto)\b'):
        intent='informacional' if hit(t,r'\b(?:como saber|o que|significa)\b') else 'cálculo contextual'
        return decided('ano_bissexto','Datas','Calendário','Ano bissexto',intent,'Ano bissexto é informação/cálculo de calendário, não conversão de unidades.',status='RESSALVA' if intent!='informacional' else 'ALTA')
    if hit(t,r'\b(?:calculadora\s+(?:de\s+)?(?:metros?\s+quadrados?|volume\s+(?:do\s+)?cilindro|litros?|telhado)|calcular\s+(?:a\s+)?area\s+em\s+metros?\s+quadrados?)\b') and not hit(t,r'^como\s+calcular'):
        return decided('calculadora_area_volume','Construção','Medidas e geometria','Área e volume','cálculo contextual','Cálculo geométrico necessita dimensões, sem criar equivalência linear/área.',status='RESSALVA')
    if hit(t,r'\b(?:tijolos?)\b') and hit(t,r'\b(?:metros?\s+quadrados?|m2)\b') and hit(t,r'\b(?:quantos?|quantas?|faz|da|rendem?)\b'):
        return decided('tijolos_por_area','Construção','Materiais','Rendimento de tijolos','cálculo contextual','Área coberta depende do tamanho dos tijolos, junta e desperdício.',status='RESSALVA')
    # Moedas: moeda origem/destino identificáveis pela preposição, inclusive quantidades coladas.
    cpat=re.search(r'(?<![a-z])(?:\d+(?:[.,]\d+)?\s*)?('+CURRENCY_RE+r')\s+(?:em|para)\s+('+CURRENCY_RE+r')\b',t)
    if cpat:
        src,dst=CURRENCY[cpat.group(1)],CURRENCY[cpat.group(2)]
        if src!=dst and src!='VES':
            return decided('moedas_par_explicito','Conversores','Moedas e câmbio','Conversão de moedas','conversão direta','Par e direção monetária explícitos; cotação é variável no tempo.',status='RESSALVA',src=src,dst=dst)
    # cotação de libra, franca ou euro: não presumir segundo par
    if hit(t,r'\b(?:cotacao|quanto\s+vale|preco|valor)\b') and hit(t,r'\b(?:franco\s+suico|libra\s+esterlina|dolar|euro|won|iene|francos?\s+suicos?)\b') and not hit(t,r'\b(?:rendimento|investimento|moeda antiga|moeda rara|colecion)\b'):
        return decided('cotacao_moeda_sem_par','Finanças','Câmbio','Cotação e valor atual','informacional','Consulta de cotação sem direção/par/instante definidos; exigir moeda de referência.',status='RESSALVA')
    # Grandezas físicas: regex com duas unidades e conector para/em/to, dimensões iguais.
    pat=r'(?<![a-z0-9])(?:\d+(?:[.,]\d+)?\s*)?('+UNIT_REGEX+r')\s+(?:para|em|to)\s+('+UNIT_REGEX+r')(?![a-z0-9])'
    match=re.search(pat,t)
    if match and not hit(t,r'\b(?:formula|como\s+transformar|como\s+converter|quartos|quarto|quarts?|galao|galoes|galon|gal|pints?|tabela|n\s+m\s+(?:para|em)\s+ft\s+lb|stone\s+para\s+libra\s+esterlina)\b'):
        x,y=UNIT_ALIASES[match.group(1)],UNIT_ALIASES[match.group(2)]
        # BARRAS REMOVIDAS: no speed '100 milhas em km h' equivale unidade comprimento vs velocidade.
        if x!=y:
            common=[d for d,units in DIMENSIONS.items() if x in units and y in units]
            if len(common)==1 and not hit(t,r'\b(?:por\s+(?:hora|segundo)|preco|cust[ao]|quantos?\s+reais|per\s+hour|km\s+h|m\s+s|r\$)\b'):
                dim=common[0]
                if {x,y}=={'g','ml'} or {x,y}=={'kg','l'}:return None
                area='Conversores';sub={'frequencia':'Frequência','corrente':'Corrente elétrica','voltagem':'Tensão elétrica','potencia':'Potência','dados digitais':'Dados digitais','pressao':'Pressão','temperatura':'Temperatura','comprimento':'Comprimento e distância','massa':'Massa e peso','volume':'Volume','energia':'Energia','area':'Área e superfície','tempo':'Tempo'}[dim]
                return decided('unidades_mesma_dimensao','Conversores',sub,sub,'conversão direta','Unidades da mesma dimensão e direção explícita.',src=x,dst=y)
    return None

def readcsv(z,n):
    return list(csv.DictReader(io.TextIOWrapper(z.open(n),encoding='utf-8-sig',newline=''),delimiter=';'))
def writecsv(z,name,rows,fields):
    with z.open(name,'w',force_zip64=True) as binary:
        s=io.TextIOWrapper(binary,encoding='utf-8-sig',newline='')
        w=csv.DictWriter(s,fieldnames=fields,delimiter=';',extrasaction='ignore');w.writeheader();w.writerows(rows);s.flush();s.detach()
def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for part in iter(lambda:f.read(1<<20),b''):h.update(part)
    return h.hexdigest()

def main():
    p=argparse.ArgumentParser();p.add_argument('--raiz',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--saida',type=Path,default=None);p.add_argument('--preview',action='store_true');args=p.parse_args()
    root=args.raiz; outdir=args.saida or root/'saida-p2-v4'
    az=zipfile.ZipFile(root/'08-Entregas/P2-v3/auditoria-p2-v3-csv-integral.zip')
    bz=zipfile.ZipFile(root/'08-Entregas/P2-v3/lotes-001-a-030-p0-p1-p2-v3.zip')
    pending=readcsv(az,'p2-v3-pendencias-remanescentes.csv')
    assert len(pending)==5946,len(pending)
    selected={};cc=Counter();eg=defaultdict(list);families=defaultdict(list)
    for row in pending:
        d=decide(row['Keyword']); families[row['familia_id']].append(row)
        if d:
            selected[row['id_global']]=d; cc[d['regra']]+=1
            if len(eg[d['regra']])<15:eg[d['regra']].append(row['Keyword'])
    print('REGRAS',cc,'TOTAL',len(selected),flush=True)
    for k,v in eg.items(): print(k,len(v), ' | '.join(v[:10]),flush=True)
    if args.preview:return
    outdir.mkdir(parents=True,exist_ok=True)
    prior=readcsv(az,'p2-v3-decisoes-25050.csv'); queue=readcsv(az,'p2-v3-fila-geral.csv')
    assert len(prior)==25050 and len({x['id_global'] for x in prior})==25050
    assert len({x['id_global'] for x in queue})==len(queue)
    assert set(selected).issubset({x['id_global'] for x in pending})
    pmap={};patches=[];decision=[];remaining=[];changed_families=Counter();pending_ids={x['id_global'] for x in pending}
    def replacement(d):
        return dict(area_principal=d['area'],cluster=d['cluster'],subcluster=d['sub'],tipo_intencao=d['intent'],intencao_principal=d['intent'],confianca='alta' if d['status']=='ALTA' else 'média',revisao_manual='não' if d['status']=='ALTA' else 'sim',justificativa_curta=f"P2-v4 {d['regra']}: {d['reason']}",unidade_origem=d['src'],unidade_destino=d['dst'],direcao_conversao=d['src']+'->'+d['dst'] if d['src'] and d['dst'] else '')
    for row in prior:
        row=dict(row);key=row['id_global'];d=selected.get(key)
        if d:
            changes=replacement(d)
            patches.append({'id_global':key,'lote':row['lote'],'familia_id':row['familia_id'],'Keyword':row['Keyword'],'regra':d['regra'],'status':'RESOLVIDO' if d['status']=='ALTA' else 'COM_RESSALVA','antes':json.dumps({k:row.get(k,'') for k in EDIT_FIELDS},ensure_ascii=False),'depois':json.dumps(changes,ensure_ascii=False),'justificativa':d['reason']})
            changed_families[row['familia_id']]+=1
        row.update({'regra_p2_v4':d['regra'] if d else '', 'status_p2_v4':('RESOLVIDO' if d['status']=='ALTA' else 'COM_RESSALVA') if d else ('PENDENTE_CONTEXTUAL' if row['id_global'] in pending_ids else 'MANTIDO_P2_V3'), 'justificativa_p2_v4':d['reason'] if d else '', 'area_final_p2_v4':d['area'] if d else row['area_final_p2_v3'], 'cluster_final_p2_v4':d['cluster'] if d else row['cluster_final_p2_v3'], 'subcluster_final_p2_v4':d['sub'] if d else row['subcluster_final_p2_v3'], 'tipo_intencao_final_p2_v4':d['intent'] if d else row['tipo_intencao_final_p2_v3'], 'unidade_origem_final_p2_v4':d['src'] if d else row['unidade_origem_final_p2_v3'], 'unidade_destino_final_p2_v4':d['dst'] if d else row['unidade_destino_final_p2_v3'], 'classificacao_alterada_p2_v4':'sim' if d else 'não'})
        decision.append(row);pmap[key]=row
    # pending remains from the same rows, with new metadata
    remaining=[pmap[x['id_global']] for x in pending if x['id_global'] not in selected]
    # Family-level report contains aggregate and isolated exceptions (never propagates decisions automatically).
    family_report=[]
    for fam,rows in families.items():
        n=sum(x['id_global'] in selected for x in rows)
        rules=Counter(selected[x['id_global']]['regra'] for x in rows if x['id_global'] in selected)
        rest=[x['Keyword'] for x in rows if x['id_global'] not in selected]
        family_report.append({'familia_id':fam,'pendentes_v3':len(rows),'classificados_v4':n,'ainda_abertos':len(rows)-n,'regras':', '.join(f'{k}:{v}' for k,v in rules.most_common()),'amostras_abertas':' | '.join(rest[:5]),'revisao_por_familia':'análise individual da keyword; variantes não herdaram decisão automaticamente'})
    family_report.sort(key=lambda x:(-int(x['ainda_abertos']),-int(x['pendentes_v3']),x['familia_id']))
    changed=0;nbase=nctl=0;qa=[];allids=set()
    zpath=outdir/'lotes-001-a-030-p0-p1-p2-v4.zip'
    with zipfile.ZipFile(zpath,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as out:
        for path in sorted(bz.namelist()):
            if not path.endswith('.csv'):continue
            rows=readcsv(bz,path);fields=list(rows[0]);lotebase=lotectl=lotemod=0
            for row in rows:
                before=dict(row)
                if row['tipo_registro']=='controle':lotectl+=1
                elif row['tipo_registro']=='base':
                    lotebase+=1;key=row['id_global'];assert key not in allids;allids.add(key)
                    d=selected.get(key)
                    if d:
                        row.update(replacement(d));lotemod+=1
                assert all(row.get(k,'')==before.get(k,'') for k in SAFE_FIELDS)
                assert row==before if row['tipo_registro']!='base' or row['id_global'] not in selected else all(row.get(k)==before.get(k) for k in fields if k not in EDIT_FIELDS)
            changed+=lotemod;nbase+=lotebase;nctl+=lotectl
            outpath=path.replace('-v3.csv','-v4.csv')
            writecsv(out,outpath,rows,fields)
            qa.append({'lote':path.split('/')[-1][:8],'registros_base':lotebase,'controles':lotectl,'alteracoes_p2_v4':lotemod,'campos_protegidos':'PASSOU','nao_alvos_intactos':'PASSOU'})
    assert len(qa)==30 and nbase==294905 and nctl==2190 and changed==len(selected),(len(qa),nbase,nctl,changed,len(selected))
    qfields=list(queue[0])+ADD_FIELDS
    for r in queue:
        d=selected.get(r['id_global'])
        if d:r.update({k:v for k,v in replacement(d).items() if k in r})
        r.update({k:pmap.get(r['id_global'],{}).get(k,'') for k in ADD_FIELDS})
    zz=outdir/'auditoria-p2-v4-csv-integral.zip'
    with zipfile.ZipFile(zz,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as out:
        writecsv(out,'p2-v4-decisoes-25050.csv',decision,list(decision[0]))
        writecsv(out,'p2-v4-pendencias-restantes.csv',remaining,list(decision[0]))
        writecsv(out,'p2-v4-patches.csv',patches,list(patches[0]) if patches else ['id_global'])
        writecsv(out,'p2-v4-fila-geral.csv',queue,qfields)
        writecsv(out,'p2-v4-qa-regressao-30-lotes.csv',qa,list(qa[0]))
        writecsv(out,'p2-v4-familias-analisadas.csv',family_report,list(family_report[0]))
    summary={'universo_p2':25050,'pendencias_entrada_v3':len(pending),'reclassificadas':len(selected),'sem_ressalva':sum(d['status']=='ALTA' for d in selected.values()),'com_ressalva':sum(d['status']=='RESSALVA' for d in selected.values()),'pendencias_restantes':len(remaining),'familias_totais_com_pendencias':len(families),'familias_com_correcao':len(changed_families),'registros_base':nbase,'controles':nctl,'lotes':len(qa),'regras':dict(cc),'sha256_lotes':sha(zpath),'sha256_auditoria':sha(zz),'exemplos':{k:v[:5] for k,v in eg.items()}}
    (outdir/'resumo-p2-v4.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('RESUMO',json.dumps({k:v for k,v in summary.items() if k not in ('exemplos','regras')},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
