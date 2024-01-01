# -*- coding: windows-1250 -*-
# saved: 2023/03/02 23:32:59

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

OIDS=[[35000,36000],[19000,20000],]

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   global CONTEXT
   # avalue = CONTEXT['_ObjectImportValue']
   for idmin,idmax in OIDS:
      if (OID>=idmin) and (OID<idmax):
         CONTEXT['_AllowObjectImport']=0
         break
   return
