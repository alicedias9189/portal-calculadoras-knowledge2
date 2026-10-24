# DEC-087 — P3 v5.1: revisão crítica individual de 75 pareceres

**Data:** 2026-10-24. **Fonte:** P3 v5.0 (DEC-086). **Estado:** concluído tecnicamente; homologação editorial **PENDENTE**.

## Decisão e escopo

Revisar **exatamente os 75 IDs** classificados na P3 v5.0, sem adicionar registros à seleção. Cada palavra-chave recebeu parecer individual contextualizado. Resultado: **19 refinamentos** e **56 classificações mantidas com ressalvas**, em **49 famílias e 8 grupos**.

Os patches modificam apenas campos taxonômicos e semânticos permitidos dos 19 registros-base correspondentes. Nenhum controle, palavra-chave, ID, família ou valor de Google Ads foi modificado. Não há homologação editorial humana implícita.

## Refinamentos por grupo

| Grupo | Revisados | Refinados | Mantidos |
| --- | ---: | ---: | ---: |
| BTU/h, watts e climatização | 7 | 7 | 0 |
| Prazos e dias úteis/corridos | 4 | 0 | 4 |
| Desconto de benefícios | 4 | 0 | 4 |
| Estatística descritiva | 12 | 0 | 12 |
| Geometria / perímetro | 14 | 2 | 12 |
| Potenciação | 17 | 7 | 10 |
| Probabilidade | 9 | 1 | 8 |
| Regra de três | 8 | 2 | 6 |
| **Total** | **75** | **19** | **56** |

## Motivações de maior impacto

1. Nos sete IDs de BTU/h, distinguir potência térmica, expressável em W térmicos, de potência elétrica de entrada, que depende da eficiência e do equipamento. A palavra “watts” não desambigua essa intenção sozinha; confiança baixa nesses sete casos.
2. ID `85882`: a consulta pede descobrir o **perímetro a partir da área** e não o contrário. A área isolada geralmente não determina perímetro.
3. IDs `207492` e `207494`: grafias `23`/`32` não autorizam substituir por `2³`/`3²`; tratar como consulta de notação ambígua com confiança baixa.
4. As frases genéricas sobre propriedades de expoentes e frações (`160019`, `207450`, `207458`, `207640`, `242905`) não contêm operandos e portanto não autorizam resultados específicos.
5. A expressão `probabilidade da intersecção de dois eventos` (ID `212548`) pede fórmula/procedimento, não prova independência entre os eventos.
6. ID `200874`: “perímetro de triângulo com três lados” não informa comprimentos; busca por fórmula, não resultado numérico.
7. IDs `18136` e `245615`: menções genéricas à regra de três com dinheiro/valores não equivalem a pedido de cálculo fechado.

## Regulação de alterações e testes

- Regressão **independente** sobre todos os **30 lotes**: **PASSOU**.
- **294.905 registros-base** e **2.190 controles** preservados, 19 alterações permitidas e 56 classificações intactas.
- Filas completas com **23.965** e **52.046** linhas: preservadas, célula por célula, as **382 colunas anteriores**; adicionadas **8 colunas** exclusivas de rastreabilidade v5.1.
- **4.660 pendências P2** e **98 propostas globais** não reabertas; arquivo das 98 propostas idêntico byte a byte.
- Restam **19.637 P3** elegíveis, mesma quantidade da v5.0.
- Planilha de QA com **7 abas**, **1.885 células preenchidas e centralizadas**, conferidas via OOXML.

## Artefatos e reprodução

O ZIP **`portal-calculadoras-auditoria-P3-v5.1-unico.zip`** inclui os 30 lotes CSV completos, as duas filas, 75 pareceres, 19 patches com valores antes/depois, regressões independentes, XLSX centralizada e scripts para reaplicação. A subpasta `FONTES-REPRODUCAO` contém a origem integral v5.0 necessária à execução.

Executar da raiz extraída, em ordem:

```bash
python 07-Scripts/P3/auditar_p3_v51.py
python 07-Scripts/P3/regressao_independente_p3_v51.py
python 07-Scripts/P3/gerar_qa_p3_v51.py
```

A terceira etapa requer `artifact_tool`. A fonte principal da verdade é o pacote fechado entregue no ChatGPT; o ZIP binário não foi carregado no GitHub nesta execução.

**Próxima etapa:** **P3 v5.2**, expansão seletiva de novos registros entre os 19.637 ainda elegíveis, condicionada às verificações de regressão e sem reabrir pareceres anteriores. **Homologação editorial ainda pendente.**