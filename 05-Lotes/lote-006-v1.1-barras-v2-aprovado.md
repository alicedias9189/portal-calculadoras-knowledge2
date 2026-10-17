# Lote 006 — aprovado sob Taxonomia v1.1 + barras v2

## Status

**APROVADO** após classificação, pós-processamento e auditoria final.

## Invariantes

- 9.831 keywords base.
- 73 controles.
- 9.831 IDs base únicos.
- Colunas originais preservadas.
- Área/cluster/subcluster vazios: 0.
- Golden Set v1.1: 107/107.
- Controles incorporados: 73/73.
- Reconstruções `/`: 5.
- Conversões diretas sem origem/destino/direção: 0.
- Flags finais: 0.

## Confiança

- alta: 6.845
- média: 1.474
- baixa: 1.512
- revisão manual: 1.572

## Correções da auditoria

A primeira passagem retornou 5 flags:

- 4 casos `WORK_RIGHTS_DATE`, com consultas de licença/direito parental classificadas em Datas;
- 1 falso positivo `PDF_CONTENT` em `site que converte word em pdf`.

A camada `finalizar_auditar_lote_v1_2.py` corrigiu apenas os quatro casos que efetivamente haviam caído em Datas para `Trabalho > Afastamentos > Licenças e afastamentos`, preservando outras consultas de maternidade/paternidade já classificadas corretamente. A flexão verbal `converte` passou a ser reconhecida como evidência explícita de conversão de formato PDF.

## Decisão

- Taxonomia v1.1 permanece ativa.
- R21 foi reforçada operacionalmente no finalizador v1.2.
- Nenhuma Taxonomia v1.2 foi necessária.
- Lote 007 está liberado.
