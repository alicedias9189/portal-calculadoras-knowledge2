# Protocolo de Lotes

## Objetivo

Classificar a base em lotes sem perder consistência global.

## Tamanho alvo

- aproximadamente **10.000 palavras-chave novas por lote**;
- adicionar uma pequena amostra de controle já classificada quando necessário;
- manter `id_global` e `lote_id` para permitir recomposição exata.

## Antes dos lotes completos

1. Criar uma amostra estratificada global.
2. Construir a Taxonomia v1 em High.
3. Construir o Golden Set.
4. Definir regras de inclusão/exclusão e ambiguidades recorrentes.
5. Só então gerar os lotes completos.

## Durante cada lote

- usar a mesma taxonomia-mestra;
- não criar silenciosamente novos nomes de cluster;
- registrar novos casos ambíguos;
- registrar decisões que afetem lotes futuros;
- marcar baixa confiança para revisão manual;
- validar casos de controle presentes no lote.

## Depois de cada lote

Registrar em `05-Lotes/lote-XXX.md`:

- quantidade de palavras processadas;
- versão da taxonomia usada;
- novos clusters propostos;
- novas regras;
- ambiguidades encontradas;
- divergências no Golden Set;
- quantidade por confiança;
- quantidade enviada para revisão manual.

## Reconciliação final

Após todos os lotes:

1. unir por `id_global`;
2. detectar clusters/subclusters equivalentes com nomes diferentes;
3. comparar classificações do Golden Set;
4. revisar termos de várias áreas de origem;
5. revisar baixa confiança;
6. aplicar testes de regressão;
7. produzir auditoria global por cluster.
