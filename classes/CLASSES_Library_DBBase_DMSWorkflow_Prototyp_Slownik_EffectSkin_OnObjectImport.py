# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   global CONTEXT
   # avalue = CONTEXT['_ObjectImportValue']
   for idmin,idmax in [[35000,36000],]:
      if (OID>=idmin) and (OID<idmax):
         CONTEXT['_AllowObjectImport']=0
         break
   return
