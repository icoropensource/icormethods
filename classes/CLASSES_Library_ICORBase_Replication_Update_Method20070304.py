# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Replication_Update_UpdateManager as UpdateManager

import string

def CleanCSS(atext):
   apos=string.find(atext,'TD.TabelaWartoscPolaMain')
   if apos<0:
      return None
   apos=string.find(atext,'TD.TabelaWartoscPolaMain0')
   if apos>=0:
      return ''
   bpos=string.find(atext,'}',apos)
   if bpos<0:
      return ''
   s1=atext[apos:bpos+1]
   s2=string.replace(s1,'TD.TabelaWartoscPolaMain','TD.TabelaWartoscPolaMain0')
   atext=atext+'\n'+s2+'\n'
   s2=string.replace(s1,'TD.TabelaWartoscPolaMain','TD.TabelaWartoscPolaMain1')
   atext=atext+'\n'+s2+'\n'
   return atext

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aupdate='PageCSS_2007_03_04'
   if not UpdateManager.CheckUpdate(aupdate):
      return
   #***************************************************************************
   aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_PageCSS']
   aobj=aclass.GetFirstObject()
   while aobj:
      atext=CleanCSS(aobj.CSSSystem)
      if atext is None
         print 'bad CSS:',aobj.OID,aobj.CSSName
      elif not atext:
         pass
      else:
         aobj.CSSSystem=atext
      aobj.Next()
   return

