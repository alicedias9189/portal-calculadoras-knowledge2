# DEC-060 — Guardião de prioridades P3 e quarentena global

## Decisão
A classificação P3 deve ser limitada à interseção da fila P3, da fila geral `prioridade=P3` e da base dos 30 lotes. **Não é permitido incluir automaticamente termos de outros estágios, nem termos fora da fila geral.**

## Regras de segurança
- Falhar em presença de IDs duplicados, campos de identidade divergentes, campos protegidos propostos, ou IDs fora do estágio.
- Simular por padrão, sem modificar dados. Para aplicar patches, exigir comando explícito, arquivo de saída novo e comparação com valores anteriores.
- Manter as 98 propostas da v2.2 fora da fila como backlog global sem prioridade; não supor que são P0/P1/P2.
- Nenhuma das 98 propostas constitui decisão editorial aprovada. A triagem contém apenas sugestões e ressalvas.
- Arquivos dos lotes P3 v2.3 devem permanecer intactos nesta etapa P3 v2.4.

## Resultado e integridade
Ver `08-Entregas/P3-v2.4/RELATORIO-P3-V2.4.md` e testes em `p3-v2.4-testes-seletor.json`. 108 decisões avaliadas, 98 bloqueadas, 10 elegíveis; nenhuma alteração efetiva.
