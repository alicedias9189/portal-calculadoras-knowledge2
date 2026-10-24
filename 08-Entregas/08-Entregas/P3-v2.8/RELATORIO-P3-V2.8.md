# Auditoria seletiva P3 v2.8 — expansão controlada

**Data da execução:** 22/10/2026 (Mato Grosso, Brasil). **Estado:** proposta técnica auditada, não homologação editorial definitiva.

## Resultado

Foram aplicados **66 patches em 37 famílias**, todos em IDs da P3 explicitamente elegíveis e conferidos em três fontes (fila P3, fila geral com prioridade P3 e lote correspondente). **Zero IDs globais foram alterados.**

| Regra | Patches |
|---|---:|
| Taxas de financiamento de veículos | 45 |
| INSS de obra/construção civil | 9 |
| Conversões entre bases numéricas | 5 |
| Celsius ↔ Fahrenheit | 2 |
| Potência W ↔ energia kWh, com tempo necessário | 2 |
| Duração de viagem por velocidade | 2 |
| Desvio padrão em contexto matemático | 1 |
| **Total** | **66** |

## Critérios de contexto

- As buscas de taxas de financiamento automotivo foram separadas de rendimentos de investimento, impostos e energia elétrica. Consultas por taxa ou tabela **não são automaticamente simulações**; não se presume qualquer taxa vigente.
- INSS em obra civil não é dimensionamento solar, áudio nem metragem de piso; não foi inferido valor de alíquota, data ou regra previdenciária aplicável.
- Base binária/decimal e base 36 referem-se a sistemas de numeração; o texto não fornece necessariamente operandos.
- Fahrenheit e Celsius são escalas de temperatura; preservar direção não informada quando a keyword usa apenas “x”.
- **W representa potência e kWh representa energia; a relação depende de tempo**, portanto as buscas não foram marcadas como conversão direta.
- Tempo de viagem requer distância e velocidade e não equivale à aritmética do calendário.

## Regressão independente e testes negativos

- **30/30 lotes passaram**. Base: **294.905**; controles: **2.190**.
- Todos os **66 patches** conferidos pelos valores exatos antes/depois.
- Nenhum outro ID ou campo protegido (incluindo Keyword, família, lote, origem e Google Ads) foi alterado.
- Fila P3 de **23.965** linhas e fila geral de **52.046** linhas preservaram todas as colunas antigas. Foram acrescentadas 8 colunas para v2.8.
- **105 testes de seletor passaram**, inclusive os **98 IDs da fila global** bloqueados, P2, ID inexistente, duplicata, palavra-chave/família/lote divergentes.
- As **98 propostas globais permaneceram byte a byte iguais** ao arquivo de fonte, sem promoção automática.

## Divergência histórica de contagem — não ocultar

O relatório da v2.7 mencionava **20.383** itens P3 ainda fora dos pilotos. Porém, a reconstrução verificável com os status de linha mostra:

- 21.875 registros marcados como `FORA_DO_PILOTO` no estágio original;
- 1.501 foram posteriormente tocados pelas expansões registradas (união por ID, sem somar eventos repetidos);
- **20.374** são verdadeiramente não classificados no início da v2.8;
- após os 66 patches, restam **20.308**.

A diferença de **nove** entre o total reportado historicamente e o total recalculado é documentada em `p3-v2.8-reconciliacao-contagem.csv`. **Não foi feita alteração artificial em registros para fazer números coincidirem.**

## Observações e próximo passo

A amostra QA **inclui 100% dos 66 registros**. As classificações são propostas técnicas e casos limítrofes exigem homologação editorial humana, principalmente questões bancárias, INSS e palavras-chave sem parâmetros numéricos.

Próxima etapa: revisão crítica independente dos 66 patches, priorizando as 45 buscas de financiamento de veículos, antes de outra expansão. Preservar as **4.660 pendências P2** e as 98 propostas globais.
