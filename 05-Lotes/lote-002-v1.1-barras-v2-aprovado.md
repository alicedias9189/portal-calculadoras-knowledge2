# Lote 002 — v1.1 + barras v2 — APROVADO

## Status

**APROVADO** após classificação e auditoria pós-classificação.

## Escopo

- 9.831 keywords base
- 73 controles incorporados
- 9.831 IDs base únicos
- Taxonomia v1.1
- Regras R01–R26
- Golden Set v1.1
- Mapa mestre de reconstruções de `/` v2

## QA final

- Colunas originais preservadas: sim
- Área/cluster/subcluster vazios: 0
- Controles incorporados: 73/73 preservados
- Golden Set completo: 107/107 exato em área + cluster + subcluster + intenção
- Reconstruções de `/` aplicadas: 20
- Conversões diretas sem origem/destino/direção: 0
- Regressões críticas finais: 0
- Alertas médios finais: 0

## Confiança

- alta: 7.446
- média: 1.212
- baixa: 1.173
- revisão manual marcada: 1.316

A baixa confiança e os casos contextuais/ambíguos permaneceram explicitamente marcados; não foram promovidos artificialmente para alta confiança.

## Correções relevantes da auditoria

A auditoria corrigiu padrões como:

- `g cm3 para kg m3` → interpretação `g/cm³ → kg/m³`, classificada em Densidade e concentração;
- equações exponenciais com fração reconstruída → Potências, raízes e logaritmos;
- `kwh dia` → `kWh/dia`, consumo elétrico, não custo;
- valores de rescisão/INSS → cálculo trabalhista, não preço de mercado;
- consultas cambiais com `hoje` → cotação atual;
- preço por m² de construção → Construção / custos e orçamento;
- `kwanza angolano` e `moeda argentina` com direção monetária corrigida;
- consultas de conversor com apenas um lado especificado deixaram de ser conversão direta.

## Regressões verificadas

Foram rechecadas as famílias que falharam no lote 001: potência elétrica vs potenciação; licenças/direitos trabalhistas vs Datas; preço/notícia de combustível; cotação vs conversão cambial; poupança vs Trabalho; valor de verba trabalhista vs preço de mercado; construção vs matemática genérica; PDF conteúdo vs conversão; `peso` genérico; e metadados de conversão direta.

Nenhum padrão crítico novo permaneceu aberto e não foi necessária Taxonomia v1.2.

## Decisão

A Taxonomia v1.1 continua congelada e válida. O **lote 003 está liberado** para classificação com o mesmo contrato semântico e o mapa mestre de barras v2.
