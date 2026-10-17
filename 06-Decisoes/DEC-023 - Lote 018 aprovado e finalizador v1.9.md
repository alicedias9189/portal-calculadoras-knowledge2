# DEC-023 — Lote 018 aprovado e finalizador v1.9

## Decisão
O lote 018 foi aprovado sob **Taxonomia v1.1 + barras v2** após a criação do `finalizar_auditar_lote_v1_9.py`.

## Motivo da nova camada
A auditoria residual encontrou `probabilidade para concursos pdf` classificado como conversão de arquivo. A nova regra diferencia busca por material de concurso em PDF de conversão de formato.

## Regra consolidada
Quando a keyword contém contexto de concurso/concurseiro + PDF, sem par de formatos nem verbo inequívoco de conversão, classificar como:

`Fora de escopo > Busca por conteúdo > Documento/PDF informacional`

## Resultado final
- Golden Set: **107/107**
- Controles: **73/73**
- Flags finais: **0**
- Conversões diretas sem metadados: **0**
- Reconstruções `/`: **41**
- Taxonomia permanece em **v1.1**

O lote 019 pode prosseguir usando o lote 018 aprovado e o finalizador v1.9.
