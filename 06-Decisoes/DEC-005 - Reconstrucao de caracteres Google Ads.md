# DEC-005 - Reconstrução de caracteres Google Ads

## Contexto

No Google Ads, os caracteres `[]/\\` e `,` não podem ser tratados como texto comum da mesma forma que os demais caracteres usados nas sementes.

A vírgula é especialmente perigosa porque, no fluxo usado para inserir as palavras-chave, ela separa a entrada em partes. Por isso, a reconstrução de vírgulas não deve ser inferida a partir de números separados na base consolidada: ela deve partir das sementes originais.

## Decisão

### Vírgula

Fluxo obrigatório:

1. auditar os arquivos `Sementes*.ods`;
2. localizar somente sementes que realmente continham `,`;
3. registrar arquivo, aba, linha, coluna e célula da semente;
4. dividir a semente nos fragmentos esperados;
5. procurar esses fragmentos nos resultados/consolidados;
6. confirmar a reconstrução somente quando a evidência for suficiente;
7. manter `Keyword` intacta e registrar a interpretação em uma camada separada.

## Auditoria confirmada das sementes

Os 7 arquivos de sementes foram auditados e foram encontradas 4 células com vírgula:

- `SementesMatematica.ods` / `GPT!G1` — `Média, Mediana e Estaística` — cabeçalho;
- `SementesMatematica.ods` / `GPT!W61` — `como arredondar 2,5 corretamente` — keyword real;
- `SementesMatematica.ods` / `GPT!V81` — `converter 0,75 em fração` — keyword real;
- `SementesMatematica.ods` / `GPT2!G1` — `Média, Mediana e Estaística Básica` — cabeçalho.

Portanto, existem somente **2 sementes reais com vírgula** nas sementes atuais.

## Fragmentações confirmadas

### `como arredondar 2,5 corretamente`

No `palavras-chave-Matematica.csv` consolidado aparecem consecutivamente:

- linha 18.927: `como arredondar 2`;
- linha 18.928: `5 corretamente`.

Na base global `unificadas-Todas-corrigida.ods` os dois fragmentos também existem separadamente:

- linha lógica 74.077: `como arredondar 2`;
- linha lógica 9.126: `5 corretamente`.

Reconstrução: **confirmada / confiança alta**.

### `converter 0,75 em fração`

No `palavras-chave-Matematica.csv` consolidado aparecem consecutivamente:

- linha 19.339: `converter 0`;
- linha 19.340: `75 em fração`.

Também aparece a variante relacionada `0 75 em fração` na linha 19.342.

Na base global:

- linha lógica 109.603: `converter 0`;
- linha lógica 10.885: `75 em fração`;
- linha lógica 110: `0 75 em fração`.

Reconstrução: **confirmada / confiança alta**.

## Barra `/` — regra v2

A regra anterior, que tratava `1 3` como baixa confiança por padrão, foi substituída.

O histórico de preparação das sementes confirma que `/` foi o caractere que, em parte do processo, foi substituído por espaço e, em outra parte, simplesmente removido. Por isso, sequências compatíveis com barra removida podem receber **confiança alta quando o contexto semântico confirma a leitura**.

### Formas por extenso

`um terço`, `dois terços`, `um quarto`, `meio` e formas semelhantes **não são reconstruídas**. Não há como distinguir retroativamente se foram escritas assim originalmente ou se resultaram de substituição manual de `1/3`, `2/3`, `1/4` etc. Elas permanecem intactas e são entendidas apenas semanticamente.

### Numéricos com espaço

A decisão é contextual:

- `férias com 1 3` → `férias com 1/3` — confiança alta;
- `cálculo de 1 3 de férias` → `1/3` — alta;
- `como calcular 2 3 de um número` → `2/3` — alta;
- `3 4 polegada` → `3/4 polegada` — alta;
- `dsr horista 1 6` → `1/6` — alta;
- `12 36` em escala/jornada → `12/36` — alta como reconstrução histórica; semanticamente pode ser normalizado depois para `12x36`;
- `potenciação 2 3` → não reconstruir como fração;
- `traço de concreto 1 2 3` → não reconstruir como fração;
- valores como `3 5 litros` ou `1 5 milhão` não recebem `/` automaticamente; ficam como decimal provável/revisão quando o contexto indicar isso.

