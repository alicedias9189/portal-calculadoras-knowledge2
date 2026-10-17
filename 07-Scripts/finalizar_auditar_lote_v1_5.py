#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finalizador/Auditor semântico v1.5 — Taxonomia v1.1 + barras v2.

Camada complementar ao `finalizar_auditar_lote_v1_4.py`.

Novidade validada no lote 011:
- consultas de custo/gasto/valor de combustível vinculadas a rota, trajeto ou
  distância (`por km`, `km rodado`, `rota`) são cálculo de custo de viagem,
  não preço de mercado nem simples consumo/autonomia.
- reclassifica esses casos para:
  Energia > Combustíveis > Custo de viagem
  com intenção `estimativa de custo`.

Uso:
  python3 finalizar_auditar_lote_v1_5.py --lote 11 --controle-anterior 10 --root .

O script preserva integralmente as colunas originais do lote e executa primeiro
todas as camadas anteriores via v1.4.
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
    help='Caminho do finalizar_auditar_lote_v1_4.py. Padrão: root/finalizar_auditar_lote_v1_4.py',
)
args = parser.parse_args()

LOT = args.lote
PREV = args.controle_anterior or LOT - 1
ROOT = Path(args.root).resolve()
PREVIOUS_FINALIZER = (
    Path(args.finalizador_anterior).resolve()
    if args.finalizador_anterior
    else ROOT / 'finalizar_auditar_lote_v1_4.py'
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


def fuel_cost_context(text):
    """Retorna True quando a keyword pede custo/gasto de combustível ligado ao deslocamento."""
    t = norm(text)
    fuel = bool(re.search(r'\b(combustivel|gasolina|etanol|diesel)\b', t))
    cost = bool(re.search(r'\b(custo|gasto|gastar|valor|despesa|reais)\b', t))
    travel = bool(re.search(
        r'\b(por km|km rodado|quilometro rodado|por quilometro|rota|trajeto|viagem|distancia|percurso)\b',
        t,
    ))
    return fuel and cost and travel


subprocess.run([
    sys.executable,
    str(PREVIOUS_FINALIZER),
    '--lote', str(LOT),
    '--controle-anterior', str(PREV),
    '--root', str(ROOT),
], check=True)

class_path = ROOT / f'lote-{LOT:03d}-classificado-v1.1-barras-v2.csv'
flag_path = ROOT / f'auditoria-pos-classificacao-lote-{LOT:03d}-v1.1-barras-v2-final-flags.csv'
report_path = ROOT / f'relatorio-classificacao-lote-{LOT:03d}-v1.1-barras-v2.md'
audit_path = ROOT / f'auditoria-pos-classificacao-lote-{LOT:03d}-v1.1-barras-v2-final.md'

classified = rd(class_path)
patched_ids = set()

for r in classified:
    if r.get('tipo_registro') != 'base':
        continue
    if not fuel_cost_context(r.get('Keyword', '')):
        continue
    if r.get('area_principal') == 'Energia' and r.get('cluster') == 'Combustíveis':
        r['area_principal'] = 'Energia'
        r['cluster'] = 'Combustíveis'
        r['subcluster'] = 'Custo de viagem'
        r['intencao_principal'] = 'Estimar custo: Custo de viagem'
        r['tipo_intencao'] = 'estimativa de custo'
        r['dominio_ou_grandeza'] = 'Combustíveis'
        r['unidade_origem'] = ''
        r['unidade_destino'] = ''
        r['direcao_conversao'] = ''
        r['confianca'] = 'alta'
        r['revisao_manual'] = 'não'
        r['justificativa_curta'] = (
            'Custo/gasto de combustível vinculado a rota ou distância; '
            'é estimativa de custo de viagem, não cotação/preço de mercado nem conversão.'
        )
        patched_ids.add(r['id_global'])

wr(class_path, classified, list(classified[0].keys()))

flags = rd(flag_path)
kept = []
removed_fuel_flags = 0
for f in flags:
    if f.get('issue_code') == 'FUEL_MARKET' and f.get('id_global') in patched_ids:
        removed_fuel_flags += 1
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
    f'## Correções determinísticas v1.5\n- Keywords de custo/gasto de combustível ligado a deslocamento reclassificadas: **{len(patched_ids)}**\n'
    f'- Flags FUEL_MARKET removidas após correção contextual: **{removed_fuel_flags}**\n',
    encoding='utf-8',
)

audit_path.write_text(
    f'''# Auditoria pós-classificação — Lote {LOT:03d}\n\n## Veredito\n**{status}.**\n\n'''
    f'- Linhas totais: **{len(classified):,}**\n- Base: **{len(basef):,}**\n- Controles: **{len(ctrlf)}**\n'
    f'- IDs únicos: **{len({r["id_global"] for r in basef}):,}**\n- Colunas originais preservadas: **{"sim" if orig_ok else "não"}**\n'
    f'- Área/cluster/subcluster vazios: **{blank}**\n- Golden Set: **{gold_exact}/107**\n- Controles incorporados: **{ctrl_exact}/73**\n'
    f'- Reconstruções `/`: **{bars}**\n- Conversões diretas sem origem/destino/direção: **{direct_missing}**\n'
    f'- Flags finais: **{len(kept)}**\n- Lote {LOT+1:03d}: **{"liberado" if status == "APROVADO" else "não liberado"}**\n\n'
    f'## Revisão v1.5\n- Casos de custo/gasto de combustível por distância/rota corrigidos: **{len(patched_ids)}**\n'
    f'- Flags FUEL_MARKET removidas após correção contextual: **{removed_fuel_flags}**\n',
    encoding='utf-8',
)

print({
    'status': status,
    'patched_fuel_cost_rows': len(patched_ids),
    'removed_fuel_market_flags': removed_fuel_flags,
    'flags': len(kept),
    'direct_missing': direct_missing,
    'gold': gold_exact,
    'controls_exact': ctrl_exact,
    'confidence': dict(conf),
    'review': dict(review),
})
