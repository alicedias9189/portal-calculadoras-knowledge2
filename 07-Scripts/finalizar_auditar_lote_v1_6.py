#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finalizador/Auditor semântico v1.6 — Taxonomia v1.1 + barras v2.

Camada complementar ao `finalizar_auditar_lote_v1_5.py`.

Novidades validadas a partir do lote 012:
- `dias trabalhados` é domínio trabalhista por padrão, não cálculo de datas.
  * família genérica -> Trabalho > Remuneração > Valor da hora e dias trabalhados;
  * pagamento/salário/folha/adiantamento -> Trabalho > Remuneração > Salário líquido e bruto;
  * contextos específicos (13º, férias, rescisão, escala, DSR, adicionais etc.) mantêm o subcluster específico.
- afastamentos/licenças calculados por dias permanecem em Trabalho > Afastamentos.
- `TRCT` em PDF/DOC é conteúdo trabalhista de rescisão, não conversão de arquivo.
- `fatorial pdf` é conteúdo matemático, não conversão de arquivo.
- pares explícitos adjacentes de formatos como `pdf word`, `pdf powerpoint` continuam sendo conversão de arquivo mesmo sem preposição/verbo.

Uso:
  python3 finalizar_auditar_lote_v1_6.py --lote 12 --controle-anterior 11 --root .
