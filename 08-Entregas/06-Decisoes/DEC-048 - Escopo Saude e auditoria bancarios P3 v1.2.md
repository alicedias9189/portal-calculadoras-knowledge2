# DEC-048 — Formalização de Saúde e auditoria de 43 buscas bancárias

**Data:** 2026-10-21. **Base:** P3 v1.1, DEC-047. **Nova versão:** P3 v1.2 paralela.

## Decisões
1. Considerar Saúde e gestação dentro do escopo planejado do portal; criar especificação de taxonomia v1.2, não substituir a v1.1 em silêncio.
2. Aplicar 187 ajustes de Saúde: 184 termos explícitos de gestação cuja mudança fora suspensa; mais 3 falsos negativos com intenção operacional explícita da amostra de 210.
3. Revisar cada um dos 43 alertas de crédito mencionando instituição financeira: 27 com termo explícito `simulador` passam a intenção `navegacional/transacional`, mantendo `Finanças > Crédito`, com ressalva de possível interesse misto; 16 com `simular` ou `simulação` **não** recebem correção automática pois podem significar tanto cálculo quanto acesso ao site do banco.
4. Nenhum caso é promovido a aprovação editorial definitiva. Nenhuma taxa bancária, prazo, percentual nem direção de conversão é inferido.

## Regressão
- **214 IDs** modificados (187 Saúde + 27 bancários); 16 alertas bancários preservados.
- 30/30 lotes testados em comparação integral; apenas 8 campos analíticos podem mudar.
- **294.905 registros-base**, **2.190 controles**, IDs, keywords e dados de Google Ads preservados.
- A fila histórica (85 colunas) não foi sobrescrita: oito colunas auditáveis de P3 v1.2 foram acrescentadas na versão paralela.
- Não foi realizada nova aferição independente do Golden Set, que permanece com histórico separado.

## Pendências
- P3 v1.1: 21.875 keywords fora do piloto; revisão editorial das propostas antes de expansão em massa.
- P2: 4.660 pendências contextuais, mantidas.
- Validar 16 buscas bancárias de intenção híbrida com critérios de interface/SEO antes de publicá-las como páginas de calculadora ou rotas de acesso.
- Revisar cinco falsos negativos **não relacionados à gestação** detectados na amostra de 210 em etapa própria.
- Confirmar escopo editorial de Saúde/gestação antes de estender a taxonomia para todas as famílias.

## Evidências
`08-Entregas/P3-v1.2/`: CSV individual de 43, CSV de 187, patches antes/depois, 30 lotes atualizados, fila geral, QA, regressão e hashes. Scripts em `07-Scripts/P3/`.
