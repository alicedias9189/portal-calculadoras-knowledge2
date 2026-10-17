#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finalizador/Auditor semântico v1.3 — Taxonomia v1.1 + barras v2.

Camada complementar ao `finalizar_auditar_lote_v1_2.py`.

Novidades validadas no lote 007:
- R21 reforçada: inclui licença/folga por casamento quando a consulta é sobre
  direito ou quantidade de dias.
- PDF_CONTENT: reconhece conversões implícitas como `fotos em pdf`,
  `pagina web em pdf` e pares de formatos em contexto de download/ferramenta.
- Edição/manipulação de PDF sem troca de formato (ex.: mudar cor, quebrar PDF)
  é redirecionada para Fora de escopo > Conteúdo técnico/produto.

Uso:
  python3 finalizar_auditar_lote_v1_3.py --lote 7 --controle-anterior 6 --root .

O script preserva integralmente as colunas originais do lote.
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
    help='Caminho do finalizar_auditar_lote_v1_2.py. Padrão: root/finalizar_auditar_lote_v1_2.py',
)
args = parser.parse_args()

LOT = args.lote
PREV = args.controle_anterior or LOT - 1
ROOT = Path(args.root).resolve()
PREVIOUS_FINALIZER = (
    Path(args.finalizador_anterior).resolve()
    if args.finalizador_anterior
    else ROOT / 'finalizar_auditar_lote_v1_2.py'
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


def patch_work_rights(row):
    """Aplica R21 quando dias/direito decorrem de licença/folga trabalhista."""
    t = norm(row.get('Keyword', ''))

    parental = bool(
        re.search(r'\b(pai|mae|maternidade|paternidade|nascimento do filho|nascimento de filho)\b', t)
    )
    marriage = bool(re.search(r'\b(casamento|casar|casou|casamento civil)\b', t))
    days_or_right = bool(re.search(r'\b(quantos dias|direito|dias de folga|folga)\b', t))

    if row.get('area_principal') != 'Datas' or not ((parental or marriage) and days_or_right):
        return False
    if re.search(r'\b(viagem|hotel|turismo|lua de mel)\b', t):
        return False

    row['area_principal'] = 'Trabalho'
    row['cluster'] = 'Afastamentos'
    row['subcluster'] = 'Licenças e afastamentos'
    row['intencao_principal'] = 'Consultar informação: Licenças e afastamentos'
    row['tipo_intencao'] = 'informacional'
    row['dominio_ou_grandeza'] = 'licenças e afastamentos trabalhistas'
    row['unidade_origem'] = ''
    row['unidade_destino'] = ''
    row['direcao_conversao'] = ''
    row['confianca'] = 'alta'
    row['revisao_manual'] = 'não'
    row['justificativa_curta'] = (
        'R21: quantidade de dias/direito de licença ou folga regida por regra trabalhista; '
        'não é simples diferença entre datas.'
    )
    return True


def patch_pdf_nonconversion(row):
    """Retira de Conversores manipulações de PDF que não convertem formato."""
    if row.get('area_principal') != 'Conversores' or row.get('subcluster') != 'Documentos e PDF':
        return False
    t = norm(row.get('Keyword', ''))
    if 'pdf' not in t:
        return False
    # Não tirar de Conversores quando há destino/origem de formato explícito.
    if obvious_pdf_format_conversion(t):
        return False
    manipulation = bool(
        re.search(r'\b(mudar|alterar) a cor (?:do|de) pdf\b', t)
        or re.search(r'\b(quebrar|dividir|separar) pdf\b', t)
    )
    if not manipulation:
        return False
    row['area_principal'] = 'Fora de escopo'
    row['cluster'] = 'Conteúdo técnico/produto'
    row['subcluster'] = 'Consulta técnica não conversível'
    row['intencao_principal'] = 'Fora de escopo: Consulta técnica não conversível'
    row['tipo_intencao'] = 'fora de escopo'
    row['dominio_ou_grandeza'] = 'edição/manipulação de PDF'
    row['unidade_origem'] = ''
    row['unidade_destino'] = ''
    row['direcao_conversao'] = ''
    row['confianca'] = 'alta'
    row['revisao_manual'] = 'não'
    row['justificativa_curta'] = (
        'Manipulação/edição de PDF sem troca de formato; fora do escopo dos conversores definidos.'
    )
    return True


def obvious_pdf_format_conversion(t):
    """Reconhece intenção inequívoca de transformar conteúdo/formato para/de PDF."""
    if 'pdf' not in t:
        return False
    formats = set(re.findall(r'\b(pdf|word|docx|jpg|jpeg|png|excel|xlsx|foto|fotos|imagem|imagens)\b', t))
    web_to_pdf = bool(re.search(r'\bpagina (?:da )?web\b.*\bem pdf\b', t))
    format_pair = len(formats) >= 2 or web_to_pdf
    return bool(
        re.search(r'\bpara pdf\b|\bpdf para\b', t)
        or re.search(
            r'\b(converter|converte|convertendo|convertido|conversor|conversao|transformar|passar|colocar|juntar|gerar|montar|ocr|ilovepdf)\b',
            t,
        )
        or re.search(r'\b(foto|fotos|imagem|imagens|pagina web|pagina da web)\b.*\bem pdf\b', t)
        or re.search(r'\b(word|docx|jpg|jpeg|png|excel|xlsx|foto|imagem|arquivo|documento)\b.*\b(em|para)\b.*\bpdf\b', t)
        or re.search(r'\bpdf\b.*\b(em|para)\b.*\b(word|docx|jpg|jpeg|png|excel|xlsx|texto|txt)\b', t)
        or (format_pair and re.search(r'\b(baixar|gratis|online|site|ferramenta)\b', t))
    )


# 1) Executa a camada anterior completa.
cmd = [
    sys.executable,
    str(PREVIOUS_FINALIZER),
    '--lote', str(LOT),
    '--controle-anterior', str(PREV),
    '--root', str(ROOT),
]
subprocess.run(cmd, check=True)

# 2) Aplica R21 reforçada no classificado.
class_path = ROOT / f'lote-{LOT:03d}-classificado-v1.1-barras-v2.csv'
flag_path = ROOT / f'auditoria-pos-classificacao-lote-{LOT:03d}-v1.1-barras-v2-final-flags.csv'
report_path = ROOT / f'relatorio-classificacao-lote-{LOT:03d}-v1.1-barras-v2.md'
audit_path = ROOT / f'auditoria-pos-classificacao-lote-{LOT:03d}-v1.1-barras-v2-final.md'

classified = rd(class_path)
fields = list(classified[0].keys())
patched_rights = 0
patched_pdf_nonconversion = 0
for row in classified:
    if row.get('tipo_registro') != 'base':
        continue
    if patch_work_rights(row):
        patched_rights += 1
    if patch_pdf_nonconversion(row):
        patched_pdf_nonconversion += 1
wr(class_path, classified, fields)

# 3) Limpa somente flags que foram resolvidas deterministicamente.
flags = rd(flag_path)
by_id = {r['id_global']: r for r in classified if r.get('tipo_registro') == 'base'}
kept = []
removed_rights = 0
removed_pdf = 0
for f in flags:
    row = by_id.get(f.get('id_global'))
    if f.get('issue_code') == 'WORK_RIGHTS_DATE' and row:
        if (
            row.get('area_principal') == 'Trabalho'
            and row.get('cluster') == 'Afastamentos'
            and row.get('subcluster') == 'Licenças e afastamentos'
        ):
            removed_rights += 1
            continue
    if f.get('issue_code') == 'PDF_CONTENT':
        t = norm((row or {}).get('Keyword', f.get('Keyword', '')))
        if row and row.get('area_principal') != 'Conversores':
            removed_pdf += 1
            continue
        if obvious_pdf_format_conversion(t):
            removed_pdf += 1
            continue
    kept.append(f)

flag_fields = ['severity','issue_code','id_global','Keyword','label','tipo_intencao','reason']
wr(flag_path, kept, flag_fields)

# 4) Recalcula todos os invariantes finais.
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
    f'## Correções determinísticas v1.3\n- R21/licenças/folgas trabalhistas corrigidas: **{patched_rights}**\n'
    f'- Manipulações de PDF fora de escopo corrigidas: **{patched_pdf_nonconversion}**\n'
    f'- Flags WORK_RIGHTS_DATE resolvidas: **{removed_rights}**\n- Flags PDF_CONTENT resolvidas contextualmente: **{removed_pdf}**\n',
    encoding='utf-8',
)

