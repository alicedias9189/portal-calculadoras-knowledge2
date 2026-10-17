#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Finalizador semântico v1.16 — complemento ao v1.15, validado no lote 026.

Novidades:
- XPS passa a ser formato documental reconhecido em pares com PDF;
  direção explícita (`xps em pdf`) é conversão; par nu (`xps pdf`) fica ambíguo/revisão;
- buscas por material identificado de cálculo/teorema em PDF, sem operação de conversão,
  são conteúdo/documento informacional, não conversão de arquivo.
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
    prefix='Converter arquivo/mídia' if typ=='conversão de arquivo/mídia' else 'Revisar intenção' if typ=='ambígua/revisão' else 'Fora de escopo'
    r.update(area_principal=a,cluster=c,subcluster=s,intencao_principal=f'{prefix}: {s}',tipo_intencao=typ,dominio_ou_grandeza=dom,unidade_origem='',unidade_destino='',direcao_conversao='',confianca=conf,revisao_manual=rev,justificativa_curta=why)
if not a.skip_anterior:subprocess.run([sys.executable,str(ROOT/'finalizar_auditar_lote_v1_15.py'),'--lote',str(LOT),'--controle-anterior',str(PREV),'--root',str(ROOT)],check=True)
cp=ROOT/f'lote-{LOT:03d}-classificado-v1.1-barras-v2.csv';fp=ROOT/f'auditoria-pos-classificacao-lote-{LOT:03d}-v1.1-barras-v2-final-flags.csv';rp=ROOT/f'relatorio-classificacao-lote-{LOT:03d}-v1.1-barras-v2.md';apath=ROOT/f'auditoria-pos-classificacao-lote-{LOT:03d}-v1.1-barras-v2-final.md'
rows=rd(cp);xps=set();content=set()
for r in rows:
    if r.get('tipo_registro')!='base':continue
    t=n(r['Keyword'])
    if 'pdf' in t and re.search(r'\bxps\b',t):
        directional=bool(re.search(r'\bxps\b\s+(?:em|para|to)\s+\bpdf\b',t) or re.search(r'\bpdf\b\s+(?:em|para|to)\s+\bxps\b',t) or re.search(r'\b(converter|transformar|convert)\b',t))
        if directional:
            setrow(r,'Conversores','Arquivos e documentos','Documentos e PDF','conversão de arquivo/mídia','XPS/PDF','alta','não','XPS e PDF com direção/verbo indicam conversão documental.');
            if re.search(r'\bxps\b\s+(?:em|para|to)\s+\bpdf\b',t):r['unidade_origem']='XPS';r['unidade_destino']='PDF';r['direcao_conversao']='XPS→PDF'
            elif re.search(r'\bpdf\b\s+(?:em|para|to)\s+\bxps\b',t):r['unidade_origem']='PDF';r['unidade_destino']='XPS';r['direcao_conversao']='PDF→XPS'
        else:setrow(r,'Conversores','Arquivos e documentos','Documentos e PDF','ambígua/revisão','par de formatos XPS/PDF','média','sim','Par nu XPS/PDF não informa direção da conversão.')
        xps.add(r['id_global'])
    if 'pdf' in t and re.search(r'\b(teorema fundamental do calculo|calculo integral|calculo diferencial|aplicacoes do calculo)\b',t) and not re.search(r'\b(converter|transformar|para pdf|pdf para)\b',t):
        setrow(r,'Fora de escopo','Busca por conteúdo','Documento/PDF informacional','fora de escopo','material matemático em PDF','alta','não','Busca por material identificado de Cálculo em PDF é conteúdo/documento, não conversão de arquivo.');content.add(r['id_global'])
wr(cp,rows,list(rows[0].keys()))
patched=xps|content;flags=rd(fp);kept=[];removed=0
for f in flags:
    if f.get('issue_code')=='PDF_CONTENT' and f.get('id_global') in patched:removed+=1
    else:kept.append(f)
wr(fp,kept,['severity','issue_code','id_global','Keyword','label','tipo_intencao','reason'])
lot=rd(ROOT/f'lote-{LOT:03d}.csv');base=[r for r in rows if r['tipo_registro']=='base'];ctr=[r for r in rows if r['tipo_registro']=='controle'];orig=list(lot[0].keys());orig_ok=all(all(x[k]==y[k] for k in orig) for x,y in zip(lot,rows));blank=sum(1 for r in base if not r['area_principal'] or not r['cluster'] or not r['subcluster']);dm=sum(1 for r in base if r['tipo_intencao']=='conversão direta' and (not r['unidade_origem'] or not r['unidade_destino'] or not r['direcao_conversao']))
prev=rd(ROOT/f'lote-{PREV:03d}-classificado-v1.1-barras-v2.csv');pc={r['controle_id']:r for r in prev if r['tipo_registro']=='controle'};fields=list(rows[0].keys());sem=[k for k in fields if k not in orig];ce=sum(1 for r in ctr if r['controle_id'] in pc and all(r.get(f,'')==pc[r['controle_id']].get(f,'') for f in sem));g=rd(ROOT/f'lote-{LOT:03d}-golden-qa-v1.1.csv');ge=sum(r.get('match_exato')=='sim' for r in g);conf=Counter(r['confianca'] for r in base);rev=Counter(r['revisao_manual'] for r in base);bars=sum(bool(r.get('keyword_interpretada')) for r in base);status='APROVADO' if not kept and dm==0 and blank==0 and orig_ok and ce==73 and ge==107 else 'REVISAR'
rp.write_text(f'# Relatório de classificação — Lote {LOT:03d}\n\n- Keywords base: **{len(base):,}**\n- Controles: **{len(ctr)}**\n- IDs base únicos: **{len({r["id_global"] for r in base}):,}**\n- Reconstruções de `/`: **{bars}**\n- Golden Set v1.1: **{ge}/107**\n- Controles: **{ce}/73**\n- Conversões diretas sem metadados: **{dm}**\n- Flags finais: **{len(kept)}**\n\n## Confiança\n- alta: **{conf["alta"]:,}**\n- média: **{conf["média"]:,}**\n- baixa: **{conf["baixa"]:,}**\n- revisão manual: **{rev["sim"]:,}**\n\n## v1.16\n- XPS/PDF: **{len(xps)}**\n- conteúdo matemático em PDF: **{len(content)}**\n',encoding='utf-8')
apath.write_text(f'# Auditoria pós-classificação — Lote {LOT:03d}\n\n## Veredito\n**{status}.**\n\n- Base: **{len(base):,}**\n- Controles: **{len(ctr)}**\n- IDs únicos: **{len({r["id_global"] for r in base}):,}**\n- Colunas originais preservadas: **{"sim" if orig_ok else "não"}**\n- Área/cluster/subcluster vazios: **{blank}**\n- Golden Set: **{ge}/107**\n- Controles incorporados: **{ce}/73**\n- Reconstruções `/`: **{bars}**\n- Conversões diretas sem metadados: **{dm}**\n- Flags finais: **{len(kept)}**\n- Lote {LOT+1:03d}: **{"liberado" if status=="APROVADO" else "não liberado"}**\n',encoding='utf-8')
print({'status':status,'xps_pdf':len(xps),'math_pdf_content':len(content),'flags':len(kept),'gold':ge,'controls_exact':ce,'confidence':dict(conf),'review':dict(rev),'base':len(base),'bars':bars})
