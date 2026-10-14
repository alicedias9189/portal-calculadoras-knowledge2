# DEC-001 - Estratégia de classificação em lotes

## Status

Aceita.

## Contexto

A base corrigida possui aproximadamente 294,9 mil palavras-chave. Processar semanticamente toda a base de uma vez aumenta o risco de timeout e reduz a capacidade de revisar casos ambíguos com profundidade.

## Decisão

A classificação será feita em lotes controlados, com mecanismos de consistência global.

### Mecanismos obrigatórios

- taxonomia-mestra única;
- regras globais compartilhadas;
- `id_global` persistente;
- `lote_id` persistente;
- Golden Set para detectar drift;
- amostra estratificada global antes dos lotes completos;
- registro de novas decisões no vault;
- reconciliação programática após os lotes;
- auditoria global final por cluster.

## Alternativas rejeitadas

### Classificar toda a base em um único turno

Rejeitada pelo risco operacional e pela experiência anterior de timeout em processamento extenso.

### Dividir cegamente a cada 10.000 linhas

Rejeitada como estratégia única porque pode separar famílias semanticamente próximas e favorecer drift entre lotes.

## Consequência

O Obsidian/GitHub funciona como memória global entre lotes. A planilha continua sendo a fonte de dados; o vault contém as regras necessárias para interpretar a planilha de forma consistente.
