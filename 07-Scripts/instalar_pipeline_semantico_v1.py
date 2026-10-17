#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Monta os scripts reutilizáveis do pipeline semântico v1 dentro do cofre.

O classificador e o finalizador já ficam salvos diretamente em 07-Scripts.
O pós-processador é armazenado em duas partes para facilitar manutenção no cofre;
este instalador concatena as duas partes e cria o arquivo executável completo.

Uso:
    python3 instalar_pipeline_semantico_v1.py

Depois, a partir da pasta que contém os lotes e arquivos de referência:
    python3 07-Scripts/classificar_lote_semantico_v1.py --lote 5 --treino 4 --root .
    python3 07-Scripts/posprocessar_lote_semantico_v1.py --lote 5 --root .
    python3 07-Scripts/finalizar_auditar_lote_v1.py --lote 5 --controle-anterior 4 --root .
"""
from pathlib import Path
import hashlib

HERE = Path(__file__).resolve().parent
PARTS = [
    HERE / "posprocessar_lote_semantico_v1.py.part1",
    HERE / "posprocessar_lote_semantico_v1.py.part2",
]
OUT = HERE / "posprocessar_lote_semantico_v1.py"
EXPECTED_SHA256 = "cd73c777dc89ac56ecb279c113304f9006453d22c68dc81f0110d106377f6207"

missing = [str(p) for p in PARTS if not p.exists()]
if missing:
    raise SystemExit("Partes ausentes: " + ", ".join(missing))

content = b"".join(p.read_bytes() for p in PARTS)
sha = hashlib.sha256(content).hexdigest()
if sha != EXPECTED_SHA256:
    raise SystemExit(
        "Falha de integridade ao montar o pós-processador. "
        f"SHA esperado={EXPECTED_SHA256}; obtido={sha}"
    )

OUT.write_bytes(content)
try:
    OUT.chmod(0o755)
except OSError:
    pass

print(f"Criado: {OUT}")
print(f"SHA-256: {sha}")
