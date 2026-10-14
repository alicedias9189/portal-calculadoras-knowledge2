# MOC - Intenções

## Status

Lista de intenções **v1 — ativa** para os primeiros lotes.

O tipo de intenção descreve o que a pessoa quer fazer, não apenas o assunto mencionado.

## Tipos de intenção

- **cálculo direto** — fórmula determinística com entradas suficientes.
- **conversão direta** — transformação entre unidades/representações compatíveis.
- **simulação/projeção** — evolução, parcelas, rendimento ou cenário ao longo do tempo.
- **dimensionamento** — tamanho/capacidade/quantidade técnica necessária.
- **estimativa de quantidade** — materiais/itens necessários.
- **estimativa de consumo** — consumo energético/combustível.
- **estimativa de custo** — custo calculado a partir de quantidade, tarifa ou preço.
- **cotação atual** — requer taxa/preço corrente.
- **cotação histórica** — requer taxa/preço de data passada.
- **tabela/referência** — tabela ou equivalência, sem necessariamente cálculo interativo.
- **informacional** — explicação, regra ou conceito.
- **navegacional/transacional** — acessar serviço, app, saldo, banco ou produto específico.
- **conversão de arquivo/mídia** — transformar formato de documento, imagem, áudio ou vídeo.
- **cálculo contextual** — relação depende de variável adicional, como densidade, tarifa ou fator de potência.
- **consulta de preço/mercado** — preço comercial de bem, commodity ou serviço.
- **fora de escopo** — não representa ferramenta útil para o portal.
- **ambígua/revisão** — há mais de uma interpretação plausível sem contexto suficiente.

## Exemplos de fronteira

- `1 milhas em km` → conversão direta.
- `converter gramas em ml` → cálculo contextual.
- `cotacao do dolar hoje` → cotação atual.
- `1 dólar em real` → conversão direta.
- `calculadora de juros compostos` → simulação/projeção.
- `ar condicionado 12000 btus consumo` → estimativa de consumo.
- `calcular quantidade de telhas` → estimativa de quantidade.
- `apk whatsapp gb` → fora de escopo.

## Regra

Quando o tipo de intenção for contextual, ambíguo ou dependente de dado dinâmico, isso deve aparecer também em `confianca` e `revisao_manual` quando aplicável.

Veja [[../03-Ambiguidades/Ambiguidades Globais]] e [[Taxonomia Mestre v1]].
