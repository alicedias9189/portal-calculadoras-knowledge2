# DEC-068 — Expansão seletiva P3 v3.2

Data: 2026-10-23.

**Decisão:** ampliar exclusivamente os registros P3 previamente `FORA_DO_PILOTO`, sem status de auditorias posteriores, usando cruzamento estrito entre fila P3, fila geral, lotes e exclusão de 98 IDs globais. Corrigir seis grupos de domínio com 68 propostas individualizadas e ressalvas de intenção; preservar os demais registros.

**Critério de segurança:** bloqueio por prioridade, ID, palavra-chave, família e lote; proibição de alterar controles ou campos protegidos; regressão independente obrigatória para 30 lotes; patches antes/depois; proteção das duas filas com adição de 9 colunas v3.2.

**Decisões semânticas:** consultas a modelos/planilhas de horas extras são informacionais; buscas `como calcular` são orientação; payback descontado não é rendimento genérico; diferença de datas no Excel não é estatística; IPVA depende do estado/ano; kWh é tarifa elétrica e não juros.

**Resultado:** 68 patches/36 famílias; fila P3 fora dos pilotos 20.272→20.204; 4.660 P2 e 98 casos globais intocados. Classificações sujeitas a homologação editorial.

Próxima etapa: revisão contextual crítica dos 68 casos, dando atenção a horas extras, IPVA e payback descontado antes de nova expansão.
