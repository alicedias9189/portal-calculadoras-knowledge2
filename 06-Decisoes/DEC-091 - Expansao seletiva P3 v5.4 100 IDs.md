# DEC-091 — Expansão seletiva P3 v5.4: 100 novos IDs

**Data:** 24/10/2026. **Base:** P3 v5.3 e filtro reversível Ouro (DEC-089 / DEC-090). **Homologação editorial: PENDENTE.**

## Escopo e decisão

Foi adotada a meta de **100 registros por expansão**, mantendo rastreabilidade por ID e revisão crítica posterior, sem flexibilizar o controle de regressão. Selecionaram-se **100 IDs novos / 34 famílias** dentre **19.462 P3 elegíveis após filtro Ouro**. A elegibilidade foi conferida em todas as colunas históricas `status_p3_v*`, excluindo-se somente o marcador inicial `FORA_DO_PILOTO` e rejeitando qualquer registro já tratado em rodadas anteriores. Foram verificados também conflito com o backlog global de 98 e com a lista de 3.609 IDs Ouro filtrados.

| Grupo | IDs |
|---|---:|
| Cálculo e ferramentas de gestação | 15 |
| Direitos trabalhistas de gestantes | 15 |
| Calculadoras de prazos e dias úteis | 12 |
| Juros e faturas de cartão | 14 |
| Planilhas de orçamento financeiro | 15 |
| Simuladores e consultas sobre investimentos | 14 |
| Estatística, moda e média do ENEM | 15 |
| **Total** | **100** |

## Princípios editoriais e casos-limite

- **Calculadora gestacional** demanda DUM ou parâmetros de ultrassom; não é calculadora de idade civil nem de jornada trabalhista, e não autoriza conclusão médica individual.
- **Direitos de gestantes no emprego** são informação trabalhista: evitar classificá-los como acompanhamento clínico; depende das circunstâncias e normas aplicáveis.
- **Prazos processuais** buscam ferramentas de datas e necessitam marco inicial, calendário, feriados e regras aplicáveis; não são matemática genérica.
- **Cartão e fatura**: taxas informativas não são simulações com taxa e saldo conhecidos nem rentabilidade de investimentos.
- **Planilhas de gastos** são busca por modelo/ferramenta, e não cálculo de CDB; separar fins empresarial e pessoal apenas com evidência textual.
- **Simuladores de investimentos** não são dimensionamento solar, empréstimos ou simples prazo cronológico; retornos futuros e taxas não devem ser inventados.
- **ENEM/média/moda**: distinguir consulta sobre notas, média aritmética e ferramenta; sem entradas não há cálculo fechado. Consulta "média do ENEM" pode pedir indicador publicado, exigindo contexto.

## Proteções e evidências

- Auditoria gerou **100 patches individuais**, com JSON antes/depois e justificativa textual rastreável, restritos a nove campos de classificação.
- A regressão **independente** comparou os **60 lotes** (30 canônicos e 30 operacionais), linha a linha e campo a campo: **PASSOU**.
- Controles mantidos: **294.905 bases canônicas**, **291.296 bases sem Ouro**, **2.190 controles por conjunto**, **3.609 IDs Ouro somente na exclusão operacional**.
- As quatro filas mantêm suas **406 colunas históricas idênticas** e incluem oito colunas novas; linhas: 23.965 / 52.046 (canônico), 23.865 / 51.884 (operacional).
- Backlog global de **98 propostas idêntico byte a byte**, pendências P2 = **4.660** preservadas.
- P3 ainda elegíveis: **19.362 operacionais** (eram 19.462); **19.462 canônicos** (eram 19.562).
- A classificação é proposta técnica, **não aprovação editorial humana**, e a redução é do número de elegíveis, não da contagem física dos registros da base.

## Entrega e próxima fase

`08-Entregas/P3-v5.4/` contém dois ZIPs de 30 lotes, quatro filas completas, 100 pareceres, 100 patches, plano por ID, QA, regressão e planilha XLSX de sete abas com alinhamento central. Quatro scripts reutilizáveis em `07-Scripts/P3/*p3_v54.py`. Pacote único completo entregue em conversa ChatGPT; **artefatos binários não enviados ao GitHub**.

**Próximo passo:** P3 v5.5 — revisão crítica contextual e individual dos 100 pareceres da v5.4, sem ampliar IDs nessa revisão; depois novas expansões de 100 IDs sobre a fila sem Ouro.