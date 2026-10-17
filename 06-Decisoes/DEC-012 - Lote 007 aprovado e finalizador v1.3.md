# DEC-012 - Lote 007 aprovado e finalizador v1.3

## Contexto

O lote 007 expôs dois refinamentos que não exigem ampliar a Taxonomia v1.1, mas exigem melhorar a camada de auditoria final.

## Decisão 1 — casamento e dias de folga

Consultas sobre quantidade de dias, direito, abono, dispensa ou folga por casamento pertencem a:

`Trabalho > Afastamentos > Licenças e afastamentos`

quando o contexto indicar benefício/licença ligada à relação de trabalho.

Isso amplia operacionalmente a R21, que já impedia licenças trabalhistas de serem tratadas como simples diferença entre datas.

## Decisão 2 — PDF

A auditoria deve distinguir três situações:

1. conversão/criação de formato: `fotos em pdf`, `pagina web em pdf`, `pdf para word` → Conversores;
2. pares de formatos em contexto de ferramenta/download: `baixar pdf word gratis` → Conversores quando os dois formatos indicarem transformação;
3. manipulação sem troca de formato: `mudar a cor do pdf`, `quebrar pdf` → Fora de escopo sob a taxonomia atual.

Se uma consulta de manipulação também explicitar formato de destino, por exemplo `quebrar pdf para word`, a intenção de conversão prevalece.

## Implementação

Foi criado:

`07-Scripts/finalizar_auditar_lote_v1_3.py`

Ele executa o finalizador v1.2 e adiciona os refinamentos acima sem sobrescrever as colunas originais nem a coluna `Keyword`.

## Validação

No lote 007:

- Golden Set: **107/107**;
- controles: **73/73**;
- conversões diretas sem metadados: **0**;
- flags finais: **0**;
- lote 007: **APROVADO**;
- lote 008: **LIBERADO**.
