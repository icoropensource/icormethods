# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Replication_Receive_ReceiveReplication import ICORXMLReplicationParser

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if OID<0:
      adialog=InputElementDialog('Wybierz klasę',0,0)
      if not adialog.Show():
         return
      bclass=aICORDBEngine.Classes[adialog.ClassPath]
      if bclass is None:
         return
   else:
      bclass=aICORDBEngine.Classes[OID]
   aoid=aclass.FirstObject()
   if aoid<0:
      aoid=aclass.AddObject()
   if not aclass.EditObject(aoid):
      return
   rclass=aICORDBEngine.Classes['CLASSES_Library_ICORBase_Replication_Receive']
   roid=rclass.Name.Identifiers('CLASS_REPLICATION')
   if roid<0:
      print 'Klasa odpowiedzialna za replikację nie posiada wzorca głównego replikacji'
      return
   aobj,robj=aclass[aoid],rclass[roid]
   robj.AllowUpdateProtected=aobj.AllowUpdateProtected
   robj.ImportMethodExecute=aobj.ImportMethodExecute
   robj.InputFile=aobj.InputFile
   robj.OverrideDeleted=aobj.OverrideDeleted
   robj.ReceiveMethods=aobj.ReceiveMethods
   robj.AlwaysUpdateMethod=aobj.AlwaysUpdateMethod
   aparser=ICORXMLReplicationParser(roid)
   aparser.Parse()
   MessageDialog('Zakończono pobieranie replikacji. Zalecane jest ponowne uruchomienie ICOR.')
   return



