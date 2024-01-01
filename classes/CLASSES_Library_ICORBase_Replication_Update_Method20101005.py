# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Replication_Update_UpdateManager as UpdateManager

def ProcessRozdzialy(robj,trefs,mrefs):
   while robj:
      trefs2=robj.Class.PageTemplate.GetRefList(robj.OID)
      mrefs2=robj.Class.MetaTemplate.GetRefList(robj.OID)
      trefs.AddRefs(trefs2)
      mrefs.AddRefs(mrefs2)
      robj2=robj.PodRozdzialy
      if robj2:
         ProcessRozdzialy(robj2,trefs,mrefs)
      robj.Next()

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aupdate='2010_10_05 NewsletterAcceptTemplate'
   if not UpdateManager.CheckUpdate(aupdate):
      return

   aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_ListyWysylkowe_ListaWysylkowa']
   sobj=aclass.GetFirstObject()
   while sobj:
      sobj.SzablonPotwierdzenia='''<p><%=aNewsletter.KrotkiOpis%></p>
<p>Aby potwierdzić chęć otrzymywania informacji z listy wysyłkowej należy wybrać <a href="<%=aHRefAccept%>">ten adres</a></p>
<p>Aby zakończyć odbieranie informacji z listy wysyłkowej należy wybrać <a href="<%=aHRefDecline%>">ten adres</a></p>
<p><%=aNewsletter.DlugiOpis%></p>
'''
      sobj.Next()
   return

