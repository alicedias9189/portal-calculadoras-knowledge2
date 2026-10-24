# DEC-086 — Expansão seletiva P3 v5.0

**Data:** 24/10/2026. **Fonte:** P3 v4.9 (DEC-085). **Situação:** auditoria técnica validada, homologação editorial **PENDENTE**.

## Escopo

Seleção fechada de **75 novos IDs / 49 famílias**, dentre **19.712 P3 estritamente elegíveis**, em oito temas: potenciação matemática (17), geometria/perímetro (14), estatística descritiva (12), probabilidade (9), regra de três (8), BTU/h versus potência elétrica (7), descontos de benefícios trabalhistas (4) e contagem de prazos (4).

Não reabrir as 75 classificações revisadas na v4.9; não misturar P2 ou as 98 propostas globais.

## Salvaguardas semânticas

- Potência numérica não é consumo de eletricidade; “potência de 23” não autoriza interpretar 2³ sem contexto.
- Área isolada não define perímetro sem forma geométrica e dados complementares.
- Média, mediana e moda são medidas diferentes; não presumir amostra.
- Probabilidade de interseção não implica independência; cálculos dependem de eventos e parâmetros.
- BTU/h indica capacidade térmica, não potência elétrica em watts: eficiência e modelo são necessários.
- Desconto de vale-refeição/alimentação não é juros de cartão; regras dependem de contexto contratual e normativo.
- Dias corridos diferem de dias úteis, que dependem de feriados e calendário aplicável.

## Regressão independente

**30/30 lotes; 75/75 patches.** Preservados **294.905 registros-base**, **2.190 controles**, **4.660 pendências P2** e **98 propostas globais** (arquivo global byte a byte idêntico). Filas de 23.965 e 52.046 linhas: **374 colunas históricas idênticas**; oito novas colunas exclusivamente de rastreabilidade v5.0.

SHA-256 dos campos protegidos: `7be09e2ffc2cecbf3e267c82cb7d737c5f5ffabeea02536634bebf208ddd1055`.

P3 elegíveis restantes: **19.637**.

## Arquivos e sequência

Os CSVs completos, ZIP com 30 lotes, plano por ID, patches, pareceres, QA XLSX, scripts reexecutáveis e fontes v4.9 estão no pacote **portal-calculadoras-auditoria-P3-v5.0-unico.zip**, entregue na conversa ChatGPT de 24/10/2026. Arquivos binários **não foram enviados ao repositório nesta etapa**.

**Próxima tarefa:** P3 v5.1, revisão crítica individual das 75 propostas v5.0, sem expandir novos IDs; homologação editorial continua pendente.
