#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finalizador compatível com o pipeline v1, acrescentando a revisão PDF/content
introduzida no lote 005.

Uso recomendado:
  python3 finalizar_auditar_lote_v1_1.py --lote 5 --controle-anterior 4 --root .

Por padrão chama `finalizar_auditar_lote_v1.py` na mesma pasta/root e depois
aplica somente correções determinísticas de PDF que foram validadas na auditoria.
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
parser.add_argument('--finalizador', default='', help='Caminho do finalizar_auditar_lote_v1.py. Padrão: root/finalizar_auditar_lote_v1.py')
args = parser.parse_args()
LOT = args.lote
PREV = args.controle_anterior or LOT - 1
ROOT = Path(args.root).resolve()
FINALIZER = Path(args.finalizador).resolve() if args.finalizador else ROOT / 'finalizar_auditar_lote_v1.py'


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


def is_pdf_format_conversion(t):
    if 'pdf' not in t:
        return False
    return bool(
        re.search(r'\bpara pdf\b|\bpdf para\b', t)
        or re.search(r'\b(converter|conversor|transformar|passar|colocar|juntar|gerar|enviar|montar|conversao|ocr|ilovepdf)\b', t)
        or re.search(r'\b(pdf|arquivo|foto|imagem|documento)\b.*\b(para|em|como)\b.*\b(word|docx|jpg|jpeg|png|pdf|excel|xlsx)\b', t)
        or re.search(r'\b(pdf escaneado|escaneado)\b.*\b(word|docx)\b', t)
        or re.search(r'\beditar\b.*\bpdf\b.*\b(word|docx)\b', t)
        or re.search(r'\bpdf\b.*\beditar\b.*\b(word|docx)\b', t)
    )


def patch_semantic_row(r):
    t = norm(r.get('Keyword', ''))
    changed = False
    if 'pdf' in t and re.search(r'\bconversao de medidas\b', t):
        r['area_principal'] = 'Conversores'
        r['cluster'] = 'Conversões gerais'
        r['subcluster'] = 'Conversor genérico de unidades'
        r['intencao_principal'] = 'Consultar referência: Conversor genérico de unidades'
        r['tipo_intencao'] = 'tabela/referência'
        r['dominio_ou_grandeza'] = 'Conversor genérico de unidades'
        r['unidade_origem'] = r['unidade_destino'] = r['direcao_conversao'] = ''
        r['confianca'] = 'alta'
        r['revisao_manual'] = 'não'
        r['justificativa_curta'] = 'PDF é suporte/referência para conversão de medidas, não conversão de formato de arquivo.'
        changed = True
    elif 'pdf' in t and re.search(r'\b(editar|modificar|alterar|tornar)\b', t) and not re.search(r'\b(word|docx|jpg|jpeg|png|excel|xlsx|texto|txt)\b', t):
        r['area_principal'] = 'Fora de escopo'
        r['cluster'] = 'Serviços/software'
        r['subcluster'] = 'Consulta navegacional'
        r['intencao_principal'] = 'Fora de escopo: Consulta navegacional'
        r['tipo_intencao'] = 'fora de escopo'
        r['dominio_ou_grandeza'] = 'Consulta navegacional'
        r['unidade_origem'] = r['unidade_destino'] = r['direcao_conversao'] = ''
        r['confianca'] = 'alta'
        r['revisao_manual'] = 'não'
        r['justificativa_curta'] = 'Edição de PDF sem conversão de formato explícita; fora do escopo do portal de conversores.'
        changed = True
    return changed


cmd = [sys.executable, str(FINALIZER), '--lote', str(LOT), '--controle-anterior', str(PREV), '--root', str(ROOT)]
subprocess.run(cmd, check=True)

class_path = ROOT / f'lote-{LOT:03d}-classificado-v1.1-barras-v2.csv'
flag_path = ROOT / f'auditoria-pos-classificacao-lote-{LOT:03d}-v1.1-barras-v2-final-flags.csv'
report_path = ROOT / f'relatorio-classificacao-lote-{LOT:03d}-v1.1-barras-v2.md'
audit_path = ROOT / f'auditoria-pos-classificacao-lote-{LOT:03d}-v1.1-barras-v2-final.md'

classified = rd(class_path)
fields = list(classified[0].keys())
patched = 0
for r in classified:
    if r.get('tipo_registro') == 'base' and patch_semantic_row(r):
        patched += 1
wr(class_path, classified, fields)

