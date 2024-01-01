# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ProcessSecurity(aclass):
   aobj=aclass.GetFirstObject()
   while aobj:
      arefs=aobj.Class.AccessLevelView.GetRefList(aobj.OID)
      dobj=aobj.DBAccess
      while dobj:
         dobj.Class.AccessLevelView.AddRefs(dobj.OID,arefs.refs,ainsertifnotexists=1)
         dobj.Next()
      aobj.Next()

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Projekt']
   ProcessSecurity(aclass)
   aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Struktura']
   ProcessSecurity(aclass)
   return
