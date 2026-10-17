# Lote 007 — Taxonomia v1.1 + barras v2 — APROVADO

## Resultado

O lote 007 foi classificado com o pipeline semântico sob Taxonomia v1.1, regras R01–R26, Golden Set v1.1 e mapa mestre de barras v2.

- Linhas totais: **9.904**
- Keywords base: **9.831**
- Controles incorporados: **73**
- IDs base únicos: **9.831**
- Reconstruções de `/`: **19**
- Golden Set v1.1: **107/107**
- Controles incorporados preservados: **73/73**
- Área/cluster/subcluster vazios: **0**
- Conversões diretas sem origem/destino/direção: **0**
- Flags finais: **0**

## Confiança

- alta: **6.893**
- média: **1.421**
- baixa: **1.517**
- revisão manual: **1.625**

## Revisão contextual

A auditoria inicial encontrou 10 flags: 3 de direitos/folga por casamento que haviam caído em Datas e 7 relacionadas a PDF.

A revisão v1.3 corrigiu **26** consultas de folga/licença por casamento para `Trabalho > Afastamentos > Licenças e afastamentos`, incluindo famílias como `abono casamento quantos dias`, `casamento quantos dias de folga` e `tenho direito a quantos dias quando casar`.

No bloco PDF:

- `fotos em pdf gratis` e `pagina web em pdf` foram mantidos como conversão de arquivo/mídia;
- pares de formatos como `baixar pdf word gratis` foram mantidos em conversão;
- `como mudar a cor do pdf` e `como quebrar pdf` foram redirecionados para Fora de escopo por serem edição/manipulação sem troca de formato;
- `quebrar pdf em/para word` permaneceu como conversão, pois há formato de destino explícito.

## Decisão

- Taxonomia v1.1 permanece ativa.
- Nenhuma Taxonomia v1.2 foi necessária.
- Finalizador v1.3 passa a ser a camada final para os lotes seguintes.
- **Lote 008 liberado.**
