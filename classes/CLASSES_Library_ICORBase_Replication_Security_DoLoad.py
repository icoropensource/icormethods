# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from icorupgrade.securityload import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   SecurityLoad('c:/icor/tmp/save.xml')
   return

