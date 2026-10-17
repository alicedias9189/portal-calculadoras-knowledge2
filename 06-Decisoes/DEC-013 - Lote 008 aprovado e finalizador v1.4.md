# DEC-013 — Lote 008 aprovado e finalizador v1.4

## Contexto

Durante a auditoria do lote 008, a camada v1.3 deixou duas flags críticas `PDF_CONTENT`:

- `pdf em imagem`
- `pdf em xml`

A classificação semântica já estava correta em ambos os casos: `Conversores > Arquivos e documentos > Documentos e PDF`, intenção `conversão de arquivo/mídia`.

## Decisão

Pares explícitos de formatos/representações ligados por direção (`em`, `para`, `to`) devem ser reconhecidos como conversão mesmo quando não existe verbo explícito.

Exemplos:

- `pdf em imagem` → conversão de arquivo/mídia;
- `pdf em xml` → conversão de arquivo/mídia;
- `imagem em pdf` → conversão de arquivo/mídia.

Essa regra não autoriza classificar qualquer ocorrência de `pdf` + outro token como conversão. É necessário haver dois formatos/representações reconhecidos e relação direcional explícita, ou verbo de transformação já coberto pelas camadas anteriores.

## Implementação

Criado:

`07-Scripts/finalizar_auditar_lote_v1_4.py`

A v1.4 executa toda a cadeia anterior e remove somente falsos positivos `PDF_CONTENT` que atendam à regra acima.

## Resultado do lote 008

- Golden Set: **107/107**
- controles: **73/73**
- conversões diretas sem metadados: **0**
- flags finais: **0**
- colunas originais preservadas: **sim**

**Lote 008 aprovado; lote 009 liberado.**
