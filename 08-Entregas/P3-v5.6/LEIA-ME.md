# Portal de Calculadoras — pacote P3 v5.6 (24/10/2026)

Este pacote contém apenas **cópias derivadas** da P3 v5.5. Nenhum arquivo histórico/original foi sobrescrito.

## Resumo

- 100 IDs novos em 52 famílias e 12 temas; 100 pareceres e 100 patches.
- Regressão independente: **60/60 lotes PASSOU**.
- Filtro Ouro reversível: 3.609 registros removidos apenas da visão operacional.
- Pendências P3 sem Ouro: **19.362 → 19.262**; fonte canônica **19.462 → 19.362**.
- Homologação editorial **PENDENTE**.

## Arquivos

- `08-Entregas/P3-v5.6/lotes-001-a-030-p3-v5.6.zip`: fonte canônica atualizada (30 lotes).
- `08-Entregas/P3-v5.6/lotes-001-a-030-p3-v5.6-sem-ouro.zip`: visão operacional atualizada (30 lotes).
- Quatro CSVs `fila` com todas as colunas históricas + oito colunas P3 v5.6.
- `p3-v5.6-pareceres-100.csv`, `p3-v5.6-patches-100.csv`, `p3-v5.6-plano-por-id.csv` e `p3-v5.6-qa-por-grupo.csv`.
- `qa-auditoria-P3-v5.6-centralizada.xlsx`: sete abas, conteúdo centralizado.
- `p3-v5.6-regressao-independente-60-lotes.csv` e resumo JSON.
- Quatro scripts Python em `07-Scripts/P3/`, decisão DEC-093 e registro de continuidade.
- `SHA256SUMS-P3-V5.6.txt` com hashes verificáveis de todos os arquivos internos, exceto ele mesmo.

## Como reproduzir

É necessário também o **pacote P3 v5.5** da rodada anterior, cuja pasta `08-Entregas/P3-v5.5/` deve estar dentro do mesmo diretório-base destes scripts. O pacote v5.6 não inclui uma segunda cópia da base v5.5 de ~25 MB. Não executar contra lotes anteriores a v5.5.

Na raiz do diretório:

```bash
python 07-Scripts/P3/auditar_p3_v56.py
python 07-Scripts/P3/regressao_independente_p3_v56.py
python 07-Scripts/P3/gerar_qa_p3_v56.py
python 07-Scripts/P3/montar_entrega_p3_v56.py
```

Dependência adicional apenas para o Excel: `artifact_tool`. Os demais scripts utilizam a biblioteca padrão Python. A planilha possui cabeçalhos, filtros visuais por abas, textos centralizados e 100 IDs rastreáveis.

**Próxima tarefa:** P3 v5.7 — revisar os 100 pareceres, sem adicionar novos IDs até completar a revisão crítica.