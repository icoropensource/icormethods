# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import string

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aobj=aclass.GetFirstObject()
   while aobj:
      print aobj.Name
      aobj.Next()

   return
   aobj=aclass.GetFirstObject()
   while aobj:
      s1=aobj.Name
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
      print '  <OBJECT oid="%d" fieldname="Name" fieldvalue="%s" class="CLASSES_Library_NetBase_WWW_Dictionary_Named_MenuAction" var="MENUACTION_%s_OID" />'%(aobj.OID,s1,s2)
      aobj.Next()
   return
             


