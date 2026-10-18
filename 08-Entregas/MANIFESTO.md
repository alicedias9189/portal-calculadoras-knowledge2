# Manifesto de sincronização P1/P2

Data: 2026-10-17. Repositório: `alicedias9189/portal-calculadoras-knowledge2`.
Objetivo: distinguir entregas commitadas em Git das entregas binárias que só existem na Biblioteca do ChatGPT.

## Importado para Git
Relatórios completos das fases P1 V1, P1 V2, P2 V1 e P2 V2 (subpastas nesta pasta); LEIA-ME P2 V2; código-fonte P1 V1 em Markdown; 10 scripts Python individuais distribuídos em `07-Scripts/P1` e `07-Scripts/P2`; DEC-038, DEC-039, DEC-040; registros de continuidade. Esses arquivos aparecem após `git pull`.

## Ainda NÃO importado para GitHub
Os arquivos binários seguintes estão preservados na Biblioteca do ChatGPT:
- P1 V1: `/Portal de Calculadoras - Auditorias/P1 - Revisao inicial/qa-revisao-p1-centralizado.xlsx`; `p1-lotes-001-a-030-versoes-paralelas.zip`; `p1-relatorios-qa-scripts.zip`.
- P1 V2: `/Portal de Calculadoras - Auditorias/P1 - Validacao semantica/qa-validacao-semantica-p1-v2-centralizada.xlsx`; `lotes-001-a-030-p0-p1-v2.zip`; `p1-v2-auditoria-relatorios-scripts.zip`.
- P2 V1: `/Portal de Calculadoras - Auditorias/P2 - Revisao/qa-revisao-p2-centralizada.xlsx`; `lotes-001-a-030-p0-p1-p2-v1.zip`; `p2-v1-auditoria-relatorios-scripts.zip`.
- P2 V2: `/Portal de Calculadoras - Auditorias/P2 - Validacao semantica v2/qa-validacao-p2-v2-centralizada.xlsx`; `lotes-001-a-030-p0-p1-p2-v2.zip`; `p2-v2-auditoria-csv-scripts.zip`.
- Os CSVs completos e diffs ficam dentro dos ZIPs; portanto também não estão disponíveis por `git pull`.

## Motivo da pendência
O acesso disponível ao GitHub permite gravação direta de texto e blobs cujo conteúdo esteja acessível como texto. A transferência direta de ZIP/XLSX da Biblioteca/ambiente de arquivos para a integração GitHub não ficou disponível nesta operação. Não inventar links GitHub para esses binários nem declarar sincronização integral.
Próxima ação operacional: encontrar mecanismo seguro de envio dos 12 binários preservados, com hashes e versões; não alterar nem apagar as fontes.

## Integridade declarada nos relatórios
Base total 294.905 IDs, 2.190 controles preservados, decisões P0/P1 anteriores sem alteração nas revisões P2. Essas contagens foram reportadas em entregas anteriores, não recalculadas neste commit.