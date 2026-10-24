#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auditoria P3 v1.2: Saúde/gestação e 43 alertas navegacionais.

Preserva P3 v1.1, P2 v7 e fontes originais; produz nova versão paralela.
Dependências: apenas biblioteca padrão. Para XLSX use gerar_qa_p3_v1_2.py.
Uso: python auditar_p3_v1_2.py --fonte <pacote-P3-v1.1-extraido> --destino <pasta>
"""
import argparse, csv, hashlib, io, json, re, unicodedata, zipfile
from pathlib import Path
from collections import Counter

CAMPOS_ANALITICOS={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','confianca','revisao_manual','justificativa_curta'}
FIELDS_NEW=['status_p3_v1_2','regra_p3_v1_2','nota_qa_p3_v1_2','area_final_p3_v1_2','cluster_final_p3_v1_2','subcluster_final_p3_v1_2','tipo_intencao_final_p3_v1_2','classificacao_alterada_p3_v1_2']
def ler_csv_bytes(b):return list(csv.DictReader(io.StringIO(b.decode('utf-8-sig')),delimiter=';'))
def csv_bytes(rows, cols):
 s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=cols,delimiter=';',lineterminator='\n');w.writeheader();w.writerows(rows);return ('\ufeff'+s.getvalue()).encode('utf-8')
def salvar_csv(path,rows,cols):path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(csv_bytes(rows,cols))
def norma(s):return ''.join(c for c in unicodedata.normalize('NFKD',s.casefold()) if not unicodedata.combining(c))
def cifrar_protegidos(rows,campos):
 h=hashlib.sha256()
 for row in rows:
  h.update(json.dumps([row.get(k,'') for k in campos if k not in CAMPOS_ANALITICOS],ensure_ascii=False,separators=(',',':')).encode('utf-8'));h.update(b'\n')
 return h.hexdigest()

def decidir_saude(r):
 kw=r['Keyword'];t=norma(kw)
 if not re.search(r'gesta|gravid',t): raise ValueError('Sem evidencia de gestacao: '+kw)
 oper=bool(re.search(r'calculad|calcular|calculo|quanto|quantas|quantos|converter|conversao',t))
 meses=bool('mes' in t and ('seman' in t or 'dia' in t))
 sub='Equivalência de semanas e meses gestacionais' if meses else 'Idade gestacional em semanas e dias'
 return dict(area_principal='Saúde',cluster='Saúde reprodutiva e gestação',subcluster=sub,
             intencao_principal=('Calcular/interpretar idade gestacional (não diagnóstica)' if oper else 'Consultar tempo de gestação (não diagnóstica)'),
             tipo_intencao=('cálculo contextual' if oper else 'informacional'),
             confianca='média',revisao_manual='sim',
             justificativa_curta='P3 v1.2: gestação explícita no termo. Escopo Saúde; semanas/dias e meses gestacionais requerem convenção explicitada. Não é diagnóstico nem conversão de calendário por fator fixo.')

def decidir_navegacional(r):
 return dict(area_principal='Finanças',cluster='Crédito',subcluster='Simuladores bancários por instituição',
             intencao_principal='Localizar simulador de crédito de instituição específica',tipo_intencao='navegacional/transacional',
             confianca='média',revisao_manual='sim',
             justificativa_curta='P3 v1.2: nome da instituição e termo SIMULADOR explícitos; busca prioritariamente por ferramenta específica. Possível interesse também em simulação, sujeito a revisão editorial.')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--fonte',type=Path,required=True);ap.add_argument('--destino',type=Path,required=True);a=ap.parse_args()
 fonte=a.fonte; out=a.destino;out.mkdir(parents=True,exist_ok=True)
 ent=fonte/'08-Entregas/P3-v1.1'
 qa=ler_csv_bytes((ent/'p3-v1.1-reavaliacao-1207.csv').read_bytes())
 ids_health={r['id_global'] for r in qa if r['veredito_qa_automatica']=='SUSPENDER_ESCOPO'}
 amostra=ler_csv_bytes((ent/'p3-v1.1-qa-amostra-210.csv').read_bytes())
 ids_extra={r['id_global'] for r in amostra if r['veredito_QA']=='INVESTIGAR_ESCOPO_SAUDE'}
 ids_health |= ids_extra
 ids_nav={r['id_global']:r for r in qa if r['veredito_qa_automatica']=='CONFIRMAR_COM_ALERTA_NAVEGACIONAL'}
 assert len(ids_health)==187 and len(ids_nav)==43 and len(ids_extra)==3,(len(ids_health),len(ids_nav),len(ids_extra))
 nova_zip=out/'lotes-001-a-030-p3-v1.2.zip'
 old_zip=ent/'lotes-001-a-030-p3-v1.1.zip'
 patches=[]; qa_nav=[];qa_health=[]; por_lote=[];index_updates={};base_count=ctrl_count=0
 all_health=set();all_nav=set(); p_protegidos=[]
 with zipfile.ZipFile(old_zip) as zin,zipfile.ZipFile(nova_zip,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zout:
  names=zin.namelist();assert len(names)==30
  for fn in names:
   olddata=zin.read(fn); rows=ler_csv_bytes(olddata)
   cols=list(rows[0].keys()); protected_before=cifrar_protegidos(rows,cols)
   changed=set();ctrl_before=[];base_before=[]
   for row in rows:
    id_=row['id_global'];is_base=row['tipo_registro']=='base'
    base_count+=is_base;ctrl_count+=not is_base
    if not is_base:ctrl_before.append(dict(row))
    if id_ not in ids_health and id_ not in ids_nav:continue
    assert is_base, f'ID alvo nao e base: {id_}'
    before=dict(row); kw=row['Keyword'];tf=norma(kw)
    if id_ in ids_health:
     all_health.add(id_)
     after=decidir_saude(row); row.update(after)
     status='SAUDE_INCLUIDA_V12';rule='gestacao_contexto_explicito'
     note='Gestação explicitada na consulta; área Saúde, subárea Saúde reprodutiva. Não diagnosticar nem converter meses por taxa fixa.'
     qa_health.append({'id_global':id_,'lote':row['lote_id'],'Keyword':kw,'area_anterior':before['area_principal'],
                       'classificacao_proposta':'Saúde > Saúde reprodutiva e gestação > '+after['subcluster'],
                       'tipo_intencao':after['tipo_intencao'],'origem_alerta':'P3 v1.1 escopo suspenso' if id_ not in ids_extra else 'amostra 210 falso negativo',
                       'evidencia':'Termo gestação/gravidez explícito','ressalva':'Sem diagnóstico; meses gestacionais apenas por convenção documentada',
                       'status':'APLICADO_V1_2'})
    else:
     all_nav.add(id_)
     has_simulador='simulador' in tf
     if has_simulador:
      after=decidir_navegacional(row);row.update(after)
      status='NAVEGACIONAL_ESPECIFICO';rule='instituicao_mais_simulador'
      note='Instituição citada e simulador explícito: navegação por ferramenta bancária específica, com ressalva.'
     else:
      status='INTENCAO_MISTA_PRESERVADA';rule='instituicao_mais_simular_ou_simulacao'
      note='Expressão simular/simulação com instituição: pode pedir cálculo ou acesso à ferramenta. Sem mudança automática.'
     inst='Itaú' if 'itau' in tf else 'Santander' if 'santander' in tf else 'Caixa' if 'caixa' in tf else 'Banco do Brasil' if 'banco do brasil' in tf else 'Nubank' if 'nubank' in tf else 'Não identificada'
     qa_nav.append({'id_global':id_,'lote':row['lote_id'],'familia_id':row['familia_id'],'Keyword':kw,'instituicao':inst,
                    'evidencia':'Simulador + instituição explícita' if has_simulador else 'Simular/simulação + instituição (sentido misto)',
                    'status_qa':status,'area_anterior':before['area_principal'],'intencao_anterior':before['tipo_intencao'],
                    'intencao_final':row['tipo_intencao'],'acao':'ALTERAR' if has_simulador else 'MANTER',
                    'justificativa':note})
    changed_fields=[key for key in cols if row[key]!=before[key]]
    if changed_fields:
     assert set(changed_fields)<=CAMPOS_ANALITICOS,(id_,changed_fields)
     changed.add(id_)
     patches.append({'id_global':id_,'lote':row['lote_id'],'Keyword':kw,'categoria':rule,'campos_alterados':','.join(changed_fields),
                     'antes_json':json.dumps({k:before[k] for k in changed_fields},ensure_ascii=False),
                     'depois_json':json.dumps({k:row[k] for k in changed_fields},ensure_ascii=False)})
    index_updates[id_]=(status,rule,note,dict(row),bool(changed_fields))
   assert cifrar_protegidos(rows,cols)==protected_before,fn
   assert all(x['tipo_registro']!='base' for x in ctrl_before)
   zout.writestr(fn.replace('v1.1.csv','v1.2.csv'),csv_bytes(rows,cols))
   por_lote.append({'lote':fn.split('/')[-1].split('-')[1],'registros':len(rows),'controles':len(ctrl_before),
      'IDs alterados':len(changed),'campos_protegidos_sha256':protected_before,'resultado':'PASSOU'})
 assert len(all_health)==187 and len(all_nav)==43,(len(all_health),len(all_nav))
 assert len(patches)==214, (len(patches),Counter(p['categoria'] for p in patches))
 assert len(qa_nav)==43 and sum(x['acao']=='MANTER' for x in qa_nav)==16
 assert base_count==294905 and ctrl_count==2190,(base_count,ctrl_count)
 # Verificacao REAL de arquivo reaberto, todas as linhas e colunas, somente alvos permitidos.
 with zipfile.ZipFile(old_zip) as zin,zipfile.ZipFile(nova_zip) as zout:
  for old_fn,new_fn in zip(zin.namelist(),zout.namelist()):
   oldrows=ler_csv_bytes(zin.read(old_fn));newrows=ler_csv_bytes(zout.read(new_fn)); assert len(oldrows)==len(newrows)
   for oldrow,newrow in zip(oldrows,newrows):
    assert oldrow['id_global']==newrow['id_global'] and oldrow['Keyword']==newrow['Keyword']
    diffs={k for k in oldrow if oldrow[k]!=newrow[k]}
    assert diffs<=CAMPOS_ANALITICOS
    assert not diffs or newrow['id_global'] in index_updates
    if oldrow['tipo_registro']!='base': assert oldrow==newrow
 # Fila original com 85 colunas intactas; 8 novos campos de rastreamento.
 for name in ('fila-geral-p0-p1-p2-p3-v1.1.csv','p3-v1.1-fila-23965.csv'):
  rows=ler_csv_bytes((ent/name).read_bytes());cols=list(rows[0]); assert not (set(cols)&set(FIELDS_NEW))
  for row in rows:
   u=index_updates.get(row['id_global']); vals=['','','','','','','','']
   if u:
    status,rule,note,rr,didchange=u
    vals=[status,rule,note,rr['area_principal'],rr['cluster'],rr['subcluster'],rr['tipo_intencao'],'sim' if didchange else 'não']
   row.update(zip(FIELDS_NEW,vals))
  salvar_csv(out/name.replace('v1.1','v1.2'),rows,cols+FIELDS_NEW)
 qa_nav.sort(key=lambda x:int(x['id_global']));qa_health.sort(key=lambda x:int(x['id_global']))
 for file,rr in [('auditoria-43-simuladores.csv',qa_nav),('auditoria-saude-187.csv',qa_health),('patches-214-p3-v1.2.csv',patches),('regressao-30-lotes-p3-v1.2.csv',por_lote)]:
  salvar_csv(out/file,rr,list(rr[0]))
 resumo={'versao':'P3 v1.2','total_saude':len(all_health),'saude_suspensos_anteriores':184,'saude_falsos_negativos_amostra':3,'alertas_bancarios_auditados':43,
  'navegacionais_aplicados':27,'intencao_mista_preservada':16,'ids_alterados':len(patches),'registros_base':base_count,'controles':ctrl_count,
  'lotes_testados':len(por_lote),'p3_fora_piloto':21875,'p2_pendencias_remanescentes':4660,
  'nota':'Taxonomia Saúde v1.2 proposta técnica controlada; rótulos introduzidos em versão paralela sem edição da v1.1. Decisões automatizadas ainda requerem validação editorial por amostra.'}
 (out/'resumo-p3-v1.2.json').write_text(json.dumps(resumo,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(resumo,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
