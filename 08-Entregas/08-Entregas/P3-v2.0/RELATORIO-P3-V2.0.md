# Relatório — P3 v2.0

Expansão seletiva da base P3 v1.9: **272 alterações** em **132 famílias**; P3 fora dos pilotos: **20.672 → 20.400**.

| Regra | Ajustes |
|---|---:|
| `P3V20_INSS_DOMINIO` | 32 |
| `P3V20_TAXA_JUROS_INFORME` | 77 |
| `P3V20_MATERIAL_DIDATICO` | 21 |
| `P3V20_ALGEBRA_DOMINIO` | 32 |
| `P3V20_ESTATISTICA_DOMINIO` | 4 |
| `P3V20_SALARIO_MATERNIDADE` | 9 |
| `P3V20_IRRF_DOMINIO` | 1 |
| `P3V20_CONSUMO_VEICULO` | 94 |
| `P3V20_CONVERSAO_ENERGIA` | 2 |

A regressão estrutural independente verificou 30/30 lotes, 294.905 registros-base, 2.190 controles e diffs reais antes/depois de 272 patches. Colunas históricas das duas filas intocadas. Os 165 itens da amostra cobrem as 9 regras. Casos remanescentes: 20.400 P3 fora dos pilotos e 4.660 pendências P2.

**Limite:** decisões por regras e inspeção de padrões, não validação editorial individual independente nem auditoria de resultados de busca. Nenhum cálculo de juros, taxa real, dados de saúde ou consumo de veículo foi fabricado.
