# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil

import icordbmain.adoutil as ADOLibInit
import icordbmain.dbaccess as dbaccess

import pythoncom
import string
import sys
import os
import re


def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
#   print 'RefreshChapter:',FieldName,':',OID,':',Value
   pobj,wobj=None,None
   aobj=aclass[OID]
   if Value=='DELETE':
      wclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Struktura']
      if FieldName:
         wobj=wclass[int(FieldName)]
   else:
      wobj=None
      bobj=aobj.AsObject()
      while not wobj and bobj:
         wobj=bobj.Struktura
         bobj=bobj.NadRozdzial
   if wobj:
      pobj=wobj.Projekt
   if pobj is None:
      return
   tobj=aobj.TabelaZrodlowa
   if tobj:                
      aTableID=tobj.OID
      aTableName=tobj.Nazwa
   else:
      aTableID=-1
      aTableName=''
   ainfotablessufix=str(wobj['InfoTablesSufix',mt_Integer])
   try:
      aadoutil=ADOLibInit.ADOUtil(acominitialize=1,dbaccessobj=pobj.DBAccess)
   except:
      return
   try:
      if Value=='UPDATE':
         w=0
         try:
            rs=aadoutil.GetRS("select * from %schapters_%s where ChapterID=%d"%(pobj.BaseNameModifier,ainfotablessufix,OID))
            w=1
         except:
            pass
         if w and rs.State!=aadoutil.adoconst.adStateClosed:
            if rs.EOF or rs.BOF:
               rs.AddNew()
            rs.Fields.Item('ChapterID').Value=OID
            rs.Fields.Item('TableID').Value=aTableID
            rs.Fields.Item('TableName').Value=aTableName[:200]
            rs.Fields.Item('ChapterName').Value=aobj.Naglowek[:200]
            aadoutil.UpdateRS(rs)
            rs=aadoutil.CloseRS(rs)
      elif Value=='DELETE':
         aadoutil.Execute("DELETE %schapters_%s where ChapterID=%d"%(pobj.BaseNameModifier,ainfotablessufix,OID))
      elif Value=='IsAutoGenerate':
         w=0
         try:
            rs=aadoutil.GetRS("select * from %schapterstate_%s where ChapterID=%d"%(pobj.BaseNameModifier,ainfotablessufix,OID))
            w=1
         except:
            pass
         if w and rs.State!=aadoutil.adoconst.adStateClosed:
            if rs.EOF or rs.BOF:
               rs.AddNew()
               rs.Fields.Item('ChapterID').Value=OID
            if aobj['IsAutoGenerate']:
               rs.Fields.Item('Status2').Value='G'
            else:
               rs.Fields.Item('Status2').Value=''
            aadoutil.UpdateRS(rs)
            rs=aadoutil.CloseRS(rs)
      elif Value=='DataChange':
         if 0:
            w=0
            try:
               rs=aadoutil.GetRS("select * from %schapterstate_%s where ChapterID=%d"%(pobj.BaseNameModifier,ainfotablessufix,OID))
               w=1
            except:
               pass
            if w and rs.State!=aadoutil.adoconst.adStateClosed:
               if rs.EOF or rs.BOF:
                  rs.AddNew()
                  rs.Fields.Item('ChapterID').Value=OID
               rs.Fields.Item('Status1').Value='N'
               aadoutil.UpdateRS(rs)
               rs=aadoutil.CloseRS(rs)
         rclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Rozdzial']
         rclass.DoSetChapterState(str(wobj.OID),OID,'',UID)
   finally:
      aadoutil.Close()
   return