flags = rd(flag_path)
by_id = {r['id_global']: r for r in classified if r.get('tipo_registro') == 'base'}
kept = []
for f in flags:
    if f.get('issue_code') != 'PDF_CONTENT':
        kept.append(f); continue
    row = by_id.get(f.get('id_global'))
    t = norm((row or {}).get('Keyword', f.get('Keyword', '')))
    resolved = row and not (row.get('area_principal') == 'Conversores' and row.get('cluster') == 'Arquivos e documentos')
    if resolved or is_pdf_format_conversion(t):
        continue
    kept.append(f)
flag_fields = ['severity','issue_code','id_global','Keyword','label','tipo_intencao','reason']
wr(flag_path, kept, flag_fields)

lot = rd(ROOT / f'lote-{LOT:03d}.csv')
basef = [r for r in classified if r['tipo_registro'] == 'base']
ctrlf = [r for r in classified if r['tipo_registro'] == 'controle']
orig_fields = list(lot[0].keys())
orig_ok = all(all(a[k] == b[k] for k in orig_fields) for a, b in zip(lot, classified))
blank = sum(1 for r in basef if not r['area_principal'] or not r['cluster'] or not r['subcluster'])
direct_missing = sum(1 for r in basef if r['tipo_intencao'] == 'conversão direta' and (not r['unidade_origem'] or not r['unidade_destino'] or not r['direcao_conversao']))
prev = rd(ROOT / f'lote-{PREV:03d}-classificado-v1.1-barras-v2.csv')
prev_ctrl = {r['controle_id']: r for r in prev if r['tipo_registro'] == 'controle'}
semantic = [k for k in fields if k not in orig_fields]
ctrl_exact = sum(1 for r in ctrlf if all(r.get(f, '') == prev_ctrl[r['controle_id']].get(f, '') for f in semantic))
goldqa = rd(ROOT / f'lote-{LOT:03d}-golden-qa-v1.1.csv')
gold_exact = sum(r.get('match_exato') == 'sim' for r in goldqa)
conf = Counter(r['confianca'] for r in basef)
review = Counter(r['revisao_manual'] for r in basef)
status = 'APROVADO' if not kept and direct_missing == 0 and blank == 0 and orig_ok and ctrl_exact == 73 and gold_exact == 107 else 'REVISAR'

report_path.write_text(
    f'''# Relatório de classificação — Lote {LOT:03d} — Taxonomia v1.1 + barras v2\n\n'''
    f'- Keywords base: **{len(basef):,}**\n- Controles: **{len(ctrlf)}**\n- IDs base únicos: **{len({r["id_global"] for r in basef}):,}**\n'
    f'- Reconstruções de `/`: **{sum(bool(r.get("keyword_interpretada")) for r in basef)}**\n- Golden Set v1.1: **{gold_exact}/107**\n'
    f'- Controles incorporados preservados: **{ctrl_exact}/73**\n- Conversões diretas sem metadados: **{direct_missing}**\n- Flags críticas/médias finais: **{len(kept)}**\n\n'
    f'## Confiança\n- alta: **{conf["alta"]:,}**\n- média: **{conf["média"]:,}**\n- baixa: **{conf["baixa"]:,}**\n- revisão manual: **{review["sim"]:,}**\n\n'
    f'A revisão PDF/content distinguiu criação/conversão de PDF, edição pura de PDF e PDFs de referência de unidades. Correções semânticas aplicadas: **{patched}**.\n',
    encoding='utf-8'
)

audit_path.write_text(
    f'''# Auditoria pós-classificação — Lote {LOT:03d}\n\n## Veredito\n**{status}.**\n\n'''
    f'- Linhas totais: **{len(classified):,}**\n- Base: **{len(basef):,}**\n- Controles: **{len(ctrlf)}**\n'
    f'- IDs únicos: **{len({r["id_global"] for r in basef}):,}**\n- Colunas originais preservadas: **{"sim" if orig_ok else "não"}**\n'
    f'- Área/cluster/subcluster vazios: **{blank}**\n- Golden Set: **{gold_exact}/107**\n- Controles incorporados: **{ctrl_exact}/73**\n'
    f'- Reconstruções `/`: **{sum(bool(r.get("keyword_interpretada")) for r in basef)}**\n- Conversões diretas sem origem/destino/direção: **{direct_missing}**\n'
    f'- Flags finais: **{len(kept)}**\n- Lote {LOT+1:03d}: **{"liberado" if status == "APROVADO" else "não liberado"}**\n',
    encoding='utf-8'
)

print({'status': status, 'patched_pdf_rows': patched, 'flags': len(kept), 'direct_missing': direct_missing, 'gold': gold_exact, 'controls_exact': ctrl_exact})
