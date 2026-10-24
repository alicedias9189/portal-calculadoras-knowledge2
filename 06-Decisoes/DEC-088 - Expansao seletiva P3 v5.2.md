# DEC-088 — Expansão seletiva P3 v5.2

**Data:** 24/10/2026  
**Situação:** AUDITORIA TÉCNICA PASSOU · HOMOLOGAÇÃO EDITORIAL PENDENTE  
**Fonte imutável:** P3 v5.1; **saída:** P3 v5.2.

## Decisão

Selecionar **75 IDs novos**, organizados em **32 famílias** e **7 grupos**, exclusivamente entre os **19.637 registros P3 elegíveis** da v5.1. Após esta expansão, permanecem **19.562 registros elegíveis**. Não reabrir os 75 IDs auditados na v5.1 nem P2.

| Grupo | IDs |
|---|---:|
| Gestação e conversão temporal | 20 |
| Juros e controle do cartão de crédito | 15 |
| Estatística — intenção informacional | 12 |
| BTU/h térmico versus watts elétricos | 10 |
| Salário bruto e adicionais | 8 |
| Jornada semanal | 8 |
| Arredondamento numérico | 2 |
| **Total** | **75** |

## Regras semânticas

1. `semanas` e `meses` não provam contexto gestacional; quando gravidez/gestação estiver expressa, mapear à área Saúde. Um mês civil não possui semanas fixas — não apresentar equivalência exata sem datas e convenção.
2. Juros de cartão, consulta à taxa do banco, simulador e planilha de despesas são intenções distintas. Sem saldo, taxas e prazo, não inventar parcelas ou encargos.
3. Salário bruto/base/líquido não é investimento, geometria ou pintura. Adicionais e descontos dependem da norma e do período aplicável.
4. Jornada de trabalho em horas semanais não é diferença entre datas. Distribuir horas diárias requer quantidade de dias e escala.
5. Média/mediana/moda sem série de valores têm intenção informacional; perguntas por fórmula não incluem amostra numérica.
6. Capacidade térmica em BTU/h pode ser convertida em watts **térmicos** (1 BTU/h ≈ 0,293071 W térmico); watts elétricos consumidos dependem de eficiência/modelo e não podem ser deduzidos apenas de BTU/h.
7. Arredondamento de números e procedimentos no Excel não são operações com datas.

## Invariantes e regressão

Regressão independente **PASSOU nos 30 lotes**. Confirmados **75 patches/75 IDs** permitidos, **294.905 registros-base**, **2.190 controles** e alterações somente aos 9 campos de classificação autorizados, com JSON antes/depois por ID. As filas de **23.965** e **52.046** linhas preservaram as **390 colunas históricas**, acrescentando somente **8 colunas de rastreabilidade v5.2**. Backlog global com 98 itens permanece idêntico byte a byte; 4.660 pendências P2 não foram tocadas.

SHA-256 composto das fontes históricas protegidas: `b6514f3c1a46a5ccd35615293846106f48e9cac1df9ccd8b7b67e92d3ffe9b76`.

## Limites e continuidade

Não houve aprovação editorial humana nem pesquisa jurídica atualizada nesta etapa. Todas as sugestões requerem revisão de pertinência na próxima passagem. Os CSVs e 30 lotes completos, manifesto, QA XLSX e scripts reexecutáveis estão no pacote ZIP entregue no ChatGPT; **não confundir documentos e scripts versionados no GitHub com upload dos dados binários**.

**Próxima tarefa:** **P3 v5.3**, revisão crítica individual dos mesmos 75 pareceres, sem selecionar IDs novos até concluí-la.