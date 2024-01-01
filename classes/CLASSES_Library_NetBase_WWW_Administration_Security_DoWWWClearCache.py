# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
#   f=open('c:/icor/tmp/aaa.txt','w')
#   f.write('xxxxxxxxx')
#   f.close()
   aICORDBEngine.Refresh(asystem=1)
   aICORDBEngine.RepositoryChange('Synchronize',-1,-1,'','','')
   return