Nenhum espaço é interpretado como vírgula nesta auditoria. A vírgula continua dependendo da auditoria específica de sementes.

### Unidades compostas

A barra pode ser reconstruída com alta confiança quando a dimensionalidade é coerente, por exemplo:

- `km h` → `km/h`;
- `m s` → `m/s` em contexto de velocidade;
- `MB s` → `MB/s` em contexto de taxa de transferência;
- `g cm3` → `g/cm3`;
- `kg m3` → `kg/m3`;
- `kWh dia` → `kWh/dia`;
- `kWh mês` → `kWh/mês`.

Tokens concatenados pela remoção completa de `/` também podem ser recuperados quando o contexto confirma a unidade: `MBs`, `GBs`, `KBs`, `kmh` e `ms` em conversões de velocidade/taxa.

## Auditoria v2 executada

O script `auditar_barras_v2.py` foi aplicado aos 7 arquivos de sementes e à base global corrigida de 294.905 keywords.

### Sementes

- 14 células com `/` explícita;
- 8 fora da linha 1, correspondendo às keywords explícitas já identificadas em Conversores;
- 49 ocorrências de formas por extenso detectadas e deliberadamente ignoradas como reconstrução histórica;
- 38 achados sanitizados analisados;
- nas sementes, os três casos `1 3` ligados a férias foram promovidos para reconstrução de confiança alta;
- `traço de concreto 1 2 3` foi explicitamente bloqueado como fração.

### Base global

- 2.166 achados contextuais auditados;
- **583 keywords únicas** receberam uma `keyword_interpretada` de confiança alta;
- **1.230 keywords únicas** continuam em revisão contextual;
- os casos de revisão foram divididos em 3 lotes de até 500 registros;
- o QA não encontrou conflito entre reconstruções de fração alta e contexto de potência ou contexto decimal forte.

### Impacto imediato nos lotes semânticos

- Lote 001: 8 keywords com reconstrução de confiança alta;
- Lote 002: 13 keywords com reconstrução de confiança alta.

Exemplos do lote 001:

- `1 mach km h` → `1 mach km/h`;
- `5 32 polegadas em mm` → `5/32 polegadas em mm`;
- `abono pecuniário vende 1 3` → `abono pecuniário vende 1/3`;
- `mb s mbps` → `MB/s mbps`.

Exemplos do lote 002:

- `3 4 polegada é igual a quantos milimetros` → `3/4 polegada é igual a quantos milimetros`;
- `calculo de 1 3 de ferias na rescisão` → `calculo de 1/3 de ferias na rescisão`;
- `como calcular 2 3 de um numero` → `como calcular 2/3 de um numero`;
- `dsr horista 1 6` → `dsr horista 1/6`;
- `g cm3 para kg m3` → `g/cm3 para kg/m3`;
- `kwh dia` → `kWh/dia`;
- `turno 12 36` → `turno 12/36`.

## Regra de preservação

A coluna original `Keyword` nunca deve ser sobrescrita. Reconstruções ficam em campos paralelos:

- `keyword_interpretada`;
- `tipo_reconstrucao`;
- `confianca_reconstrucao`;
- `motivo`;
- `semente_origem`, quando houver evidência direta.

## Uso operacional

As 583 reconstruções de confiança alta podem ser usadas como contexto semântico nos lotes, mantendo a keyword original para rastreabilidade e métricas. Os 1.230 casos restantes devem ser revisados por lotes antes de qualquer promoção para confiança alta.

Antes de retomar a classificação do lote 002, o lote 001 deve ser rechecado contra as 8 reconstruções de alta confiança que o afetam.
