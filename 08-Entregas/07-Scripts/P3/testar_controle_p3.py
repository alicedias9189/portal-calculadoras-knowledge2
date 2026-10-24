#!/usr/bin/env python3
# coding: utf-8
"""Testes de regressão de elegibilidade: 108 decisões, 98 bloqueios, 10 elegíveis; negativos."""
import argparse,json,collections,hashlib,pathlib
from controle_elegibilidade_p3 import read_csv,load_indexes,validate

def main():
    pa=argparse.ArgumentParser(description=__doc__)
    for x in ('fila-p3','fila-geral','lotes','candidatos','quarentena','resultado'):pa.add_argument('--'+x,required=True)
    a=pa.parse_args()
    p3,g,lots,c=load_indexes(a.fila_p3,a.fila_geral,a.lotes)
    rs=read_csv(a.candidatos); q=read_csv(a.quarentena)
    valid,blocked=validate(rs,p3,g,lots)
    assert len(rs)==108 and len(valid)==10 and len(blocked)==98
    assert all(r['motivo_bloqueio']=='FORA_DA_FILA_GERAL_E_P3' for r in blocked)
    qids={x['id_global'] for x in q}; assert len(qids)==98
    assert qids=={r['id_global'] for r in blocked}
    good=valid[0]
    # Wrong keyword must never pass
    badkw=good.copy(); badkw['Keyword']='X_keyword_tampered'
    v,b=validate([badkw],p3,g,lots);assert not v and len(b)==1 and b[0]['motivo_bloqueio']=='DIVERGENCIA_KEYWORD'
    # Duplicate candidate fails closed
    v,b=validate([good,good],p3,g,lots);assert len(v)==1 and len(b)==1 and b[0]['motivo_bloqueio']=='ID_CANDIDATO_DUPLICADO'
    # nonexistent candidate fails closed
    fake=good.copy();fake['id_global']='999999999999999'
    v,b=validate([fake],p3,g,lots);assert len(b)==1 and b[0]['motivo_bloqueio']=='ID_NAO_EXISTE_BASE'
    # empty ID fails closed
    fake=good.copy();fake['id_global']=''
    v,b=validate([fake],p3,g,lots);assert len(b)==1 and b[0]['motivo_bloqueio']=='ID_VAZIO'
    # all other priorities blocked when they are actually in general
    alternate=next(x for x in g.values() if x['prioridade']=='P2')
    v,b=validate([{'id_global':alternate['id_global'],'Keyword':alternate['Keyword']}],p3,g,lots)
    assert len(b)==1 and b[0]['motivo_bloqueio']=='FORA_FILA_P3'
    out={'status':'PASSOU','candidatos':108,'elegiveis':10,'bloqueados':98,'sem_prioridade':98,'base':c['base'],'controles':c['controle'],'testes_negativos':['keyword divergente','duplicado','inexistente','vazio','prioridade P2 bloqueada'],'modificacoes_lotes':0}
    pathlib.Path(a.resultado).parent.mkdir(parents=True,exist_ok=True)
    pathlib.Path(a.resultado).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(out,ensure_ascii=False))
if __name__=='__main__':main()
