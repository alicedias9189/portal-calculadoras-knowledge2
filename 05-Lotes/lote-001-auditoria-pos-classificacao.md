# Lote 001 — Auditoria pós-classificação

## Veredito

**Estrutura: aprovada. Semântica: reprovada para propagação automática ao lote 002.**

A base foi preservada corretamente e os 73 controles do Golden Set continuam em 73/73, mas a auditoria independente encontrou erros sistemáticos fora do conjunto de controle.

## Integridade

- 9.904 linhas antes e depois da classificação.
- 9.831 keywords base.
- 73 controles.
- 9.831 `id_global` únicos.
- 0 alterações indevidas nas colunas originais.
- Golden Set: 73/73.

## Estado da classificação

- 8.143 confiança alta.
- 399 confiança média.
- 1.289 confiança baixa.
- 1.688 em revisão manual.
- 1.241 linhas continuam sem `cluster` e `subcluster` da Taxonomia v1.

Essas 1.241 linhas têm área atribuída, baixa confiança, revisão manual e proposta de taxonomia, mas ainda não estão totalmente classificadas.

## Problemas sistemáticos confirmados

A auditoria encontrou **259 linhas únicas** fora do conjunto já pendente de taxonomia com erros ou alertas objetivos. Dessas, **168** são de severidade alta e **91** são alertas de qualidade/metadados.

Principais padrões:

- 65 consultas de potência elétrica/aparelhos classificadas como potenciação matemática, sobretudo micro-ondas e air fryer.
- 47 usos de `consulta de preço/mercado` em verbas trabalhistas calculáveis, como rescisão, férias e 13º.
- 34 erros de extração/direção de moedas.
- 25 casos de `peso` genérico tratados com confiança alta apesar da moeda ser ambígua.
- 21 consultas de notícia/preço de combustível tratadas como consumo/custo calculável.
- 19 consultas com `quantos anos` que não representam cálculo de datas.
- 19 conversões diretas com origem/destino/direção vazios.
- 14 consultas de direito/licença trabalhista classificadas como Datas.
- 6 consultas de dia da semana/tradução classificadas como conversão temporal.
- 5 consultas de cotação/variação atual classificadas como conversão direta.
- 3 consultas sobre remuneração de poupança classificadas como remuneração trabalhista.
- 1 consulta de argamassa/obra classificada como Matemática.

## Exemplos

- `potência de microondas em watts` → classificada como Matemática; contexto é potência elétrica/aparelho.
- `remuneração da caderneta de poupança` → classificada como Trabalho; deve ser Finanças/Poupança.
- `nascimento do filho o pai tem direito a quantos dias` → classificada em Datas; é regra/licença trabalhista.
- `variação do dolar em tempo real` → classificada como conversão; é cotação/mercado.
- `gasolina subiu hoje de novo` → classificada como consumo; é notícia/preço de mercado.
- `proporção de argamassa por metro quadrado` → classificada como Matemática; o domínio dominante é Construção.
- `converter dolar australiano em reais` → metadado extraído como `AUD→USD`, quando deveria envolver BRL.
- `convert pesos argentinos to reais` → metadado extraído como `ARS→PESO`, quando deveria envolver BRL.

## Consequência para o Golden Set

O resultado 73/73 continua válido, mas o Golden Set não cobre alguns falsos positivos lexicais importantes. Ele precisa ser ampliado antes do lote 002.

## Próximo passo recomendado

1. Não iniciar o lote 002 ainda.
2. Corrigir os padrões sistemáticos encontrados.
3. Ampliar o Golden Set com os novos casos de regressão.
4. Decidir a Taxonomia v1.1 para as 1.241 linhas sem cluster/subcluster.
5. Reclassificar o lote 001.
6. Repetir a auditoria pós-classificação.
7. Só depois congelar as regras e seguir para o lote 002.
