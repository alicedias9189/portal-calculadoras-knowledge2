#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Finalizador semântico v1.15 — complemento ao v1.14, validado no lote 025.

Novidades:
- MOBI/Kindle entra no reconhecimento de conversões PDF↔ebook; par nu `pdf mobi`
  fica ambíguo/revisão;
- `intervalos numéricos ... pdf` e `equação linear ... pdf` são conteúdo matemático,
  não conversão de arquivo;
- busca genérica pela marca Smallpdf sem operação/destino é navegacional;
- preço/valor de gasolina por km é custo de viagem;
- flexão `transforma pdf` é ação genérica de conversão PDF;
- `power point em pdf` é conversão PowerPoint→PDF.
"""
import argparse,csv,re,subprocess,sys,unicodedata
from collections import Counter
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--lote',type=int,required=True);ap.add_argument('--controle-anterior',type=int,default=None);ap.add_argument('--root',default='.');ap.add_argument('--skip-anterior',action='store_true');a=ap.parse_args()
LOT=a.lote;PREV=a.controle_anterior or LOT-1;ROOT=Path(a.root).resolve()
def rd(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def wr(p,rows,fields):
    with p.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=fields,delimiter=';',extrasaction='ignore');w.writeheader();w.writerows(rows)
def n(s):
    s=unicodedata.normalize('NFKD',(s or '').casefold());s=''.join(c for c in s if not unicodedata.combining(c));return re.sub(r'\s+',' ',s).strip()
def setrow(r,a,c,s,typ,dom,conf='alta',rev='não',why=''):
    r.update(area_principal=a,cluster=c,subcluster=s,intencao_principal=('Converter arquivo/mídia: '+s if typ=='conversão de arquivo/mídia' else 'Consultar informação: '+s if typ=='informacional' else 'Estimar custo: '+s if typ=='estimativa de custo' else 'Revisar intenção: '+s),tipo_intencao=typ,dominio_ou_grandeza=dom,unidade_origem='',unidade_destino='',direcao_conversao='',confianca=conf,revisao_manual=rev,justificativa_curta=why)
if not a.skip_anterior:subprocess.run([sys.executable,str(ROOT/'finalizar_auditar_lote_v1_14.py'),'--lote',str(LOT),'--controle-anterior',str(PREV),'--root',str(ROOT)],check=True)
cp=ROOT/f'lote-{LOT:03d}-classificado-v1.1-barras-v2.csv';fp=ROOT/f'auditoria-pos-classificacao-lote-{LOT:03d}-v1.1-barras-v2-final-flags.csv';rp=ROOT/f'relatorio-classificacao-lote-{LOT:03d}-v1.1-barras-v2.md';apath=ROOT/f'auditoria-pos-classificacao-lote-{LOT:03d}-v1.1-barras-v2-final.md'
rows=rd(cp); mobi=set(); mathc=set(); brand=set(); fuel=set(); verb=set(); ppt=set()
for r in rows:
    if r.get('tipo_registro')!='base':continue
    t=n(r['Keyword'])
    if 'pdf' in t and 'mobi' in t:
        directional=bool(re.search(r'\bpdf\b\s+(?:em|para|to)\s+\bmobi\b',t) or re.search(r'\bmobi\b\s+(?:em|para|to)\s+\bpdf\b',t) or re.search(r'\b(converter|transformar|passar)\b',t))
        if directional:setrow(r,'Conversores','Arquivos e documentos','Documentos e PDF','conversão de arquivo/mídia','formato de ebook/PDF','alta','não','PDF e MOBI com direção/verbo indicam conversão de arquivo.')
        else:setrow(r,'Conversores','Arquivos e documentos','Documentos e PDF','ambígua/revisão','par de formatos PDF/MOBI','média','sim','Par nu PDF/MOBI não informa direção da conversão.')
        mobi.add(r['id_global'])
    if re.search(r'\bintervalos? numericos?\b',t) and 'pdf' in t:
        setrow(r,'Matemática','Números e operações','Aritmética e operações básicas','informacional','intervalos numéricos','alta','não','PDF é formato de referência; a intenção é conteúdo matemático sobre intervalos numéricos.');mathc.add(r['id_global'])
    if re.search(r'\bequacao linear\b',t):
        setrow(r,'Matemática','Álgebra','Equações e expressões','informacional','equação linear','alta','não','Equação linear é conteúdo de Álgebra; PDF é apenas formato/referência quando presente.');mathc.add(r['id_global'])
    if re.search(r'\bsmall\s*pdf\b',t) and not re.search(r'\b(para|em|to|converter|conversor|transformar|word|excel|jpg|jpeg|png|ppt|powerpoint|mobi|dwg|dxf)\b',t.replace('small pdf','').replace('smallpdf','')):
        setrow(r,'Fora de escopo','Conteúdo técnico/produto','Consulta técnica não conversível','navegacional/transacional','serviço externo Smallpdf','alta','não','Busca genérica pela marca Smallpdf sem operação/formato-alvo é navegacional.');brand.add(r['id_global'])
    if re.search(r'\b(gasolina|diesel|etanol|combustivel)\b',t) and re.search(r'\b(preco|valor|gasto|custo)\b',t) and re.search(r'\b(km|quilometro|quilometros)\b',t):
        setrow(r,'Energia','Combustíveis','Custo de viagem','estimativa de custo','custo de combustível por distância','alta','não','Preço/valor de combustível por km é custo de viagem, não preço de mercado nem autonomia.');fuel.add(r['id_global'])
    if re.search(r'\btransforma\s+pdf\b',t):
        setrow(r,'Conversores','Arquivos e documentos','Documentos e PDF','conversão de arquivo/mídia','conversão genérica de PDF','média','não','Flexão "transforma PDF" expressa ação de transformação/conversão, embora o destino não esteja explícito.');verb.add(r['id_global'])
    if re.search(r'\bpower\s*point\b\s+(?:em|para|to)\s+\bpdf\b',t):
        setrow(r,'Conversores','Arquivos e documentos','Documentos e PDF','conversão de arquivo/mídia','PowerPoint/PDF','alta','não','PowerPoint em PDF é conversão explícita de formato.');r['unidade_origem']='PowerPoint';r['unidade_destino']='PDF';r['direcao_conversao']='PowerPoint→PDF';ppt.add(r['id_global'])
wr(cp,rows,list(rows[0].keys()))
patched=mobi|mathc|brand|fuel|verb|ppt;flags=rd(fp);kept=[];removed=0
for f in flags:
    if f.get('id_global') in patched and f.get('issue_code') in {'PDF_CONTENT','FUEL_MARKET'}:removed+=1
    else:kept.append(f)
wr(fp,kept,['severity','issue_code','id_global','Keyword','label','tipo_intencao','reason'])
lot=rd(ROOT/f'lote-{LOT:03d}.csv');base=[r for r in rows if r['tipo_registro']=='base'];ctr=[r for r in rows if r['tipo_registro']=='controle'];orig=list(lot[0].keys());orig_ok=all(all(x[k]==y[k] for k in orig) for x,y in zip(lot,rows));blank=sum(1 for r in base if not r['area_principal'] or not r['cluster'] or not r['subcluster']);dm=sum(1 for r in base if r['tipo_intencao']=='conversão direta' and (not r['unidade_origem'] or not r['unidade_destino'] or not r['direcao_conversao']))
prev=rd(ROOT/f'lote-{PREV:03d}-classificado-v1.1-barras-v2.csv');pc={r['controle_id']:r for r in prev if r['tipo_registro']=='controle'};fields=list(rows[0].keys());sem=[k for k in fields if k not in orig];ce=sum(1 for r in ctr if r['controle_id'] in pc and all(r.get(f,'')==pc[r['controle_id']].get(f,'') for f in sem));g=rd(ROOT/f'lote-{LOT:03d}-golden-qa-v1.1.csv');ge=sum(r.get('match_exato')=='sim' for r in g);conf=Counter(r['confianca'] for r in base);rev=Counter(r['revisao_manual'] for r in base);bars=sum(bool(r.get('keyword_interpretada')) for r in base);status='APROVADO' if not kept and dm==0 and blank==0 and orig_ok and ce==73 and ge==107 else 'REVISAR'
rp.write_text(f'# Relatório de classificação — Lote {LOT:03d}\n\n- Keywords base: **{len(base):,}**\n- Controles: **{len(ctr)}**\n- IDs base únicos: **{len({r["id_global"] for r in base}):,}**\n- Reconstruções de `/`: **{bars}**\n- Golden Set v1.1: **{ge}/107**\n- Controles: **{ce}/73**\n- Conversões diretas sem metadados: **{dm}**\n- Flags finais: **{len(kept)}**\n\n## Confiança\n- alta: **{conf["alta"]:,}**\n- média: **{conf["média"]:,}**\n- baixa: **{conf["baixa"]:,}**\n- revisão manual: **{rev["sim"]:,}**\n\n## v1.15\n- PDF/MOBI: **{len(mobi)}**\n- conteúdo matemático em PDF: **{len(mathc)}**\n- Smallpdf navegacional: **{len(brand)}**\n- combustível por km: **{len(fuel)}**\n- transforma PDF: **{len(verb)}**\n- PowerPoint→PDF: **{len(ppt)}**\n',encoding='utf-8')
apath.write_text(f'# Auditoria pós-classificação — Lote {LOT:03d}\n\n## Veredito\n**{status}.**\n\n- Base: **{len(base):,}**\n- Controles: **{len(ctr)}**\n- IDs únicos: **{len({r["id_global"] for r in base}):,}**\n- Colunas originais preservadas: **{"sim" if orig_ok else "não"}**\n- Área/cluster/subcluster vazios: **{blank}**\n- Golden Set: **{ge}/107**\n- Controles incorporados: **{ce}/73**\n- Reconstruções `/`: **{bars}**\n- Conversões diretas sem metadados: **{dm}**\n- Flags finais: **{len(kept)}**\n- Lote {LOT+1:03d}: **{"liberado" if status=="APROVADO" else "não liberado"}**\n',encoding='utf-8')
print({'status':status,'mobi':len(mobi),'math_pdf':len(mathc),'smallpdf_nav':len(brand),'fuel_per_km':len(fuel),'transforma_pdf':len(verb),'ppt_pdf':len(ppt),'flags':len(kept),'gold':ge,'controls_exact':ce,'confidence':dict(conf),'review':dict(rev),'base':len(base),'bars':bars})
