#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Marca variantes douradas em sete sementes ODS e gera VISÕES filtradas da auditoria P3 v5.2.
Uso: python auditar_e_filtrar_ouro.py --ods-zip todas_originais_ods.zip --p3-zip portal-calculadoras-auditoria-P3-v5.2-unico.zip --saida saida
O ZIP de entrada, IDs, controles e valores originais são preservados. Exclui somente de visões derivadas.
Requer lxml; restante da lógica usa a biblioteca padrão Python.
"""
import argparse,csv,io,json,re,unicodedata,hashlib,zipfile,collections
from pathlib import Path
from lxml import etree
N={'office':'urn:oasis:names:tc:opendocument:xmlns:office:1.0','style':'urn:oasis:names:tc:opendocument:xmlns:style:1.0','fo':'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0','table':'urn:oasis:names:tc:opendocument:xmlns:table:1.0','text':'urn:oasis:names:tc:opendocument:xmlns:text:1.0'}
T=lambda k:'{%s}%s'%(N['table'],k)
O=lambda k:'{%s}%s'%(N['office'],k)
S=lambda k:'{%s}%s'%(N['style'],k)
F=lambda k:'{%s}%s'%(N['fo'],k)
GOLD={'#ffbf00':'Ouro','#e8a202':'Ouro escuro 1'}

def norm(s):
 s=unicodedata.normalize('NFKD',s.casefold());s=''.join(c for c in s if not unicodedata.combining(c))
 return ' '.join(re.findall(r'\w+',s,flags=re.U))
def sha(data):return hashlib.sha256(data).hexdigest()
def read_csv(z,name):return csv.DictReader(io.TextIOWrapper(z.open(name),encoding='utf-8-sig',newline=''),delimiter=';')
def save(path,rows,cols):
 with open(path,'w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=cols,delimiter=';',lineterminator='\n');w.writeheader();w.writerows(rows)
def extract_ods(z,fname):
 data=z.read(fname)
 with zipfile.ZipFile(io.BytesIO(data)) as inner:
  content=etree.fromstring(inner.read('content.xml'))
  stylesroot=etree.fromstring(inner.read('styles.xml'))
  styles={}
  for tree in (stylesroot,content):
   for st in tree.xpath('//style:style',namespaces=N):
    nm=st.get(S('name'));tp=st.find('style:text-properties',N);cp=st.find('style:table-cell-properties',N)
    styles[nm]={'font':tp.get(F('color')) if tp is not None else None,'bg':cp.get(F('background-color')) if cp is not None else None,'parent':st.get(S('parent-style-name'))}
  def prop(nm,k):
   for _ in range(10):
    ent=styles.get(nm,{})
    v=ent.get(k)
    if v and v!='transparent':return v.lower()
    nm=ent.get('parent')
    if not nm:break
   return ''
  out=[]
  for tab in content.xpath('//table:table',namespaces=N):
   aba=tab.get(T('name'));ri=0
   for row in tab.xpath('table:table-row',namespaces=N):
    rr=int(row.get(T('number-rows-repeated'),'1'));ci=0
    for c in row:
     if c.tag not in (T('table-cell'),T('covered-table-cell')):continue
     cc=int(c.get(T('number-columns-repeated'),'1'))
     val=' '.join(x.strip() for x in c.xpath('text:p//text()',namespaces=N) if x.strip())
     if not val and c.get(O('value')):val=c.get(O('value'))
     if val:
      st=c.get(T('style-name')) or row.get(T('default-cell-style-name'))
      color=prop(st,'font')
      if color in GOLD:
       # repeated nonempty cell is the same source row; preserve multiplicity if present
       for r in range(rr):
        out.append({'arquivo_ods':Path(fname).name,'aba_ods':aba,'linha_ods':ri+r+1,'coluna_ods':ci+1,'cor_hex':color,'cor_nome':GOLD[color],'termo_origem':val,'chave_normalizada':norm(val)})
     ci+=cc
    ri+=rr
  return out

def main():
 p=argparse.ArgumentParser();p.add_argument('--ods-zip',required=True);p.add_argument('--p3-zip',required=True);p.add_argument('--saida',required=True);args=p.parse_args()
 out=Path(args.saida);out.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(args.ods_zip) as inp:
  source=sorted(inp.namelist()); colored=[];counts=[]
  for fn in source:
   if not fn.endswith('.ods'):continue
   rows=extract_ods(inp,fn);colored.extend(rows)
   counts.append({'planilha':Path(fn).name,'ouro':sum(x['cor_nome']=='Ouro' for x in rows),'ouro_escuro_1':sum(x['cor_nome']=='Ouro escuro 1' for x in rows)})
 bykey=collections.defaultdict(list)
 for x in colored:bykey[x['chave_normalizada']].append(x)
 # Detecta casos também presentes sem dourado na planilha; isso é importante
 # porque a Keyword única da base foi derivada de várias origens distintas.
 nongold=set()
 with zipfile.ZipFile(args.ods_zip) as inp:
  for fn in source:
   if not fn.endswith('.ods'):continue
   data=inp.read(fn)
   with zipfile.ZipFile(io.BytesIO(data)) as inner:
    content=etree.fromstring(inner.read('content.xml'));stylesroot=etree.fromstring(inner.read('styles.xml'))
    styles={}
    for tr in (stylesroot,content):
     for st in tr.xpath('//style:style',namespaces=N):
      nm=st.get(S('name'));tp=st.find('style:text-properties',N)
      styles[nm]=(tp.get(F('color')) or '') if tp is not None else ''
    for tab in content.xpath('//table:table',namespaces=N):
     for cell in tab.xpath('.//table:table-cell',namespaces=N):
      val=' '.join(x.strip() for x in cell.xpath('text:p//text()',namespaces=N) if x.strip())
      if val and norm(val) in bykey and styles.get(cell.get(T('style-name')),'').lower() not in GOLD:nongold.add(norm(val))
 with zipfile.ZipFile(args.p3_zip) as audit:
  original_batch_name=next(x for x in audit.namelist() if x.endswith('/lotes-001-a-030-p3-v5.2.zip'))
  original_qa_name=next(x for x in audit.namelist() if x.endswith('/p3-v5.2-fila-23965.csv'))
  general_name=next(x for x in audit.namelist() if x.endswith('/fila-geral-p0-p1-p2-p3-v5.2.csv'))
  batch=zipfile.ZipFile(io.BytesIO(audit.read(original_batch_name)))
  found=[];base_n=0;ctrl_n=0;originals=[]
  for filename in sorted(x for x in batch.namelist() if x.endswith('.csv')):
   r=read_csv(batch,filename)
   for row in r:
    if row['tipo_registro']=='controle':ctrl_n+=1;continue
    assert row['tipo_registro']=='base';base_n+=1
    key=norm(row['Keyword'])
    if key not in bykey:continue
    origin=bykey[key]
    found.append({'id_global':row['id_global'],'Keyword':row['Keyword'],'lote_id':row['lote_id'],'familia_id':row['familia_id'],'area_principal':row['area_principal'],'cor':origin[0]['cor_nome'],'cor_hex':origin[0]['cor_hex'],'origens_douradas':len(origin),'arquivo_ods':origin[0]['arquivo_ods'],'aba_ods':origin[0]['aba_ods'],'linha_ods':origin[0]['linha_ods'],'coluna_ods':origin[0]['coluna_ods'],'texto_dourado':origin[0]['termo_origem'],'match':'exato' if origin[0]['termo_origem'].strip().casefold()==row['Keyword'].strip().casefold() else 'normalizado','tambem_aparece_sem_dourado':'SIM' if key in nongold else 'NAO','decisao':'REVISAR_ORIGEM_DUPLA' if key in nongold else 'EXCLUIR_DE_VISOES_DERIVADAS'})
  assert (base_n,ctrl_n)==(294905,2190), (base_n,ctrl_n)
  assert len(found)==3621,len(found)
  safe={x['id_global'] for x in found if x['decisao']=='EXCLUIR_DE_VISOES_DERIVADAS'}
  review={x['id_global'] for x in found if x['decisao']=='REVISAR_ORIGEM_DUPLA'}
  assert len(safe)==3609 and len(review)==12 and not(safe & review)
  # Fila P3 derivada, sem alterar a canônica.
  rd=read_csv(audit,original_qa_name);headers=list(rd.fieldnames)
  status_cols=[k for k in headers if k.startswith('status_p3_v') and k!='status_p3_v1']
  eligible=lambda r:r['prioridade']=='P3' and r['status_p3_v1']=='FORA_DO_PILOTO' and not any(r[x] for x in status_cols)
  p3_rows=list(rd)
  eligibility=[r for r in p3_rows if eligible(r)]; p3_safe={r['id_global'] for r in eligibility}&safe
  assert len(p3_rows)==23965 and len(eligibility)==19562 and len(p3_safe)==100
  save(out/'fila-p3-v5.2-sem-ouro-23865.csv',[r for r in p3_rows if r['id_global'] not in p3_safe],headers)
  save(out/'pendentes-p3-sem-ouro-19462.csv',[r for r in eligibility if r['id_global'] not in p3_safe],headers)
  # Fila geral em visão derivada preservando os P2 já tratados (não alterá-los sem critério formal).
  general=list(read_csv(audit,general_name));gh=list(general[0]);assert len(general)==52046
  safe_general={r['id_global'] for r in general}&safe
  save(out/'fila-geral-v5.2-sem-ouro-51884.csv',[r for r in general if r['id_global'] not in safe_general],gh)
  assert len(safe_general)==162 and len(general)-len(safe_general)==51884
  # Lotes derivados; controles mantidos em todos os 30 lotes.
  count_original=count_filtered=count_ctrl=0
  rows_by_lote=[]
  with zipfile.ZipFile(out/'lotes-30-trabalho-sem-ouro.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as zout:
   for name in sorted(x for x in batch.namelist() if x.endswith('.csv')):
    rd=read_csv(batch,name);fieldnames=list(rd.fieldnames)
    b0=b1=controls=0;buff=io.StringIO();writer=csv.DictWriter(buff,fieldnames=fieldnames,delimiter=';',lineterminator='\n');writer.writeheader()
    for row in rd:
     if row['tipo_registro']=='controle':controls+=1;writer.writerow(row);continue
     b0+=1
     if row['id_global'] in safe:continue
     b1+=1;writer.writerow(row)
    rows_by_lote.append({'lote':name.split('/')[-1],'bases_originais':b0,'exclusoes_confirmadas':b0-b1,'bases_trabalho':b1,'controles_preservados':controls})
    count_original+=b0;count_filtered+=b1;count_ctrl+=controls
    zout.writestr(name,('\ufeff'+buff.getvalue()).encode('utf-8'))
  assert (count_original,count_filtered,count_ctrl)==(294905,291296,2190)
  # Relacionamentos auditáveis.
  found.sort(key=lambda x:int(x['id_global']))
  save(out/'ids-ouro-cruzados-3621.csv',found,list(found[0]))
  save(out/'ids-ouro-excluir-3609.csv',[x for x in found if x['id_global'] in safe],list(found[0]))
  save(out/'ids-ouro-revisar-12.csv',[x for x in found if x['id_global'] in review],list(found[0]))
  save(out/'ids-p3-ouro-removidos-100.csv',[x for x in found if x['id_global'] in p3_safe],list(found[0]))
  save(out/'estatistica-planilhas-ods.csv',counts,list(counts[0]))
  save(out/'regressao-30-lotes.csv',rows_by_lote,list(rows_by_lote[0]))
  matched_norms={norm(x['Keyword']) for x in found}
  missing=[{'chave_normalizada':key,'exemplo':val[0]['termo_origem'],'cor':val[0]['cor_nome'],'arquivo':val[0]['arquivo_ods']} for key,val in bykey.items() if key not in matched_norms]
  assert len(missing)==9
  save(out/'sementes-douradas-sem-match-na-base-9.csv',missing,list(missing[0]))
  totals={
   'arquivos_ods':len(counts),'celulas_douradas':len(colored),'ouro':sum(x['ouro'] for x in counts),'ouro_escuro_1':sum(x['ouro_escuro_1'] for x in counts),
   'sementes_normalizadas_unicas':len(bykey),'sementes_encontradas_na_base':len(bykey)-len(missing),'sementes_nao_encontradas':len(missing),
   'base_antes':base_n,'controles':ctrl_n,'ids_correspondentes_base':len(found),'ids_exclusao_segura':len(safe),'ids_origem_duplicada_revisar':len(review),
   'base_trabalho_depois':count_filtered,'fila_geral_antes':len(general),'fila_geral_trabalho_depois':len(general)-len(safe_general),
   'fila_p3_total_antes':len(p3_rows),'fila_p3_total_trabalho_depois':len(p3_rows)-len(p3_safe),
   'p3_elegiveis_antes':len(eligibility),'p3_removidos':len(p3_safe),'p3_elegiveis_depois':len(eligibility)-len(p3_safe),
   'p3_ja_tratados_cor_dourada':len({r['id_global'] for r in p3_rows}&safe)-len(p3_safe),
   'p2_na_fila_geral_dourado':sum(r['prioridade']=='P2' and r['id_global'] in safe_general for r in general),
   'integridade':'30 lotes: contagem de IDs excluídos explícita, 2190 controles inalterados, campos e valores dos IDs retidos preservados',
   'aprovacao_editorial':'PENDENTE','escopo':'Apenas visões derivadas; originais nunca regravados.'
  }
  assert totals['p3_ja_tratados_cor_dourada']==29
  (out/'resumo.json').write_text(json.dumps(totals,ensure_ascii=False,indent=2),encoding='utf8')
  meta={'fontes_sha256':{str(args.ods_zip):sha(Path(args.ods_zip).read_bytes()),str(args.p3_zip):sha(Path(args.p3_zip).read_bytes())},'resumo':totals}
  (out/'manifesto-fontes.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')
  print(json.dumps(totals,ensure_ascii=False,indent=2))
if __name__=='__main__':main()