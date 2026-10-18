# Validação semântica das pendências P1 — v2

- **Pendências p1 originais:** 1.093
- **Validados:** 700
- **Validados com ressalva:** 361
- **Pendências ainda abertas:** 32
- **Registros modificados nos lotes:** 1.061
- **Registros base preservados:** 294.905
- **Controles preservados:** 2.190

## Critérios

A análise usa regras semânticas explícitas, por domínio e contexto, aplicadas individualmente a cada termo. Não representa checagem humana independente de todos os 1.093 termos.

- VALIDADO: consulta classificada com confiança contextual suficiente.
- VALIDADO_COM_RESSALVA: área/intenção conhecida, mas são necessários parâmetros adicionais para cálculo (ex.: país do peso, ingrediente, mês calendário, seleção de par ou direção). Não se forçou direção.
- PENDENTE_CONTEXTUAL: consulta sem evidência que sustente decisão segura; mantida pendente para revisão humana.

Os arquivos originais das 16 primeiras colunas, os dados Ads, as keywords e os controles são preservados; somente os IDs com P1 pendente poderiam receber alterações nos campos analíticos. P0 e P2/P3 não foram alterados.

## Limites importantes

O portal de calculadoras deve solicitar dados ausentes. Termos com intenção de busca informacional, comercial ou navegacional foram separados de calculadoras operacionais. Os volumes Ads não foram multiplicados ou somados por variante.

## Exemplos de decisões

- `20mm em polegadas`: direção `mm→in`, segura porque as unidades e a preposição constam na consulta.
- `libra x real`: GBP/BRL identificado, mas **sem direção**; usar escolha bidirecional. A variante `libra para dólar` tem direção explícita.
- `peso em reais`: “peso” não traz país emissor; exigir Argentina, Chile, Colômbia, México etc. antes de calcular.
- `gramas em ml`: conversão física massa↔volume depende de ingrediente/densidade. Não aplicar fator único.
- `24 semanas são quantos meses`: conversão depende da convenção de mês e, em algumas buscas, pode haver contexto gestacional não explicitado.
- `quanto ganha técnico de enfermagem`: busca salarial informativa, não operação aritmética.
- `converter pdf em pdf`: destino idêntico ao formato de origem; pode significar compactação, OCR ou reparo, por isso ficou pendente.

## Abrangência

Esta etapa cobriu todos os 1.093 registros **que ainda estavam pendentes**. Os 1.464 registros anteriores da P1 sem pendência foram preservados, e sua revisão independente integral está fora do escopo desta segunda passagem. Os 32 termos sem evidência suficiente continuam na fila de ambiguidade, devidamente identificados. Não se deve apresentar toda a P1 como completamente aprovada sem essa ressalva.

## Arquivos entregues

- `qa-validacao-semantica-p1-v2-centralizada.xlsx`: planilha completa, com resumo, decisões, ressalvas, pendências, patches, QA e regras; campos centralizados.
- `lotes-001-a-030-p0-p1-v2.zip`: versões novas e paralelas dos 30 lotes; arquivos anteriores permanecem intactos.
- `validacao-semantica-1093-p1-v2.csv`: trilha por keyword, mantendo colunas originais e a decisão v2.
- `p1-v2-pendencias-reais.csv`: apenas 32 termos que seguem sem contexto suficiente.
- `p1-v2-ressalvas-de-operacao.csv`: 361 itens que requerem parâmetros de operação.
- `patches-semanticos-p1-v2.csv`: valores antes/depois de 1.061 alterações analíticas.
- `fila-30-lotes-p0-p1-v2.csv`: fila consolidada; só os IDs P1 verificados foram atualizados.
- `regressao-30-lotes-p1-v2.csv`: testes por lote.
- scripts `.py` de revisão e planilha para reexecução local.
