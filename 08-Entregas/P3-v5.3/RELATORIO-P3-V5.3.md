# Relatório técnico — P3 v5.3

**24 de outubro de 2026 — Revisão contextual individual, sem nova expansão**

| Indicador | Resultado |
|---|---:|
| Pareceres da v5.2 revisados | 75 |
| Refinamentos justificados | 6 |
| Mantidos com ressalvas | 69 |
| Famílias / grupos | 32 / 7 |
| Lotes canônicos conferidos | 30 / 30 |
| Lotes filtrados Ouro conferidos | 30 / 30 |
| Registros canônicos / operacionais sem Ouro | 294.905 / 291.296 |
| Controles preservados em cada versão | 2.190 |
| Colunas históricas preservadas nas quatro filas | 398 |
| Novas colunas de rastreabilidade | 8 |
| P3 pendentes, canônico / operacional | 19.562 / 19.462 |
| P2 pendentes preservados | 4.660 |
| Backlog global preservado | 98 |

Os **seis ajustes** referem-se aos IDs **4473, 47574, 47583, 148231, 254173 e 270768**, com justificativas e valores antes/depois no CSV de patches. Nenhuma mudança de classificação foi feita nos outros 69 casos, nem em qualquer ID fora da lista autorizada.

O motivo para não ampliar artificialmente o número de refinamentos é metodológico: quando a classificação da v5.2 é adequada, sua manutenção com ressalva é o parecer correto. A coluna `justificativa_individual` contém 75 verificações distintas por intenção contextual.

A filtragem Ouro permanece **reversível** e foi aplicada somente a visões de trabalho, conforme DEC-089. Os 75 IDs revisados não coincidem com os 3.609 IDs excluídos da visão operacional.

A **regressão independente** comparou campos, chaves e ordem de todos os registros dos 60 lotes, além das quatro filas. Todos os registros mantidos têm conteúdo inalterado fora dos seis patches. As 98 propostas globais são idênticas em bytes à fonte.

A planilha `qa-auditoria-P3-v5.3-centralizada.xlsx` tem abas de resumo, 75 pareceres, 6 patches, QA por grupo, regressão de 60 lotes, quatro filas, os 12 conflitos de cor e invariantes de controle. As células utilizadas estão centralizadas.

**Homologação editorial: PENDENTE.** Os pareceres são revisão técnica, não aprovação humana.

**Próxima tarefa:** P3 v5.4, 100 novos IDs dentre os **19.462 elegíveis sem Ouro**, seguidos de revisão e regressão integral.