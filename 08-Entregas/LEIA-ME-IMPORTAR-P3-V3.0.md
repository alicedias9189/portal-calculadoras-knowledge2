# Portal de Calculadoras — importar a P3 v3.0 no cofre/GitHub

1. Extraia o arquivo ZIP **sem alterar os nomes internos**.
2. Confirme os arquivos com `sha256sum -c SHA256SUMS-P3-V3.0.txt` (Linux).
3. Leia `08-Entregas/P3-v3.0/RELATORIO-P3-V3.0.md` e a `06-Decisoes/DEC-066`.
4. Copie a estrutura de pastas para o cofre/repositório. O ZIP foi preparado para importação **manual**, não houve push automático.
5. Faça commit após inspecionar os 36 patches e o histórico.

## Principais arquivos

- `08-Entregas/P3-v3.0/lotes-001-a-030-p3-v3.0.zip` — todos os 30 lotes atualizados.
- `08-Entregas/P3-v3.0/p3-v3.0-fila-23965.csv` — fila P3 completa.
- `08-Entregas/P3-v3.0/fila-geral-p0-p1-p2-p3-v3.0.csv` — fila geral completa.
- `08-Entregas/P3-v3.0/p3-v3.0-decisoes.csv` — 36 decisões por ID.
- `08-Entregas/P3-v3.0/p3-v3.0-patches.csv` — valores antes/depois por campo.
- `08-Entregas/P3-v3.0/qa-auditoria-P3-v3.0-centralizada.xlsx` — QA com todas as células usadas centralizadas.
- `07-Scripts/P3/auditar_p3_v30.py`, `regressao_independente_p3_v30.py`, `gerar_qa_p3_v30.py` — scripts reutilizáveis.
- `08-Entregas/P3-v3.0/FONTES-REPRODUCAO/` — insumos v2.9 para reexecução.
- `08-Continuidade/ESTADO-ATUAL.md` e registro datado — pontos de retomada.

## Reexecução

No diretório raiz extraído, rode:

```bash
python3 07-Scripts/P3/auditar_p3_v30.py
python3 07-Scripts/P3/regressao_independente_p3_v30.py
python3 07-Scripts/P3/gerar_qa_p3_v30.py
```

Os três scripts usam os dados locais incluídos no próprio ZIP. A reprodução dos arquivos de lotes deve ser avaliada pelo conteúdo dos 30 CSVs internos (o arquivo ZIP pode apresentar diferenças de metadata).
