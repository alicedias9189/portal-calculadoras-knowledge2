# LEIA-ME — Entrega única P3 v2.9

O pacote contém a revisão crítica dos 66 patches aplicados na v2.8. Esta é a versão paralela seguinte e **não deve substituir a v2.8 sem preservar a versão histórica**.

## Importação manual no repositório/vault

1. Descompacte o ZIP em uma pasta temporária.
2. Confira `SHA256SUMS-P3-V2.9.txt` (via `sha256sum -c SHA256SUMS-P3-V2.9.txt` na raiz do pacote).
3. Leia `06-Decisoes/DEC-065 - Revisao critica 66 ajustes P3 v2.8.md` e `08-Entregas/P3-v2.9/RELATORIO-P3-V2.9.md`.
4. Copie os arquivos na estrutura de diretórios do repositório, sem apagar a v2.8 nem históricos de decisões.
5. Importe os 30 lotes v2.9 apenas como nova versão; a P2 e o backlog global de 98 não foram alterados.
6. Faça seu commit manualmente.

## Principais artefatos

- `08-Entregas/P3-v2.9/lotes-001-a-030-p3-v2.9.zip`
- `08-Entregas/P3-v2.9/p3-v2.9-fila-23965.csv`
- `08-Entregas/P3-v2.9/fila-geral-p0-p1-p2-p3-v2.9.csv`
- `08-Entregas/P3-v2.9/p3-v2.9-revisao-66.csv` (parecer por ID)
- `08-Entregas/P3-v2.9/p3-v2.9-patches.csv` (antes/depois)
- `08-Entregas/P3-v2.9/qa-auditoria-P3-v2.9-centralizada.xlsx`
- `07-Scripts/P3/` (auditador, regressão independente e geração de QA, scripts reutilizáveis)
- `08-Entregas/P3-v2.9/FONTES-REPRODUCAO/` (dados completos para reexecutar)

## Reexecução

Na raiz do pacote, com Python 3.10+:

```
python 07-Scripts/P3/auditar_p3_v29.py
python 07-Scripts/P3/regressao_independente_p3_v29.py
python 07-Scripts/P3/gerar_qa_p3_v29.py
```

A geração da planilha requer `artifact_tool`. Os outros dois scripts usam somente a biblioteca padrão.

**Nenhum repositório GitHub foi alterado automaticamente.**
