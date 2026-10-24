# DEC-046 — P3 v1: piloto por famílias e QA conservador

Data: 2026-10-20. Continuidade de [[06-Decisoes/DEC-045 - Fechamento conservador P2 v7 e prioridade P3]].

**Decisão:** executar piloto estratificado por tamanho/área em **66 famílias / 2.090 keywords** da P3 (23.965 itens / 9.278 famílias). Criar versão paralela P3 v1 com **1.207 patches semânticos** (418 sem ressalva de regra e 789 com ressalva), mantendo 883 analisados sem evidência e 21.875 fora do piloto intactos. Uma proposta de regra não é aprovação editorial.

**Regressão:** 30/30 PASSOU; 294.905 bases e 2.190 controles; 207 trocas de área e 604 de tipo de intenção, contagens não disjuntas. Preservar todos os registros P0/P1/P2 e a P2 v7 (4.660 pendentes). Nenhum Golden Set reexecutado.

**Riscos e continuidade:** solicitar revisão editorial da amostra de 210 decisões no Excel, testar exceções por regra antes de expandir a P3. Permanecem **22.758 P3 sem proposta de ajuste** (883 do piloto + 21.875 não selecionados), o que NÃO significa que todos sejam erros ou precisem de correção.

**Evidências:** `08-Entregas/P3-v1/RELATORIO.md`, CSVs integrais, patches, planilha centralizada, regressão independente e scripts `07-Scripts/P3/`. As duas fontes ZIP P2 v7 seguem no pacote.
