# Protocolo de Lotes

## Objetivo

Classificar a base em lotes sem perder consistência global.

## Tamanho alvo

- aproximadamente **10.000 palavras-chave novas por lote**;
- controles do [[../04-Regressao/Golden Set]] são acrescentados separadamente;
- manter `id_global`, `lote_id` e `familia_id` para permitir recomposição exata.

## Preparação dos lotes

A base não deve ser cortada simplesmente a cada 10.000 linhas.

O script `preparar_lotes_semanticos.py` faz uma etapa intermediária de **famílias lexicais/temáticas aproximadas**:

1. lê a base corrigida;
2. atribui `id_global` determinístico pela ordem da base;
3. calcula frequências de tokens apenas para agrupamento;
4. identifica uma macrofamília interna de roteamento;
5. cria `familia_id` usando macrofamília + padrão de intenção + unidades detectadas + âncora lexical;
6. mantém cada família no mesmo lote sempre que possível;
7. só divide uma família quando ela excede o limite configurado;
8. balanceia os lotes em torno de 10 mil registros;
9. ordena cada lote por `familia_id`, mantendo consultas próximas juntas;
10. acrescenta controles do Golden Set;
11. gera manifestos de lotes, famílias e controles.

### Proteção contra viés

A `macro_familia_interna` existe **somente nos manifestos**. Ela não aparece no arquivo que será entregue ao High e não é uma classificação final.

`familia_id` também não é cluster final: serve apenas para coesão local.

A classificação verdadeira deve obedecer à [[../00-Mapa-Global/MOC - Taxonomia|Taxonomia-mestra]] e às [[../02-Regras/Regras Globais]].

## Formato dos lotes

Para a etapa de classificação, **CSV UTF-8 com `;` é o padrão recomendado** porque:

- reduz tempo de geração e leitura;
- ocupa menos recursos;
- é mais apropriado para upload e processamento automático;
- não precisamos preservar formatação visual durante a classificação.

ODS continua disponível no script como opção manual, mas é significativamente mais lento.

## Golden Set

Cada controle possui uma classificação esperada no `manifesto-controles.csv`.

Nos lotes, aparecem somente:

- a keyword;
- os campos de origem disponíveis;
- `tipo_registro=controle`;
- `controle_id`.

As respostas esperadas **não são colocadas no lote**.

O padrão atual usa os **73 controles** em todos os lotes, uma sobrecarga inferior a 1% por lote.

## Antes dos lotes completos

1. Criar uma amostra estratificada global. ✅
2. Construir a Taxonomia v1 em High. ✅
3. Construir o Golden Set. ✅
4. Definir regras de inclusão/exclusão e ambiguidades recorrentes. ✅
5. Gerar famílias e lotes completos. ← etapa atual

## Durante cada lote

- usar a mesma taxonomia-mestra;
- analisar famílias contíguas como contexto comparativo, sem presumir que toda família tenha a mesma classificação;
- não criar silenciosamente novos nomes de cluster;
- registrar novos casos ambíguos;
- registrar decisões que afetem lotes futuros;
- marcar baixa confiança para revisão manual;
- classificar controles sem consultar `manifesto-controles.csv` durante a análise do lote;
- comparar os controles com o manifesto somente depois que o lote estiver classificado.

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

1. manter somente `tipo_registro=base`;
2. unir por `id_global`;
3. verificar que todo `id_global` aparece exatamente uma vez;
4. detectar clusters/subclusters equivalentes com nomes diferentes;
5. comparar classificações do Golden Set entre todos os lotes;
6. revisar termos de várias áreas de origem;
7. revisar baixa confiança;
8. aplicar testes de regressão;
9. produzir auditoria global por cluster.

Veja também [[../06-Decisoes/DEC-003 - Preparação dos lotes semânticos]].
