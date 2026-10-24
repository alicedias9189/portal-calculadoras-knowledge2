#!/usr/bin/env python3
"""Auditoria independente de integridade P2 v3→v4.
Confronta TODOS os registros das 30 planilhas CSV, sem alterar os arquivos.
"""
import argparse,csv,hashlib,io,json,zipfile
from pathlib import Path

def open_rows(z,name):return csv.DictReader(io.TextIOWrapper(z.open(name),encoding='utf-8-sig',newline=''),delimiter=';')
def main():
 p=argparse.ArgumentParser();p.add_argument('--raiz',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--saida',type=Path,default=None);a=p.parse_args()
 root=a.raiz;out=a.saida or root/'08-Entregas/P2-v4';out.mkdir(exist_ok=True,parents=True)
 source=zipfile.ZipFile(root/'08-Entregas/P2-v3/lotes-001-a-030-p0-p1-p2-v3.zip')
 target=zipfile.ZipFile(out/'lotes-001-a-030-p0-p1-p2-v4.zip')
 aud=zipfile.ZipFile(out/'auditoria-p2-v4-csv-integral.zip')
 patches=list(open_rows(aud,'p2-v4-patches.csv'))
 ids={r['id_global'] for r in patches};expected=json.loads((out/'resumo-p2-v4.json').read_text(encoding='utf-8'))
 assert len(ids)==len(patches)==expected['reclassificadas']
 changed_fields={'area_principal','cluster','subcluster','tipo_intencao','intencao_principal','confianca','revisao_manual','justificativa_curta','unidade_origem','unidade_destino','direcao_conversao'}
 sourcepaths=[n for n in source.namelist() if n.endswith('.csv')]
 targetpaths=[n for n in target.namelist() if n.endswith('.csv')]
 assert len(sourcepaths)==len(targetpaths)==30
 stats=[];seen=set();nbase=ncontrol=nchanged=0
 for src in sorted(sourcepaths):
  dst=src.replace('-v3.csv','-v4.csv');assert dst in targetpaths
  r1=open_rows(source,src);r2=open_rows(target,dst);nrows=bc=cc=changed=0
  for old,new in zip(r1,r2):
   nrows+=1; assert set(old)==set(new)
   assert old['id_global']==new['id_global'] and old['tipo_registro']==new['tipo_registro']
   id=old['id_global'];t=old['tipo_registro']
   if t=='controle':cc+=1
   if t=='base':
    bc+=1;assert id not in seen;seen.add(id)
   diff={k for k in old if old[k]!=new[k]}
   if id in ids and t=='base':
    assert diff and diff.issubset(changed_fields),(id,diff)
    changed+=1
   else:assert not diff, (id,diff)
  assert nrows==bc+cc and cc==73,(src,nrows,bc,cc)
  nbase+=bc;ncontrol+=cc;nchanged+=changed
  stats.append({'lote':src.split('/')[-1],'linhas':nrows,'base':bc,'controles':cc,'revisadas':changed,'teste':'PASSOU'})
 assert nbase==294905 and ncontrol==2190 and nchanged==expected['reclassificadas'],(nbase,ncontrol,nchanged)
 # Checagem independente dos 388 IDs únicos em decisão e metadados de conversão.
 decisions={r['id_global']:r for r in open_rows(aud,'p2-v4-decisoes-25050.csv')}
 assert len(decisions)==25050
 for id in ids:
  r=decisions[id];assert r['classificacao_alterada_p2_v4']=='sim'
  if r['tipo_intencao_final_p2_v4'] in ('conversão direta','conversão de arquivo/mídia'):
   assert r['unidade_origem_final_p2_v4'] and r['unidade_destino_final_p2_v4'],id
 pending=list(open_rows(aud,'p2-v4-pendencias-restantes.csv'))
 assert len(pending)==expected['pendencias_restantes']
 assert {x['id_global'] for x in pending}.isdisjoint(ids)
 report={'status':'PASSOU','lotes':30,'base':nbase,'controles':ncontrol,'alteracoes':nchanged,'pendencias':len(pending),'checklist':stats}
 (out/'regressao-independente-p2-v4.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('AUDITORIA INDEPENDENTE PASSOU:',nbase,ncontrol,nchanged,flush=True)
if __name__=='__main__':main()
