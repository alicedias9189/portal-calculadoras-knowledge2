# P3 v2.4 — Correção do seletor de prioridades e triagem da quarentena

## Resultado

- Registros propostos em v2.2: **108**.
- Elegíveis simultaneamente na fila P3 e na fila geral: **10**.
- Registros excluídos dessas duas filas e restaurados na v2.3: **98**.
- As 98 propostas foram examinadas e receberam parecer contextual individual. Todas são **não priorizadas**; nenhuma pertence a P0, P1, P2 ou P3 na fila existente.
- **0 patches novos** e nenhum arquivo de lote alterado. O conteúdo dos 30 lotes e das duas filas continua idêntico à v2.3 por SHA-256.

## Revisão semântica das 98

Por regra: {'P3V22_IRRF_BASE_FINANCAS': 37, 'P3V22_CET_CREDITO': 33, 'P3V22_INSS_DESCONTO_INFO': 4, 'P3V22_TAXA_FINANC_IMOVEL': 24}.
Por tipo de parecer: {'CORRIGIR_INTENCAO_DA_PROPOSTA': 9, 'AJUSTAR_INTENCAO_DA_PROPOSTA': 5, 'AJUSTAR_SUBTIPO_DA_PROPOSTA': 1, 'PLAUSIVEL_COM_RESSALVAS': 64, 'REVISAR_INTENCAO_INSTITUICAO': 18, 'REVISAR_INTENCAO_SERVICO': 1}.

As tabelas de IRRF não devem ser tratadas automaticamente como cálculo. Consultas a instituições não devem virar navegação bancária automaticamente. Consultas envolvendo INSS e IRPF exigem subtipo combinado. Buscas explícitas por calculadora de CET devem preservar a necessidade de parâmetros de crédito.

## Solução técnica

- `controle_elegibilidade_p3.py`: exige ID único presente na P3 de 23.965 registros, confirmado como P3 na fila geral de 52.046 e no lote-base de 294.905. Divergências de keyword/família/lote bloqueiam a seleção.
- `aplicar_patches_p3_protegido.py`: aceita alterações só nos campos analíticos, exige pré-condição `antes_json`, execução dry-run por padrão, saída nova e aborta atomicamente se qualquer candidato for inelegível.
- `testar_controle_p3.py`: teste positivo com 10 IDs, negativo para os 98, divergência de palavra-chave, duplicação, ID inexistente/vazio e prioridade P2.

## Integridade

Os 30 lotes P3 v2.3, a fila P3 e a fila geral são cópias com SHA-256 idêntico à entrada. **Nenhuma classificação P0/P1/P2/P3 foi modificada nesta etapa.**

## Próximo passo

Revisar a proposta de prioridade global para os 98 casos **em processo separado**, com aprovação da taxonomia/escopo, antes de qualquer alteração de dados; expandir a P3 somente com o novo guardião de elegibilidade.
