# -*- coding: windows-1250 -*-
# saved: 2021/06/12 15:22:47

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

OIDS=[[100000000,100001000],]

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   global CONTEXT
   # avalue = CONTEXT['_ObjectImportValue']
   for idmin,idmax in OIDS:
      if (OID>=idmin) and (OID<idmax):
         CONTEXT['_AllowObjectImport']=0
         break
   return

