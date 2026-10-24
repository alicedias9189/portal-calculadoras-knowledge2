# DEC-042 — Revisão semântica P2 v4 por famílias e regressão independente

Data: 2026-10-18. Versão paralela, partindo da P2 v3 (DEC-041).

## Decisão
Aplicar apenas classificações sustentadas por padrões linguísticos específicos aos **5.946 registros P2 ainda pendentes na v3**, sem herdar automaticamente a decisão de outros integrantes da família. Preservar as ambiguidades e manter P0, P1, P3 e demais registros P2 intocados. A versão anterior permanece válida e não é sobrescrita.

## Resultados finais
- P2 total: 25.050 keywords; pendências v3 examinadas: 5.946; famílias originais envolvidas: 2.983.
- 384 registros receberam classificação; 109 por regra sem ressalva e 275 com ressalva (dependentes de dados ou parâmetros adicionais).
- 143 famílias receberam ao menos uma reclassificação; **5.562 pendências** permanecem abertas.
- Lotes completos: 30, contendo **294.905 bases e 2.190 controles**. Regressão independente de cada CSV linha por linha: PASSOU, somente 384 IDs P2 sofreram mudanças nos campos analíticos autorizados.

## Regras examinadas
- Simulação de rendimento: exige taxa, prazo, produto, eventuais impostos. Nunca aplicar rendimento fixo do Nubank/poupança sem fonte específica.
- Unidades da mesma dimensão: dois nomes inequívocos de unidade e direção textual; não interpretar uma distância como velocidade nem tensão como potência.
- Câmbio: par e direção textual, sem taxa fixa. A expressão «bolívar» sem ano/série histórica não deve receber código monetário contemporâneo automaticamente.
- Calculadoras matemáticas, intervalos, materiais, combustível e formatos de arquivos: separar intenção operacional, tutorial e busca comercial; reconhecer parâmetros ausentes.
- Não converter galões/quarts/pints indeterminados como se fossem necessariamente dos EUA, nem «N m para ft lb» como comprimento; não classificar «tabela de conversão» como conversão solicitada de um valor.

## Limites e evidências
Esta foi revisão reexecutável por regras e auditoria semântica direcionada, **não homologação editorial independente de todas as 5.946 keywords**. O relatório `08-Entregas/P2-v4/RELATORIO.md` e `auditoria-p2-v4-csv-integral.zip` guardam decisão por ID, patches antes/depois, 2.983 famílias e pendências remanescentes. A planilha XLSX contém auditoria amostral e todos os 384 patches; os CSVs preservam todo o universo.

Scripts: `07-Scripts/revisar_p2_v4.py`, `auditar_regressao_p2_v4.py`, `gerar_qa_p2_v4.py`.

## Continuidade
Próxima prioridade: revisão editorial por famílias das 5.562 pendências, em particular padrões sem intenção explícita (semanas + dias sem gestação, número + °F sem destino, siglas de equipamentos, unidades de galão/ano de moeda etc.). Não iniciar P3 sem alinhamento de prioridade. 
