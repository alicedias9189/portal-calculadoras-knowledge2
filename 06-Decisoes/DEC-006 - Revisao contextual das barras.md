# DEC-006 - Revisão contextual das barras

## Status

**Concluída.**

A revisão semântica foi aplicada aos 3 lotes de candidatos restantes da auditoria de `/`.

## Escopo

- 1.253 linhas candidatas;
- 1.230 keywords únicas;
- a `Keyword` original foi preservada;
- formas por extenso como `um terço` continuam intactas;
- vírgula não foi inferida nesta etapa;
- a decisão de `/` foi feita pelo contexto semântico.

## Resultado

- **256 keywords** promovidas para reconstrução `/` com confiança alta;
- **1 keyword** com reconstrução de confiança média (`150 150 mbps` → possível `150/150 Mbps`);
- **925 keywords** classificadas como não reconstruir;
- **48 keywords** permanecem ambíguas;
- **1 keyword** possui reconstrução parcial confirmada e outro padrão ainda ambíguo.

A revisão resolveu 1.181 das 1.230 keywords sem ambiguidade residual, cerca de 96%.

## Exemplos confirmados

- `1 3 do salário` → `1/3 do salário`;
- `1 12 avos` → `1/12 avos`;
- `arcsen 1 2` → `arcsen 1/2`;
- `1 2 hp em watts` → `1/2 hp em watts`;
- `conversão de 3 4 para mm` → `conversão de 3/4 para mm`;
- `resolução conama 237 97` → `resolução conama 237/97`;
- `regra 85 95 aposentadoria` → `regra 85/95 aposentadoria`;
- `planejamento financeiro 50 30 20` → `planejamento financeiro 50/30/20`;
- `transformador de voltagem 220 110` → `transformador de voltagem 220/110`;
- `resolva as equações exponenciais 1 2 x 1 32` → `resolva as equações exponenciais 1/2 x 1/32`;
- datas como `01 04 2022` → `01/04/2022`.

## Não reconstruir

Foram rejeitados como barra, entre outros:

- valores monetários (`19 99 dólares`);
- taxas como `100 5 do CDI`;
- volumes de produto como `3 6 litros`;
- códigos/modelos;
- progressões, listas e coeficientes matemáticos;
- artigos/parágrafos legais;
- coordenadas;
- valores como `2 80` em pé-direito.

## Ambiguidades remanescentes

As 49 keywords com algum grau de ambiguidade são principalmente expressões matemáticas onde operadores foram removidos e não é possível afirmar onde havia `/`.

Exemplos:

- `calcular 3 2`;
- `calcular 4 3`;
- `resolva a equação x 1 2 3`;
- `resolva as equações 3 2 1 2 3`;
- `resultado de 52 52`.

Há uma reconstrução parcial em `resolva as seguintes proporções 1 7 x 6 49`: `1/7` é confirmada, mas `6 49` continua sem evidência suficiente para afirmar `6/49`.

## Mapa mestre

O mapa automático anterior possuía 583 keywords de confiança alta.

A revisão contextual adicionou 256 keywords de confiança alta. Quatro IDs já existiam no mapa anterior e receberam reconstruções mais completas.

O novo **mapa mestre v2 contém 835 keywords únicas com interpretação de `/` em confiança alta**.

## QA

- duplicatas no mapa contextual alto: 0;
- duplicatas no mapa mestre: 0;
- reconstruções altas iguais à keyword original: 0;
- reconstruções altas sem `/`: 0;
- falsos positivos detectados em contexto monetário, tinta/litros, MMC/MDC ou artigos legais no mapa contextual alto: 0.

## Regra operacional

1. usar `keyword_interpretada` somente quando a reconstrução estiver no mapa mestre de confiança alta;
2. manter `Keyword` como fonte original e referência para as métricas;
3. não propagar automaticamente a única reconstrução de confiança média;
4. manter as 49 keywords com ambiguidade residual em revisão específica;
5. formas por extenso continuam intactas;
6. antes de retomar o lote 002, reauditar o lote 001 usando o mapa mestre v2.

Ver também [[DEC-005 - Reconstrucao de caracteres Google Ads]].
