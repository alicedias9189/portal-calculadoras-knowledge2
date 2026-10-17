#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Finalizador semântico v1.14 — complemento ao v1.13, validado no lote 023.

Novidades:
- preço unitário atual de combustível (ex.: preço do litro de diesel) é consulta de mercado,
  não consumo/autonomia;
- buscas de marca `Convertio` + PDF sem operação explícita são navegacionais para serviço,
  não conversão semântica específica;
- folga/direito de mesário/presidente de mesa é direito/afastamento trabalhista, não Datas.
"""
import argparse,csv,re,subprocess,sys,unicodedata
from collections import Counter
from pathlib import Path
ap=argparse.ArgumentParser(); ap.add_argument('--lote',type=int,required=True); ap.add_argument('--controle-anterior',type=int,default=None); ap.add_argument('--root',default='.'); ap.add_argument('--skip-anterior',action='store_true'); a=ap.parse_args()
LOT=a.lote; PREV=a.controle_anterior or LOT-1; ROOT=Path(a.root).resolve()
def rd(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def wr(p,rows,fields):
    with p.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=fields,delimiter=';',extrasaction='ignore');w.writeheader();w.writerows(rows)
def n(s):
    s=unicodedata.normalize('NFKD',(s or '').casefold());s=''.join(c for c in s if not unicodedata.combining(c));return re.sub(r'\s+',' ',s).strip()
if not a.skip_anterior:subprocess.run([sys.executable,str(ROOT/'finalizar_auditar_lote_v1_13.py'),'--lote',str(LOT),'--controle-anterior',str(PREV),'--root',str(ROOT)],check=True)
cp=ROOT/f'lote-{LOT:03d}-classificado-v1.1-barras-v2.csv'; fp=ROOT/f'auditoria-pos-classificacao-lote-{LOT:03d}-v1.1-barras-v2-final-flags.csv'; rp=ROOT/f'relatorio-classificacao-lote-{LOT:03d}-v1.1-barras-v2.md'; apath=ROOT/f'auditoria-pos-classificacao-lote-{LOT:03d}-v1.1-barras-v2-final.md'
rows=rd(cp); fuel=set(); brand=set(); leave=set()
for r in rows:
    if r.get('tipo_registro')!='base':continue
    t=n(r['Keyword'])
    if re.search(r'\b(preco|valor)\b.*\b(litro|l)\b.*\b(diesel|gasolina|etanol|combustivel)\b',t) or re.search(r'\b(preco|valor)\b.*\b(diesel|gasolina|etanol|combustivel)\b.*\b(litro|l)\b',t):
        r.update(area_principal='Fora de escopo',cluster='Preço de mercado',subcluster='Combustíveis/preço de mercado',intencao_principal='Consultar preço de combustível',tipo_intencao='consulta de preço/mercado',dominio_ou_grandeza='preço de combustível',unidade_origem='',unidade_destino='',direcao_conversao='',confianca='alta',revisao_manual='não',justificativa_curta='Preço unitário de combustível é consulta de mercado, não consumo/autonomia.'); fuel.add(r['id_global'])
    if 'convertio' in t and 'pdf' in t and not re.search(r'\b(convert|converter|conversao|transform|para|to|em|word|docx|jpg|png|excel|xlsx|dwg|dxf)\b',t.replace('convertio','')):
        r.update(area_principal='Fora de escopo',cluster='Conteúdo técnico/produto',subcluster='Consulta técnica não conversível',intencao_principal='Navegar para serviço externo',tipo_intencao='navegacional/transacional',dominio_ou_grandeza='serviço externo de conversão',unidade_origem='',unidade_destino='',direcao_conversao='',confianca='alta',revisao_manual='não',justificativa_curta='Marca Convertio + PDF sem operação/formato de destino é busca navegacional por serviço.'); brand.add(r['id_global'])
    if re.search(r'\b(mesario|presidente de mesa)\b',t) and re.search(r'\b(folga|dias?|direito)\b',t):
        r.update(area_principal='Trabalho',cluster='Afastamentos',subcluster='Licenças e afastamentos',intencao_principal='Entender direito a folga/afastamento',tipo_intencao='informacional',dominio_ou_grandeza='folga eleitoral/trabalhista',unidade_origem='',unidade_destino='',direcao_conversao='',confianca='alta',revisao_manual='não',justificativa_curta='Folga de mesário/presidente de mesa é direito de afastamento do trabalho, não calendário.'); leave.add(r['id_global'])
wr(cp,rows,list(rows[0].keys()))
flags=rd(fp); kept=[]; removed=0
for f in flags:
    iid=f.get('id_global'); code=f.get('issue_code')
    if (code=='FUEL_MARKET' and iid in fuel) or (code=='PDF_CONTENT' and iid in brand) or (code=='WORK_RIGHTS_DATE' and iid in leave):removed+=1
    else:kept.append(f)
wr(fp,kept,['severity','issue_code','id_global','Keyword','label','tipo_intencao','reason'])
lot=rd(ROOT/f'lote-{LOT:03d}.csv'); base=[r for r in rows if r['tipo_registro']=='base']; ctr=[r for r in rows if r['tipo_registro']=='controle']; orig=list(lot[0].keys()); orig_ok=all(all(x[k]==y[k] for k in orig) for x,y in zip(lot,rows)); blank=sum(1 for r in base if not r['area_principal'] or not r['cluster'] or not r['subcluster']); dm=sum(1 for r in base if r['tipo_intencao']=='conversão direta' and (not r['unidade_origem'] or not r['unidade_destino'] or not r['direcao_conversao']))
prev=rd(ROOT/f'lote-{PREV:03d}-classificado-v1.1-barras-v2.csv'); pc={r['controle_id']:r for r in prev if r['tipo_registro']=='controle'}; fields=list(rows[0].keys()); sem=[k for k in fields if k not in orig]; ce=sum(1 for r in ctr if r['controle_id'] in pc and all(r.get(f,'')==pc[r['controle_id']].get(f,'') for f in sem)); g=rd(ROOT/f'lote-{LOT:03d}-golden-qa-v1.1.csv'); ge=sum(r.get('match_exato')=='sim' for r in g); conf=Counter(r['confianca'] for r in base); rev=Counter(r['revisao_manual'] for r in base); bars=sum(bool(r.get('keyword_interpretada')) for r in base); status='APROVADO' if not kept and dm==0 and blank==0 and orig_ok and ce==73 and ge==107 else 'REVISAR'
rp.write_text(f'# Relatório de classificação — Lote {LOT:03d}\n\n- Keywords base: **{len(base):,}**\n- Controles: **{len(ctr)}**\n- IDs base únicos: **{len({r["id_global"] for r in base}):,}**\n- Reconstruções de `/`: **{bars}**\n- Golden Set v1.1: **{ge}/107**\n- Controles incorporados preservados: **{ce}/73**\n- Conversões diretas sem metadados: **{dm}**\n- Flags finais: **{len(kept)}**\n\n## Confiança\n- alta: **{conf["alta"]:,}**\n- média: **{conf["média"]:,}**\n- baixa: **{conf["baixa"]:,}**\n- revisão manual: **{rev["sim"]:,}**\n\n## v1.14\n- preço unitário combustível: **{len(fuel)}**\n- Convertio navegacional: **{len(brand)}**\n- folga eleitoral: **{len(leave)}**\n',encoding='utf-8')
apath.write_text(f'# Auditoria pós-classificação — Lote {LOT:03d}\n\n## Veredito\n**{status}.**\n\n- Base: **{len(base):,}**\n- Controles: **{len(ctr)}**\n- IDs únicos: **{len({r["id_global"] for r in base}):,}**\n- Colunas originais preservadas: **{"sim" if orig_ok else "não"}**\n- Área/cluster/subcluster vazios: **{blank}**\n- Golden Set: **{ge}/107**\n- Controles incorporados: **{ce}/73**\n- Reconstruções `/`: **{bars}**\n- Conversões diretas sem metadados: **{dm}**\n- Flags finais: **{len(kept)}**\n- Lote {LOT+1:03d}: **{"liberado" if status=="APROVADO" else "não liberado"}**\n',encoding='utf-8')
print({'status':status,'fuel_market':len(fuel),'convertio_nav':len(brand),'electoral_leave':len(leave),'flags':len(kept),'gold':ge,'controls_exact':ce,'confidence':dict(conf),'review':dict(rev),'base':len(base),'bars':bars})
