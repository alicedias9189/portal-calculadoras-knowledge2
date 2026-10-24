# Auditoria P2 v7 — revisão de segurança contextual e decisão P3

Data de fechamento: 2026-10-20. Fonte: P2 v6, 30 lotes; execução por regras restritas e QA independente.

## Resultados confirmados

| Indicador | Valor |
|---|---:|
| Universo P2 | 25.050 |
| Pendentes herdadas P2 v6 | 4.761 |
| Alterações analíticas nesta revisão | **101** |
| Decisões sem ressalva operacional | 28 |
| Decisões com ressalva | 73 |
| Famílias atingidas pelos patches | 81 |
| **Pendências P2 mantidas** | **4.660** |
| Lotes com regressão independente aprovada | **30/30** |
| IDs-base mantidos | 294.905 |
| Controles mantidos | 2.190 |
| P3 ainda não revisada | 23.965 keywords / 9.278 famílias |

Taxa de resolução sobre os 4.761 itens da rodada: **2,12%**. O valor não mede qualidade editorial; mostra apenas o rendimento da abordagem por regras conservadoras nesta passagem.

## Padrões tratados

Direção explicitamente expressa em pares de unidades compatíveis (como kV → V, km³ → m³, J → eV, conversão entre bases numéricas); cálculo contextual de consumo de combustível e pedágio; consulta de indicadores financeiros; informações de direito trabalhista; educação matemática; buscas comerciais e navegação para serviços de empresas. As descrições individuais, regras e campos antes/depois de cada patch estão nos CSVs integrais.

### Casos deliberadamente mantidos em aberto

- **157** termos no formato «N semanas e D dias»: o período é reconhecível, mas o objetivo pode ser gestação ou duração cronológica; a atribuição de intenção não é garantida pelo texto.
- **61** temperaturas isoladas no padrão «N Fahrenheit» ou «Fahrenheit N», sem unidade de destino declarada.
- Moedas sem país/direção, palavras isoladas ou siglas sem contexto, entradas técnicas fisicamente incompatíveis e pesquisas que misturam manual, produto e conversão.
- As 4.660 pendências restantes não foram reclassificadas automaticamente por pertencer a uma família.

## Integridade e limitações

O script `auditar_independente_p2_v7.py` comparou os CSVs físicos v6/v7 **linha por linha**. Verificou mesmo ID e keyword; ausência de mudanças fora dos 11 campos analíticos permitidos; controles intactos; valores reais de origem coincidentes com `antes`, e destinos com `depois` para 101 alterações; 294.905 IDs e 2.190 controles; e 30 lotes íntegros. Todas as colunas originais Google Ads, rastreamento e reconstrução de barras foram preservadas. Golden Set histórico não foi reexecutado nesta rodada.

**Não é validação humana independente de todas as 4.761 keywords.** «Alta confiança» é confiança na regra contextual, não homologação editorial. O usuário deve revisar amostras antes de aplicar decisões ao catálogo SEO.

## Decisão de prioridade

**Recomenda-se iniciar uma P3 v1 antes de outra passada massiva pela P2.** Justificativa: após sucessivas rodadas, somente 101/4.761 (2,12%) pendências desta revisão permitiram novas decisões pelas regras conservadoras, enquanto a P3 tem 23.965 keywords/9.278 famílias ainda não triadas. A P2 permanece congelada na versão paralela v7 com 4.660 casos abertos para revisão individual ou dados de contexto adicionais.

A P3 **não foi classificada nesta entrega**. O próximo trabalho deve fazer primeiro um piloto P3 por famílias e medir falsos positivos antes de classificar toda a fila. P0/P1/P2 anteriores não devem ser sobrescritas.

## Arquivos

- `lotes-001-a-030-p0-p1-p2-v7.zip`: 30 CSVs completos v7.
- `auditoria-p2-v7-csv-integral.zip`: decisões de 25.050 itens P2, 4.660 pendências, 101 patches, fila geral incluindo P3, regressão 30 lotes, famílias analisadas.
- `qa-revisao-p2-v7-centralizada.xlsx`: resumo, todas as 101 decisões, regras, amostra das pendências, grupos P3 e QA centralizado; todos os valores/células utilizados alinhados ao centro.
- `resumo-p2-v7.json`, `regressao-independente-p2-v7.json`, `SHA256SUMS-P2-V7.txt`.
- `07-Scripts/revisar_p2_v7.py`, `auditar_independente_p2_v7.py`, `gerar_qa_p2_v7.py`.
- As duas fontes ZIP da P2 v6 para reprodução também acompanham o pacote final.
