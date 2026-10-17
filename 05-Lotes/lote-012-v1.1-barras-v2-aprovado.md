# Lote 012 — aprovado sob Taxonomia v1.1 + barras v2

Status final: **APROVADO**.

- Linhas totais: 9.904
- Keywords base: 9.831
- Controles: 73
- IDs base únicos: 9.831
- Golden Set v1.1: 107/107
- Controles preservados: 73/73
- Reconstruções de `/`: 6
- Conversões diretas sem metadados: 0
- Flags finais: 0
- Confiança alta: 5.780
- Confiança média: 1.742
- Confiança baixa: 2.309
- Revisão manual: 2.450

## Correções consolidadas

O lote revelou uma deriva sistemática em `dias trabalhados`: 74 keywords estavam sendo empurradas para Datas/Matemática/outros domínios. A regra foi consolidada no finalizador v1.6:

- família genérica `dias trabalhados` → Trabalho > Remuneração > Valor da hora e dias trabalhados;
- pagamento/salário/folha/adiantamento por dias trabalhados → Trabalho > Remuneração > Salário líquido e bruto;
- contextos específicos (13º, férias, rescisão, escalas, DSR, adicionais etc.) permanecem em seus subclusters específicos;
- 2 casos de licença/afastamento por dias foram mantidos em Trabalho > Afastamentos > Licenças e afastamentos;
- 2 casos de TRCT em PDF/DOC foram tratados como conteúdo trabalhista de rescisão, não conversão de arquivo;
- 2 casos de conteúdo matemático com PDF foram corrigidos para Matemática;
- pares adjacentes de formatos como `pdf word` e `pdf powerpoint` permanecem conversões mesmo sem verbo/preposição.

Lote 013: **liberado**.