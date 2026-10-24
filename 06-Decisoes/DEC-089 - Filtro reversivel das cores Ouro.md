# DEC-089 — Filtro reversível das cores Ouro e Ouro escuro 1 (sementes de Energia)

**Data:** 2026-10-24. **Base:** P3 v5.2 / DEC-088. **Status:** auditoria técnica validada; **homologação editorial pendente**.

## Evidência de origem
O ZIP `todas_originais_ods.zip` contém 7 planilhas de sementes. Somente `SementesEnergia.ods`, aba `Codex`, contém os estilos de fonte **Ouro `#FFBF00` (3.368 células preenchidas)** e **Ouro escuro 1 `#E8A202` (348)**. Total: **3.716 células**, correspondentes a 3.610 textos normalizados distintos.

A correspondência com os 30 lotes P3 v5.2 foi realizada por texto idêntico (ignorando caixa) ou normalização conservadora (acentos, pontuação, espaços). **Nenhuma regra fuzzy, semelhança aproximada ou exclusão em cascata por família.**

**Resultado:** 3.601 textos de semente encontrados na base de 294.905 registros, em **3.621 IDs**. Desses, **3.609** sem evidência de origem não colorida foram excluídos exclusivamente de **visões derivadas de trabalho**. **12 IDs** também aparecem em células não douradas das sementes e permanecem na fila manual, **sem exclusão automática**. Nove sementes douradas não possuem correspondente na base.

## Impacto das visões derivadas
- Lotes de trabalho: **294.905 → 291.296 registros-base**; os **2.190 controles** são mantidos.
- Fila geral de trabalho: **52.046 → 51.884**; menos 162 IDs (100 P3 elegíveis, 29 P3 previamente tratados e 33 P2). A trilha canônica P2/P3 permanece intacta.
- Fila P3 de trabalho: **23.965 → 23.865**, removendo apenas os 100 elegíveis identificados, sem mexer nos 29 previamente tratados.
- P3 estritamente elegíveis: **19.562 → 19.462**.

## Garantias e limites
- Os 30 lotes derivados foram comparados **linha a linha** com as fontes v5.2: todos os campos de todos os IDs preservados são idênticos. Regressão **30/30 PASSOU**.
- Não modificar nem sobrescrever ZIP, lotes canônicos, valores Google Ads, classificações ou aprovações históricas. Não somar volumes artificiais.
- A cor identifica origem marcada por geração, mas não demonstra ausência de volume de pesquisa real; a exclusão é uma decisão **operacional reversível**, não apagamento definitivo de dados.
- Os arquivos CSV/XLSX e lotes derivados foram disponibilizados em pacote ZIP na conversa ChatGPT; **apenas relatório e scripts** foram versionados no GitHub.

## Reprodução
Consultar `08-Entregas/P3-v5.2-Auditoria-Cores-Ouro/LEIA-ME.md` e três scripts em `07-Scripts/P3/cores/`. Fontes obrigatórias: ZIP com as 7 ODS e ZIP P3 v5.2 completo.

**Próxima etapa:** P3 v5.3, revisar os 75 pareceres v5.2; nas expansões seguintes partir dos 19.462 P3 elegíveis após filtro. Os 12 casos de origem dupla continuam para revisão editorial.