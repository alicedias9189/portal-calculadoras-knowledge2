# Golden Set

Conjunto de controle usado para detectar drift entre lotes e regressões da taxonomia.

## Estado

Ainda não preenchido definitivamente. Será construído a partir da amostra estratificada global.

## Critérios de seleção

O Golden Set deve incluir:

- casos fáceis e representativos de cada área;
- casos compartilhados por várias áreas de origem;
- ambiguidades lexicais;
- conversões dimensionais incompatíveis;
- consultas de cotação vs conversão;
- consultas informativas vs calculadoras;
- dados digitais bit/byte e taxa de transferência;
- consultas com alto volume de busca;
- consultas de baixa confiança;
- termos curtos e contextualmente frágeis.

## Casos mínimos já conhecidos

- `conversor metro polegada`
- `converter centimetros em metros`
- `tabela de conversao de unidades peso`
- `converter hectares em alqueires paulista`
- `tabela de conversao de pressao psi para bar`
- `converter metros cubicos em metros quadrados`
- `converter centimetros em metros quadrados`
- `converter gramas em ml`
- `converter megabits por segundo em megabytes por segundo`
- `whatsapp gb`
- `preço da arroba do boi`
- `libras hoje valor`
- `euro hj`
- `medidas de mitigação das mudanças climáticas pdf`

## Uso

Uma amostra do Golden Set será reapresentada em lotes diferentes. Divergência de classificação entre repetições deve disparar revisão antes da consolidação.
