# DEC-017 — Lote 012 aprovado e finalizador v1.6

## Decisão

Adotar `finalizar_auditar_lote_v1_6.py` como camada final recomendada a partir do lote 013.

## Motivo

O lote 012 expôs três classes de deriva que não estavam suficientemente cobertas:

1. `dias trabalhados` sendo tratados como operação genérica de Datas;
2. PDF/DOC usado apenas como formato de conteúdo em termos como TRCT/fatorial;
3. pares adjacentes de formatos (`pdf word`, `pdf powerpoint`) sem verbo/preposição sendo marcados como falso positivo de conversão.

## Regras incorporadas

- `dias trabalhados` é trabalhista por padrão;
- pagamento/salário/folha/adiantamento por dias trabalhados vai para Remuneração > Salário líquido e bruto;
- consultas genéricas de dias trabalhados vão para Remuneração > Valor da hora e dias trabalhados;
- contextos específicos (13º, férias, rescisão, jornada, DSR, adicionais etc.) prevalecem;
- contagem/cálculo de dias de licença ou afastamento permanece em Trabalho > Afastamentos;
- TRCT PDF/DOC é conteúdo de rescisão trabalhista, não conversão de arquivo;
- `fatorial pdf` é conteúdo matemático;
- pares adjacentes de formatos explícitos podem representar conversão mesmo sem verbo/preposição.

## Resultado do lote 012

- Golden: 107/107
- Controles: 73/73
- Flags finais: 0
- Conversões diretas sem metadados: 0
- Status: APROVADO

O lote 013 pode usar o lote 012 aprovado como treino/controle anterior.