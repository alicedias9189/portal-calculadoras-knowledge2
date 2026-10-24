# DEC-056 — Expansão seletiva de famílias P3 v2.0

Data: 2026-10-22. Fonte: versão paralela P3 v1.9. **Não sobrescrever arquivos históricos.**

## Escopo e números verificados
- Fila P3: 23.965 registros; fora dos pilotos na entrada: **20.672**.
- Novos patches efetivos: **272**, em **132 famílias**, distribuídos em 9 regras; fora dos pilotos na saída: **20.400**.
- Regras: {"P3V20_INSS_DOMINIO": 32, "P3V20_TAXA_JUROS_INFORME": 77, "P3V20_MATERIAL_DIDATICO": 21, "P3V20_ALGEBRA_DOMINIO": 32, "P3V20_ESTATISTICA_DOMINIO": 4, "P3V20_SALARIO_MATERNIDADE": 9, "P3V20_IRRF_DOMINIO": 1, "P3V20_CONSUMO_VEICULO": 94, "P3V20_CONVERSAO_ENERGIA": 2}.
- Amostra estratificada por regra: **165 itens**, com regras de maior volume amostradas e regras pequenas integralmente listadas. Trata-se de QA de padrões, não homologação editorial independente.
- Integridade: comparação independente **30/30 lotes PASSOU**, 294.905 registros-base e 2.190 controles mantidos; 272 IDs alterados, somente campos analíticos autorizados.
- Fila P3 e fila geral (52.046 linhas): as 149 colunas anteriores são preservadas e foram acrescentadas 8 colunas de rastreabilidade P3 v2.0.
- P2 mantém **4.660 pendências**, sem alterações nesta etapa.

## Interpretações
1. **Consumo por modelo de veículo:** pergunta sobre consumo de um automóvel específico é predominantemente informacional (94 entradas); não pressupõe estimativa parametrizada nem certifica consumo real.
2. **Taxas de bancos (77):** perguntas sobre taxa de empréstimo/CET e rendimentos de poupança ou CDB, sem simulação expressa, são informacionais. Diferenciar crédito de investimento.
3. **INSS (32), salário-maternidade (9) e IRRF (1):** corrigir domínio errado (energia/construção/conversores), sem definir alíquota ou direito previdenciário automaticamente; subgrupo de estabilidade é trabalhista.
4. **Álgebra (32), materiais didáticos (21), estatística (4):** não confundir exercício, livro ou PDF didático com conversor de arquivo ou cálculo efetivo.
5. **Conversão física (2):** direção Wh↔kWh explícita; preencher unidade de origem/destino e sentido, sem inventar taxa de câmbio nem equivalência física de grandezas distintas.

## Limitações e aprovação
As 272 correções são **propostas técnicas conservadoras** apoiadas por padrões textuais e amostragem. A revisão por modelo não representa revisão humana individual de cada palavra-chave, nem verificação de SERP. Há 270 classificações com ressalvas e 2 sem ressalvas quanto à direção explícita; ambas requerem aprovação editorial antes de uso em produção. Permanecem ambiguidade e necessidade de parâmetros externos em várias buscas.

## Evidências
- `08-Entregas/P3-v2.0/p3-v2.0-patches.csv`: diffs auditáveis por ID, com JSON antes/depois reais.
- `p3-v2.0-decisoes.csv`: todas as 272 propostas.
- `p3-v2.0-amostra-qa.csv`: amostra estratificada (165).
- `p3-v2.0-regressao-independente-resumo.json` e CSV com 30 lotes.
- `lotes-001-a-030-p3-v2.0.zip`, filas completas e QA Excel centralizada.
- Scripts em `07-Scripts/P3/`; fontes de reprodução dentro da entrega.

## Próxima etapa
Revisar criticamente uma amostra dirigida das **272 decisões**, dando prioridade às famílias de consumo de veículo, juros de bancos, INSS e materiais PDF; corrigir falsos positivos antes de ampliar a P3. Manter as 4.660 pendências P2 separadas e decidir quando a revisão manual passa a ser mais útil que novas regras amplas.
