# Relatório P3 v2.6 — Revisão global A50 e expansão segura da P3

**Executado em 22/10/2026** com fontes documentadas no subdiretório `FONTES-P3-v2.5/`.

| Item | Resultado |
|---|---:|
| Propostas globais priorizadas | 98 |
| Revisadas contextualmente na faixa A | 50 |
| Intenção refinada vs. proposta na faixa A | 10 |
| Plausíveis com ressalvas na faixa A | 40 |
| Faixas B/C aguardando | 48 |
| Propostas globais aplicadas aos lotes | 0 |
| Expansão legítima P3 aplicada em cópia | 17 |
| Famílias alcançadas na P3 | 9 |
| Lotes aprovados em regressão | 30 de 30 |
| Registros-base preservados | 294.905 |
| Controles preservados | 2.190 |
| Pendências P2 inalteradas | 4.660 |
| P3 fora dos pilotos após esta fase | 20.383 |

## Revisão contextual dos 50 casos

- CET: separou-se localização de ferramenta de cálculo (`calculadora cet`) de pedidos de explicação (`como calcular cet`) e de consultas informacionais sobre conceito/taxa. Sempre exigir condições do contrato antes do cálculo.
- IRRF: referências a tabela e base de cálculo são informacionais; buscas por calculadora ou operação precisam de dados e regime/período correspondentes. Não se aplicaram alíquotas nem se interpretaram datas históricas como regras de 2026.
- Cada um dos 50 recebeu parecer individual, incluindo justificativa, ressalva, tipo de intenção sugerido, autorização de aplicação `NÃO` e homologação editorial `PENDENTE`.
- Não representa homologação editorial por um especialista humano.

## P3 v2.6

- 17 IDs foram validados individualmente nas filas P3 e geral e confrontados com o CSV do lote-base antes de alterar campos analíticos permitidos.
- Tratamento específico de salário-maternidade, contribuição previdenciária em atraso, piso de benefício e elegibilidade. Nada foi alterado fora desses 17 registros.
- Script independente confirmou patches por valores originais/posteriores e identidade dos campos protegidos.
- 98/98 registros do backlog global foram bloqueados pelo seletor P3; 17/17 da expansão foram aceitos. Foram testados cenários de duplicidade, divergência de palavra-chave, família e ID inexistente.

## Cuidados

Os pareceres são classificações contextuais geradas por regras revisadas, não opiniões de profissionais tributários/previdenciários nem confirmação de regras legais vigentes. O conjunto ainda necessita revisão editorial de qualidade. Não inferir que as 17 mudanças foram homologadas em definitivo.

## Arquivos e reprodução

Reexecute `python3 07-Scripts/P3/auditar_global_e_p3_v26.py`, depois `python3 07-Scripts/P3/testar_escopo_v26.py` e, com `artifact_tool` instalado, `python3 07-Scripts/P3/gerar_qa_global_p3_v26.py`. A fonte P3 v2.3 está incluída e nunca é sobrescrita. Esses scripts regeneram as cópias P3 v2.6; o ZIP final pode ter metadados diferentes ao ser recompresso.
