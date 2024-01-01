# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import icordbmain.adoutil as ADOLibInit
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import re
import string
import CLASSES_Library_ICORBase_External_MLog as MLog

def GetNewsletterText(aadoutil,anewsletteroid,aoidref,this=None):
   alogfname=MLog.GetLogTempFileName('newsletterpage')
   alog=MLog.MLog(alogfname,aconsole=0)

   aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_ListyWysylkowe_ListaWysylkowa']
   aobj=aclass[anewsletteroid]
   cobj=aobj.Kategorie
   aCategories={}
   while cobj:
      aCategories[cobj.OID]=cobj.AsObject()
      cobj.Next()
   pobj=aobj.Projekt
   aBaseNameModifier=pobj.BaseNameModifier
   ret=''
   w=0
   try:
      rs=aadoutil.GetRS("select NewsletterOID,OIDRef,TableID,ChapterID,Status,DataWyslania,WyslanyPrzez from %sNEWSLETTERITEMS_0 where OIDRef='%s' and NewsletterOID=%d"%(aBaseNameModifier,aoidref,anewsletteroid),aclient=1)
      w=1
   except:
      alog.LogException()
   if w and rs.State!=aadoutil.adoconst.adStateClosed:
      if this is None:
         athis={'IsPreview':1,'ShowAllCategories':1,'AllowSend':1}
      else:
         athis=this
         athis['IsPreview']=0
      achapterid=ADOLibInit.GetRSValueAsStr(rs,'ChapterID',astype=1)
      wobj=None
      cobj=None
      if achapterid>0:
         cclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Rozdzial']
         cobj=cclass[achapterid]
         bobj=cobj.AsObject()
         while not wobj and bobj:
            wobj=bobj.Struktura
            bobj=bobj.NadRozdzial
      atableid=ADOLibInit.GetRSValueAsStr(rs,'TableID')
      rs1=aadoutil.GetRS("select * from %sBZR_%s where _OID='%s'"%(aBaseNameModifier,atableid,aoidref),aclient=1)
      bthis=ICORUtil.DummyParameters(athis)
      arepldict={'aNewsletter':aobj,'aCategories':aCategories,'alog':alog,'this':bthis,'rs':rs1,'aWWWMenuStruct':wobj,'aChapter':cobj,'re':re,'string':string,'ICORUtil':ICORUtil,'ADOLibInit':ADOLibInit,'aadoutil':aadoutil}
      atext=ICORUtil.GetTextAsHTMLText(aobj.SzablonListu,repldict=arepldict,aengine=aICORDBEngine,aashtmlstring=0,ascriptname='NewsletterText '+str(anewsletteroid)+' '+aoidref)
      ret=ret+atext
      rs1=aadoutil.CloseRS(rs1)
#            aadoutil.UpdateRS(rs)
      rs=aadoutil.CloseRS(rs)
   return ret

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   anewsletteroid=OID
   aoidref=Value
#   print 'Generate preview:',anewsletteroid,aoidref
   ret=''
   aobj=aclass[OID]
   pobj=aobj.Projekt
   try:
      aadoutil=ADOLibInit.ADOUtil(acominitialize=1,dbaccessobj=pobj.DBAccess)
   except:
      return
   try:
      if 1:
         ret=GetNewsletterText(aadoutil,anewsletteroid,aoidref)
      if 0:
         aadoutil.Execute("DELETE %schapters_%s where ChapterID=%d"%(pobj.BaseNameModifier,ainfotablessufix,OID))
   finally:
      aadoutil.Close()
   return ret

