#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compara 30 CSVs P2-v7 e P3 piloto v1, registros originais e patches reais.
Uso: python3 regressao_independente_p3_v1.py --origem /.../P2-v7 --saida /.../p3-v1-qa
"""
import argparse, csv, io, zipfile, json, hashlib
from pathlib import Path
from collections import Counter

def rows_file(f):
    return csv.DictReader(io.TextIOWrapper(f,encoding='utf-8-sig',newline=''),delimiter=';')

def run(origem,saida):
    zsrc=zipfile.ZipFile(origem/'lotes-001-a-030-p0-p1-p2-v7.zip')
    oldnames=sorted(x for x in zsrc.namelist() if x.startswith('lotes/') and x.endswith('.csv'))
    files=sorted((saida/'lotes').glob('lote-*-p3-v1.csv'))
    assert len(files)==len(oldnames)==30
    p=dict()
    with (saida/'p3-v1-patches.csv').open(encoding='utf-8-sig',newline='') as f:
        for row in csv.DictReader(f,delimiter=';'):
            assert row['id_global'] not in p; p[row['id_global']]=row
    edited=set();base=0;controls=0;changes_by_field=Counter();changed_area=0;changed_intent=0; per_lot=[];hash_protected=hashlib.sha256();seen=set()
    allow={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','confianca','revisao_manual','justificativa_curta'}
    for orig,pout in zip(oldnames,files):
        assert orig.replace('-v7.csv','-p3-v1.csv').endswith(pout.name), (orig,pout)
        with zsrc.open(orig) as fi,pout.open('rb') as fo:
            before=rows_file(fi);after=rows_file(fo)
            assert before.fieldnames==after.fieldnames
            n=0;nchanged=0;ncontrol=0
            from itertools import zip_longest
            for o,c in zip_longest(before,after):
                assert o is not None and c is not None,'linha faltante/excedente'
                n+=1;assert o['id_global']==c['id_global'] and o['Keyword']==c['Keyword'] and o['tipo_registro']==c['tipo_registro']
                if o['tipo_registro']=='controle':controls+=1;ncontrol+=1;assert o==c
                elif o['tipo_registro']=='base':base+=1;assert o['id_global'] not in seen;seen.add(o['id_global'])
                else:raise AssertionError('tipo desconhecido')
                diff={k:(o[k],c[k]) for k in o if o[k]!=c[k]}
                if diff:
                    assert o['tipo_registro']=='base' and o['id_global'] in p
                    assert set(diff)<=allow,(o['id_global'],set(diff)-allow)
                    patch=p[o['id_global']];prev=json.loads(patch['antes_json']);dest=json.loads(patch['depois_json']);
                    assert prev=={k:v[0] for k,v in diff.items()},o['id_global']
                    assert dest=={k:v[1] for k,v in diff.items()},o['id_global']
                    assert patch['campos_alterados']==', '.join(diff.keys())
                    assert o['id_global'] not in edited;edited.add(o['id_global']);nchanged+=1
                    if 'area_principal' in diff:changed_area+=1
                    if 'tipo_intencao' in diff:changed_intent+=1
                    for k in diff:changes_by_field[k]+=1
                else:
                    assert o['id_global'] not in p or o['tipo_registro']=='controle',('patch fantasma',o['id_global'])
                for k in o:
                    if k not in allow:
                        hash_protected.update((o[k]+'\x1f').encode('utf-8'))
            per_lot.append({'lote':pout.name[:8],'linhas':n,'controle':ncontrol,'patches':nchanged,'resultado':'PASSOU'})
    assert base==294905 and controls==2190,(base,controls)
    assert edited==set(p),('patches sem alteracao',len(set(p)-edited))
    res={'status':'PASSOU','lotes':len(per_lot),'registros_base':base,'controles':controls,'ids_alterados':len(edited),
      'alteracao_area':changed_area,'alteracao_tipo_intencao':changed_intent,'alteracoes_por_campo':dict(changes_by_field),
      'hash_sha256_fonte_campos_protegidos':hash_protected.hexdigest(),'por_lote':per_lot,
      'observacao':'Regressão estrutural e da trilha de patches; não revisa julgamento editorial nem reexecuta Golden Set.'}
    (saida/'p3-v1-regressao-independente.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8')
    return res

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--origem',required=True,type=Path);p.add_argument('--saida',required=True,type=Path);a=p.parse_args()
    r=run(a.origem,a.saida)
    print(json.dumps({k:v for k,v in r.items() if k!='por_lote'},ensure_ascii=False,indent=2))
