# DEC-044 — Revisão contextual P2 v6

Data: **2026-10-20**. Continuidade de [[DEC-043 - Auditoria contextual P2 v5]].

**Decisão:** aceitar uma versão paralela de patches para **387 keywords P2** de **160 famílias**, com rastreabilidade e sem alteração de registros ou decisões aprovadas fora do alvo. Destas, 106 classificadas por regra sem ressalva e 281 com ressalva de parâmetros/operação. Manter **4.761 pendências** sem evidência suficiente.

**Qualidade:** regressão independente **30/30**, 294.905 registros-base preservados, 2.190 controles intactos, dados Ads protegidos, valores de patch antes/depois conferidos com arquivos reais. Ver `08-Entregas/P2-v6/RELATORIO.md`.

**Casos não forçados:** semanas e dias sem contexto (157), temperaturas Fahrenheit sem destino (68), moedas sem país/direção, conversão kg↔saca sem tipo de saca e grandezas elétricas sem condições para relacionar V e A.

**Limitação:** classificação automatizada supervisionada por exceções, não validação editorial humana de todos os itens.

**Próximo passo:** rever 4.761 pendências por prioridade de negócio, ou avançar P3 se novas reclassificações P2 não forem seguras. Não sobrescrever DEC-043 nem volumes do Google Ads.
