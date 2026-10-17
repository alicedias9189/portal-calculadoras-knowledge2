#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finalizador/Auditor semântico v1.8 — Taxonomia v1.1 + barras v2.

Camada complementar ao v1.7, validada no lote 014.

Novidades:
- direito/folga de aniversário do trabalhador é direito trabalhista, não calendário;
- consultas genéricas de marca/ferramenta `i love pdf` sem operação são navegacionais/fora de escopo;
- pares PDF↔outro formato com `em/para/to` são conversão mesmo quando uma camada anterior os marcou como fora de escopo;
- variantes de marca como `pdf i love word` são tratadas como conversão PDF↔Word quando dois formatos inequívocos aparecem.
"""
import argparse,csv,re,subprocess,sys,unicodedata
from collections import Counter
from pathlib import Path

ap=argparse.ArgumentParser(); ap.add_argument('--lote',type=int,required=True); ap.add_argument('--controle-anterior',type=int,default=None); ap.add_argument('--root',default='.'); ap.add_argument('--finalizador-anterior',default='')
a=ap.parse_args(); LOT=a.lote; PREV=a.controle_anterior or LOT-1; ROOT=Path(a.root).resolve(); PREVFIN=Path(a.finalizador_anterior).resolve() if a.finalizador_anterior else ROOT/'finalizar_auditar_lote_v1_7.py'

def rd(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def wr(p,rows,fields):
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter=';',extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def norm(s):
    s=unicodedata.normalize('NFKD',(s or '').casefold()); s=''.join(c for c in s if not unicodedata.combining(c)); return re.sub(r'\s+',' ',s).strip()
def setrow(r,a,c,s,tipo='informacional',domain='',conf='alta',review='não',just=''):
    r['area_principal']=a; r['cluster']=c; r['subcluster']=s; r['intencao_principal']=f'{tipo}: {s}'; r['tipo_intencao']=tipo; r['dominio_ou_grandeza']=domain or c; r['unidade_origem']=''; r['unidade_destino']=''; r['direcao_conversao']=''; r['confianca']=conf; r['revisao_manual']=review; r['justificativa_curta']=just

FMT=r'(?:pdf|word|docx?|excel|xlsx?|pptx?|powerpoint|jpg|jpeg|png|webp|svg|xml|csv|txt)'
def explicit_pdf_pair(t):
    return bool(re.search(rf'\bpdf\b.*\b(?:em|para|to)\b.*\b{FMT}\b',t) or re.search(rf'\b{FMT}\b.*\b(?:em|para|to)\b.*\bpdf\b',t))
def branded_two_format(t):
    toks=set(re.findall(r'\b(?:pdf|word|doc|docx|excel|xlsx|ppt|pptx|powerpoint|jpg|jpeg|png|xml|csv|txt)\b',t))
    return ('i love' in t or 'ilovepdf' in t) and 'pdf' in toks and len(toks)>=2
def generic_ilovepdf(t):
    if not ('i love pdf' in t or 'ilovepdf' in t): return False
    if explicit_pdf_pair(t) or branded_two_format(t): return False
    if re.search(r'\b(converter|conversor|juntar|quebrar|dividir|editar|comprimir|assinar|desbloquear)\b',t): return False
    return True

subprocess.run([sys.executable,str(PREVFIN),'--lote',str(LOT),'--controle-anterior',str(PREV),'--root',str(ROOT)],check=True)
cp=ROOT/f'lote-{LOT:03d}-classificado-v1.1-barras-v2.csv'; fp=ROOT/f'auditoria-pos-classificacao-lote-{LOT:03d}-v1.1-barras-v2-final-flags.csv'; rp=ROOT/f'relatorio-classificacao-lote-{LOT:03d}-v1.1-barras-v2.md'; apath=ROOT/f'auditoria-pos-classificacao-lote-{LOT:03d}-v1.1-barras-v2-final.md'
rows=rd(cp); patched_bday=set(); patched_pdfpair=set(); patched_brand=set(); patched_nav=set()
for r in rows:
    if r.get('tipo_registro')!='base': continue
    t=norm(r.get('Keyword',''))
    if 'aniversario' in t and re.search(r'\b(trabalhador|empregado|funcionario)\b',t) and re.search(r'\b(direito|folga)\b',t):
        setrow(r,'Trabalho','Legislação e direitos','Direitos trabalhistas e CLT','informacional','direito a folga','alta','não','Direito/folga de aniversário do trabalhador é questão trabalhista, não calendário.'); patched_bday.add(r['id_global']); continue
    if explicit_pdf_pair(t):
        setrow(r,'Conversores','Arquivos e documentos','Documentos e PDF','conversão de arquivo/mídia','formato de documento','alta','não','Par explícito PDF↔outro formato com direção indica conversão de arquivo.'); patched_pdfpair.add(r['id_global']); continue
    if branded_two_format(t):
        setrow(r,'Conversores','Arquivos e documentos','Documentos e PDF','conversão de arquivo/mídia','formato de documento','média','não','Marca/ferramenta PDF com dois formatos inequívocos indica intenção de conversão.'); patched_brand.add(r['id_global']); continue
    if generic_ilovepdf(t):
        setrow(r,'Fora de escopo','Conteúdo técnico/produto','Consulta técnica não conversível','navegacional/transacional','ferramenta PDF','alta','não','Busca genérica por marca/ferramenta PDF sem operação ou par de formatos; intenção navegacional, não conversão.'); patched_nav.add(r['id_global']); continue
wr(cp,rows,list(rows[0].keys()))
flags=rd(fp); kept=[]; removed=0; patched_all=patched_bday|patched_pdfpair|patched_brand|patched_nav
for f in flags:
    if f.get('id_global') in patched_all and f.get('issue_code') in {'WORK_RIGHTS_DATE','PDF_CONTENT'}: removed+=1; continue
    kept.append(f)
wr(fp,kept,['severity','issue_code','id_global','Keyword','label','tipo_intencao','reason'])
lot=rd(ROOT/f'lote-{LOT:03d}.csv'); base=[r for r in rows if r['tipo_registro']=='base']; ctr=[r for r in rows if r['tipo_registro']=='controle']; orig=list(lot[0].keys()); orig_ok=all(all(a[k]==b[k] for k in orig) for a,b in zip(lot,rows)); blank=sum(1 for r in base if not r['area_principal'] or not r['cluster'] or not r['subcluster']); dm=sum(1 for r in base if r['tipo_intencao']=='conversão direta' and (not r['unidade_origem'] or not r['unidade_destino'] or not r['direcao_conversao']))
prev=rd(ROOT/f'lote-{PREV:03d}-classificado-v1.1-barras-v2.csv'); pc={r['controle_id']:r for r in prev if r['tipo_registro']=='controle'}; fields=list(rows[0].keys()); sem=[k for k in fields if k not in orig]; ce=sum(1 for r in ctr if r['controle_id'] in pc and all(r.get(f,'')==pc[r['controle_id']].get(f,'') for f in sem)); g=rd(ROOT/f'lote-{LOT:03d}-golden-qa-v1.1.csv'); ge=sum(r.get('match_exato')=='sim' for r in g); conf=Counter(r['confianca'] for r in base); rev=Counter(r['revisao_manual'] for r in base); bars=sum(bool(r.get('keyword_interpretada')) for r in base); status='APROVADO' if not kept and dm==0 and blank==0 and orig_ok and ce==73 and ge==107 else 'REVISAR'
text=f'''# Relatório de classificação — Lote {LOT:03d} — Taxonomia v1.1 + barras v2\n\n- Keywords base: **{len(base):,}**\n- Controles: **{len(ctr)}**\n- IDs base únicos: **{len({r['id_global'] for r in base}):,}**\n- Reconstruções de `/`: **{bars}**\n- Golden Set v1.1: **{ge}/107**\n- Controles incorporados preservados: **{ce}/73**\n- Conversões diretas sem metadados: **{dm}**\n- Flags críticas/médias finais: **{len(kept)}**\n\n## Confiança\n- alta: **{conf['alta']:,}**\n- média: **{conf['média']:,}**\n- baixa: **{conf['baixa']:,}**\n- revisão manual: **{rev['sim']:,}**\n\n## Correções determinísticas v1.8\n- Direito/folga de aniversário: **{len(patched_bday)}**\n- Pares PDF explícitos reclassificados: **{len(patched_pdfpair)}**\n- Pares de formatos com marca iLovePDF: **{len(patched_brand)}**\n- Buscas genéricas/navegacionais iLovePDF: **{len(patched_nav)}**\n- Flags removidas: **{removed}**\n'''; rp.write_text(text,encoding='utf-8')
audit=f'''# Auditoria pós-classificação — Lote {LOT:03d}\n\n## Veredito\n**{status}.**\n\n- Linhas totais: **{len(rows):,}**\n- Base: **{len(base):,}**\n- Controles: **{len(ctr)}**\n- IDs únicos: **{len({r['id_global'] for r in base}):,}**\n- Colunas originais preservadas: **{'sim' if orig_ok else 'não'}**\n- Área/cluster/subcluster vazios: **{blank}**\n- Golden Set: **{ge}/107**\n- Controles incorporados: **{ce}/73**\n- Reconstruções `/`: **{bars}**\n- Conversões diretas sem origem/destino/direção: **{dm}**\n- Flags finais: **{len(kept)}**\n- Lote {LOT+1:03d}: **{'liberado' if status=='APROVADO' else 'não liberado'}**\n\n## Revisão v1.8\n- Direito/folga de aniversário corrigido: **{len(patched_bday)}**\n- Pares PDF explícitos corrigidos: **{len(patched_pdfpair)}**\n- Pares com marca iLovePDF corrigidos: **{len(patched_brand)}**\n- Buscas genéricas iLovePDF reclassificadas: **{len(patched_nav)}**\n- Flags removidas: **{removed}**\n'''; apath.write_text(audit,encoding='utf-8')
print({'status':status,'birthday_rights':len(patched_bday),'pdf_pairs':len(patched_pdfpair),'brand_pairs':len(patched_brand),'ilovepdf_nav':len(patched_nav),'flags':len(kept),'direct_missing':dm,'gold':ge,'controls_exact':ce,'confidence':dict(conf),'review':dict(rev)})
