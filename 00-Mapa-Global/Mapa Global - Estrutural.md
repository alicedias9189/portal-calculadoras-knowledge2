# Mapa Global - Estrutural

> Este mapa é estrutural, não semântico. Ele registra o que já foi confirmado programaticamente antes da classificação High.

## Base

- Palavras-chave válidas esperadas após remover os 2 metadados indevidos: **294.905**.
- Duplicatas técnicas: **0**.
- Palavras-chave vazias: **0**.
- Soma de `ocorrencias_origem` antes da remoção dos dois metadados: **1.709.960**.
- Expressões presentes em mais de uma área após a remoção dos metadados: **57.463 (19,49%)**.
- Expressões presentes em apenas uma área após a remoção dos metadados: **237.442 (80,51%)**.

## Áreas de origem — contagens estruturais esperadas após a correção

Estas contagens indicam em quantas expressões cada área aparece em `areas_origem`. Elas **não representam a classificação semântica final**.

- [[../01-Taxonomia/Finanças]]: **129.560**
- [[../01-Taxonomia/Trabalho]]: **79.460**
- [[../01-Taxonomia/Matemática]]: **41.344**
- [[../01-Taxonomia/Conversores]]: **40.878**
- [[../01-Taxonomia/Datas]]: **30.090**
- [[../01-Taxonomia/Construção]]: **17.650**
- [[../01-Taxonomia/Energia]]: **16.293**

## Distribuição pelo número de áreas de origem

Após a remoção dos dois metadados conhecidos:

- 1 área: **237.442**
- 2 áreas: **54.743**
- 3 áreas: **2.539**
- 4 áreas: **175**
- 5 áreas: **6**
- 6 áreas: **0**

O único registro de 6 áreas na auditoria original era um intervalo de datas do Google Ads, portanto não era uma palavra-chave.

## Sobreposições estruturais mais frequentes na auditoria original

As combinações abaixo são úteis para escolher amostras e lotes. Elas descrevem **origem**, não intenção final.

- Trabalho | Finanças: 28.825
- Conversores | Finanças: 10.361
- Matemática | Finanças: 7.472
- Matemática | Conversores: 2.140
- Datas | Trabalho: 2.041
- Matemática | Construção: 1.399
- Datas | Trabalho | Finanças: 1.024
- Datas | Conversores: 1.007

## Implicações para a etapa semântica

- Termos compartilhados entre áreas devem ser super-representados na amostra estratificada inicial.
- A área de origem nunca deve decidir sozinha o cluster final.
- Sobreposições Trabalho/Finanças e Conversores/Finanças merecem regras específicas.
- A taxonomia global deve ser criada antes de processar os lotes completos.

## Próximo passo

Construir uma amostra estratificada global da base para criar a [[MOC - Taxonomia|taxonomia-mestra v1]] e o [[../04-Regressao/Golden Set|Golden Set]].
