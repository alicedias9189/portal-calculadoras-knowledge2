#!/usr/bin/env python3
# coding: utf-8
"""Revisa os itens de quarentena da P3 v2.3 e os separa por tipo de ressalva.
Nenhum resultado deve ser aplicado automaticamente a lotes. A saída é uma fila de QA.
"""
import argparse,csv,re,collections,json,pathlib
from controle_elegibilidade_p3 import read_csv,write_csv,load_indexes,validate

def parecer(r):
    k=r['Keyword'].lower()
    regra=r['regra']
    if regra=='P3V22_IRRF_BASE_FINANCAS':
        if 'tabela' in k:
            return ('CORRIGIR_INTENCAO_DA_PROPOSTA','informacional','Referência a tabela histórica de base de IRRF, não pedido de calcular um valor; conferir exercício fiscal e regime.')
        if k.startswith(('base de calculo','base de cálculo','base para')) and not any(w in k for w in ('calculadora','calcular')):
            return ('CORRIGIR_INTENCAO_DA_PROPOSTA','informacional','Busca pela base tributável do IRRF, não uma operação numérica com entradas fornecidas; regime e ano variáveis.')
        return ('PLAUSIVEL_COM_RESSALVAS','cálculo contextual','Subdomínio IRRF plausível; fórmulas dependem de ano, natureza do rendimento (aluguel/salário) e dados informados.')
    if regra=='P3V22_CET_CREDITO':
        if 'como calcular' in k:
            return ('PLAUSIVEL_COM_RESSALVAS','informacional','Pedido de instrução sobre CET, sem dados de custos; não calcular taxa presumida.')
        if 'calculadora' in k or re.search(r'\bcalcular\b',k):
            return ('AJUSTAR_INTENCAO_DA_PROPOSTA','cálculo contextual','Busca ferramenta para cálculo de CET; exige fluxo de pagamentos, custos e encargos, não resultado automático.')
        if any(x in k for x in ('caixa','banco do brasil')):
            return ('REVISAR_INTENCAO_INSTITUICAO','informacional','Instituição citada; não presumir navegação direta nem taxa específica. Preservar consulta e validar serviço quando disponível.')
        return ('PLAUSIVEL_COM_RESSALVAS','informacional','CET é custo efetivo total, distinto da taxa nominal; verificar contexto de crédito e custo informado.')
    if regra=='P3V22_INSS_DESCONTO_INFO':
        if 'irpf' in k:
            return ('AJUSTAR_SUBTIPO_DA_PROPOSTA','cálculo contextual','Consulta combina descontos de INSS e IRPF; subgrupo só INSS é incompleto, demanda subtipo conjunto.')
        if 'consultar' in k:
            return ('REVISAR_INTENCAO_SERVICO','informacional','"Consultar" pode indicar serviço de consulta ou informação; não presumir cálculo nem navegação a órgão.')
        return ('PLAUSIVEL_COM_RESSALVAS','informacional','Consulta sobre desconto de INSS; regras, ano e tipo de vínculo não podem ser presumidos.')
    if regra=='P3V22_TAXA_FINANC_IMOVEL':
        if any(x in k for x in ('caixa','bradesco','itau','itaú','santander','banco central')):
            return ('REVISAR_INTENCAO_INSTITUICAO','informacional','Busca de taxa associada a instituição, não simulador; consultar data, modalidade e fonte sem criar taxa fictícia.')
        return ('PLAUSIVEL_COM_RESSALVAS','informacional','Taxa de financiamento imobiliário pode variar por data, modalidade e perfil; não confundir cotação, comparador e simulação.')
    return ('REVISAR_REGRA_DESCONHECIDA','','Sem regra de revisão reconhecida; revisão manual necessária.')

def rotear(qu, p3, geral, lots):
    can,blocked=validate(qu,p3,geral,lots)
    if can: raise ValueError('Quarentena contém ID elegível à P3; examinar origem antes de prosseguir')
    if len(qu)!=len(blocked):raise ValueError('Quarentena não conciliada')
    tri=[]
    for row in blocked:
        estado,tipo,nota=parecer(row)
        tri.append({**row,'prioridade_verificada':'SEM_PRIORIDADE_NA_FILA_52046','destino_recomendado':'BACKLOG_GLOBAL_NAO_PRIORIZADO','parecer_contextual':estado,'tipo_intencao_proposto_revisado':tipo,'observacao_individual':nota,'aplicar_agora':'NAO','motivo_nao_aplicar':row['motivo_bloqueio'],'proxima_acao':'Reavaliar em triagem global de prioridades, com validação editorial e sem alterar P0/P1/P2/P3'})
    return tri

def main():
    pa=argparse.ArgumentParser(description=__doc__)
    for x in ('fila-p3','fila-geral','lotes','quarentena','saida'):pa.add_argument('--'+x,required=True)
    a=pa.parse_args()
    p3,g,lots,c=load_indexes(a.fila_p3,a.fila_geral,a.lotes)
    tri=rotear(read_csv(a.quarentena),p3,g,lots)
    out=pathlib.Path(a.saida);out.mkdir(parents=True,exist_ok=True)
    write_csv(out/'p3-v2.4-quarentena-98-triada.csv',tri)
    summary={'total':len(tri),'fora_fila_p3_e_geral':len(tri),'por_regra':dict(collections.Counter(x['regra'] for x in tri)),'por_parecer':dict(collections.Counter(x['parecer_contextual'] for x in tri)),'destino':'BACKLOG_GLOBAL_NAO_PRIORIZADO','aplicacoes':0}
    (out/'p3-v2.4-triagem-resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
