# DEC-003 - Preparação dos lotes semânticos

## Status

Aceita.

## Contexto

A base corrigida tem 294.905 keywords. Classificar tudo em uma única análise aumenta muito o risco de timeout; cortar a base cegamente a cada 10.000 linhas aumenta o risco de drift entre lotes e separa consultas semanticamente próximas.

## Decisão

Os lotes serão preparados por um processo determinístico de **famílias lexicais/temáticas aproximadas** antes da classificação High.

O processo:

1. atribui `id_global` pela ordem estável da base;
2. calcula frequências de tokens apenas para agrupamento;
3. identifica macrofamílias internas de roteamento;
4. cria `familia_id` a partir de sinais lexicais, intenção aproximada e unidades detectadas;
5. mantém famílias juntas sempre que possível;
6. divide apenas famílias acima do limite configurado;
7. balanceia aproximadamente 10.000 keywords novas por lote;
8. ordena famílias de forma contígua dentro dos lotes;
9. acrescenta controles do Golden Set em todos os lotes;
10. gera manifestos para recomposição e QA.

## Proteção contra viés

A macrofamília interna **não é exibida no lote de classificação** e nunca deve ser tratada como rótulo semântico final.

`familia_id` também não representa cluster da Taxonomia-mestra: é somente um mecanismo de coesão local.

## Formato operacional

CSV UTF-8 com delimitador `;` passa a ser o formato recomendado para os lotes de classificação. ODS permanece opcional.

Razões:

- menor custo de leitura/escrita;
- arquivos mais simples e leves;
- nenhuma necessidade de formatação visual durante classificação;
- mais fácil consolidar e validar por script.

## Golden Set

O padrão atual repete os 73 controles do Golden Set em todos os lotes. Isso acrescenta menos de 1% ao tamanho de um lote de 10 mil registros e fornece um teste constante contra drift.

As classificações esperadas ficam fora do lote, em `manifesto-controles.csv`, para evitar vazamento da resposta durante a classificação.

## Integridade

A consolidação final usará apenas `tipo_registro=base` e deve verificar:

- cada `id_global` exatamente uma vez;
- nenhuma perda de keyword;
- controles excluídos da base final;
- consistência do Golden Set entre lotes;
- revisão de baixa confiança e conflitos entre lotes.

## Implementação

Script: `preparar_lotes_semanticos.py`.

Veja [[../05-Lotes/Protocolo de Lotes]], [[../00-Mapa-Global/MOC - Taxonomia]] e [[../04-Regressao/Golden Set]].
