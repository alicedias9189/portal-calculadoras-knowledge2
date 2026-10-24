# DEC-092 — Revisão crítica individual das 100 classificações P3 v5.4 (versão v5.5)

**Data:** 24/10/2026  
**Fonte:** DEC-091, base P3 v5.4 + filtro Ouro reversível DEC-089.  
**Estado:** auditoria técnica validada; **homologação editorial PENDENTE**.

## Escopo e decisão

Foram examinados **exatamente os 100 IDs da expansão v5.4**, abrangendo **34 famílias e sete grupos**. Não foram selecionados IDs novos nem reabertos registros de ciclos anteriores. Resultado: **23 refinamentos semanticamente justificados** e **77 classificações mantidas com ressalvas**. Cada linha tem parecer individual no CSV `p3-v5.5-pareceres-100.csv` e, nos 23 casos alterados, diff `antes_json`/`depois_json` no CSV `p3-v5.5-patches-23.csv`.

### Motivos dos 23 refinamentos

| Grupo | Refinamentos | Fundamentação |
|---|---:|---|
| Gestação e ferramentas | 1 | Calendário gestacional é material de referência, não um cálculo previamente parametrizado |
| Direitos da gestante | 9 | Direito/lei genérica não significa automaticamente estabilidade; separar retorno e restrições ao trabalho |
| Estatística/ENEM | 3 | Moda salarial, consulta conceitual de média e solicitação de resolução de probabilidade exigem intenções diferentes |
| Investimentos | 3 | Verbo “simular” não equivale automaticamente à busca por ferramenta chamada simulador |
| Planilhas financeiras | 6 | Não atribuir uso pessoal onde a consulta não explicita o público |
| Juros de cartão | 1 | Fatura com juros não indica, por si só, parcelamento ou financiamento formal |
| Prazos | 0 | Doze buscas pedem calculadoras e suas especializações já eram defensáveis |
| **Total** | **23** | |

Os termos de legislação geral ainda apresentam **ambiguidade de âmbito jurídico**. Foram refinados os subclusters, mas não se afirmou que tenham exclusivamente intenção trabalhista: a área atual `Trabalho` foi mantida como hipótese operacional e a ressalva permanece explícita para homologação futura. Não extrapolar aconselhamento jurídico, dados clínicos, percentuais financeiros, notas do ENEM ou cálculos sem parâmetros.

## Invariantes e regressão independente

- **60/60 lotes PASSOU** (30 canônicos, 30 com filtro Ouro), conferindo registro a registro os arquivos v5.4/v5.5.
- **23/23 patches aprovados**, exclusivamente nos IDs revisados; todos os demais registros foram preservados integralmente.
- Totais: **294.905 registros-base canônicos**, **291.296 operacionais sem Ouro**, **2.190 controles por versão**.
- Ouro: **3.609 IDs retirados somente de cópias operacionais**, com origem e reversibilidade documentadas na DEC-089.
- Quatro filas: **23.965**, **52.046**, **23.865** e **51.884** linhas. **414 colunas anteriores intactas** e somente oito novas colunas de rastreabilidade da v5.5.
- **4.660 pendências P2** não reabertas; **98 propostas globais** idênticas byte a byte.
- Sem novos IDs, elegíveis P3 continuam em **19.362 operacionais** e **19.462 canônicos**.

## Entrega e reprodução

Os **quatro scripts** (`auditar_p3_v55.py`, `regressao_independente_p3_v55.py`, `gerar_qa_p3_v55.py` e `montar_entrega_p3_v55.py`) estão em `07-Scripts/P3/`. Para reproduzir, extrair primeiro o ZIP **P3 v5.4**, preservando `08-Entregas/P3-v5.4/`, e depois executar os scripts na raiz da pasta.

O pacote completo da v5.5 contém 30+30 lotes, quatro filas, pareceres, patches, Excel de oito abas, relatórios e SHA-256. **A documentação e scripts são versionados no GitHub; arquivos CSV/XLSX/ZIP completos permanecem entregues pelo ChatGPT, não necessariamente sincronizados no GitHub.**

**Próxima fase:** P3 v5.6, expansão seletiva de **100 novos IDs** exclusivamente dentre os **19.362 elegíveis operacionais sem Ouro**, seguida de nova revisão crítica. **Não considerar a auditoria técnica como homologação editorial humana.**