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
- `finalizar_auditar_lote_v1_12.py` — reconhece `convert`/`conversion` em inglês e formatos CAD DWG/DXF em pares com PDF; validado no lote 021.
- `finalizar_auditar_lote_v1_13.py` — reconhece `salvar ... em PDF` como criação/conversão com origem implícita e reforça R21 para feriado/compensação sob CLT; validado no lote 022.
- `finalizar_auditar_lote_v1_14.py` — separa preço unitário de combustível, buscas navegacionais por Convertio e folga eleitoral de mesário/presidente de mesa; validado no lote 023 e suficiente no lote 024.
- `finalizar_auditar_lote_v1_15.py` — amplia PDF↔MOBI/Kindle, conteúdo matemático em PDF, Smallpdf navegacional, combustível por km, `transforma PDF` e PowerPoint→PDF; validado no lote 025.
- `finalizar_auditar_lote_v1_16.py` — reconhece XPS↔PDF e reclassifica material identificado de Cálculo em PDF como conteúdo/documento informacional; validado no lote 026.
- `finalizar_auditar_lote_v1_17.py` — corrige pares TIFF↔PDF com direção explícita e marca pares nus PDF/DWG/DXF como ambíguos; aplicado no lote 030.
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

Exemplo final reproduzível do lote 030 usando o lote 029 aprovado como treino/controle anterior:

```bash
python3 07-Scripts/classificar_lote_semantico_v1_1.py --lote 30 --treino 29 --root .
python3 07-Scripts/posprocessar_lote_semantico_v1.py --lote 30 --root .
python3 07-Scripts/finalizar_auditar_lote_v1_17.py --lote 30 --controle-anterior 29 --root .
python3 07-Scripts/gerar_planilhas_centralizadas_v2.py --lote 30 --root . --qa-only
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
- Pares nus como `pdf e word`, `pdf x word`, `pdf mobi` e `xps pdf`, sem verbo/direção, permanecem em revisão por ambiguidade.
- `transformador`, `transforma`, `convert` e `conversion` em contexto documental podem indicar conversão quando o contexto é inequívoco.
- `salvar ... em PDF` é criação/conversão para PDF mesmo com origem implícita.
- PDF↔MOBI/Kindle e XPS↔PDF são famílias de conversão documental reconhecidas quando há direção/verbo.
- Busca por material de concurso, livro ou conteúdo matemático identificado em PDF, sem operação de conversão, é conteúdo/documento informacional.
- Marca iLovePDF/Smallpdf/Convertio sem operação específica é navegacional/fora de escopo; com par inequívoco de formatos pode ser conversão.
- Licenças/afastamentos, luto/óbito, folga de aniversário e folga eleitoral no contexto de trabalho permanecem em Trabalho.
- Consulta CLT sobre feriado/compensação é direito trabalhista, não cálculo de datas.
- `dias trabalhados` e `horas trabalhadas` são domínios trabalhistas por padrão.
- salário por hora/proporcional é remuneração trabalhista.
- IR/IRRF sobre salário/folha é Trabalho > Folha e encargos > INSS e IRRF.
- `intervalos reais` e `intervalos numéricos` são conteúdo matemático mesmo quando PDF aparece como formato de referência.
- reajuste salarial, sem subcontexto mais específico, fica em Finanças > Correção monetária > Inflação e índices.
- custo/gasto/preço de combustível por rota ou distância fica em Energia > Combustíveis > Custo de viagem.
- preço unitário atual por litro de combustível, sem rota/distância, é consulta de mercado.

## Planilhas

A partir do lote 004, toda planilha XLSX gerada deve manter **todas as linhas e colunas usadas centralizadas horizontal e verticalmente**. CSV não possui formatação visual.

## Encerramento (30/30 lotes)

O lote 030 encerrou o processamento de 294.905 keywords base. O relatório global de encerramento está em `00-Mapa-Global/Encerramento de 30 lotes - auditoria transversal.md`.

A auditoria global identificou 73 conversões diretas com metadados incompletos no lote 001; os lotes 002 a 030 passaram nesse critério. Existem 52.050 keywords sinalizadas para revisão manual. **Os testes automáticos aprovados não substituem essa revisão.**
