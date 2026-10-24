#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera fila P3 integral e fila global com anotação do piloto, sem alterar colunas anteriores.
Uso: python3 gerar_filas_p3_v1.py --origem /.../P2-v7 --saida /.../qa
"""
import argparse,csv,zipfile,io,collections,json
from pathlib import Path

def make(src,out):
    with zipfile.ZipFile(src/'auditoria-p2-v7-csv-integral.zip') as z:
        with z.open('p2-v7-fila-geral.csv') as f:
            allr=list(csv.DictReader(io.TextIOWrapper(f,encoding='utf-8-sig',newline=''),delimiter=';'))
    with (out/'p3-v1-piloto-2090-decisoes.csv').open(encoding='utf-8-sig',newline='') as f:
        examined={r['id_global']:r for r in csv.DictReader(f,delimiter=';')}
    with (out/'p3-v1-patches.csv').open(encoding='utf-8-sig',newline='') as f:
        patches={r['id_global']:r for r in csv.DictReader(f,delimiter=';')}
    add=['status_p3_v1','regra_p3_v1','justificativa_p3_v1','area_final_p3_v1','cluster_final_p3_v1','subcluster_final_p3_v1','tipo_intencao_final_p3_v1','classificacao_alterada_p3_v1']
    fields=list(allr[0])+add
    p3rows=[]
    for r in allr:
        n=r.copy();n.update({c:'' for c in add});ident=r['id_global']
        if r['prioridade']!='P3':n['status_p3_v1']='NAO_ALVO_P3'
        elif ident not in examined:n['status_p3_v1']='FORA_DO_PILOTO'
        else:
            d=examined[ident];n['status_p3_v1']=d['status'];n['regra_p3_v1']=d['regra'];n['justificativa_p3_v1']=d['justificativa'];n['classificacao_alterada_p3_v1']=d['houve_patch']
            patch=patches.get(ident)
            if patch:
                new=json.loads(patch['depois_json'])
                # Campos ausentes em patches mantêm a classificação anterior do lote, presente na fila de base
                n['area_final_p3_v1']=new.get('area_principal',r['area'])
                n['cluster_final_p3_v1']=new.get('cluster',r['cluster'])
                n['subcluster_final_p3_v1']=new.get('subcluster',r['subcluster'])
                n['tipo_intencao_final_p3_v1']=new.get('tipo_intencao',r['tipo_intencao_atual'])
        if r['prioridade']=='P3':p3rows.append(n)
        r.clear();r.update(n)
    assert len(p3rows)==23965 and len(examined)==2090 and len(patches)==1207
    def write(path, rows):
        with path.open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.DictWriter(f,fieldnames=fields,delimiter=';');w.writeheader();w.writerows(rows)
    write(out/'p3-v1-fila-23965.csv',p3rows)
    write(out/'fila-geral-p0-p1-p2-p3-v1.csv',allr)
    return {'p3_total':len(p3rows),'fila_total':len(allr),'status_p3':dict(collections.Counter(x['status_p3_v1'] for x in p3rows))}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--origem',type=Path,required=True);p.add_argument('--saida',type=Path,required=True);a=p.parse_args();print(json.dumps(make(a.origem,a.saida),ensure_ascii=False,indent=2))
