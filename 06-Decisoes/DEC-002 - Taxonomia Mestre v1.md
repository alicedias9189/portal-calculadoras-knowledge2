# DEC-002 - Taxonomia Mestre v1

## Decisão

Adotar a [[../00-Mapa-Global/Taxonomia Mestre v1]] como contrato global para os primeiros lotes da classificação semântica.

## Contexto

A base corrigida contém 294.905 keywords únicas. Uma amostra estratificada global de 10.000 keywords foi analisada antes de formar os lotes completos, com cobertura das sete áreas, sobreposições, faixas de volume, recorrência e famílias de risco semântico.

## Resultado

- 7 áreas temáticas principais.
- saída controlada `Fora de escopo`.
- 92 subclusters na v1.
- 17 tipos de intenção.
- 18 regras globais explícitas.
- Golden Set inicial com 73 casos: 61 reais + 12 regressões sintéticas.

## Regras de mudança

1. Não renomear/fundir subclusters durante um lote sem registrar nova decisão.
2. Novo subcluster pode ser criado apenas quando uma família recorrente não couber na v1.
3. Toda mudança que altere fronteiras entre áreas precisa atualizar o [[../04-Regressao/Golden Set]].
4. Mudanças devem valer prospectivamente para os lotes seguintes e, quando necessário, disparar revalidação dos lotes anteriores afetados.
5. `areas_origem` continua sendo evidência, não verdade de classificação.

## Consequência

A próxima etapa é construir os lotes semânticos usando esta taxonomia e controles repetidos do Golden Set para medir drift entre lotes.
