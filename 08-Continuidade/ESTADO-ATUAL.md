# ESTADO ATUAL — Portal de Calculadoras

Última atualização: 2026-10-24 (P3 v5.2 + filtro de cores Ouro, DEC-089).
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
5. P3 já em andamento: v4.8 selecionou 75 IDs; v4.9 revisou esses 75 e refinou 27; v5.0 selecionou outros 75 (DEC-086), saldo P3 elegível = 19.637.

## Estado de sincronização
- P0 estava no GitHub antes desta operação.
- P1/P2: relatórios, 10 scripts e documentação de continuidade importados ao GitHub nesta operação; detalhes em `08-Entregas/MANIFESTO.md`.
- IMPORTANTE: planilhas XLSX, ZIPs com 30 lotes e CSVs completos ainda se encontram na Biblioteca do ChatGPT, NÃO no GitHub. O commit não sincroniza os dados binários.
- Os relatórios atuais refletem revisões automatizadas orientadas por regras, **não aprovação editorial humana**.

## Atualização prioritária — limpeza de Ouro/Ouro escuro 1 (24/10/2026)
- **DEC-089:** sete sementes ODS auditadas. Em `SementesEnergia.ods`/Codex há 3.368 palavras em Ouro e 348 em Ouro escuro 1; são 3.610 expressões distintas após normalização.
- Comparação com 294.905 IDs: 3.621 correspondências; **3.609 IDs excluídos somente de visões derivadas**, 12 retidos para revisão por origem também não dourada. 9 sementes não presentes na base.
- Regressão independente confirmou **30/30 lotes**, **2.190 controles intactos** e igualdade campo a campo de todos os IDs retidos. Base operacional dos lotes: 291.296.
- Fila P3 de trabalho: 23.865; **P3 estritamente elegíveis: 19.462** (antes 19.562). A fila geral de trabalho fica em 51.884; originais permanecem preservados.
- Três scripts reproduzíveis em `07-Scripts/P3/cores/`; relatório em `08-Entregas/P3-v5.2-Auditoria-Cores-Ouro/LEIA-ME.md`. ZIP com CSVs, lotes e XLSX foi entregue em conversa ChatGPT, **não está integralmente no GitHub**.
- Homologação editorial pendente. **Próxima etapa: P3 v5.3**, revisão crítica dos 75 pareceres da v5.2; depois expansões de 100 IDs/rodada partindo dos 19.462 elegíveis.

## Histórico — P3 v5.2 (24/10/2026)
- **DEC-088**, 75 novas classificações em 32 famílias e 7 temas sobre a base P3 v5.1; 19.637 → **19.562 elegíveis**.
- Regressão independente validou 30/30 lotes, 75/75 patches permitidos, **294.905 registros-base**, **2.190 controles** e 390 colunas históricas intactas em ambas as filas (8 novas colunas de rastreabilidade).
- P2 pendentes 4.660; 98 propostas globais preservadas byte a byte. Pareceres técnicos; homologação editorial **PENDENTE**.
- Quatro scripts Python versionados em `07-Scripts/P3/`; os arquivos binários completos estão no ZIP da conversa ChatGPT e **não foram enviados ao GitHub**.
- **Próxima tarefa: P3 v5.3 — revisar criticamente os 75 pareceres v5.2, sem seleção de novos IDs antes.**

## Histórico — P3 v5.1 (24/10/2026)
- DEC-087 e registro `08-Continuidade/Registros/2026-10-24-06-P3-v5.1-revisao-75.md`: **75 pareceres revisados, 19 refinamentos e 56 mantidos com ressalvas**, 49 famílias e oito grupos.
- Regressão independente **30/30 lotes PASSOU**, 294.905 bases, 2.190 controles. Filas 23.965/52.046 linhas com **382 colunas históricas intactas**, mais oito novas de rastreabilidade.
- P3 ainda elegíveis **19.637**; P2 pendentes **4.660**; 98 propostas globais preservadas byte a byte.
- Quatro scripts Python reproduzíveis estão versionados em `07-Scripts/P3/` no GitHub; as filas CSV completas, os lotes e o XLSX estão no ZIP entregue no ChatGPT, **não no GitHub**.
- Homologação editorial **PENDENTE**. P3 v5.2 concluída; consultar DEC-088.

## Histórico — P3 v5.0 (24/10/2026)
- Fonte técnica: pacote ZIP P3 v4.9 e relatórios dos 30 lotes.
- DEC-086: 75 novos IDs, 49 famílias, 8 temas; 30/30 regressões e 75/75 patches autorizados. Históricos preservados. P2 pendentes 4.660, P3 elegíveis 19.637.
- Pareceres técnicos pendentes de homologação editorial. ZIP v5.0 completo disponibilizado em conversa ChatGPT, não armazenado integralmente no GitHub.
- Revisão crítica dos mesmos 75 IDs concluída na P3 v5.1; consulte DEC-087.

## Próximos passos históricos (anotações de 17/10; não substituem a tarefa prioritária)
1. Completar a transferência dos 12 arquivos ZIP/XLSX da Biblioteca para o GitHub, com checagem de hashes, sem sobrescrever fontes ou aprovações históricas.
2. Revisar contextualmente 6.138 pendências P2 e os 5 alertas semânticos; validar amostra dos classificados.
3. Revisar as 32 ambiguidades P1 se surgirem novos dados.
4. Somente então avançar demais prioridades, incluindo P3, com controle de regressão e documentação de DEC.
5. Após CADA resposta substantiva de ChatGPT, salvar novo registro .md em `08-Continuidade/Registros/` e atualizar este estado, conforme DEC-040.

## Retomada numa nova conversa
Peça "Leia `08-Continuidade/ESTADO-ATUAL.md` e os dois registros mais recentes no GitHub `alicedias9189/portal-calculadoras-knowledge2` antes de continuar". Conferir branch `main`. Não usar "Cofre" do ChatGPT como sinônimo do vault Obsidian. Não confundir blobs preparados com commit publicado; verificar ref `main` antes de confirmar o resultado.