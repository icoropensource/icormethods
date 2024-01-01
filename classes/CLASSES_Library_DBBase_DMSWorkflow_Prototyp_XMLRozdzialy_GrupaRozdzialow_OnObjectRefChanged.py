# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if not aclass.ObjectExists(OID):
      return
   amode,boid,bcid=eval(Value)
#   print 'T1: Ref Changed',aclass.CID,aclass.NameOfClass
#   print 'OID:',OID # obiekt w klasie GrupaRozdzialow
#   print 'Value:',Value,type(Value)
#   print 'Value:',amode,boid,bcid
#   bclass=aICORDBEngine.Classes[int(bcid)]
#   print 'BClass:',bclass.NameOfClass
   rclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Rozdzial']
   sclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Struktura']
   if bcid in [rclass.CID,sclass.CID]:
      if amode==1:
         pass
#         aclass.Rozdzialy.AddRefs(OID,[boid,bcid],ainsertifnotexists=1)
      else:
         aclass.Rozdzialy.DeleteRefs(OID,[boid,bcid])
   return


