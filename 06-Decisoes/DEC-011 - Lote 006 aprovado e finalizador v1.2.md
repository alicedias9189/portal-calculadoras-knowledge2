# DEC-011 - Lote 006 aprovado e finalizador v1.2

## Decisão

O lote 006 foi aprovado sob **Taxonomia v1.1 + barras v2** após auditoria final com zero flags.

A auditoria revelou dois ajustes operacionais que passam a integrar o pipeline:

1. consultas sobre quantidade de dias/direitos de licença parental que tenham caído em Datas devem ser redirecionadas para `Trabalho > Afastamentos > Licenças e afastamentos` conforme R21;
2. flexões verbais inequívocas de conversão, como `site que converte word em pdf`, devem ser reconhecidas como conversão de formato e não como busca de conteúdo PDF.

## Implementação

Novo script reutilizável:

`07-Scripts/finalizar_auditar_lote_v1_2.py`

Ele executa a camada v1.1 anterior, aplica somente correções determinísticas validadas e recalcula os invariantes do lote.

## Guardrail importante

A correção de licença parental é aplicada somente quando a classificação anterior caiu em **Datas** e o texto contém contexto parental + `quantos dias` ou `direito`. Isso evita sobrescrever consultas trabalhistas já corretamente classificadas em outros subclusters.

## Planilhas

Continua válida a regra de projeto: todo XLSX gerado pelo pipeline deve ter as células usadas centralizadas horizontal e verticalmente. CSV não armazena formatação visual.

## Próximo passo

Lote 007 liberado usando:

`classificador v1 -> pós-processador v1 -> finalizador v1.2 -> QA centralizado v2`.
