# Relatório de auditoria — P3 v5.4

**Data:** 24/10/2026. **Escopo:** expansão seletiva de 100 novas palavras sobre P3 v5.3 com filtro Ouro DEC-089; revisão editorial posterior.

## Resultado

- **100 IDs novos**, **34 famílias**, **7 temas**. Todos estavam entre os **19.462 estritamente elegíveis**, sem reutilização de qualquer ID já marcado em P3, nem de IDs excluídos pelo filtro Ouro.
- **100 propostas técnicas com ressalvas**, com justificativa contextual por ID e patches antes/depois. Não são 100 aprovações humanas.
- Campos modificados: **45 mudanças de área**, **92 mudanças de cluster**, **100 de subcluster** e **89 de tipo de intenção**, além de ajustes de justificativa, domínio, confiança e descrição. Cada um dos 100 IDs apresenta modificação em pelo menos um campo semântico.
- **60/60 lotes aprovados** na regressão independente; nenhuma modificação de classificação nos outros 294.805 registros-base canônicos, nem nos registros filtrados não selecionados.
- **406 colunas históricas intactas nas quatro filas**, acrescidas de 8 de rastreabilidade da v5.4. Backlog global de 98 idêntico byte a byte.
- **Saldo P3 operacional: 19.362 elegíveis** (contra 19.462 antes). Saldo P3 canônico: 19.462 elegíveis.

## Distribuição

| Tema | IDs |
|---|---:|
| Ferramentas gestacionais | 15 |
| Direitos de gestantes | 15 |
| Ferramentas para prazos | 12 |
| Juros e faturas de cartão | 14 |
| Planilhas financeiras | 15 |
| Simuladores de investimento | 14 |
| Estatística, moda e média do ENEM | 15 |
| **Total** | **100** |

## Limites e reprodução

A presença de um termo de busca não oferece parâmetros suficientes para cálculo particular. As classificações com ressalvas registram especificamente quando faltam dados (como DUM, calendário processual, taxas bancárias, notas do ENEM ou aportes financeiros).

Os arquivos de produção são `lotes-001-a-030-p3-v5.4.zip`, `lotes-001-a-030-p3-v5.4-sem-ouro.zip`, as quatro filas CSV, as listas de pareceres e patches, a planilha XLSX centralizada e os arquivos de regressão independente. O manifesto SHA-256 foi gerado para os conteúdos do ZIP final.

Para reproduzir os resultados, descompactar **P3 v5.3** na mesma raiz da estrutura de v5.4 e executar, nessa ordem: `auditar_p3_v54.py`, `regressao_independente_p3_v54.py`, `gerar_qa_p3_v54.py` e `montar_entrega_p3_v54.py`.

**Homologação editorial PENDENTE. Próxima fase: P3 v5.5 — revisão crítica individual dos mesmos 100 IDs.**