"""
import argparse
import csv
import re
import subprocess
import sys
import unicodedata
from collections import Counter
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--lote', type=int, required=True)
parser.add_argument('--controle-anterior', type=int, default=None)
parser.add_argument('--root', default='.')
parser.add_argument('--finalizador-anterior', default='')
args = parser.parse_args()
LOT = args.lote
PREV = args.controle_anterior or LOT - 1
ROOT = Path(args.root).resolve()
PREVIOUS_FINALIZER = Path(args.finalizador_anterior).resolve() if args.finalizador_anterior else ROOT / 'finalizar_auditar_lote_v1_5.py'


def rd(path):
    with path.open('r', encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter=';'))


def wr(path, rows, fields):
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter=';', extrasaction='ignore')
        w.writeheader(); w.writerows(rows)


def norm(s):
    s = unicodedata.normalize('NFKD', (s or '').casefold())
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'\s+', ' ', s).strip()


def label_row(r, area, cluster, subcluster, tipo='cálculo direto', domain='trabalho', conf='alta', review='não', just=''):
    r['area_principal'] = area
    r['cluster'] = cluster
    r['subcluster'] = subcluster
    r['intencao_principal'] = f'{tipo}: {subcluster}'
    r['tipo_intencao'] = tipo
    r['dominio_ou_grandeza'] = domain
    r['unidade_origem'] = ''
    r['unidade_destino'] = ''
    r['direcao_conversao'] = ''
    r['confianca'] = conf
    r['revisao_manual'] = review
    r['justificativa_curta'] = just


FORMAT_TOKENS = r'(?:pdf|word|docx?|powerpoint|pptx?|excel|xlsx?|csv|txt|xml|html|jpg|jpeg|png|webp|svg|rtf|epub)'
def adjacent_format_pair(t):
    return bool(re.search(rf'\b{FORMAT_TOKENS}\b\s+\b{FORMAT_TOKENS}\b', t))


subprocess.run([
    sys.executable, str(PREVIOUS_FINALIZER), '--lote', str(LOT),
    '--controle-anterior', str(PREV), '--root', str(ROOT)
], check=True)

class_path = ROOT / f'lote-{LOT:03d}-classificado-v1.1-barras-v2.csv'
flag_path = ROOT / f'auditoria-pos-classificacao-lote-{LOT:03d}-v1.1-barras-v2-final-flags.csv'
report_path = ROOT / f'relatorio-classificacao-lote-{LOT:03d}-v1.1-barras-v2.md'
audit_path = ROOT / f'auditoria-pos-classificacao-lote-{LOT:03d}-v1.1-barras-v2-final.md'
classified = rd(class_path)
patched_days = set(); patched_leave = set(); patched_trct = set(); patched_math_pdf = set(); explicit_pair_ids = set()

specific_days = re.compile(
    r'\b(decimo terceiro|13o|13º|ferias|rescis|acerto|12x36|12/36|escala|jornada|turno|banco de horas|dsr|descanso semanal|periculosidade|insalubridade|aviso previo|hora extra|adicional noturno|fgts|inss|pis|pasep)\b'
)
pay_context = re.compile(r'\b(pagamento|pagar|salario|salarial|folha|adiantamento|a receber|receber|remuneracao)\b')

for r in classified:
    if r.get('tipo_registro') != 'base':
        continue
    t = norm(r.get('Keyword', ''))
    if ('afastamento' in t or 'licenca' in t) and 'dias' in t and re.search(r'\b(calcul\w*|contar|contagem|quantos?)\b', t):
        label_row(r, 'Trabalho', 'Afastamentos', 'Licenças e afastamentos',
                  tipo='cálculo direto', domain='licenças e afastamentos', conf='alta', review='não',
                  just='Contagem/cálculo de dias de licença ou afastamento é regra trabalhista, não operação genérica de datas.')
        patched_leave.add(r['id_global'])
        continue
    if 'dias trabalhados' in t and not specific_days.search(t):
        if pay_context.search(t):
            target = ('Trabalho', 'Remuneração', 'Salário líquido e bruto')
            just = 'Pagamento/salário proporcional a dias trabalhados pertence à remuneração trabalhista.'
        else:
            target = ('Trabalho', 'Remuneração', 'Valor da hora e dias trabalhados')
            just = 'Cálculo de dias trabalhados é cálculo trabalhista; não é diferença genérica entre datas.'
        conf = 'alta' if 'Trabalho' in (r.get('areas_origem') or '') else 'média'
        label_row(r, *target, tipo='cálculo direto', domain='remuneração trabalhista', conf=conf, review='não', just=just)
        patched_days.add(r['id_global'])
        continue
    if re.search(r'\btrct\b', t) and re.search(r'\b(pdf|doc|docx|arquivo|modelo|formulario)\b', t):
        label_row(r, 'Trabalho', 'Rescisão', 'Rescisão trabalhista', tipo='informacional',
                  domain='rescisão trabalhista', conf='média', review='não',
                  just='TRCT é documento de rescisão do contrato de trabalho; a menção a PDF/DOC não implica conversão de arquivo.')
        patched_trct.add(r['id_global'])
        continue
    if 'fatorial' in t and 'pdf' in t:
        label_row(r, 'Matemática', 'Números e operações', 'Aritmética e operações básicas', tipo='informacional',
                  domain='fatorial', conf='média', review='não',
                  just='PDF é apenas o formato do conteúdo pesquisado; a intenção principal é matemática/fatorial.')
        patched_math_pdf.add(r['id_global'])
        continue
    if adjacent_format_pair(t) and 'pdf' in t and r.get('area_principal') == 'Conversores':
        explicit_pair_ids.add(r['id_global'])

wr(class_path, classified, list(classified[0].keys()))
flags = rd(flag_path)
kept=[]; removed_work=removed_pdf=0
for f in flags:
    iid=f.get('id_global','')
    code=f.get('issue_code')
    if code=='WORK_RIGHTS_DATE' and (iid in patched_days or iid in patched_leave):
        removed_work += 1; continue
    if code=='PDF_CONTENT' and (iid in patched_trct or iid in patched_math_pdf or iid in explicit_pair_ids):
        removed_pdf += 1; continue
    kept.append(f)
flag_fields=['severity','issue_code','id_global','Keyword','label','tipo_intencao','reason']
wr(flag_path, kept, flag_fields)

lot=rd(ROOT / f'lote-{LOT:03d}.csv')
basef=[r for r in classified if r['tipo_registro']=='base']
ctrlf=[r for r in classified if r['tipo_registro']=='controle']
orig_fields=list(lot[0].keys())
orig_ok=all(all(a[k]==b[k] for k in orig_fields) for a,b in zip(lot,classified))
blank=sum(1 for r in basef if not r['area_principal'] or not r['cluster'] or not r['subcluster'])
direct_missing=sum(1 for r in basef if r['tipo_intencao']=='conversão direta' and (not r['unidade_origem'] or not r['unidade_destino'] or not r['direcao_conversao']))
prev=rd(ROOT / f'lote-{PREV:03d}-classificado-v1.1-barras-v2.csv')
prev_ctrl={r['controle_id']:r for r in prev if r['tipo_registro']=='controle'}
fields=list(classified[0].keys()); semantic=[k for k in fields if k not in orig_fields]
ctrl_exact=sum(1 for r in ctrlf if r['controle_id'] in prev_ctrl and all(r.get(f,'')==prev_ctrl[r['controle_id']].get(f,'') for f in semantic))
goldqa=rd(ROOT / f'lote-{LOT:03d}-golden-qa-v1.1.csv'); gold_exact=sum(r.get('match_exato')=='sim' for r in goldqa)
conf=Counter(r['confianca'] for r in basef); review=Counter(r['revisao_manual'] for r in basef)
bars=sum(bool(r.get('keyword_interpretada')) for r in basef)
status='APROVADO' if not kept and direct_missing==0 and blank==0 and orig_ok and ctrl_exact==73 and gold_exact==107 else 'REVISAR'

report_path.write_text(
    f'# Relatório de classificação — Lote {LOT:03d} — Taxonomia v1.1 + barras v2\n\n'
    f'- Keywords base: **{len(basef):,}**\n- Controles: **{len(ctrlf)}**\n- IDs base únicos: **{len({r["id_global"] for r in basef}):,}**\n'
    f'- Reconstruções de `/`: **{bars}**\n- Golden Set v1.1: **{gold_exact}/107**\n- Controles incorporados preservados: **{ctrl_exact}/73**\n'
    f'- Conversões diretas sem metadados: **{direct_missing}**\n- Flags críticas/médias finais: **{len(kept)}**\n\n'
    f'## Confiança\n- alta: **{conf["alta"]:,}**\n- média: **{conf["média"]:,}**\n- baixa: **{conf["baixa"]:,}**\n- revisão manual: **{review["sim"]:,}**\n\n'
    f'## Correções determinísticas v1.6\n- Família `dias trabalhados` corrigida: **{len(patched_days)}**\n- Licenças/afastamentos corrigidos: **{len(patched_leave)}**\n'
    f'- TRCT PDF/DOC corrigidos: **{len(patched_trct)}**\n- Conteúdo matemático PDF corrigido: **{len(patched_math_pdf)}**\n'
    f'- Pares adjacentes de formatos tratados como conversão: **{len(explicit_pair_ids)}**\n- Flags WORK_RIGHTS_DATE removidas: **{removed_work}**\n- Flags PDF_CONTENT removidas: **{removed_pdf}**\n', encoding='utf-8')

audit_path.write_text(
    f'# Auditoria pós-classificação — Lote {LOT:03d}\n\n## Veredito\n**{status}.**\n\n'
    f'- Linhas totais: **{len(classified):,}**\n- Base: **{len(basef):,}**\n- Controles: **{len(ctrlf)}**\n- IDs únicos: **{len({r["id_global"] for r in basef}):,}**\n'
    f'- Colunas originais preservadas: **{"sim" if orig_ok else "não"}**\n- Área/cluster/subcluster vazios: **{blank}**\n- Golden Set: **{gold_exact}/107**\n'
    f'- Controles incorporados: **{ctrl_exact}/73**\n- Reconstruções `/`: **{bars}**\n- Conversões diretas sem origem/destino/direção: **{direct_missing}**\n'
    f'- Flags finais: **{len(kept)}**\n- Lote {LOT+1:03d}: **{"liberado" if status=="APROVADO" else "não liberado"}**\n\n'
    f'## Revisão v1.6\n- Família `dias trabalhados` corrigida: **{len(patched_days)}**\n- Licenças/afastamentos corrigidos: **{len(patched_leave)}**\n'
    f'- TRCT PDF/DOC corrigidos: **{len(patched_trct)}**\n- Conteúdo matemático PDF corrigido: **{len(patched_math_pdf)}**\n'
    f'- Pares adjacentes de formatos aceitos: **{len(explicit_pair_ids)}**\n- Flags removidas após correção: **{removed_work + removed_pdf}**\n', encoding='utf-8')

print({'status':status,'patched_days_worked':len(patched_days),'patched_leave':len(patched_leave),'patched_trct':len(patched_trct),'patched_math_pdf':len(patched_math_pdf),'explicit_format_pairs':len(explicit_pair_ids),'flags':len(kept),'direct_missing':direct_missing,'gold':gold_exact,'controls_exact':ctrl_exact,'confidence':dict(conf),'review':dict(review)})
