# MOC - Taxonomia

## Status

**Taxonomia-mestra v1 — ativa.**

Construída a partir da amostra estratificada global de 10.000 keywords da base corrigida de 294.905 keywords. Esta versão é o contrato de consistência para os primeiros lotes. Ela pode crescer, mas mudanças de escopo ou fronteira precisam ser registradas em `06-Decisoes` e testadas no [[../04-Regressao/Golden Set]].

## Áreas primárias

- [[../01-Taxonomia/Matemática]]
- [[../01-Taxonomia/Datas]]
- [[../01-Taxonomia/Conversores]]
- [[../01-Taxonomia/Construção]]
- [[../01-Taxonomia/Trabalho]]
- [[../01-Taxonomia/Energia]]
- [[../01-Taxonomia/Finanças]]

Além das sete áreas, a classificação pode usar **Fora de escopo** quando a consulta não representa uma calculadora/conversor útil para o portal. Casos irresolvidos não devem ser forçados: recebem baixa confiança e revisão manual.

## Princípio central

A pasta/área que originou uma keyword é apenas evidência. A classificação final deve representar a **intenção dominante**.

Exemplos de fronteira:

- `calculadora salario liquido` → Trabalho, não Matemática/Finanças.
- `calculadora de dias entre datas` → Datas, mesmo que apareça em Matemática/Trabalho.
- `1 milhas em km` → Conversores.
- `calculadora metro quadrado parede` → Construção, não Matemática.
- `1 kwh em reais` → Energia e cálculo contextual de custo, não conversão física direta.
- `cotacao do dolar hoje` → Finanças; `1 dólar em real` → Conversores.

## Campos esperados na classificação dos lotes

- `id_global`
- `area_principal`
- `cluster`
- `subcluster`
- `intencao_principal`
- `tipo_intencao`
- `dominio_ou_grandeza`
- `unidade_origem` quando aplicável
- `unidade_destino` quando aplicável
- `direcao_conversao` quando aplicável
- `confianca`
- `revisao_manual`
- `justificativa_curta` para casos não triviais

## Prioridade de decisão entre áreas

1. Contexto temático explícito vence matemática genérica.
2. Conversão direta entre unidades/representações compatíveis → Conversores.
3. Cálculo que depende de regras/variáveis de um domínio → área temática desse domínio.
4. Conversão explícita entre moedas → Conversores; cotação atual/histórica → Finanças.
5. Metragem/material de obra → Construção.
6. Jornada, salário, FGTS, rescisão, férias e benefícios → Trabalho.
7. Consumo/custo/dimensionamento energético → Energia; conversão pura de unidade → Conversores.
8. Datas/calendário genéricos → Datas; períodos regidos por regra trabalhista → Trabalho.
9. Matemática funciona como área geral somente quando nenhum domínio específico domina.

## Governança

1. Uma keyword recebe uma única classificação primária.
2. Novo subcluster só deve ser criado quando uma família recorrente não couber adequadamente na v1.
3. Mudança de nome, fusão ou fronteira exige decisão versionada.
4. Toda mudança relevante deve ser testada contra o Golden Set.
5. `areas_origem` nunca decide sozinha a classificação.
6. Volume do Google Ads serve para priorização, não para decidir intenção.

## Versão

- v1: 92 subclusters
- 17 tipos de intenção
- 18 regras globais explícitas
- Golden Set inicial com 73 casos

Ver também [[MOC - Intenções]], [[../02-Regras/Regras Globais]] e [[../03-Ambiguidades/Ambiguidades Globais]].
