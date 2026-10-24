# Registro 2026-10-21 — P3 v1.5: revisão 98 e expansão limitada

## Pedido do usuário
“Faça” = cumprir a etapa sugerida na última resposta: auditar a amostra estratificada de 98 decisões da P3 v1.4, corrigir falsos positivos e depois expandir P3 com cautela. Entrega em ZIP único, para o usuário enviar manualmente ao GitHub.

## Trabalho executado
1. Recuperado ZIP da P3 v1.4 da conversa e extraídos os dados originais, incluindo 98 registros de `Amostra expansao` da planilha com `artifact_tool`.
2. Revisados 98 pareceres: cinco correções diretamente identificadas, 12 mantidos com ressalvas explícitas, 81 sem erro evidente na revisão textual. Foram identificadas 31 taxas bancárias incorretamente tratadas como navegação, nove tutoriais de aposentadoria como cálculo e uma explicação de jornada.
3. Propagadas apenas as correções de regras com contexto idêntico; 41 revisões no total, sem modificar registros não correspondentes.
4. Classificadas 78 novas keywords P3 ainda fora dos pilotos (35 famílias), com regras para domínio de finanças e matemática; cinco conflitos temporais de salário mínimo mantidos pendentes.
5. Gerada P3 v1.5 paralela, os 30 CSVs, filas completas, 119 patches individuais, planilha centralizada e scripts.
6. Regressão **independente** comparou os lotes e as filas v1.4/v1.5: `PASSOU`, 30/30 lotes, 294.905 bases, 2.190 controles e SHA256 dos campos protegidos igual. Todos os 119 patches correspondem ao antes/depois real.

## Resultado
- P3 original: 23.965 keywords; fora dos pilotos: **20.985 → 20.907**.
- 119 alterações = 41 QA + 78 expansão; 35 famílias novas.
- P2: 4.660 pendências, não tocadas.
- Escopo de Saúde v1.2: pendente de homologação, não mudado nesta revisão.

## Entregáveis
ZIP único `portal-calculadoras-auditoria-P3-v1.5-unico.zip`; os arquivos internos são relativos à raiz do vault Obsidian; relatório `08-Entregas/P3-v1.5/RELATORIO-P3-V1.5.md`; decisão `06-Decisoes/DEC-051 - Revisao critica P3 v1.5 e expansao segura.md`; scripts `07-Scripts/P3/*v1_5.py`; estado atual deste diretório.

## Próxima etapa
Revisão amostral de 78 novas decisões, especialmente salário mínimo histórico e antecipação de FGTS; corrigir falsos positivos e ampliar a P3 por regras mais específicas. Sem inserir números de demanda Ads ou modificar decisões históricas.

## Importação e cuidado
O ZIP **não foi enviado diretamente ao GitHub**. Extrair com conferência dos arquivos existentes e preservar cópias anteriores; em seguida `git add/commit/push`. `ESTADO-ATUAL.md` deve ser mesclado se a cópia local estiver mais nova. O arquivo `LEIA-ME-IMPORTAR-P3-V1.5.md` contém o procedimento. A revisão não é homologação editorial integral.
