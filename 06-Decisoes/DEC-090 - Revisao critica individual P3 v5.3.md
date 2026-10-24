# DEC-090 — P3 v5.3: revisão contextual individual de 75 pareceres

**Data:** 2026-10-24. **Base:** P3 v5.2 (DEC-088), associada ao filtro reversível Ouro (DEC-089). **Homologação editorial:** PENDENTE.

## Decisão

Revisar **exatamente os 75 IDs** da expansão v5.2, sem incluir novas palavras-chave; todos permanecem presentes no recorte operacional após exclusão Ouro. Resultado: **6 refinamentos e 69 classificações mantidas com ressalvas**, em 32 famílias e sete temas. As 75 justificativas, individualizadas por ID, constam de `p3-v5.3-pareceres-75.csv`.

### Seis refinamentos

| ID | Keyword | Ajuste | Justificativa central |
|---|---|---|---|
| 4473 | 17 semanas meses | `informacional` → `cálculo contextual` | Valor (17 semanas) e destino (meses) aparecem, mesmo sem verbo; não presumir gestação. |
| 47574 | calcular semanas em meses | `informacional` → `cálculo contextual` | Verbo calcular requer operação; parâmetros ausentes, logo contextual. |
| 47583 | calcular semanas para meses | `informacional` → `cálculo contextual` | Pedido operacional, diferente de “como calcular”, que pede método. |
| 148231 | excel como arredondar para cima | Subcluster específico para arredondamento no Excel | É procedimento de planilha, não calculadora numérica genérica. |
| 254173 | salario bruto minimo | Subcluster de salário mínimo e remuneração bruta | Evitar confundir referência de salário mínimo com conversão bruto–líquido genérica. |
| 270768 | tabela conversão btu x watts | Subcluster `BTU (energia), BTU/h (potência) e watts` | Sem `/h` não há conversão direta entre energia BTU e potência W. |

Os novos rótulos de subcluster nos três últimos casos alteram também `dominio_ou_grandeza` e `intencao_principal` para preservar consistência. As três mudanças de tipo atualizam `intencao_principal`. Demais campos e IDs fora desses seis permanecem idênticos.

## Regressão e garantias

- Duas visões sincronizadas, ambas validadas contra a respectiva fonte v5.2: **30 lotes canônicos (294.905 registros-base)** e **30 lotes filtrados Ouro (291.296 registros-base)**. Em ambas há **2.190 controles**.
- **6 IDs alterados**, nenhum fora da lista autorizada; os outros **69 pareceres mantidos**. Documentação de valores anteriores/posteriores em `p3-v5.3-patches-6.csv`.
- **Quatro filas** preservam suas 398 colunas anteriores, com somente oito novas colunas de rastreabilidade: 23.965 e 52.046 linhas canônicas; 23.865 e 51.884 linhas filtradas.
- **3.609 exclusões Ouro** permanecem reversíveis, sem alterar arquivo de origem. Os 12 casos com origem também não-dourada ficam em revisão, sem exclusão automática.
- As **98 propostas globais** permanecem byte a byte idênticas, e as **4.660 pendências P2** não sofreram reclassificação.
- **P3 elegíveis: 19.562 canônicos / 19.462 após filtro Ouro**. A revisão v5.3 não abre nem fecha novos casos; os 75 já haviam sido tratados na v5.2.

## Critérios semânticos enfatizados

1. Distinguir “calcular” (intenção operacional, mesmo sem valores completos) de “como calcular” (instruções).
2. Não inferir gestação em semanas/meses sem menção explícita.
3. Não inventar período, dias de jornada, taxa de cartão, eficiência de aparelho, bases salariais ou conversão exata de mês civil.
4. BTU é unidade de **energia**; BTU/h é taxa de energia (potência térmica); W é potência. Não inferir automaticamente consumo elétrico.
5. Manter classificação informativa quando palavras sem amostra listam média, moda e mediana.

## Reprodução e arquivos

Pacote ZIP `portal-calculadoras-auditoria-P3-v5.3-unico.zip`: 60 lotes (em 2 arquivos ZIP), quatro filas, 75 pareceres, 6 patches, relatório de regressão, planilha QA centralizada, documentação, manifesto SHA-256 e três scripts reutilizáveis. Scripts precisam das duas fontes anteriores: pacote P3 v5.2 e pacote de filtro Ouro v5.2. **Arquivos binários completos não sincronizados com GitHub**; texto/relatórios/scripts estão versionados no vault.

**Próxima etapa:** P3 v5.4, expansão seletiva de **100 novos IDs** exclusivamente dos **19.462 P3 elegíveis na fila operacional sem Ouro**, seguida de revisão contextual individual, regressão e preservação de originais.