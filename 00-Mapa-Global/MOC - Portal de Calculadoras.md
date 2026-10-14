# MOC - Portal de Calculadoras

## Objetivo

Manter uma memória global e versionada para a classificação semântica das palavras-chave do portal.

A planilha é a base de dados. Este vault registra regras, taxonomia, ambiguidades, decisões, testes de regressão e o estado dos lotes.

## Estado atual

- Base esperada após correção estrutural: **294.905 palavras-chave únicas**.
- Classificação semântica definitiva: **ainda não iniciada**.
- Estratégia: lotes controlados por uma taxonomia global, com conjunto de controle e reconciliação final.

## Navegação

- [[Mapa Global - Estrutural]]
- [[MOC - Áreas]]
- [[MOC - Intenções]]
- [[MOC - Taxonomia]]
- [[../02-Regras/Regras Globais]]
- [[../03-Ambiguidades/Ambiguidades Globais]]
- [[../04-Regressao/Golden Set]]
- [[../05-Lotes/Protocolo de Lotes]]
- [[../06-Decisoes/DEC-001 - Estratégia de classificação em lotes]]

## Princípios

1. Não classificar por palavra isolada quando o contexto contradiz a regra lexical.
2. Não confundir área de origem com área/intenção final.
3. Não tratar confiança alta como simples correspondência de padrão.
4. Preservar a rastreabilidade até a expressão original.
5. Registrar toda regra que possa afetar mais de um lote.
6. Toda mudança de taxonomia deve ser versionada e reavaliada contra o conjunto de regressão.
