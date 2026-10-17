# Encerramento da classificação semântica — 30 lotes

Data: 2026-10-17. Taxonomia v1.1, Golden Set v1.1, regras R01–R26 e reconstrução de barras v2.

## Integridade e cobertura

- **30/30 lotes** processados.
- **294.905 keywords base**, com **294.905 IDs únicos**, cobrindo integralmente os IDs de 1 a 294.905.
- **0 IDs duplicados ou ausentes**; **0 keywords tecnicamente duplicadas entre lotes**.
- Colunas originais preservadas em todos os lotes.
- **2.190 controles** (73 por lote), sem divergências de controle entre lotes adjacentes.
- **3.210/3.210** verificações Golden Set (107 por lote).
- **0** flags finais no conjunto dos auditores específicos de cada lote.
- **0** área/cluster/subcluster vazios.
- **835** reconstruções de barras aplicadas.

## Confiança e revisão

- Alta: **199.960**.
- Média: **46.361**.
- Baixa: **48.584**.
- Revisão manual sinalizada: **52.050** keywords (17,65% do total).

A aprovação dos lotes se refere às verificações automatizadas, não à revisão humana integral de cada keyword.

## Exceção histórica relevante

**73** keywords do **lote 001**, com intenção **conversão direta**, seguem sem origem/destino/direção completos. Nos lotes **002–030** há **zero** casos nesse critério.

A pendência deverá ser corrigida após revisão contextual: preencher origem/destino quando inequívocos, ou reclassificar a intenção quando faltarem os parâmetros indispensáveis. Não houve alteração automática do lote 001 nesta auditoria.

O arquivo entregue ao usuário `pendencias-metadados-diretos-lote-001.csv` discrimina as 73 linhas. O relatório `relatorio-consolidado-30-lotes.md` contém todas as métricas e a planilha `auditoria-consolidada-30-lotes-centralizada.xlsx` apresenta resumo, indicadores por lote e pendências.

## Etapas posteriores

1. Saneamento controlado das 73 pendências do lote 001.
2. Revisão humana priorizada dos 52.050 casos sinalizados.
3. Agrupamento em intents, clusters e páginas canônicas, sem somar volumes de close variants do Google Ads.
