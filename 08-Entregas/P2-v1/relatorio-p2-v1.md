# Auditoria P2 — triagem contextual e validação determinística

- P2 original: **25,050** keywords nos 30 lotes.
- Validadas por regra: **8,946**.
- Com ressalvas operacionais/contextuais: **7,291**.
- Ainda pendentes por evidência insuficiente: **8,813**.
- Registros com campos analíticos alterados: **16,237**.
- Base preservada: **294,905** keywords; controles preservados: **2,190**.
- Assinatura SHA256 de todas as colunas protegidas antes/depois: `902805a347ba53570bbbb6f080600983881a875712fd4ea5ad2feba9acf27e35`.

## Método e limitações

Análise feita por regras de linguagem e contexto, não por leitura humana independente de 25 mil termos. Os estados VALIDADO e COM_RESSALVA refletem apenas confiança das regras e **não equivalem a aprovação editorial definitiva**. Casos incertos permanecem na fila `p2-pendencias.csv`; ajustes são propostos somente quando há evidência textual, sem adivinhar parâmetros, moeda, unidade ou direção. As classificações P0 e P1, os 2.190 controles, todos os dados Ads e colunas de reconstrução de barras foram preservados. Nunca se deve aplicar taxa fixa para converter massa↔volume, comprimento↔área, V↔W, nem tratar menções a PDF didático como conversão de arquivos.

## Pistas de regressão e reexecução

`qa-regressao-30-lotes-p2.csv` contém os 30 lotes com status PASSOU; `p2-patches.csv` apresenta os campos antes/depois; `resumo-p2-v1.json` discrimina regras, decisões e SHA256. Os scripts executáveis `revisar_p2_30_lotes_v1.py` e `p2_classificador_base.py` reproduzem a trilha a partir dos ZIPs P0/P1 v2, e `gerar_planilha_p2_v1.py` gera a planilha. A base original não foi sobrescrita.

## Escopo

P2 não implica revisão independente de P0/P1 nem P3. A validação é uma etapa de triagem e saneamento com controles de integridade. A próxima passada útil é revisão amostral estratificada por regra de maior volume e revisão contextual manual de pendências, antes de usar as decisões como taxonomia de produção.

## Planilha centralizada

A planilha `.xlsx` apresenta resumo e **amostra estratificada**, não todo o universo P2. A lista completa de 25.050 registros, com todas as colunas, está em `p2-validacao-semantica-25050.csv`, e a fila consolidada completa está em `fila-30-lotes-p0-p1-p2-v1.csv`. A planilha também inclui 1.100 pendências como amostra, enquanto `p2-pendencias.csv` tem todos os 8.813 casos.