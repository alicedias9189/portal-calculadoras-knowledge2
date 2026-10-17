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
- `finalizar_auditar_lote_v1_1.py` — revisão PDF/content validada no lote 005.
- `finalizar_auditar_lote_v1_2.py` — reforço de licenças/direitos parentais e flexões de conversão PDF, validado no lote 006.
- `finalizar_auditar_lote_v1_3.py` — casamento/licenças e manipulações PDF sem troca de formato, validado no lote 007.
- `finalizar_auditar_lote_v1_4.py` — pares explícitos de formatos sem verbo, validado no lote 008.
- `finalizar_auditar_lote_v1_5.py` — custo de combustível por rota/distância, validado no lote 011.
- `finalizar_auditar_lote_v1_6.py` — `dias trabalhados`, licença/afastamento por dias, TRCT/fatorial em PDF e pares adjacentes `pdf word`/`pdf powerpoint`, validado no lote 012.
- `finalizar_auditar_lote_v1_7.py` — `intervalos reais`, luto/óbito trabalhista, `horas trabalhadas`, salário por hora/proporcional, IRRF sobre salário/folha e reajuste salarial, validado no lote 013.
- `instalar_pipeline_semantico_v1.py` — monta `posprocessar_lote_semantico_v1.py` e valida SHA-256.
- `gerar_qa_centralizado_v1.py` — gerador anterior de QA.
- `gerar_planilhas_centralizadas_v2.py` — gera XLSX com todas as células usadas centralizadas horizontal e verticalmente; `--qa-only` gera apenas o workbook de QA.

## Instalação do pós-processador

```bash
python3 07-Scripts/instalar_pipeline_semantico_v1.py
```

O instalador gera `07-Scripts/posprocessar_lote_semantico_v1.py` e valida o SHA-256 esperado:

```text
cd73c777dc89ac56ecb279c113304f9006453d22c68dc81f0110d106377f6207
```

## Execução de um lote

Exemplo para o lote 014 usando o lote 013 aprovado como treino/controle anterior:

```bash
python3 07-Scripts/classificar_lote_semantico_v1_1.py --lote 14 --treino 13 --root .
python3 07-Scripts/posprocessar_lote_semantico_v1.py --lote 14 --root .
python3 07-Scripts/finalizar_auditar_lote_v1_7.py --lote 14 --controle-anterior 13 --root .
python3 07-Scripts/gerar_planilhas_centralizadas_v2.py --lote 14 --root . --qa-only
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
- Edição/manipulação de PDF sem troca de formato fica fora do escopo do conversor.
- Pares inequívocos de formatos podem representar conversão mesmo sem verbo/preposição.
- Licenças/afastamentos e luto/óbito previstos em lei/CLT permanecem em Trabalho.
- `dias trabalhados` é domínio trabalhista por padrão; pagamento/salário/folha/adiantamento por dias trabalhados é Remuneração.
- `horas trabalhadas` é domínio de Jornada e adicionais por padrão.
- salário por hora/proporcional é remuneração trabalhista.
- IR/IRRF sobre salário/folha é Trabalho > Folha e encargos > INSS e IRRF.
- `intervalos reais` é conteúdo matemático, inclusive quando o termo menciona PDF/DOC/PPT.
- reajuste salarial, sem subcontexto mais específico, fica em Finanças > Correção monetária > Inflação e índices.
- custo/gasto/valor de combustível ligado a rota, trajeto ou distância fica em Energia > Combustíveis > Custo de viagem.

## Planilhas

A partir do lote 004, toda planilha XLSX gerada por este fluxo deve manter **todas as linhas e colunas usadas centralizadas horizontal e verticalmente**. CSV não possui formatação visual.
