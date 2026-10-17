#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finalizador/Auditor semântico v1.4 — Taxonomia v1.1 + barras v2.

Camada complementar ao `finalizar_auditar_lote_v1_3.py`.

Novidade validada no lote 008:
- PDF_CONTENT reconhece pares de formato explícitos sem verbo, inclusive
  `pdf em imagem`, `pdf em xml` e equivalentes. Esses casos continuam em
  Conversores > Arquivos e documentos > Documentos e PDF com intenção
  `conversão de arquivo/mídia` e não geram falso positivo de conteúdo PDF.

Uso:
  python3 finalizar_auditar_lote_v1_4.py --lote 8 --controle-anterior 7 --root .

O script preserva integralmente as colunas originais do lote e executa primeiro
as camadas v1.3 → v1.2 → v1.1.
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
parser.add_argument(
    '--finalizador-anterior',
    default='',
    help='Caminho do finalizar_auditar_lote_v1_3.py. Padrão: root/finalizar_auditar_lote_v1_3.py',
)
args = parser.parse_args()

LOT = args.lote
PREV = args.controle_anterior or LOT - 1
ROOT = Path(args.root).resolve()
PREVIOUS_FINALIZER = (
    Path(args.finalizador_anterior).resolve()
    if args.finalizador_anterior
    else ROOT / 'finalizar_auditar_lote_v1_3.py'
)


def rd(path):
    with path.open('r', encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter=';'))


def wr(path, rows, fields):
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter=';', extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)


def norm(s):
    s = unicodedata.normalize('NFKD', (s or '').casefold())
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'\s+', ' ', s).strip()


FORMAT_TOKENS = {
    'pdf', 'word', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'imagem', 'imagens',
    'foto', 'fotos', 'xml', 'html', 'csv', 'txt', 'texto', 'xlsx', 'xls',
    'excel', 'svg', 'webp', 'ppt', 'pptx', 'powerpoint', 'rtf', 'epub'
}


def explicit_pdf_format_pair(text):
    """Detecta transformação inequívoca entre PDF e outro formato/representação."""
    t = norm(text)
    if 'pdf' not in t:
        return False
    tokens = set(re.findall(r'\b[a-z0-9]+\b', t))
    present = tokens & FORMAT_TOKENS
    if 'pdf' not in present or len(present) < 2:
        return False

    # Relação explícita por preposição/direção, com ou sem verbo.
    fmt = r'(?:word|doc|docx|jpg|jpeg|png|imagem|imagens|foto|fotos|xml|html|csv|txt|texto|xlsx|xls|excel|svg|webp|ppt|pptx|powerpoint|rtf|epub)'
    return bool(
        re.search(rf'\bpdf\b\s+(?:em|para|to)\s+\b{fmt}\b', t)
        or re.search(rf'\b{fmt}\b\s+(?:em|para|to)\s+\bpdf\b', t)
        or re.search(rf'\bpdf\b.*\b{fmt}\b', t) and re.search(r'\b(converter|conversor|conversao|transformar|passar|exportar|salvar)\b', t)
    )


# 1) Executa todas as camadas anteriores.
cmd = [
    sys.executable,
    str(PREVIOUS_FINALIZER),
    '--lote', str(LOT),
    '--controle-anterior', str(PREV),
    '--root', str(ROOT),
]
subprocess.run(cmd, check=True)

class_path = ROOT / f'lote-{LOT:03d}-classificado-v1.1-barras-v2.csv'
flag_path = ROOT / f'auditoria-pos-classificacao-lote-{LOT:03d}-v1.1-barras-v2-final-flags.csv'
report_path = ROOT / f'relatorio-classificacao-lote-{LOT:03d}-v1.1-barras-v2.md'
audit_path = ROOT / f'auditoria-pos-classificacao-lote-{LOT:03d}-v1.1-barras-v2-final.md'

classified = rd(class_path)
flags = rd(flag_path)
by_id = {r['id_global']: r for r in classified if r.get('tipo_registro') == 'base'}

# 2) Remove somente falsos positivos PDF_CONTENT com par de formatos inequívoco.
kept = []
removed_pdf_pair = 0
for f in flags:
    row = by_id.get(f.get('id_global'))
    if f.get('issue_code') == 'PDF_CONTENT' and row:
        if (
            row.get('area_principal') == 'Conversores'
            and row.get('cluster') == 'Arquivos e documentos'
            and row.get('subcluster') == 'Documentos e PDF'
            and row.get('tipo_intencao') == 'conversão de arquivo/mídia'
            and explicit_pdf_format_pair(row.get('Keyword', ''))
        ):
            removed_pdf_pair += 1
            continue
    kept.append(f)

