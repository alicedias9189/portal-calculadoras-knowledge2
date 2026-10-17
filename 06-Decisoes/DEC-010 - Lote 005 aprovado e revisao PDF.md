# DEC-010 - Lote 005 aprovado e revisão PDF/content

## Decisão

O lote 005 foi aprovado sob **Taxonomia v1.1 + barras v2** sem necessidade de Taxonomia v1.2.

A auditoria acrescenta uma regra operacional para consultas com `PDF`:

- criação/conversão explícita de formato (`jpg para pdf`, `pdf para word`, `enviar foto em pdf`, `montar pdf com fotos`) permanece em **Conversores > Arquivos e documentos > Documentos e PDF**;
- edição pura de PDF sem formato de destino (`editar pdf online`, `ilove pdf editar pdf`) é **Fora de escopo > Serviços/software > Consulta navegacional**;
- PDF cujo assunto é uma tabela/referência de conversão (`conversão de medidas pdf`) não é conversão de arquivo; classificar em **Conversores > Conversões gerais > Conversor genérico de unidades**, intenção **tabela/referência**.

## Resultado do lote 005

- 9.831 keywords base
- 73 controles
- 107/107 Golden Set
- 73/73 controles preservados
- 47 reconstruções `/`
- 0 conversões diretas sem metadados
- 0 flags finais
- lote 006 liberado

## Implementação

A regra foi incorporada ao script reutilizável `07-Scripts/finalizar_auditar_lote_v1_1.py`.

As planilhas XLSX geradas pelo pipeline devem continuar centralizadas horizontal e verticalmente em todas as células usadas. O gerador atual é `07-Scripts/gerar_planilhas_centralizadas_v2.py`.
