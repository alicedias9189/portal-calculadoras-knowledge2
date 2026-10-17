# Scripts do pipeline semântico

Esta pasta contém versões reutilizáveis dos scripts empregados na classificação/auditoria dos lotes sob **Taxonomia v1.1 + barras v2**.

## Dependências

Para o classificador:

```bash
python3 -m pip install numpy scikit-learn
```

O gerador de XLSX centralizado usa `artifact_tool`, que precisa estar disponível no ambiente em que for executado.

## Arquivos

- `classificar_lote_semantico_v1.py` — classificador inicial do lote usando lote(s) aprovado(s) como treino, Golden Set e mapa de barras.
- `classificar_lote_semantico_v1_1.py` — mesma lógica do v1, mas com `max_iter=10000` nos dois `LinearSVC`; elimina o `ConvergenceWarning` observado no lote 010 e é a versão recomendada para os lotes seguintes.
- `posprocessar_lote_semantico_v1.py.part1` + `.part2` — regras semânticas pós-classificação usadas nas auditorias recentes.
- `finalizar_auditar_lote_v1.py` — finalizador-base v1.
- `finalizar_auditar_lote_v1_1.py` — camada de revisão PDF/content validada no lote 005; distingue conversão/criação de PDF, edição pura de PDF e PDF de referência de unidades.
- `finalizar_auditar_lote_v1_2.py` — camada validada no lote 006; reforça R21 para licenças/direitos parentais que não podem cair em Datas e reconhece flexões inequívocas de conversão de PDF como `converte word em pdf`.
- `finalizar_auditar_lote_v1_3.py` — camada validada no lote 007; amplia R21 para folgas/licenças por casamento, reconhece conversões implícitas como `fotos em pdf` e `pagina web em pdf` e retira de Conversores manipulações de PDF sem troca de formato, como `mudar a cor do pdf` e `quebrar pdf`.
- `finalizar_auditar_lote_v1_4.py` — camada validada no lote 008; reconhece pares de formato explícitos sem verbo, como `pdf em imagem` e `pdf em xml`, evitando falso positivo de conteúdo PDF. Nos lotes 009 e 010 continuou suficiente.
- `finalizar_auditar_lote_v1_5.py` — camada validada no lote 011; diferencia preço de mercado de combustível de custo de deslocamento. Consultas como `calcular valor combustível por km` e `calcular gasto combustível rota` vão para `Energia > Combustíveis > Custo de viagem`, com intenção `estimativa de custo`.
- `instalar_pipeline_semantico_v1.py` — monta `posprocessar_lote_semantico_v1.py` a partir das duas partes e valida SHA-256.
- `gerar_qa_centralizado_v1.py` — gerador anterior de QA.
- `gerar_planilhas_centralizadas_v2.py` — gera XLSX com todas as células usadas centralizadas horizontal e verticalmente; `--qa-only` gera apenas o workbook de QA.

## Instalação do pós-processador

Dentro do repositório:

```bash
python3 07-Scripts/instalar_pipeline_semantico_v1.py
```

O instalador espera estas duas partes na mesma pasta e gera:

```text
07-Scripts/posprocessar_lote_semantico_v1.py
```

O SHA-256 esperado do arquivo completo é:

```text
cd73c777dc89ac56ecb279c113304f9006453d22c68dc81f0110d106377f6207
```

## Execução de um lote

Exemplo para o lote 012 usando o lote 011 aprovado como treino/controle anterior:

```bash
python3 07-Scripts/classificar_lote_semantico_v1_1.py --lote 12 --treino 11 --root .
python3 07-Scripts/posprocessar_lote_semantico_v1.py --lote 12 --root .
python3 07-Scripts/finalizar_auditar_lote_v1_5.py --lote 12 --controle-anterior 11 --root .
python3 07-Scripts/gerar_planilhas_centralizadas_v2.py --lote 12 --root . --qa-only
```

Se o ambiente suportar a exportação XLSX grande pelo `artifact_tool`, remova `--qa-only` para também gerar o XLSX classificado completo.

## Arquivos esperados na raiz de trabalho

```text
lote-NNN.csv
lote-MMM-classificado-v1.1-barras-v2.csv
golden-set-v1.1.csv
lote-002-golden-qa-v1.1.csv
revisao_contextual_barras_v2/mapa-barras-mestre-v2.csv
```

## Regras de preservação

- Nunca sobrescrever `Keyword` original.
- Reconstruções de `/` ficam em campos paralelos.
- Área de origem é evidência, não classificação final.
- Conversão direta exige origem, destino e direção quando identificáveis.
- Ambiguidade real não deve ser promovida artificialmente para confiança alta.
- PDF com conteúdo sobre conversão de medidas não deve ser confundido com conversão de arquivo.
- Edição/manipulação de PDF sem troca de formato fica fora do escopo do conversor.
- Pares explícitos de formatos, como `pdf em imagem`, `pdf em xml`, `imagem em pdf`, representam conversão mesmo sem verbo explícito.
- Quantidade de dias/direitos de licença parental ou folga/licença por casamento regidos pela relação de trabalho deve ficar em `Trabalho > Afastamentos > Licenças e afastamentos`, e não em Datas.
- Custo/gasto/valor de combustível ligado a rota, trajeto ou distância deve ficar em `Energia > Combustíveis > Custo de viagem`; preço atual de combustível isolado continua sendo preço de mercado.

## Planilhas

A partir do lote 004, toda planilha XLSX gerada por este fluxo deve manter **todas as linhas e colunas usadas centralizadas horizontal e verticalmente**, conforme decisão do projeto. CSV não possui formatação visual, portanto essa regra se aplica aos artefatos de planilha (`.xlsx`).