flag_fields = ['severity','issue_code','id_global','Keyword','label','tipo_intencao','reason']
wr(flag_path, kept, flag_fields)

# 3) Recalcula os invariantes finais e reescreve os relatórios.
lot = rd(ROOT / f'lote-{LOT:03d}.csv')
basef = [r for r in classified if r['tipo_registro'] == 'base']
ctrlf = [r for r in classified if r['tipo_registro'] == 'controle']
orig_fields = list(lot[0].keys())
orig_ok = all(all(a[k] == b[k] for k in orig_fields) for a, b in zip(lot, classified))
blank = sum(1 for r in basef if not r['area_principal'] or not r['cluster'] or not r['subcluster'])
direct_missing = sum(
    1 for r in basef
    if r['tipo_intencao'] == 'conversão direta'
    and (not r['unidade_origem'] or not r['unidade_destino'] or not r['direcao_conversao'])
)
prev = rd(ROOT / f'lote-{PREV:03d}-classificado-v1.1-barras-v2.csv')
prev_ctrl = {r['controle_id']: r for r in prev if r['tipo_registro'] == 'controle'}
fields = list(classified[0].keys())
semantic = [k for k in fields if k not in orig_fields]
ctrl_exact = sum(
    1 for r in ctrlf
    if r['controle_id'] in prev_ctrl
    and all(r.get(f, '') == prev_ctrl[r['controle_id']].get(f, '') for f in semantic)
)
goldqa = rd(ROOT / f'lote-{LOT:03d}-golden-qa-v1.1.csv')
gold_exact = sum(r.get('match_exato') == 'sim' for r in goldqa)
conf = Counter(r['confianca'] for r in basef)
review = Counter(r['revisao_manual'] for r in basef)
bars = sum(bool(r.get('keyword_interpretada')) for r in basef)
status = (
    'APROVADO'
    if not kept and direct_missing == 0 and blank == 0 and orig_ok and ctrl_exact == 73 and gold_exact == 107
    else 'REVISAR'
)

report_path.write_text(
    f'''# Relatório de classificação — Lote {LOT:03d} — Taxonomia v1.1 + barras v2\n\n'''
    f'- Keywords base: **{len(basef):,}**\n- Controles: **{len(ctrlf)}**\n- IDs base únicos: **{len({r["id_global"] for r in basef}):,}**\n'
    f'- Reconstruções de `/`: **{bars}**\n- Golden Set v1.1: **{gold_exact}/107**\n'
    f'- Controles incorporados preservados: **{ctrl_exact}/73**\n- Conversões diretas sem metadados: **{direct_missing}**\n- Flags críticas/médias finais: **{len(kept)}**\n\n'
    f'## Confiança\n- alta: **{conf["alta"]:,}**\n- média: **{conf["média"]:,}**\n- baixa: **{conf["baixa"]:,}**\n- revisão manual: **{review["sim"]:,}**\n\n'
    f'## Correções determinísticas v1.4\n- Falsos positivos PDF_CONTENT por par explícito de formatos removidos: **{removed_pdf_pair}**\n',
    encoding='utf-8',
)

audit_path.write_text(
    f'''# Auditoria pós-classificação — Lote {LOT:03d}\n\n## Veredito\n**{status}.**\n\n'''
    f'- Linhas totais: **{len(classified):,}**\n- Base: **{len(basef):,}**\n- Controles: **{len(ctrlf)}**\n'
    f'- IDs únicos: **{len({r["id_global"] for r in basef}):,}**\n- Colunas originais preservadas: **{"sim" if orig_ok else "não"}**\n'
    f'- Área/cluster/subcluster vazios: **{blank}**\n- Golden Set: **{gold_exact}/107**\n- Controles incorporados: **{ctrl_exact}/73**\n'
    f'- Reconstruções `/`: **{bars}**\n- Conversões diretas sem origem/destino/direção: **{direct_missing}**\n'
    f'- Flags finais: **{len(kept)}**\n- Lote {LOT+1:03d}: **{"liberado" if status == "APROVADO" else "não liberado"}**\n\n'
    f'## Revisão v1.4\n- Falsos positivos PDF_CONTENT por par explícito de formatos removidos: **{removed_pdf_pair}**\n',
    encoding='utf-8',
)

print({
    'status': status,
    'removed_pdf_format_pair_flags': removed_pdf_pair,
    'flags': len(kept),
    'direct_missing': direct_missing,
    'gold': gold_exact,
    'controls_exact': ctrl_exact,
    'confidence': dict(conf),
    'review': dict(review),
})
