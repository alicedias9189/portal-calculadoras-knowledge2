# DEC-066 — Expansão seletiva P3 v3.0

**Decisão:** somente IDs presentes simultaneamente na fila P3 e na fila geral com `prioridade=P3`, metadados idênticos, `status_p3_v1=FORA_DO_PILOTO` e nenhum status de revisão posterior podem ser alterados.

**Aplicação:** 36 propostas, 18 famílias. Escopo limitado a colunas analíticas explicitadas em `ALLOWED` no script de auditoria. Não modificar anúncios do Google Ads, textos originais, controles, nem documentos globais.

**Critério técnico:** classificar apenas intenções textualmente explícitas. Em moedas, só preencher direções inequívocas. Em velocidade de conexão, potência e energia, não inferir grandezas ausentes. Em financiamento, distinguir cálculo de parcela de consulta a condições comerciais.

**Testes:** regressão independente de todos os 30 lotes, comparação integral de duas filas e reprodução por scripts usando as fontes contidas no pacote. As 98 propostas globais permanecem em quarentena.

**Limitação:** propostas técnicas, não revisão editorial final. Os pareceres individuais e os 36 patches permanecem auditáveis no pacote.
