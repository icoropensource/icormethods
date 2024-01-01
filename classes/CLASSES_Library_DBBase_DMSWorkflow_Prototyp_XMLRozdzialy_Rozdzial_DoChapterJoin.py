# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import icordbmain.adoutil as ADOLibInit
import icordbmain.dbaccess as dbaccess

import pythoncom

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   if OID<0:
      print 'Nieznany rozdział'
      return 2
   aclass=aICORDBEngine.Classes[CID]
   aobj=aclass[OID]
   print '=============================================================='
   print 'Rozdzial:',aobj.OID,aobj.Naglowek
   sobj=aobj.PodRozdzialy
   if not sobj:
      print '<h1>Rozdział nie posiada podrozdziałów.</h1>'
      return 2
   if not aobj.TabelaZrodlowa:
      print '<h1>Rozdział nie posiada tabeli źródłowej.</h1>'
      return 2
   toid=aobj.TabelaZrodlowa.OID
   while sobj:
      if sobj.PodRozdzialy:
         print '<h1>Podrozdziały nie są puste.</h1>'
         return 2
      if sobj.TabelaZrodlowa.OID!=toid:
         print '<h1>Rozdziały posiadają inną tabelę źródłową.</h1>'
         return 2
      sobj.Next()

   pobj=None
   wobj=None
   bobj=aobj.AsObject()
   while not wobj and bobj:
      wobj=bobj.Struktura
      bobj=bobj.NadRozdzial
   if wobj:
      pobj=wobj.Projekt
   if pobj is None:
      print '<h1>Rozdział jest odłączony od struktury.</h1>'
      return 2

   ainfotablessufix=str(wobj['InfoTablesSufix',mt_Integer])
   abasenamemodifier=pobj.BaseNameModifier

   import win32api
   print win32api.GetUserName()

   try:
      aadoutil=ADOLibInit.ADOUtil(acominitialize=1,dbaccessobj=pobj.DBAccess)
   except Exception,v:
      print 'Exception:',v
      ADOLibInit.handle_com_error(v)
      import traceback
      traceback.print_exc()
      return 2
   try:
      aobj.SGIsTableView='1'
      aobj.SGShowAsTable='1'
      sobj=aobj.PodRozdzialy
      while sobj:
         asql='UPDATE %sBZR_%d SET _ChapterID=%d WHERE (_ChapterID=%d)'%(abasenamemodifier,toid,aobj.OID,sobj.OID)
         print asql
         #file.write(asql+'</br>')
         aadoutil.Execute(asql)
         asql='UPDATE %sBZR_V_%d SET _ChapterID=%d WHERE (_ChapterID=%d)'%(abasenamemodifier,toid,aobj.OID,sobj.OID)
         print asql
         #file.write(asql+'</br>')
         aadoutil.Execute(asql)
         sobj.Next()
      aobj.Class.PodRozdzialy.DeleteReferencedObjects(aobj.OID)
   finally:
      aadoutil.Close()
   return
