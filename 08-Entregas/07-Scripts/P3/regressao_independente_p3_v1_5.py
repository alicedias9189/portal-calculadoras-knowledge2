#!/usr/bin/env python3
"""Regressão estrutural independente P3 v1.4 x v1.5; não aplica correções.
Uso: python regressao_independente_p3_v1_5.py --fonte DIR_EXTRAIDO --saida DIR_RESULTADO
"""
import argparse,csv,io,json,zipfile,collections,hashlib
from pathlib import Path
ALLOW={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','confianca','revisao_manual','justificativa_curta'}
def parse(b):return list(csv.DictReader(io.StringIO(b.decode('utf-8-sig')),delimiter=';'))
def load(p):
 with open(p,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def main():
 p=argparse.ArgumentParser();p.add_argument('--fonte',type=Path,required=True);p.add_argument('--saida',type=Path,required=True);a=p.parse_args()
 root=a.fonte/'08-Entregas/P3-v1.4';out=a.saida
 patch=load(out/'p3-v1.5-patches.csv');exp={x['id_global']:x for x in patch};assert len(exp)==len(patch)
 old=root/'lotes-001-a-030-p3-v1.4.zip';new=out/'lotes-001-a-030-p3-v1.5.zip'
 rows_qa=[];nbase=nctrl=ndiff=0;diff_ids=set();oldprotected=hashlib.sha256();newprotected=hashlib.sha256()
 with zipfile.ZipFile(old) as za,zipfile.ZipFile(new) as zb:
  names=za.namelist();assert len(names)==len(zb.namelist())==30
  for name in names:
   on=za.read(name);nn=name.replace('v1.4.csv','v1.5.csv');rn=zb.read(nn)
   x=parse(on);y=parse(rn);assert len(x)==len(y);beforekeys=list(x[0]);assert beforekeys==list(y[0]);lt=0;lotbase=lotctrl=0
   for oldrow,newrow in zip(x,y):
    assert oldrow['id_global']==newrow['id_global'];assert oldrow['Keyword']==newrow['Keyword']
    assert oldrow['tipo_registro']==newrow['tipo_registro']
    protected0={k:v for k,v in oldrow.items() if k not in ALLOW}
    protected1={k:v for k,v in newrow.items() if k not in ALLOW}
    assert protected0==protected1,('PROTECTED_CHANGED',name,oldrow['id_global'])
    signature=json.dumps(protected0,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode('utf8');oldprotected.update(signature);newprotected.update(json.dumps(protected1,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode('utf8'))
    rid=oldrow['id_global'];diff={k:(oldrow[k],newrow[k]) for k in beforekeys if oldrow[k]!=newrow[k]}
    if oldrow['tipo_registro']!='base':
     assert not diff,('CONTROL_CHANGED',rid);lotctrl+=1;nctrl+=1;continue
    lotbase+=1;nbase+=1
    if diff:
     lt+=1;ndiff+=1;diff_ids.add(rid)
     assert set(diff)<=ALLOW,('WRONG_FIELDS',rid,diff)
     assert rid in exp,('UNDOCUMENTED_CHANGE',rid)
     patchrow=exp[rid];before=json.loads(patchrow['antes_json']);after=json.loads(patchrow['depois_json'])
     assert set(before)==set(after)==set(diff)==set(patchrow['campos_alterados'].split(',')),('DIFF_KEYS',rid)
     assert all((oldrow[k],newrow[k])==(before[k],after[k]) for k in diff),('WRONG_BEFORE_AFTER',rid)
    else:assert rid not in exp,('PATCH_WITHOUT_CHANGE',rid)
   rows_qa.append({'arquivo_fonte':name,'arquivo_saida':nn,'bases':lotbase,'controles':lotctrl,'alterados':lt,'status':'PASSOU'})
 assert (nbase,nctrl)==(294905,2190),(nbase,nctrl)
 assert diff_ids==set(exp),('DIFFSET',len(diff_ids),len(exp))
 for original,generated in [('p3-v1.4-fila-23965.csv','p3-v1.5-fila-23965.csv'),('fila-geral-p0-p1-p2-p3-v1.4.csv','fila-geral-p0-p1-p2-p3-v1.5.csv')]:
  orig=load(root/original);newr=load(out/generated);assert len(orig)==len(newr)
  for o,n in zip(orig,newr):
   assert all(n[k]==v for k,v in o.items()),('PRIOR_QUEUE_MODIFIED',o['id_global'])
   if o['id_global'] in exp: assert n['classificacao_alterada_p3_v1_5']=='sim'
   else:assert all(not v for k,v in n.items() if k.endswith('_p3_v1_5'))
 with open(out/'p3-v1.5-regressao-independente-30-lotes.csv','w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows_qa[0]),delimiter=';');w.writeheader();w.writerows(rows_qa)
 summary={'lotes_PASSOU':len(rows_qa),'registros_base':nbase,'controles':nctrl,'ids_modificados':ndiff,'patches_conferidos':len(exp),'sha256_protegido_fonte':oldprotected.hexdigest(),'sha256_protegido_saida':newprotected.hexdigest(),'result':'PASSOU','criterios':'Campos protegidos, controles, ID/keyword, diffs reais, filas antigas e conjuntos de patches'}
 assert summary['sha256_protegido_fonte']==summary['sha256_protegido_saida']
 (out/'p3-v1.5-regressao-resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
