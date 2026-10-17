#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finalizador/Auditor semântico v1.11 — Taxonomia v1.1 + barras v2.

Camada complementar ao v1.10, validada no lote 020.

Novidade:
- `transformador` é reconhecido como substantivo de ferramenta de conversão
  quando aplicado a PDF (`transformador de pdf`, `transformador pdf`,
  `transformador em pdf`), evitando falso positivo PDF_CONTENT.
"""
import argparse, csv, re, subprocess, sys, unicodedata
from collections import Counter
from pathlib import Path

ap=argparse.ArgumentParser(); ap.add_argument('--lote',type=int,required=True); ap.add_argument('--controle-anterior',type=int,default=None); ap.add_argument('--root',default='.'); ap.add_argument('--finalizador-anterior',default='')
a=ap.parse_args(); LOT=a.lote; PREV=a.controle_anterior or LOT-1; ROOT=Path(a.root).resolve(); PREVFIN=Path(a.finalizador_anterior).resolve() if a.finalizador_anterior else ROOT/'finalizar_auditar_lote_v1_10.py'

def rd(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def wr(p,rows,fields):
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter=';',extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def norm(s):
    s=unicodedata.normalize('NFKD',(s or '').casefold()); s=''.join(c for c in s if not unicodedata.combining(c)); return re.sub(r'\s+',' ',s).strip()

def pdf_transformer_tool(t):
    return 'pdf' in t and bool(re.search(r'\btransformador\b',t))

def normalize_conversion_row(r):
    r['area_principal']='Conversores'; r['cluster']='Arquivos e documentos'; r['subcluster']='Documentos e PDF'; r['intencao_principal']='Converter arquivo/mídia: Documentos e PDF'; r['tipo_intencao']='conversão de arquivo/mídia'; r['dominio_ou_grandeza']='formato de documento'; r['unidade_origem']=''; r['unidade_destino']=''; r['direcao_conversao']=''; r['confianca']='alta'; r['revisao_manual']='não'; r['justificativa_curta']='`transformador` em contexto de PDF indica ferramenta de transformação/conversão de arquivo.'

subprocess.run([sys.executable,str(PREVFIN),'--lote',str(LOT),'--controle-anterior',str(PREV),'--root',str(ROOT)],check=True)
cp=ROOT/f'lote-{LOT:03d}-classificado-v1.1-barras-v2.csv'; fp=ROOT/f'auditoria-pos-classificacao-lote-{LOT:03d}-v1.1-barras-v2-final-flags.csv'; rp=ROOT/f'relatorio-classificacao-lote-{LOT:03d}-v1.1-barras-v2.md'; apath=ROOT/f'auditoria-pos-classificacao-lote-{LOT:03d}-v1.1-barras-v2-final.md'
rows=rd(cp); patched=set()
for r in rows:
    if r.get('tipo_registro')!='base': continue
    t=norm(r.get('Keyword',''))
    if pdf_transformer_tool(t) and r.get('area_principal')=='Conversores' and r.get('subcluster')=='Documentos e PDF':
        normalize_conversion_row(r); patched.add(r['id_global'])
wr(cp,rows,list(rows[0].keys()))
flags=rd(fp); kept=[]; removed=0
for f in flags:
    if f.get('issue_code')=='PDF_CONTENT' and f.get('id_global') in patched:
        removed+=1; continue
    kept.append(f)
wr(fp,kept,['severity','issue_code','id_global','Keyword','label','tipo_intencao','reason'])

lot=rd(ROOT/f'lote-{LOT:03d}.csv'); base=[r for r in rows if r['tipo_registro']=='base']; ctr=[r for r in rows if r['tipo_registro']=='controle']; orig=list(lot[0].keys()); orig_ok=all(all(a[k]==b[k] for k in orig) for a,b in zip(lot,rows)); blank=sum(1 for r in base if not r['area_principal'] or not r['cluster'] or not r['subcluster']); dm=sum(1 for r in base if r['tipo_intencao']=='conversão direta' and (not r['unidade_origem'] or not r['unidade_destino'] or not r['direcao_conversao']))
prev=rd(ROOT/f'lote-{PREV:03d}-classificado-v1.1-barras-v2.csv'); pc={r['controle_id']:r for r in prev if r['tipo_registro']=='controle'}; fields=list(rows[0].keys()); sem=[k for k in fields if k not in orig]; ce=sum(1 for r in ctr if r['controle_id'] in pc and all(r.get(f,'')==pc[r['controle_id']].get(f,'') for f in sem)); g=rd(ROOT/f'lote-{LOT:03d}-golden-qa-v1.1.csv'); ge=sum(r.get('match_exato')=='sim' for r in g); conf=Counter(r['confianca'] for r in base); rev=Counter(r['revisao_manual'] for r in base); bars=sum(bool(r.get('keyword_interpretada')) for r in base); status='APROVADO' if not kept and dm==0 and blank==0 and orig_ok and ce==73 and ge==107 else 'REVISAR'

rp.write_text(f'''# Relatório de classificação — Lote {LOT:03d} — Taxonomia v1.1 + barras v2\n\n- Keywords base: **{len(base):,}**\n- Controles: **{len(ctr)}**\n- IDs base únicos: **{len({r['id_global'] for r in base}):,}**\n- Reconstruções de `/`: **{bars}**\n- Golden Set v1.1: **{ge}/107**\n- Controles incorporados preservados: **{ce}/73**\n- Conversões diretas sem metadados: **{dm}**\n- Flags críticas/médias finais: **{len(kept)}**\n\n## Confiança\n- alta: **{conf['alta']:,}**\n- média: **{conf['média']:,}**\n- baixa: **{conf['baixa']:,}**\n- revisão manual: **{rev['sim']:,}**\n\n## Correções determinísticas v1.11\n- Keywords PDF com `transformador` reconhecidas como ferramenta de conversão: **{len(patched)}**\n- Flags PDF_CONTENT removidas: **{removed}**\n''',encoding='utf-8')
apath.write_text(f'''# Auditoria pós-classificação — Lote {LOT:03d}\n\n## Veredito\n**{status}.**\n\n- Linhas totais: **{len(rows):,}**\n- Base: **{len(base):,}**\n- Controles: **{len(ctr)}**\n- IDs únicos: **{len({r['id_global'] for r in base}):,}**\n- Colunas originais preservadas: **{'sim' if orig_ok else 'não'}**\n- Área/cluster/subcluster vazios: **{blank}**\n- Golden Set: **{ge}/107**\n- Controles incorporados: **{ce}/73**\n- Reconstruções `/`: **{bars}**\n- Conversões diretas sem origem/destino/direção: **{dm}**\n- Flags finais: **{len(kept)}**\n- Lote {LOT+1:03d}: **{'liberado' if status=='APROVADO' else 'não liberado'}**\n\n## Revisão v1.11\n- Keywords PDF com `transformador` corrigidas: **{len(patched)}**\n- Flags PDF_CONTENT removidas: **{removed}**\n''',encoding='utf-8')
print({'status':status,'pdf_transformer_tool':len(patched),'flags':len(kept),'direct_missing':dm,'gold':ge,'controls_exact':ce,'confidence':dict(conf),'review':dict(rev)})
