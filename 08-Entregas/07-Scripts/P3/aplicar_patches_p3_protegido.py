#!/usr/bin/env python3
# coding: utf-8
"""Aplica patches propostos APENAS após validação tripla P3.
Entrada de patch: CSV com id_global, antes_json, depois_json, Keyword opcional.
Alterações restritas a campos analíticos. Sem --aplicar, executa dry-run.
Ao executar, escreve ZIP novo num local escolhido, nunca sobrescreve a origem.
"""
import argparse, csv, io, json, pathlib, zipfile, collections
from controle_elegibilidade_p3 import load_indexes, validate, read_csv

AUTORIZADOS={'area_principal','cluster','subcluster','dominio_ou_grandeza','tipo_intencao','intencao_principal','confianca','revisao_manual','justificativa_curta'}

def main():
    pa=argparse.ArgumentParser(description=__doc__)
    for f in ('fila-p3','fila-geral','lotes','patches','saida'):pa.add_argument('--'+f,required=True)
    pa.add_argument('--aplicar',action='store_true')
    a=pa.parse_args();p3,general,lots,_=load_indexes(a.fila_p3,a.fila_geral,a.lotes)
    patches=read_csv(a.patches);allow,blocked=validate(patches,p3,general,lots)
    if blocked:raise SystemExit(f'ABORTADO: {len(blocked)} IDs inelegíveis (nenhuma saída gravada)')
    change={}
    for patch in allow:
        rid=patch['id_global']; old=json.loads(patch['antes_json']);new=json.loads(patch['depois_json'])
        if not isinstance(old,dict) or not isinstance(new,dict) or not old or set(old)!=set(new) or not set(old)<=AUTORIZADOS:
            raise SystemExit('ABORTADO: campos não autorizados no ID '+rid)
        change[rid]=(old,new)
    if not a.aplicar:
        print(json.dumps({'modo':'DRY_RUN','elegiveis':len(allow),'bloqueados':0},ensure_ascii=False));return
    output=pathlib.Path(a.saida)
    if output.exists():raise SystemExit('ABORTADO: não sobrescrever saída já existente: '+str(output))
    # preflight all patches before writing; guarantees atomicity against mismatch
    found={}
    with zipfile.ZipFile(a.lotes) as z:
        for filename in z.namelist():
            with z.open(filename) as raw:
                for r in csv.DictReader(io.TextIOWrapper(raw,encoding='utf-8-sig',newline=''),delimiter=';'):
                    rid=r.get('id_global')
                    if rid in change:
                        old,new=change[rid]
                        if r.get('tipo_registro')!='base' or any(r.get(k)!=v for k,v in old.items()):
                            raise SystemExit('ABORTADO: precondição antes_json falhou: '+rid)
                        found[rid]=True
    if set(found)!=set(change):raise SystemExit('ABORTADO: IDs dos patches não encontrados')
    # Work in temporary file, publish via rename only after success
    tmp=output.with_suffix(output.suffix+'.parcial');updated=0
    try:
        with zipfile.ZipFile(a.lotes) as za,zipfile.ZipFile(tmp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zb:
            for filename in za.namelist():
                with za.open(filename) as raw:
                    reader=csv.DictReader(io.TextIOWrapper(raw,encoding='utf-8-sig',newline=''),delimiter=';')
                    fields=reader.fieldnames; rows=[]
                    for row in reader:
                        rid=row.get('id_global')
                        if rid in change:
                            row.update(change[rid][1]);updated+=1
                        rows.append(row)
                buff=io.StringIO();w=csv.DictWriter(buff,fieldnames=fields,delimiter=';',lineterminator='\n');w.writeheader();w.writerows(rows)
                zb.writestr(filename,('\ufeff'+buff.getvalue()).encode('utf-8'))
        assert updated==len(change)
        tmp.replace(output)
        print(json.dumps({'status':'OK','aplicados':updated,'saida':str(output)},ensure_ascii=False))
    finally:
        if tmp.exists():tmp.unlink()
if __name__=='__main__':main()
