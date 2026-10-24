# Relatório de auditoria de palavras-chave — P3 v5.2

**Fonte:** P3 v5.1 · **Data:** 24/10/2026 · **Decisão:** DEC-088 · **Homologação:** PENDENTE

## Resultado

- **75** novas propostas aplicadas a IDs elegíveis que não haviam sido revisados em fases anteriores.
- **32 famílias**, **7 grupos temáticos**.
- **19.637 → 19.562** registros P3 elegíveis.
- **31** mudanças na área principal e **58** mudanças no tipo de intenção (podem ocorrer no mesmo ID).
- **30/30** lotes aprovados em regressão independente; **75/75** patches verificados com JSON antes/depois.

| Tema | Novos IDs | Cuidado principal |
|---|---:|---|
| Gestação/tempo | 20 | Semanas ↔ meses não prova gravidez; mês variável |
| Cartão/juros | 15 | Taxa bancária, planilha e simulação são intenções distintas |
| Estatística | 12 | Fórmula sem dados não permite resultado |
| BTU/h e watts | 10 | Separar potência térmica de consumo elétrico |
| Salário/adicionais | 8 | Separar bruto, base, líquido, descontos e adicionais |
| Jornada semanal | 8 | Horas por dia dependem do número de dias trabalhados |
| Arredondamento | 2 | Matemática, não calendário |

## Checagens independentes

| Propriedade | Resultado |
|---|---:|
| Lotes | 30/30 PASSOU |
| Keywords-base | 294.905 |
| Controles | 2.190 |
| Fila P3 | 23.965 linhas |
| Fila geral | 52.046 linhas |
| Colunas anteriores intactas | 390 por fila |
| Novas colunas de rastreio | 8 por fila |
| Pendências P2 preservadas | 4.660 |
| Propostas globais preservadas | 98, byte a byte |

A comparação percorreu os arquivos completos e rejeita diferenças em qualquer ID fora dos 75 selecionados, assim como alterações em campos não autorizados. Cada patch traz o valor antes/depois das colunas alteradas.

## Arquivos da entrega

`p3-v5.2-decisoes-75.csv`, `p3-v5.2-patches-75.csv`, `p3-v5.2-plano-por-id.csv`, `p3-v5.2-qa-por-grupo.csv`, `p3-v5.2-regressao-30-lotes.csv`, `p3-v5.2-regressao-independente-30-lotes.csv`, `p3-v5.2-resumo.json`, `p3-v5.2-regressao-independente-resumo.json`, `p3-v5.2-fila-23965.csv`, `fila-geral-p0-p1-p2-p3-v5.2.csv`, `lotes-001-a-030-p3-v5.2.zip`, `backlog-global-98-com-parecer-v27.csv`, QA XLSX centralizada e fontes v5.1 de reprodução.

Os scripts em `07-Scripts/P3/` regeneram resultados, regressão, QA e pacote. Arquivos são propostas técnicas e **não equivalem a validação editorial humana**.

**Próxima etapa:** P3 v5.3 — revisão contextual individual das 75 propostas antes de nova expansão.