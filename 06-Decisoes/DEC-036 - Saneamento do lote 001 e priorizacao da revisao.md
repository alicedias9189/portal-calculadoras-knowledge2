# DEC-036 — Saneamento do lote 001 e priorização da revisão

Data: 2026-10-17.

1. Corrigir **7** conversões diretas com pares explícitos, reclassificar **66** casos semanticamente não diretos, e preservar CSV original e todos os controles.
2. Não presumir origem/destino a partir de uma única grandeza ou de pares sem direção. Consultas genéricas, tabelas e aplicativos não são `conversão direta`.
3. Usar cópia versionada `lote-001-saneado-v1.1-barras-v2.csv`, não substituir o dataset histórico silenciosamente.
4. Classificar a fila de **52.046** pendências pós-saneamento em P0=474, P1=2.557, P2=25.050, P3=23.965; agrupar em **15.117 famílias**.
5. A heurística organiza o trabalho, mas **não equivale à revisão individual de 52.046 keywords**; aprovação automatizada e julgamento semântico são distintos.
6. O responsável pelo projeto decide apenas questões de produto/SEO ou casos realmente inconclusivos; a investigação, priorização e propostas de correção podem ser executadas pelo assistente.
7. Nenhum novo volume Google Ads é calculado pela soma das linhas agrupadas; respeitar variantes próximas.
