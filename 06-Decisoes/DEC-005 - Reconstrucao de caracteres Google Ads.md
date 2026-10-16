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

A barra é tratada em fase separada e com uma regra mais conservadora do que a vírgula.

### Regra central

Uma forma já sanitizada **não prova** que existia `/` originalmente.

Exemplos:

- `um terço` pode ter sido escrito originalmente assim ou pode ser substituição manual de `1/3`;
- `férias com 1 3` pode ser `1/3` com barra removida, mas só deve ser tratado como hipótese até haver evidência/contexto suficiente;
- `MB s` pode representar `MB/s`, mas em outras consultas dois tokens de unidade podem indicar apenas uma conversão;
- `um quarto` é especialmente polissêmico porque pode significar fração ou cômodo.

Portanto, nenhuma forma escrita ou com espaço recebe reconstrução automática.

### Script de auditoria

O script `auditar_barras_v1.py` separa três classes:

1. **barra explícita confirmada** — a própria semente ainda contém `/`; esta é evidência direta;
2. **candidato sanitizado ambíguo** — formas como `1 3`, `um terço`, `km h`, `MB s`; origem não confirmada;
3. **variante de busca** — forma derivada de uma semente com slash explícita para procurar nos resultados, sem virar prova sozinha.

O script registra arquivo, aba, linha, coluna e célula, preservando rastreabilidade.

### Teste nos 7 arquivos de sementes atuais

A execução de teste encontrou:

- **14 células com `/` explícita**;
- **6 prováveis cabeçalhos/categorias** com `/`;
- **8 prováveis keywords reais com `/` explícita**;
- **44 candidatos sanitizados** para revisão;
- **16 variantes de busca** derivadas das keywords explícitas.

As 8 keywords explícitas reais estão em `SementesConversores.ods`, aba `Sementes misturadas`, e incluem:

- `Mbps para MB/s`;
- `MB/s para Mbps`;
- `Gbps para GB/s`;
- `GB/s para Gbps`;
- `Kbps para KB/s`;
- `KB/s para Kbps`;
- `velocidade de internet Mbps para MB/s`;
- `quanto é 100 Mbps em MB/s`.

Entre os candidatos sanitizados existem três casos claros para investigação, mas ainda não para reconstrução automática:

- `férias com 1 3`;
- `cálculo de férias com 1 3`;
- outra ocorrência de `férias com 1 3`.

Também existem muitas ocorrências de `um terço` ligadas a férias, mas a origem delas permanece **indeterminada** porque o texto por extenso pode ser legítimo.

### Falsos positivos evitados

A auditoria não deve converter automaticamente:

- `traço de concreto 1 2 3` em `1/2`;
- `um quarto` em `1/4` sem contexto, pois pode significar cômodo;
- `meio período` em `1/2 período`;
- qualquer par numérico simplesmente porque há um espaço entre os números.

## Regra de preservação

A coluna original `Keyword` nunca deve ser sobrescrita. Reconstruções e hipóteses ficam em campos paralelos, como:

- `keyword_interpretada`;
- `fenomeno_origem`;
- `simbolo_provavel`;
- `confianca_reconstrucao`;
- `evidencia`;
- `id_keyword_parceira`, quando houver fragmentação por vírgula.

## Próximo passo

Usar as 8 sementes com `/` explícita para procurar variantes nos CSV/ODS de resultados e, separadamente, investigar os candidatos sanitizados sem tratá-los como reconstruções confirmadas. Só depois aplicar o mapa de evidências à classificação dos lotes.
