# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import string

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aobj=aclass.GetFirstObject()
   l=[]
   while aobj:
      l.append('"%s",'%(aobj.Opis,))
      if 0:
         s1=aobj.Opis
         s2=ICORUtil.strPL2ASCII(s1)
         s2=ICORUtil.strUpperPL(s2)
         s2=string.replace(s2,'-',' ')
         s2=string.replace(s2,'/',' ')
         s2=string.replace(s2,':',' ')
         s2=string.replace(s2,'(',' ')
         s2=string.replace(s2,'.',' ')
         s2=string.replace(s2,'  ',' ')
         s2=string.replace(s2,'  ',' ')
         s2=string.replace(s2,' ','_')
         print '  <OBJECT oid="%d" fieldname="Opis" fieldvalue="%s" class="CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_TypPolaDotyczy" var="TYP_%s_OID" />'%(aobj.OID,s1,s2)
      aobj.Next()
   l.sort()
   for s in l:
      print s
   return



