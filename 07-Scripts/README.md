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
- `posprocessar_lote_semantico_v1.py.part1` + `.part2` — regras semânticas pós-classificação usadas nas auditorias recentes.
- `finalizar_auditar_lote_v1.py` — metadados, confiança, controles, Golden QA, regressões e exportação final.
- `instalar_pipeline_semantico_v1.py` — monta `posprocessar_lote_semantico_v1.py` a partir das duas partes e valida SHA-256.
- `gerar_qa_centralizado_v1.py` — gera a planilha QA com **todas as células usadas centralizadas horizontal e verticalmente**.

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

Exemplo para o lote 005 usando o lote 004 aprovado como treino/controle anterior:

```bash
python3 07-Scripts/classificar_lote_semantico_v1.py --lote 5 --treino 4 --root .
python3 07-Scripts/posprocessar_lote_semantico_v1.py --lote 5 --root .
python3 07-Scripts/finalizar_auditar_lote_v1.py --lote 5 --controle-anterior 4 --root .
python3 07-Scripts/gerar_qa_centralizado_v1.py --lote 5 --root .
```

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

## Planilhas

A partir do lote 004, toda planilha XLSX gerada por este fluxo deve manter **todas as linhas e colunas usadas centralizadas horizontal e verticalmente**, conforme decisão do projeto. CSV não possui formatação visual, portanto essa regra se aplica aos artefatos de planilha (`.xlsx`).
