# ESTADO ATUAL — Portal de Calculadoras

Última atualização: 2026-10-17 (sincronização de documentação P1/P2 para o GitHub).
Fonte canônica: `alicedias9189/portal-calculadoras-knowledge2`, branch `main`.
**Leia este documento primeiro em uma nova conversa. Depois leia o registro mais recente em `08-Continuidade/Registros/` e DEC-038 a DEC-040.**

## Propósito
Portal de calculadoras de matemática, datas, conversores, trabalhistas, elétricos, construção, saúde etc. Estamos auditando, normalizando e classificando uma base de palavras-chave obtidas no Google Ads. A planilha é a base de dados; o vault Obsidian documenta taxonomia, regras, ambiguidades, decisões, regressão, status dos lotes e scripts.

## Invariantes
- 30 lotes; 294.905 IDs de keywords-base, 2.190 controles (73 por lote).
- Conservar ID, keyword, dados Ads, colunas originais e resultados já aprovados. Não somar volumes de variantes artificiais.
- Reconstituir barras removidas com contexto (ex.: `1 3` pode representar `1/3` quando evidência suficiente); não supor pontuação indiscriminadamente.
- Diferenciar intenção de calculadora de informação/comércio/navegação; moeda e direção exigem texto explícito; massa↔volume exige densidade; não alucinar valores/parâmetros.
- Golden Set histórico: 3.210/3.210 reportados no fechamento dos lotes antigos. Regressões P1/P2 foram estruturais, não revalidação integral independente desse Golden Set.

## Histórico resumido
1. 30/30 lotes classificados/encerrados no passado. DEC-036: saneamento das 73 inconsistências do lote 001 (7 conversões completadas, 66 intenções ajustadas). Fila de revisão originalmente 52.046 keywords / 15.117 famílias, antes das revisões P0 a P2.
2. P0: 474 analisadas, 462 com patches, 102 mudanças de área, 109 ainda contextualmente incertas. DEC-037 previamente versionada.
3. P1 primeira passagem: 2.557 keywords, 1.464 fortes, 1.093 pendentes. Segunda passagem: 700 validadas, 361 com ressalva, 32 ainda abertas. Documento DEC-038.
4. P2 primeira passagem: 25.050 keywords, 8.946 fortes, 7.291 com ressalva, 8.813 pendentes. Segunda passagem desses 8.813: 959 resolvidas, 1.716 com ressalvas, 6.138 pendentes; 438 amostras, 5 sinais de revisão. Documento DEC-039.
5. P3 ainda não revisada neste fluxo.

## Estado de sincronização
- P0 estava no GitHub antes desta operação.
- P1/P2: relatórios, 10 scripts e documentação de continuidade importados ao GitHub nesta operação; detalhes em `08-Entregas/MANIFESTO.md`.
- IMPORTANTE: planilhas XLSX, ZIPs com 30 lotes e CSVs completos ainda se encontram na Biblioteca do ChatGPT, NÃO no GitHub. O commit não sincroniza os dados binários.
- Os relatórios atuais refletem revisões automatizadas orientadas por regras, **não aprovação editorial humana**.

## Próximos passos, em ordem
1. Completar a transferência dos 12 arquivos ZIP/XLSX da Biblioteca para o GitHub, com checagem de hashes, sem sobrescrever fontes ou aprovações históricas.
2. Revisar contextualmente 6.138 pendências P2 e os 5 alertas semânticos; validar amostra dos classificados.
3. Revisar as 32 ambiguidades P1 se surgirem novos dados.
4. Somente então avançar demais prioridades, incluindo P3, com controle de regressão e documentação de DEC.
5. Após CADA resposta substantiva de ChatGPT, salvar novo registro .md em `08-Continuidade/Registros/` e atualizar este estado, conforme DEC-040.

## Retomada numa nova conversa
Peça "Leia `08-Continuidade/ESTADO-ATUAL.md` e os dois registros mais recentes no GitHub `alicedias9189/portal-calculadoras-knowledge2` antes de continuar". Conferir branch `main`. Não usar "Cofre" do ChatGPT como sinônimo do vault Obsidian. Não confundir blobs preparados com commit publicado; verificar ref `main` antes de confirmar o resultado.