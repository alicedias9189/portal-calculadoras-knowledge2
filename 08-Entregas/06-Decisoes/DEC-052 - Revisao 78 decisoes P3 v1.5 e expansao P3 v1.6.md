# DEC-052 — Revisão crítica dos 78 novos registros P3 v1.5 e P3 v1.6
Data: 2026-10-21. Versão paralela: **P3 v1.6**.

## Decisão
Revisar as 78 classificações propostas na expansão P3 v1.5, corrigir 11 classificações que confundem intenções ou produtos distintos e expandir P3 com 152 outras classificações contextuais em 56 famílias. A análise é por regras linguísticas e revisão contextual, não homologação editorial de todas as 23.965 consultas.

## Ajustes concretos do QA
- Fundos de títulos públicos não equivalem à aquisição direta de títulos federais.
- Títulos públicos **e privados** não devem ser classificados como apenas Tesouro Direto.
- Juros do consignado da Caixa representam busca informacional por taxa, não necessariamente simulação.
- Simulador de banco nomeado sugere navegação para ferramenta específica; intenção mista é marcada com ressalva e necessita revisão editorial.
- Consulta sobre salário mínimo do aposentado é previdenciária, não somente piso salarial de empregado.
- Acesso à antecipação do FGTS por plataforma nomeada é navegacional/transacional, mas as regras vigentes e a elegibilidade não foram presumidas.

## Expansão controlada
59 casos sobre descontos e tabelas INSS, 54 consultas informacionais de taxas imobiliárias, 15 sobre variância/desvio padrão, 13 serviços bancários, 5 combinatória, 5 numerais romanos, 1 raiz cúbica explícita. Os casos de contribuição patronal, alíquotas de obra e teto previdenciário sem contexto de folha não foram incorporados indiscriminadamente.

## Regressão
- 163 patches exatos (11 QA + 152 novos), 30/30 lotes PASSOU, 294.905 bases e 2.190 controles preservados.
- Hash SHA-256 dos campos protegidos: `fa4cfa20826ace0e4b66af49d2b8d50d927410a331bdf8781292a2c81dff1ffb`.
- P3 fora dos pilotos: 20.907 → 20.755 (total da P3: 23.965). P2: 4.660 pendências preservadas.
- Todas as informações originais Ads, palavras-chave, IDs, P0/P1/P2 e lotes anteriores permanecem intactos.

## Status e limites
- Confiança média e `revisao_manual=sim`: propostas a validar editorialmente.
- Não fixar juros de bancos, regras de FGTS, faixas INSS ou taxas históricas sem fonte datada externa.
- A categoria Saúde v1.2 e ambiguidades P2 mantêm ressalva.
- Esta decisão registra P3 v1.6 sem substituir DEC-051 ou outros arquivos anteriores.

## Próxima ação
Revisar amostra estratificada das 152 novas propostas, com prioridade para as regras INSS e taxa imobiliária, corrigindo falsos positivos antes de outra expansão; medir rendimento da triagem versus custo editorial.
