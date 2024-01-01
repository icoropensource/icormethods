# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import CLASSES_Library_ICORBase_Interface_ICORSecurity as ICORSecurity
import icordbmain.adoutil as ADOLibInit
import string
import icordbmain.dbaccess as dbaccess

def PrepareResultJSONFile(file,aaction,atext):
   file.write('{status:"%s",info:"%s"}'%(aaction,atext))

def DoMenuWorkflowAttachmentMoveDrag(file,coid1,coid2,atype,arel1,arel2,att,UID):
   rclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Rozdzial']

   if coid1==coid2:
      PrepareResultJSONFile(file,'BAD','Rozdzia�y musz� si� r�ni�.')
      return
   if not rclass.ObjectExists(coid1):
      PrepareResultJSONFile(file,'BAD','B��dny OID rozdzia�u �r�d�owego.')
      return
   if not rclass.ObjectExists(coid2):
      PrepareResultJSONFile(file,'BAD','B��dny OID rozdzia�u docelowego.')
      return
   if not att:
      PrepareResultJSONFile(file,'BAD','B��dny identyfikator za��cznika.')
      return

   aobj=rclass[coid1]
   robj=rclass[coid2]

   if not ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelEdit'):
      PrepareResultJSONFile(file,'BAD','Brak uprawnie� do rozdzia�u �r�d�owego.')
      return

   if not ICORSecurity.CheckRecursiveAccessLevelForUser(robj,'AccessLevelEdit'):
      PrepareResultJSONFile(file,'BAD','Brak uprawnie� do rozdzia�u docelowego.')
      return

   tobj=robj.TabelaZrodlowa
   if not tobj:
      PrepareResultJSONFile(file,'BAD','Rozdzia� docelowy nie ma przypisanej tabeli.')
      return

   aistableview=robj.Class.SGIsTableView.ValuesAsInt(robj.OID)
   if aistableview:
      PrepareResultJSONFile(file,'BAD','Rozdzia� docelowy jest rozdzia�em tabelarycznym.')
      return

   abasenamemodifier=tobj.Projekt.BaseNameModifier
   try:
      aado=ADOLibInit.ADOUtil(acnt=1,acominitialize=1,dbaccessobj=tobj.Projekt.DBAccess)
   except Exception,v:
      PrepareResultJSONFile(file,'BAD','Brak dost�pu do bazy danych.')
      print 'Exception:',v
      ADOLibInit.handle_com_error(v)
      import traceback
      traceback.print_exc()
      return
   try:
      try:
         anewitemoid=''
         areftable='%sBZR_%d'%(abasenamemodifier,tobj.OID,)
         rs=aado.SQL2RS("select _oid from %s where _chapterid=%d order by _datetime desc "%(areftable,coid2))
         try:
            if not rs.EOF and not rs.BOF:
               anewitemoid=ADOLibInit.GetRSValueAsStr(rs,'_oid',astype=1)
         finally:
            rs=aado.CloseRS(rs)
         if not anewitemoid:
            PrepareResultJSONFile(file,'BAD','Rozdzia� docelowy wymaga wpisu.')
            return
         aado.Execute("update %sFILEUPLOADS_0 set RefTable='%s', RefOID='%s' where _OID='%s'"%(abasenamemodifier,areftable,anewitemoid,att))
      except:
         import traceback
         traceback.print_exc()
         PrepareResultJSONFile(file,'BAD','Wyst�pi� problem z przeniesieniem za��cznika.')
         return
   finally:
      aado.Close()

   rclass.DoRefreshChapterInfo('',coid1,'DataChange')
   rclass.DoRefreshChapterInfo('',coid2,'DataChange')

   PrepareResultJSONFile(file,'OK','Rozdzia� przeniesiony')

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   return
