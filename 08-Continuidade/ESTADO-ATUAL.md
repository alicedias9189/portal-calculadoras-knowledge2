# ESTADO ATUAL — Portal de Calculadoras

Última atualização: 2026-10-24 (P3 v5.6 concluída tecnicamente, sincronização parcial).
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

## Atualização prioritária — P3 v5.6 (24/10/2026)

- Expansão técnica de **100 novos IDs**, **52 famílias** em **12 grupos** a partir da P3 v5.5 após filtro Ouro.
- **85 mudanças de área** e **73 de tipo de intenção**. A revisão crítica e homologação editorial ainda estão **PENDENTES**.
- Regressão independente **60/60 lotes PASSOU** e conferiu 100 patches por ID. **294.905 registros-base canônicos**, **291.296 operacionais**, **2.190 controles por versão** preservados; 3.609 Ouro excluídos só da visão de trabalho.
- Quatro filas mantiveram **422 colunas históricas**, acrescidas oito novas colunas P3 v5.6. Backlog 98 e 4.660 pendências P2 intactos.
- Saldo operacional P3 sem Ouro **19.362 → 19.262**; saldo canônico **19.462 → 19.362**.
- Arquivo completo: `portal-calculadoras-auditoria-P3-v5.6-unico.zip`, entregue no ChatGPT e validado por manifesto SHA-256.
- **GitHub sincronizado parcialmente:** publicados os scripts de regressão, QA e empacotamento, o relatório, o registro, README e manifesto. As publicações do script principal `auditar_p3_v56.py` e da DEC-093 foram bloqueadas; ambos permanecem no ZIP. Os binários completos não foram enviados ao GitHub. **Não tratar GitHub como cópia integral da etapa.**
- **Próxima tarefa: P3 v5.7**, revisão individual dos 100 pareceres v5.6, sem expandir novos IDs antes dessa revisão.

## Histórico — P3 v5.5 (24/10/2026)
- **DEC-092:** revisão individual de **100 IDs** da v5.4 (34 famílias, 7 grupos), com **23 refinamentos e 77 classificações mantidas com ressalvas**. **Sem expansão nova** de IDs.
- Regressão independente **60/60 lotes PASSOU**, 23/23 patches registrados com antes/depois, nenhuma alteração em IDs fora do escopo.
- Total canônico: **294.905 bases**; sem Ouro: **291.296 bases**; controles: **2.190 por versão**. Filtro Ouro de **3.609 IDs** permanece reversível (DEC-089).
- Quatro filas completas mantiveram **414 colunas históricas** sem alteração, recebendo oito novas colunas de rastreabilidade v5.5. P2 pendentes **4.660** e backlog global **98** preservados.
- P3 elegíveis: **19.362 operacionais sem Ouro** e **19.462 canônicos**. Não houve redução, pois foi uma revisão dos 100 IDs já tratados.
- Quatro scripts Python em `07-Scripts/P3/*p3_v55.py`; relatório `08-Entregas/P3-v5.5/RELATORIO-P3-V5.5.md`, DEC-092 e continuidade versionados no GitHub. Binários integrais CSV/XLSX/ZIP no pacote entregue pelo ChatGPT, não sincronizados integralmente ao GitHub.
- Homologação editorial **PENDENTE**; algumas consultas sobre direitos da gestante ainda exigem validação de âmbito, sem afirmar intenção exclusivamente trabalhista.
- P3 v5.6 concluída tecnicamente, com 100 novos IDs e regressão independente 60/60. Consulte registro mais recente.

## Histórico — P3 v5.4 (24/10/2026)
- **DEC-091**: expansão fechada de **100 novos IDs / 34 famílias / 7 grupos** dentre os 19.462 P3 elegíveis após filtro Ouro (DEC-089); nenhuma classificação anterior reaberta nesta etapa.
- **100/100 patches registrados** com JSON antes/depois; 45 alterações de área e 89 de tipo de intenção. Homologação editorial **PENDENTE**.
- Regressão independente **60/60 lotes PASSOU** (30 canônicos + 30 filtrados), 100/100 IDs; 294.905 bases canônicas e 291.296 bases de trabalho preservadas (número de linhas), com 2.190 controles em cada conjunto. Filtro de 3.609 IDs Ouro permanece reversível.
- Quatro filas preservaram **406 colunas históricas**, recebendo somente oito novas de rastreabilidade v5.4. 4.660 pendências P2 e backlog de 98 propostas globais preservados.
- P3 ainda elegíveis: **19.362 após Ouro**; **19.462 na fonte canônica**.
- Scripts Python reutilizáveis em `07-Scripts/P3/*p3_v54.py`; decisão, relatório, manifesto e registro de continuidade versionados. ZIP contendo os CSVs completos, lotes e XLSX disponível no ChatGPT, **não enviado como binário ao GitHub**.
- P3 v5.5 concluída e registrada em DEC-092. Próxima expansão v5.6 de 100 IDs sem Ouro.

## Histórico — P3 v5.3 (24/10/2026)
- **DEC-090:** 75 pareceres individuais da v5.2 revisados; **6 refinamentos e 69 mantidos com ressalvas**. Não foram incluídos novos IDs.
- Regressão independente **60/60 lotes PASSOU** (30 canônicos, 30 após filtro Ouro), 6/6 patches. Mantidos 294.905 IDs-base canônicos, 291.296 IDs-base de trabalho e 2.190 controles em cada versão.
- Quatro filas preservaram **398 colunas históricas**, recebendo somente oito novas de rastreabilidade v5.3. Backlog global 98 preservado em bytes, P2 pendentes 4.660 intactas.
- P3 **19.462 elegíveis no filtro Ouro**, 19.562 na fonte canônica, sem alteração de saldo porque a v5.3 não abriu novos IDs. O filtro Ouro de 3.609 IDs é reversível (DEC-089).
- `07-Scripts/P3/*p3_v53.py` reúne quatro scripts reproduzíveis; `08-Entregas/P3-v5.3/RELATORIO-P3-V5.3.md` e o registro atualizado detalham evidências. Os CSVs/XLSX/ZIPs completos estão no pacote entregue via ChatGPT, **não no repositório**.
- Homologação editorial **PENDENTE**. **P3 v5.4 concluída** em DEC-091; 100 novos IDs com regressão 60/60.

## Histórico — limpeza de Ouro/Ouro escuro 1 (24/10/2026)
- **DEC-089:** sete sementes ODS auditadas. Em `SementesEnergia.ods`/Codex há 3.368 palavras em Ouro e 348 em Ouro escuro 1; são 3.610 expressões distintas após normalização.
- Comparação com 294.905 IDs: 3.621 correspondências; **3.609 IDs excluídos somente de visões derivadas**, 12 retidos para revisão por origem também não dourada. 9 sementes não presentes na base.
- Regressão independente confirmou **30/30 lotes**, **2.190 controles intactos** e igualdade campo a campo de todos os IDs retidos. Base operacional dos lotes: 291.296.
- Fila P3 de trabalho: 23.865; **P3 estritamente elegíveis: 19.462** (antes 19.562). A fila geral de trabalho fica em 51.884; originais permanecem preservados.
- Três scripts reproduzíveis em `07-Scripts/P3/cores/`; relatório em `08-Entregas/P3-v5.2-Auditoria-Cores-Ouro/LEIA-ME.md`. ZIP com CSVs, lotes e XLSX foi entregue em conversa ChatGPT, **não está integralmente no GitHub**.
- Homologação editorial pendente. **P3 v5.3 concluída em DEC-090**; iniciar expansão seletiva de 100 IDs em v5.4.

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