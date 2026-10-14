# Ambiguidades Globais

Casos conhecidos que devem ser usados para calibrar a taxonomia e o Golden Set.

## Libra

- `converter libras em kg` → massa/peso.
- `libra hoje`, `valor da libra` → provável moeda/cotação.
- termos curtos como `1 libra` podem exigir contexto adicional.

## Arroba

- `converter arroba em kg` → massa/peso.
- `preço da arroba do boi` → preço/cotação de commodity; não conversão de massa.

## PDF e extensões

- presença de `pdf` não significa automaticamente conversão de arquivo.
- buscas por conteúdo, apostila, documento ou relatório em PDF devem ser separadas de intenção de converter arquivo.

## Dados digitais

- `MB/s` ≠ `Mbps`.
- `mb s` deve ser interpretado pelo contexto e nunca fundido automaticamente com Mbps.
- `WhatsApp GB` pode ser nome/variante de aplicativo e não armazenamento digital.

## Grandezas incompatíveis

- m³ → m² exige variável adicional.
- cm → m² exige variável adicional.
- g → mL depende da densidade da substância.
- N → J depende de contexto físico, como deslocamento.

## Regra

Quando uma ambiguidade recorrente for resolvida, registrar a decisão em `06-Decisoes` e criar ou atualizar casos no [[../04-Regressao/Golden Set]].
