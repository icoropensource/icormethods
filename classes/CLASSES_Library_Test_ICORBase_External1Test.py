# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   print 'External TEST:',FieldName,OID
   if OID>7:
      print 'External FINISH TEST:',FieldName,OID
      return 'OID: '+str(OID)
   aclass.External1Test('Field',OID+1,'Value',ainternalexecute=1)
   s='%d - %s - %d - %s'%(CID,FieldName,OID,Value)
   return s

