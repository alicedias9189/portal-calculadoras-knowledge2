# Registro da resposta — 2026-10-21 — P3 v1.4

## Solicitação
Usuário disse “Faça”, retomando a ação recomendada na resposta anterior: auditar criticamente os 67 registros de amostra P3 v1.3, corrigir falsos positivos e preparar expansão controlada da P3.

## O que foi executado
1. Verificada origem P3 v1.3 (30 lotes CSV, P3 fila, fila geral e decisões do piloto).
2. Recriada amostra estratificada de 67 IDs pela mesma semente da planilha P3 v1.3.
3. Corrigidas duas interpretações incorretas: ID 160013 (fração na calculadora do celular) e ID 76549 (concreto para piso de garagem).
4. Marcadas 3 consultas para ressalva editorial adicional (56082, 12838, 199183); demais 62 não demonstraram erro evidente na amostra.
5. Aplicadas 576 classificações contextuais adicionais a registros P3 fora dos pilotos, em 170 famílias, totalizando 578 patches.
6. Geradas filas completas e 30 lotes P3 v1.4 (sem sobrescrever versões anteriores), decisão por ID, patches com antes/depois reais, planilha centrada e script/regras.
7. Executada regressão independente de lotes e de campos protegidos: PASSOU em 30/30, com 294.905 bases e 2.190 controles intactos.
8. Preparado um ZIP único para importação manual no GitHub, com relatório, DEC-050, manifesto SHA-256 e fontes de reexecução.

## Números finais
- QA 67; 2 correções; 3 ressalvas editoriais; 62 sem incoerência evidente.
- 576 novos casos revisados, 170 famílias.
- P3 fora dos pilotos: 21.561 → 20.985; universo P3: 23.965.
- P2: 4.660 pendências preservadas.
- As classificações propostas continuam sob responsabilidade de revisão editorial.

## Continuidade
Próximo passo: amostra crítica de 98 propostas da expansão P3 v1.4, revisão de falsos positivos por regras e nova ampliação somente após correções. Não alterar taxonomia da Saúde sem deliberação de escopo. O usuário fará o envio ao GitHub; não declarar commit automático.
