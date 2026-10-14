# Lote 001

## Status

**Classificação concluída com Taxonomia-mestra v1.**

## Cobertura

- 9.831 keywords base.
- 73 controles do Golden Set.
- 9.904 linhas classificadas no total.
- Golden Set: **73/73 correspondências exatas** em área + cluster + subcluster + tipo de intenção.

## Confiança e revisão

- Alta: 8.143 (82,83%).
- Média: 399 (4,06%).
- Baixa: 1.289 (13,11%).
- Revisão manual: 1.688 (17,17%).

Casos de baixa confiança não foram forçados para uma precisão artificial. Eles concentram ambiguidades, consultas fora do escopo e lacunas reais da taxonomia.

## Distribuição por área

- Finanças: 2.434
- Trabalho: 2.429
- Conversores: 1.836
- Matemática: 955
- Construção: 665
- Energia: 633
- Datas: 465
- Fora de escopo: 414

## Candidatos coerentes para Taxonomia v1.1

Estes padrões apareceram de forma recorrente e específica no lote. Ainda são **propostas**, não alterações aprovadas:

- [[../01-Taxonomia/Trabalho|Trabalho]] — Previdência e benefícios: 162
- [[../01-Taxonomia/Matemática|Matemática]] — Calculadora científica: 141
- Matemática — Progressões e sequências: 85
- [[../01-Taxonomia/Construção|Construção]] — Impermeabilização: 54
- Matemática — Trigonometria e geometria angular: 34
- [[../01-Taxonomia/Finanças|Finanças]] — Calculadora financeira / HP12C: 27
- Trabalho — Direitos trabalhistas e CLT: 26
- [[../01-Taxonomia/Energia|Energia]] — Regulação e tarifas: 22
- Trabalho — PIS/PASEP: 14

## Baldes que não devem virar clusters automaticamente

Os grupos genéricos `Outras consultas financeiras`, `Outros cálculos/direitos trabalhistas`, `Outras conversões`, `Outros cálculos matemáticos`, `Outras consultas de datas` e equivalentes continuam em revisão. Eles misturam intenções diferentes e servem para descobrir lacunas reais antes da Taxonomia v1.1.

## Controles importantes confirmados

A classificação preservou as fronteiras definidas no [[../04-Regressao/Golden Set]], incluindo:

- conversão de moedas vs cotação;
- libra moeda vs massa;
- arroba commodity vs massa;
- WhatsApp GB vs armazenamento;
- bit vs byte e taxa de transferência;
- PDF como formato vs busca por conteúdo;
- conversões dimensionalmente incompatíveis;
- `g → mL` como cálculo contextual.

## Próximo passo

Antes do lote 002, revisar os candidatos coerentes acima e uma amostra dos grupos de baixa confiança. Somente mudanças aprovadas devem entrar na [[../00-Mapa-Global/MOC - Taxonomia|Taxonomia-mestra]]; depois disso o Golden Set deve ser executado novamente para garantir ausência de regressões.
