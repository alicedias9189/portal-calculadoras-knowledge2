# Auditoria P3 v1.2 — Saúde e navegação bancária

Escopo específico: revisar 184 casos suspensos de gestação na P3 v1.1, 3 falsos negativos gestacionais da amostra crítica e os 43 alertas de navegação em simuladores bancários.

| Resultado | Total |
|---|---:|
| Consultas de Saúde atualizadas | 187 |
| Alertas bancários revisados | 43 |
| Navegação bancária reclassificada | 27 |
| Bancárias com intenção mista preservadas | 16 |
| IDs efetivamente alterados | **214** |
| Lotes aprovados em regressão integral | 30 de 30 |
| Registros-base preservados | 294.905 |
| Controles preservados | 2.190 |

**Método:** revisão por padrões restritos e análise contextual da lista completa de 43. `simulador` + nome de banco foi interpretado como forte indício de navegação; `simular/simulação` + nome sem a palavra `simulador` ficou como intenção mista. Todos os registros individuais e suas justificativas estão na auditoria. Saúde trata apenas gestação explicitada no texto, não outras buscas clínicas. Nenhuma decisão equivale a revisão editorial humana independente.

**Integridade:** arquivos CSV de 30 lotes gerados em versão paralela; comparação reabrindo os ZIPs, registro por registro. Campos protegidos, IDs, keywords e controles sem alteração. O pacote também inclui os insumos exatos da P3 v1.1 para reprodução da versão v1.2. A fila consolidada mantém todas as 85 colunas históricas e adiciona oito colunas para rastreabilidade v1.2.

**Limite editorial:** propor área Saúde como novo ramo taxonômico v1.2; não aplicá-la indiscriminadamente a palavras fora da amostra. Termos bancários híbridos permanecem com intenção original e marcação de QA, sem transformar o volume de busca por marcas bancárias em demanda por calculadoras próprias.

**Próximo passo:** revisar as 16 buscas bancárias híbridas e validar taxonomia Saúde editorialmente; em seguida fazer novo piloto estratificado da P3 restante, incluindo os cinco falsos negativos de outros domínios.
