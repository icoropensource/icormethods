# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   if Value==0:
#      print aICORDBEngine.Variables._LinkCID,aICORDBEngine.Classes.MetaClass.CID
      if aICORDBEngine.Variables._LinkCID!=str(aICORDBEngine.Classes.MetaClass.CID):
#         print '  ret'
         return
      aclass=aICORDBEngine.Classes[CID]
#      print 'delete sheet:',OID,aclass.Name[OID]
      aclass.DeleteObject(OID)
   return

