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
- `classificar_lote_semantico_v1_1.py` — mesma lógica do v1, mas com `max_iter=10000` nos dois `LinearSVC`; é a versão recomendada.
- `posprocessar_lote_semantico_v1.py.part1` + `.part2` — regras semânticas pós-classificação.
- `finalizar_auditar_lote_v1.py` — finalizador-base.
- `finalizar_auditar_lote_v1_1.py` — revisão PDF/content.
- `finalizar_auditar_lote_v1_2.py` — licenças/direitos parentais e flexões de conversão PDF.
- `finalizar_auditar_lote_v1_3.py` — casamento/licenças e manipulações PDF sem troca de formato.
- `finalizar_auditar_lote_v1_4.py` — pares explícitos de formatos sem verbo.
- `finalizar_auditar_lote_v1_5.py` — custo de combustível por rota/distância.
- `finalizar_auditar_lote_v1_6.py` — `dias trabalhados`, licença/afastamento por dias, TRCT/fatorial em PDF e pares adjacentes de formatos.
- `finalizar_auditar_lote_v1_7.py` — `intervalos reais`, luto/óbito trabalhista, `horas trabalhadas`, salário por hora/proporcional, IRRF sobre salário/folha e reajuste salarial.
- `finalizar_auditar_lote_v1_8.py` — direito/folga de aniversário, pares PDF explícitos e variantes com marca iLovePDF; validado no lote 014 e suficiente nos lotes 015, 016 e 017.
- `finalizar_auditar_lote_v1_9.py` — busca de material de concurso em PDF sem troca de formato é conteúdo/documento, não conversão de arquivo; validado no lote 018.
- `finalizar_auditar_lote_v1_10.py` — reconhece PDF/A e variantes compactas de pares documentais, mantém pares nus `pdf e word`/`pdf x word` como ambíguos e reclassifica buscas por livros identificados em PDF; validado no lote 019.
- `finalizar_auditar_lote_v1_11.py` — reconhece `transformador` como substantivo de ferramenta de conversão em contexto de PDF; validado no lote 020.
- `instalar_pipeline_semantico_v1.py` — monta o pós-processador e valida SHA-256.
- `gerar_qa_centralizado_v1.py` — gerador anterior de QA.
- `gerar_planilhas_centralizadas_v2.py` — gera XLSX centralizado horizontal e verticalmente; `--qa-only` gera apenas QA.

## Instalação do pós-processador

```bash
python3 07-Scripts/instalar_pipeline_semantico_v1.py
```

SHA-256 esperado do pós-processador montado:

```text
cd73c777dc89ac56ecb279c113304f9006453d22c68dc81f0110d106377f6207
```

## Execução de um lote

Exemplo para o lote 021 usando o lote 020 aprovado como treino/controle anterior:

```bash
python3 07-Scripts/classificar_lote_semantico_v1_1.py --lote 21 --treino 20 --root .
python3 07-Scripts/posprocessar_lote_semantico_v1.py --lote 21 --root .
python3 07-Scripts/finalizar_auditar_lote_v1_11.py --lote 21 --controle-anterior 20 --root .
python3 07-Scripts/gerar_planilhas_centralizadas_v2.py --lote 21 --root . --qa-only
```

## Regras de preservação

- Nunca sobrescrever `Keyword` original.
- Reconstruções de `/` ficam em campos paralelos.
- Área de origem é evidência, não classificação final.
- Conversão direta exige origem, destino e direção quando identificáveis.
- Ambiguidade real não deve ser promovida artificialmente para confiança alta.
- PDF sem troca de formato não é automaticamente conversão.
- Pares PDF↔outro formato com direção explícita são conversão.
- PDF/A é tratado como formato documental válido em pares PDF↔PDF/A.
- Variantes compactas como `pdf de word`, `pdf no word`, `pdf for excel` e `pdf for jpg` representam conversão de arquivo.
- Pares nus como `pdf e word` e `pdf x word`, sem verbo/direção, permanecem em revisão por ambiguidade.
- `transformador` em contexto de PDF representa ferramenta de transformação/conversão de arquivo.
- Busca por material de concurso em PDF, sem troca de formato, é `Fora de escopo > Busca por conteúdo > Documento/PDF informacional`.
- Busca por livro/material identificado em PDF, sem operação de conversão, também é conteúdo/documento.
- Marca iLovePDF com dois formatos inequívocos pode representar conversão; busca genérica pela marca sem operação é navegacional/fora de escopo.
- Licenças/afastamentos, luto/óbito e direitos de folga no contexto de trabalho permanecem em Trabalho.
- `dias trabalhados` e `horas trabalhadas` são domínios trabalhistas por padrão.
- salário por hora/proporcional é remuneração trabalhista.
- IR/IRRF sobre salário/folha é Trabalho > Folha e encargos > INSS e IRRF.
- `intervalos reais` é conteúdo matemático, inclusive com PDF/DOC/PPT.
- reajuste salarial, sem subcontexto mais específico, fica em Finanças > Correção monetária > Inflação e índices.
- custo/gasto de combustível por rota/distância fica em Energia > Combustíveis > Custo de viagem.

## Planilhas

A partir do lote 004, toda planilha XLSX gerada deve manter **todas as linhas e colunas usadas centralizadas horizontal e verticalmente**. CSV não possui formatação visual.
