# MOC - Intenções

> A lista abaixo é provisória até a amostra estratificada ser analisada em High.

Tipos de intenção que devem ser distinguidos durante a classificação:

- Conversão direta
- Conversão que exige contexto ou variável adicional
- Cálculo direto
- Simulação
- Cotação atual
- Cotação histórica
- Consulta informativa
- Consulta educacional
- Tabela ou referência
- Conversão de arquivo/mídia
- Busca transacional/comercial
- Busca por documento/conteúdo
- Fora do escopo do portal
- Ambígua / revisão manual

## Princípio

O tipo de intenção deve descrever o que a pessoa quer fazer, não apenas o assunto mencionado na consulta.

Exemplos de conflitos já conhecidos:

- `preço da arroba do boi` não é automaticamente conversão de massa.
- `libras hoje valor` pode ser cotação de moeda, não unidade de peso.
- `medidas de mitigação das mudanças climáticas pdf` é busca por conteúdo/documento, não conversão de PDF.
- `converter gramas em ml` exige contexto de densidade.

Veja [[../03-Ambiguidades/Ambiguidades Globais]].
