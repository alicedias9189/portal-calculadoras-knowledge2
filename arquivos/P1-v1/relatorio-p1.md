# P1 — triagem contextual conservadora de 2.557 keywords

## Resultado
- Fila P1: **2557** registros de **1173** famílias, distribuídos nos 30 lotes.
- Regras contextuais fortes, sem pendência manual: **1464**.
- Ainda dependentes de validação semântica/editorial: **1093**.
- Registros cujo conteúdo classificatório mudou: **1719**.
- Mudanças de área: **412**; de tipo de intenção: **1195**.
- Versões paralelas corrigidas: **30** lotes.

## O que foi feito
Cada uma das 2.557 entradas P1 foi submetida a regras contextuais individuais, com marcação de regra, justificativa, antes/depois e preservação de ambiguidades. A decisão foi **automatizada e conservadora**, não equivale à leitura humana independente de todos os termos. Casos sem evidência inequívoca continuam para validação. Essa revisão não autoriza alteração automática em famílias não incluídas em P1.

## Integridade dos dados
- **2190 controles** comparados nos 30 lotes com patch; 73 por lote, **0 controles alterados**.
- **16 colunas originais (incluindo Ads), IDs e keywords mantidos** em todos os registros.
- P0/P2/P3 da fila original: idênticos antes/depois, a salvo de recalcular prioridades indevidamente.
- Conversões monetárias/físicas com direção apenas quando origem, destino e preposição tornam inequívoca a relação. Nenhuma conversão direta final pode omitir metadados.
- Arquivos reabertos e comparados; linhas fora do conjunto P1 não foram alteradas.

## Próxima validação necessária
1. Conferir amostra estratificada de regras e exceções, sobretudo câmbio (`peso` sem país), semanas/mês e `gramas em ml` sem ingrediente.
2. Resolver **1093 pendências** por contexto/produto, sem transformá-las em verdades por regra.
3. Só depois aprovar rótulos como referência para revisão P2. Não inventar demanda multiplicando volumes das variantes de Ads.

## Entregáveis
- `revisao-automatizada-2557-p1.csv`, uma decisão/justificativa por entrada;
- `patches-objetivos-p1.csv`, mudanças pontuais, antes/depois JSON;
- `p1-pendencias-validacao.csv`, itens ainda abertos;
- `fila-priorizada-30-lotes-com-p0-p1.csv`, fila com versões P0 e P1 preservadas;
- `lotes/lote-NNN-revisado-p0-p1-v1.1-barras-v2.csv`, versões paralelas dos lotes modificados;
- `qa-regressao-p1-por-lote.csv` e script reexecutável, dependência Python padrão.
