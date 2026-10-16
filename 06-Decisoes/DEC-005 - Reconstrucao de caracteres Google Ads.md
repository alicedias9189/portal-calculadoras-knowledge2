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

## Arquivos individuais do Google Ads

Os quatro fragmentos exatos das duas reconstruções não foram encontrados nos 13 arquivos individuais `Keyword Stats ...csv` de Matemática. A evidência está no consolidado `palavras-chave-Matematica.csv` e na base global.

## Barra `/`

A barra deve ser tratada em fase separada. Não se deve inferir `/` automaticamente a partir de qualquer espaço entre números ou unidades.

A fase de `/` deve combinar:

- sementes que ainda possuem `/` explicitamente;
- formas em que `/` foi removida manualmente, como `1 3`, `km h`, `g cm3`;
- formas em que a barra foi substituída por palavras, como `um terço`.

Casos como `3 5 litros` não devem ser interpretados como `3/5`: podem representar decimal (`3,5`) ou outra estrutura.

## Regra de preservação

A coluna original `Keyword` nunca deve ser sobrescrita. Reconstruções ficam em campos paralelos, como:

- `keyword_interpretada`;
- `fenomeno_origem`;
- `simbolo_provavel`;
- `confianca_reconstrucao`;
- `evidencia`;
- `id_keyword_parceira`, quando houver fragmentação por vírgula.

## Próximo passo

Executar a auditoria de `/` e das formas sanitizadas manualmente antes de retomar a classificação do lote 002.
