#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finalizador/Auditor semântico v1.7 — Taxonomia v1.1 + barras v2.

Camada complementar ao v1.6, validada no lote 013.

Novidades:
- intervalos reais / intervalos de números reais permanecem em Matemática, inclusive PDF/DOC/PPT;
- luto/óbito com dias previstos em lei/CLT é afastamento/licença trabalhista;
- horas trabalhadas é jornada trabalhista por padrão, não diferença genérica de datas;
- salário por hora e salário proporcional a dias/mês são remuneração trabalhista;
- IR/IRRF sobre salário/folha pertence a Trabalho > Folha e encargos > INSS e IRRF;
- reajuste salarial é correção monetária/índices quando não houver subcontexto trabalhista mais específico.
"""
import argparse,csv,re,subprocess,sys,unicodedata
from collections import Counter
from pathlib import Path

ap=argparse.ArgumentParser(); ap.add_argument('--lote',type=int,required=True); ap.add_argument('--controle-anterior',type=int,default=None); ap.add_argument('--root',default='.'); ap.add_argument('--finalizador-anterior',default='')
a=ap.parse_args(); LOT=a.lote; PREV=a.controle_anterior or LOT-1; ROOT=Path(a.root).resolve(); PREVFIN=Path(a.finalizador_anterior).resolve() if a.finalizador_anterior else ROOT/'finalizar_auditar_lote_v1_6.py'

def rd(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def wr(p,rows,fields):
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter=';',extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def norm(s):
    s=unicodedata.normalize('NFKD',(s or '').casefold()); s=''.join(c for c in s if not unicodedata.combining(c)); return re.sub(r'\s+',' ',s).strip()
def setrow(r,a,c,s,tipo='informacional',domain='',conf='alta',review='não',just=''):
    r['area_principal']=a; r['cluster']=c; r['subcluster']=s; r['intencao_principal']=f'{tipo}: {s}'; r['tipo_intencao']=tipo; r['dominio_ou_grandeza']=domain or c
    r['unidade_origem']=''; r['unidade_destino']=''; r['direcao_conversao']=''; r['confianca']=conf; r['revisao_manual']=review; r['justificativa_curta']=just

def calcish(t): return bool(re.search(r'\b(calcul\w*|contador|somar|soma|dividir|quanto|valor|percentual|porcentagem|taxa)\b',t))

subprocess.run([sys.executable,str(PREVFIN),'--lote',str(LOT),'--controle-anterior',str(PREV),'--root',str(ROOT)],check=True)
cp=ROOT/f'lote-{LOT:03d}-classificado-v1.1-barras-v2.csv'; fp=ROOT/f'auditoria-pos-classificacao-lote-{LOT:03d}-v1.1-barras-v2-final-flags.csv'; rp=ROOT/f'relatorio-classificacao-lote-{LOT:03d}-v1.1-barras-v2.md'; apath=ROOT/f'auditoria-pos-classificacao-lote-{LOT:03d}-v1.1-barras-v2-final.md'
rows=rd(cp)
patched_intervals=set(); patched_luto=set(); patched_hours=set(); patched_salary=set(); patched_irrf=set(); patched_reaj=set()
for r in rows:
    if r.get('tipo_registro')!='base': continue
    t=norm(r.get('Keyword',''))
    if re.search(r'\b(intervalos? reais?|intervalos? de numeros reais)\b',t):
        setrow(r,'Matemática','Números e operações','Aritmética e operações básicas','informacional','intervalos reais','alta' if ('matemat' in t or 'enem' in t) else 'média','não','Intervalos de números reais são conteúdo matemático; PDF/DOC/PPT são apenas formato/referência.')
        patched_intervals.add(r['id_global']); continue
    if re.search(r'\b(luto|obito|falecimento)\b',t) and re.search(r'\b(clt|lei|trabalhist|dias?|licenca|direito)\b',t):
        setrow(r,'Trabalho','Afastamentos','Licenças e afastamentos','informacional','licença por luto','alta','não','Dias de luto/óbito previstos em lei ou CLT são afastamento trabalhista.')
        patched_luto.add(r['id_global']); continue
    if 'horas trabalhadas' in t and r.get('area_principal')!='Trabalho':
        setrow(r,'Trabalho','Jornada e adicionais','Escalas e jornada','cálculo direto' if calcish(t) else 'informacional','jornada de trabalho','alta' if 'Trabalho' in (r.get('areas_origem') or '') else 'média','não','Horas trabalhadas pertencem à jornada trabalhista; não são diferença genérica de datas.')
        patched_hours.add(r['id_global']); continue
    if re.search(r'\bsalario\b',t) and (re.search(r'\b(por hora|em horas|hora trabalhada|dividir.*hora)\b',t) or re.search(r'\bproporcional\b.*\b(dias?|mes|mês)\b',t) or re.search(r'\bmes de 31 dias\b',t)):
        sub='Valor da hora e dias trabalhados' if re.search(r'\b(hora|horas)\b',t) else 'Salário líquido e bruto'
        setrow(r,'Trabalho','Remuneração',sub,'cálculo direto','remuneração trabalhista','alta','não','Salário por hora ou proporcional a dias/mês é cálculo de remuneração trabalhista.')
        patched_salary.add(r['id_global']); continue
    if re.search(r'\b(imposto de renda|imposto renda|irrf)\b',t) and re.search(r'\b(salario|folha|holerite|contracheque)\b',t):
        setrow(r,'Trabalho','Folha e encargos','INSS e IRRF','cálculo direto' if calcish(t) or re.search(r'\bdesconto\b',t) else 'informacional','IRRF sobre remuneração','alta','não','IR/IRRF incidente sobre salário/folha pertence aos encargos trabalhistas, não a investimentos.')
        patched_irrf.add(r['id_global']); continue
    if 'reajuste salarial' in t and not (r.get('area_principal')=='Finanças' and r.get('cluster')=='Correção monetária'):
        setrow(r,'Finanças','Correção monetária','Inflação e índices','cálculo direto' if calcish(t) else 'informacional','reajuste salarial','média','não','Reajuste salarial é atualização/correção monetária por percentual ou índice.')
        patched_reaj.add(r['id_global']); continue
wr(cp,rows,list(rows[0].keys()))
flags=rd(fp); kept=[]; removed=0
patched_all=patched_intervals|patched_luto|patched_hours|patched_salary|patched_irrf|patched_reaj
for f in flags:
    if f.get('id_global') in patched_all and f.get('issue_code') in {'PDF_CONTENT','WORK_RIGHTS_DATE'}:
        removed+=1; continue
    kept.append(f)
wr(fp,kept,['severity','issue_code','id_global','Keyword','label','tipo_intencao','reason'])
lot=rd(ROOT/f'lote-{LOT:03d}.csv'); base=[r for r in rows if r['tipo_registro']=='base']; ctr=[r for r in rows if r['tipo_registro']=='controle']; orig=list(lot[0].keys()); orig_ok=all(all(a[k]==b[k] for k in orig) for a,b in zip(lot,rows)); blank=sum(1 for r in base if not r['area_principal'] or not r['cluster'] or not r['subcluster']); dm=sum(1 for r in base if r['tipo_intencao']=='conversão direta' and (not r['unidade_origem'] or not r['unidade_destino'] or not r['direcao_conversao']))
prev=rd(ROOT/f'lote-{PREV:03d}-classificado-v1.1-barras-v2.csv'); pc={r['controle_id']:r for r in prev if r['tipo_registro']=='controle'}; fields=list(rows[0].keys()); sem=[k for k in fields if k not in orig]; ce=sum(1 for r in ctr if r['controle_id'] in pc and all(r.get(f,'')==pc[r['controle_id']].get(f,'') for f in sem)); g=rd(ROOT/f'lote-{LOT:03d}-golden-qa-v1.1.csv'); ge=sum(r.get('match_exato')=='sim' for r in g); conf=Counter(r['confianca'] for r in base); rev=Counter(r['revisao_manual'] for r in base); bars=sum(bool(r.get('keyword_interpretada')) for r in base); status='APROVADO' if not kept and dm==0 and blank==0 and orig_ok and ce==73 and ge==107 else 'REVISAR'
summary=f'''# Relatório de classificação — Lote {LOT:03d} — Taxonomia v1.1 + barras v2\n\n- Keywords base: **{len(base):,}**\n- Controles: **{len(ctr)}**\n- IDs base únicos: **{len({r['id_global'] for r in base}):,}**\n- Reconstruções de `/`: **{bars}**\n- Golden Set v1.1: **{ge}/107**\n- Controles incorporados preservados: **{ce}/73**\n- Conversões diretas sem metadados: **{dm}**\n- Flags críticas/médias finais: **{len(kept)}**\n\n## Confiança\n- alta: **{conf['alta']:,}**\n- média: **{conf['média']:,}**\n- baixa: **{conf['baixa']:,}**\n- revisão manual: **{rev['sim']:,}**\n\n## Correções determinísticas v1.7\n- Intervalos reais: **{len(patched_intervals)}**\n- Luto/óbito trabalhista: **{len(patched_luto)}**\n- Horas trabalhadas: **{len(patched_hours)}**\n- Salário por hora/proporcional: **{len(patched_salary)}**\n- IR/IRRF sobre salário/folha: **{len(patched_irrf)}**\n- Reajuste salarial fora do cluster correto: **{len(patched_reaj)}**\n- Flags removidas após correção: **{removed}**\n'''; rp.write_text(summary,encoding='utf-8')
audit=f'''# Auditoria pós-classificação — Lote {LOT:03d}\n\n## Veredito\n**{status}.**\n\n- Linhas totais: **{len(rows):,}**\n- Base: **{len(base):,}**\n- Controles: **{len(ctr)}**\n- IDs únicos: **{len({r['id_global'] for r in base}):,}**\n- Colunas originais preservadas: **{'sim' if orig_ok else 'não'}**\n- Área/cluster/subcluster vazios: **{blank}**\n- Golden Set: **{ge}/107**\n- Controles incorporados: **{ce}/73**\n- Reconstruções `/`: **{bars}**\n- Conversões diretas sem origem/destino/direção: **{dm}**\n- Flags finais: **{len(kept)}**\n- Lote {LOT+1:03d}: **{'liberado' if status=='APROVADO' else 'não liberado'}**\n\n## Revisão v1.7\n- Intervalos reais corrigidos: **{len(patched_intervals)}**\n- Luto/óbito trabalhista corrigido: **{len(patched_luto)}**\n- Horas trabalhadas corrigidas: **{len(patched_hours)}**\n- Salário por hora/proporcional corrigido: **{len(patched_salary)}**\n- IR/IRRF sobre salário/folha corrigido: **{len(patched_irrf)}**\n- Reajuste salarial corrigido: **{len(patched_reaj)}**\n- Flags removidas: **{removed}**\n'''; apath.write_text(audit,encoding='utf-8')
print({'status':status,'intervalos_reais':len(patched_intervals),'luto':len(patched_luto),'horas_trabalhadas':len(patched_hours),'salario_hora_prop':len(patched_salary),'irrf_salario':len(patched_irrf),'reajuste':len(patched_reaj),'flags':len(kept),'direct_missing':dm,'gold':ge,'controls_exact':ce,'confidence':dict(conf),'review':dict(rev)})
