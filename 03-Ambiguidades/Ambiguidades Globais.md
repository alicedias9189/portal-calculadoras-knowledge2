# Ambiguidades Globais

Casos recorrentes usados para calibrar a Taxonomia-mestra v1 e o Golden Set.

## Libra

- `converter libras em kg` → Conversores / massa e peso.
- `libra hoje`, `valor da libra`, `cotação da libra hoje` → Finanças / cotação atual.
- `1 libra em real` → provável moeda e conversão cambial; manter atenção à ambiguidade lexical.
- termos curtos como `1 libra` podem exigir contexto adicional.

## Arroba

- `converter arroba em kg` → Conversores / massa e peso.
- `preço da arroba do boi` → preço/cotação de commodity; não conversão de massa.

## PDF e extensões

- presença de `pdf`, `jpg`, `mp3`, `mp4` etc. não significa automaticamente conversão de arquivo.
- `conversão de pdf para word` → Conversores / arquivo.
- `a mulher v em pdf` → busca por conteúdo, fora de escopo da conversão.
- `dimensionamento energia solar fotovoltaica pdf` → Energia / intenção informacional sobre dimensionamento.

## Dados digitais

- `MB/s` ≠ `Mbps`.
- `mb s` deve ser interpretado pelo contexto e nunca fundido automaticamente com Mbps.
- `150mbps mb s` é uma relação de taxa de transferência que precisa preservar bit/byte.
- `WhatsApp GB` é nome/variante de aplicativo e não armazenamento digital.

## Grandezas incompatíveis

- m³ → m² exige variável adicional.
- cm → m² exige variável adicional.
- g → mL depende da densidade da substância/ingrediente.
- N → J depende de contexto físico, como deslocamento.
- kVA → kW pode depender de fator de potência.

Esses casos não devem receber conversão direta apenas porque duas unidades foram detectadas.

## Energia versus Conversores

- `1 kwh em w` → conversão de grandeza/unidade e deve ser validada tecnicamente.
- `1 kwh em reais` → Energia / custo de consumo; exige tarifa e possivelmente local/período.
- `ar condicionado 12000 btus consumo` → Energia.
- BTU↔W puramente como unidade → Conversores.

## Construção versus Matemática

- `area de um triângulo` → Matemática.
- `calculadora metro quadrado parede` → Construção.
- `1 litro de tinta pinta quantos metros quadrados` → Construção.
- `piso salarial` nunca deve ser classificado como piso/revestimento de Construção.

## Trabalho versus Datas/Finanças

- `calculadora de dias entre datas` → Datas.
- `tempo de serviço` com regra trabalhista → Trabalho.
- `calculadora salario liquido` → Trabalho, embora também apareça em Finanças/Matemática.
- `calculadora inss obra` → Construção quando o contexto de obra é explícito; INSS de folha → Trabalho.

## Câmbio

- valor explícito A→B (`100 dólares em reais`) → Conversores.
- `dólar hoje`, `cotação da libra hoje` → Finanças / cotação atual.
- consulta histórica de moeda → Finanças / cotação histórica.

## Regra

Quando uma ambiguidade recorrente for resolvida, registrar a decisão em `06-Decisoes` e criar/atualizar casos no [[../04-Regressao/Golden Set]].

Ver [[../00-Mapa-Global/Taxonomia Mestre v1]].