audit_path.write_text(
    f'''# Auditoria pós-classificação — Lote {LOT:03d}\n\n## Veredito\n**{status}.**\n\n'''
    f'- Linhas totais: **{len(classified):,}**\n- Base: **{len(basef):,}**\n- Controles: **{len(ctrlf)}**\n'
    f'- IDs únicos: **{len({r["id_global"] for r in basef}):,}**\n- Colunas originais preservadas: **{"sim" if orig_ok else "não"}**\n'
    f'- Área/cluster/subcluster vazios: **{blank}**\n- Golden Set: **{gold_exact}/107**\n- Controles incorporados: **{ctrl_exact}/73**\n'
    f'- Reconstruções `/`: **{bars}**\n- Conversões diretas sem origem/destino/direção: **{direct_missing}**\n'
    f'- Flags finais: **{len(kept)}**\n- Lote {LOT+1:03d}: **{"liberado" if status == "APROVADO" else "não liberado"}**\n\n'
    f'## Revisão v1.3\n- R21/licenças/folgas trabalhistas corrigidas: **{patched_rights}**\n'
    f'- Manipulações de PDF fora de escopo corrigidas: **{patched_pdf_nonconversion}**\n'
    f'- Falsos positivos PDF_CONTENT removidos: **{removed_pdf}**\n',
    encoding='utf-8',
)

print({
    'status': status,
    'patched_work_rights': patched_rights,
    'patched_pdf_nonconversion': patched_pdf_nonconversion,
    'removed_work_rights_flags': removed_rights,
    'removed_pdf_flags': removed_pdf,
    'flags': len(kept),
    'direct_missing': direct_missing,
    'gold': gold_exact,
    'controls_exact': ctrl_exact,
    'confidence': dict(conf),
    'review': dict(review),
})
