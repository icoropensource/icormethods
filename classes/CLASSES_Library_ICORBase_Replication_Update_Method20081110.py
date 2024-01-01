# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Replication_Update_UpdateManager as UpdateManager
import string

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aupdate='2008_11_10 EffectURLs'
   if not UpdateManager.CheckUpdate(aupdate):
      return
   #***************************************************************************
   aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Component_Effects']
   aobj=aclass.GetFirstObject()
   while aobj:
      atext=aobj.URLDocumentation+'\n'+aobj.URLExamples+'\n'+aobj.URLHomePage
      atext=string.replace(atext,'\n\n','\n')
      atext=string.replace(atext,'\n\n','\n')
      aobj.URLDocumentation=atext
      aobj.Next()

   lfields=['URLExamples','URLHomePage',]
   for afieldname in lfields:
      afield=aclass.FieldsByName(afieldname)
      afield.IsAliased='0'
      afield.IsInteractive='0'
      afield.WWWDefaultInput='0'
   return

