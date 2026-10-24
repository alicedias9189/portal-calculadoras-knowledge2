# ESTADO ATUAL — Portal de Calculadoras

Data: 2026-10-22. Versão mais recente deste pacote: **P3 v2.1**. Repositório canônico: `alicedias9189/portal-calculadoras-knowledge2` (vault Obsidian). **Os arquivos contidos neste ZIP ainda não foram enviados automaticamente ao GitHub**; importar manualmente antes de esperar `git pull` em outra máquina.

## Invariantes e contexto
- Portal de calculadoras/conversores; auditoria de palavras-chave do Google Ads por intenção e família, sem inventar parâmetros e sem somar volumes de variantes.
- 30 lotes, 294.905 base, 2.190 controles, 23.965 keywords P3 em fila, 52.046 registros em fila geral.
- Conservação de IDs, todas as colunas anteriores, barra reconstruída, Ads e decisões P0/P1/P2 fora da revisão.
- As planilhas são artefatos de QA; os CSVs e ZIP de lotes incluem todas as linhas e colunas.
- Não confundir regras automáticas de alta confiança com aprovação editorial de cada keyword.

## Linha de continuidade
- DEC-037 P0; DEC-038 P1; DEC-039 P2. P2 v7: 4.660 pendências abertas.
- DEC-046 a DEC-056: P3 v1 até P3 v2.0, com revisão piloto, auditorias e expansão.
- DEC-056 / P3 v2.0: 272 correções em 132 famílias; 165 decisões amostradas; P3 fora dos pilotos 20.400.
- **DEC-057 / P3 v2.1 (presente):** 165 amostras revisadas, 12 ajustes da amostra e um CET adicional, total 13 patches. 23 mantidas, 130 mantidas com ressalvas. Todos os 30 lotes e as filas passaram na regressão independente. P3 fora dos pilotos continua 20.400.

## Próxima ação
Expansão **pequena** da P3 priorizando famílias novas com intenção operacional clara, com revisão por regra e QA; não voltar a tratar consulta INSS de benefício ou processo como contribuição, e não classificar informação de taxa bancária ou consumo por modelo como cálculo direto. Preservar P2 aberta.

## Contrato de entrega
Usuário quer **um ZIP único aqui no chat para upload manual ao GitHub**, contendo DEC, registros Markdown de continuidade, scripts, QA centralizada, lotes e arquivos-fonte reexecutáveis. Após cada execução, atualizar `08-Continuidade/ESTADO-ATUAL.md` e salvar registro em `08-Continuidade/Registros/`. Se o usuário disser **Faça**, executar a próxima ação sugerida na resposta anterior.

## Início de nova conversa
Ler este arquivo, DEC-057 e os registros recentes antes de prosseguir. Se o GitHub ainda não contiver a P3 v2.1, solicitar importação do ZIP (não supor sincronização remota).
