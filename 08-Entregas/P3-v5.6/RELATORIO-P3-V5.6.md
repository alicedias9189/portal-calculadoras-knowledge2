# Relatório técnico — P3 v5.6

**Data:** 24/10/2026 | **DEC-093** | **Homologação editorial: PENDENTE**

### Resultado

- 100 novas palavras-chave analisadas, 52 famílias, 12 grupos semânticos.
- 100 pareceres e 100 patches com comparação de valores anteriores e posteriores.
- 85 IDs tiveram mudança de área, 73 mudança de tipo de intenção; sobreposição permitida.
- Correções abrangem ações e tributação, moedas colecionáveis, 110/127 V e energia, impostos salariais, telhados, materiais de construção, 14º salário de aposentados, combinatória, simuladores de investimentos, IRPF de aplicações, pisos/rodapés e impossibilidade de derivar nascimento do CPF.
- Não foram calculados preços, tributos, alíquotas, direitos, potenciais ganhos ou dados pessoais ausentes das palavras-chave.

### Regressão independente

- 60/60 lotes aprovados (30 canônicos + 30 filtrados sem Ouro).
- Todos os 100 patches conferidos nos dois conjuntos; nenhum ID fora do escopo mudou de classificação.
- 294.905 registros-base canônicos; 291.296 operacionais; 2.190 controles por versão.
- Filas de 23.965, 52.046, 23.865 e 51.884 linhas; todas as 422 colunas anteriores preservadas e oito novas para P3 v5.6.
- 3.609 variantes Ouro continuam excluídas somente da visão de trabalho, de forma reversível.
- Backlog global de 98 propostas idêntico em bytes; pendências P2 (4.660) sem intervenção.

### Saldo

- P3 elegíveis sem Ouro antes: 19.362.
- **P3 elegíveis sem Ouro depois: 19.262.**
- P3 elegíveis canônicos depois: 19.362.

### Documentos de suporte

- `p3-v5.6-pareceres-100.csv`: 100 análises individualizadas.
- `p3-v5.6-patches-100.csv`: alterações autorizadas por ID e JSON antes/depois.
- `p3-v5.6-regressao-independente-60-lotes.csv`: testes de todos os lotes.
- `qa-auditoria-P3-v5.6-centralizada.xlsx`: sete abas com células centralizadas.
- Quatro scripts Python reproduzíveis em `07-Scripts/P3/` e SHA-256 no ZIP.

### Próximo passo

P3 v5.7: revisão crítica individual dos 100 pareceres; não selecionar novas palavras antes dessa revisão. Classificações técnicas não são homologação editorial humana.