# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import string

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aICORDBEngine.CacheClear()
   aclass=aICORDBEngine.Classes[CID]
   aobj=aclass.GetFirstObject()
   while aobj:
      if aobj.Nazwa in ['_ChapterID','_OIDDictRef','Informacja data wytworzenia','Informacja opis czynności','Informacja osoba odpowiedzialna','Informacja podmiot udostępniający']:
         aobj.Grupa='Sygnatura'
      aobj.Next()
   
   return
   aobj=aclass.GetFirstObject()
   while aobj:
      s1=aobj.Opis
      s2=ICORUtil.strPL2ASCII(s1)
      s2=ICORUtil.strUpperPL(s2)
      s2=string.replace(s2,' ','_')
      print '  <OBJECT fieldname="Nazwa" fieldvalue="%s" class="CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_TypPolaDotyczy" var="%s_OID">'%(s1,s2)
      aobj.Next()
   return



