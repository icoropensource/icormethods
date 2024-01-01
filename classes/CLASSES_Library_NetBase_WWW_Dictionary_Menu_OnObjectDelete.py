# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
 
def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aclass.SubMenu.DeleteReferencedObjects(OID)
   aclass.Report.DeleteReferencedObjects(OID)
   aclass.Summaries.DeleteReferencedObjects(OID)
   aclass.PageHTMLItems.DeleteReferencedObjects(OID)
   sclass=aICORDBEngine.Classes['CLASSES_Library_NetBase_WWW_Server']
   soid=sclass.Name.Identifiers('Default')
   if soid>=0:
      sclass.Menu.DeleteRefs(soid,[OID,aclass.CID])
      sclass.Introduction.DeleteRefs(soid,[OID,aclass.CID])



