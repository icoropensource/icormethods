# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

class PGGenerator(object):
   def __init__(self,aclass):
      self.aclass=aclass
   def GenerateCreate(self):
      bclass=self.aclass
      lfields=[]
      atablename=bclass.NameOfClass
      print 'CREATE TABLE icor.%s ('%atablename
      print '  oid integer DEFAULT 0,'
      for afield in bclass.FieldsIterator():
         lfields.append([afield.FieldPosition,afield])
      lfields.sort()
      for aposid,afield in lfields:
         afieldname=afield.Name
         if afieldname[:1]=='a':
            afieldname=afieldname[1:]
      print '  CONSTRAINT %s_pkey PRIMARY KEY (oid)) WITH (OIDS=FALSE);'%atablename
      print 'ALTER TABLE icor.%s OWNER TO postgres;'%atablename

   def GenerateSelect(self):
      bclass=self.aclass
      lfields=[]
      for afield in bclass.FieldsIterator():
         lfields.append([afield.FieldPosition,afield.Name,afield])
      lfields.sort()
      lcolumns,ljoins=[],[]
      mainfield,mainfieldid='',-1
      for aposid,afieldname,afield in lfields:
         if afieldname[:1]=='a':
            afieldname=afieldname[1:]
         if not lcolumns:
            lcolumns.append('t%s.o as oid'%(afieldname,))
            mainfield=afieldname
            mainfieldid=afield.FOID
         else:
            ljoins.append('left join data_main2.f%d t%s on t%s.o=t%s.o'%(afield.FOID,afieldname,mainfield,afieldname))
         lcolumns.append('t%s.v as %s'%(afieldname,afieldname))
      asqlfields=','.join(lcolumns)
      asqljoins='\n'.join(ljoins)
      asql='''
select %s
from data_main2.f%d t%s
%s
order by t%s.v;
'''%(asqlfields,mainfieldid,mainfield,asqljoins,mainfield)
      for s in asql.split('\n'):
         print s
   def GenerateSelectJSONB(self,aoidinclude=0,lfieldsallowed=None,aprint=0,aoid=-1):
      if lfieldsallowed is None:
         lfieldsallowed=[]
      swhere=''
      if aoid>=0:
         swhere=' where o=%d '%aoid
      bclass=self.aclass
      lfields=[]
      for afield in bclass.FieldsIterator():
         if lfieldsallowed and not afield.Name in lfieldsallowed:
            continue
         lfields.append([afield.FieldPosition,afield.Name,afield])
      lfields.sort()
      lcolumns=[]
      for aposid,afieldname,afield in lfields:
         if afieldname[:1]=='a':
            afieldname=afieldname[1:]
         lcolumns.append("  union all select o,to_jsonb(v) as v,'%s' as n from data_main2.f%d%s"%(afieldname,afield.FOID,swhere))
      scolumns='\n'.join(lcolumns)
      soid=''
      if aoidinclude:
         soid='o,'
      asql='''
with qdata as ( 
  select o,to_jsonb(o) as v,'oid' as n from data_main2.c%d%s
%s
)
select %sjsonb_object_agg(qdata.n,qdata.v) from qdata group by o order by o;
'''%(bclass.CID,swhere,scolumns,soid)
      if aprint:
         for s in asql.split('\n'):
            print s
      return asql

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   return
