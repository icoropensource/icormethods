# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:13:04

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_ICORBase_External_MLog as MLog
import CLASSES_Library_NetBase_Utils_ImageUtil as ImageUtil
import CLASSES_Library_ICORBase_Interface_ICORSync as ICORSync
import icorlib.projekt.mcrmrssinterface as MCRMRSSInterface
import icorlib.projekt.mcrmbasesimple as MCRMBaseSimple

import CLASSES_Library_NetBase_Utils_Slimmer as Slimmer
import string

import icordbmain.adoutil as ADOLibInit
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import pythoncom
#import win32com.client
import string
import os
import shutil
import re
                           
import shutil   
import sys
import smtplib
import types

import icordbmain.dbaccess as dbaccess

import traceback
#import CLASSES_Library_NetBase_Utils_SpeechUtil as SpeechUtil
                  
USER_DICT={}
USER_EMAIL={}                    
TWO32=2L**32

adolib,adoconst,amajor,aminor=ADOLibInit.ADOInitialize()

class DataGenerator:
   def __init__(self,aobj,alog):
      self.Obj=aobj
      self.Log=alog
      self.BaseNameModifier=aobj.BaseNameModifier
      self.ConnectionString=dbaccess.GetConnectionString(aobj.DBAccess)
   def Process(self,atableoid,afname):
      self.Connection=adolib.Connection()
      acnt=3
      while acnt:
         try:
            self.Connection.Open(self.ConnectionString)
            break
         except:
            self.Log.Log('timeout nr %d w dostepie do bazy danych'%acnt)
            acnt=acnt-1
            if not acnt:
               raise
            time.sleep(2)
      self.Connection.CursorLocation=adoconst.adUseClient
      self.Connection.CommandTimeout=0
      try:
         self.ProcessTable(atableoid,afname)
      finally:
         self.Connection.Close()
   def ProcessTable(self,atableoid,afname):
      tclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Dotyczy']
      tobj=tclass[atableoid]
      asql='select * from %sBZR_%d'%(self.BaseNameModifier,atableoid)
      self.fout=XMLUtil.MXMLFile(afname,anopl=1)
      self.fout.Header()
      self.fout.TagOpen('DATA')
      self.fout.TagOpen('TABLE',{'id':str(atableoid)})
      try:
         try:
            rs,status=self.Connection.Execute(asql)
         except Exception,e:
            print str(e)
            print 'Error in SQL Chapter command:',asql
            if self.Log:
               self.Log.LogException('Error in SQL Chapter command: '+asql)
            raise
         try:
            if rs.State!=adoconst.adStateClosed:
               self.Recordset2XML(rs,atableoid)
         except Exception,e:
            print 'Error in XML Chapter command'
            if self.Log:
               self.Log.LogException('Error in XML Chapter command')
            import traceback
            traceback.print_exc()
            raise
      finally:
         self.fout.TagClose()
         self.fout.TagClose()
         self.fout.close()
   def CheckTableTag(self,wtabletag,void=''):
      if not wtabletag:
         self.fout.TagOpen('RECORD',{'oid':void})
         wtabletag=1
      return wtabletag
   def Recordset2XML(self,rs,atableoid,alevel=0,axmlmode=0):
      if type(atableoid)!=type(1):
         atable=atableoid
      else:
         atable=self.BaseNameModifier+'BZR_'+str(atableoid)
      mf=rs.Fields.Count
      while not rs.EOF and not rs.BOF:
         if not alevel:
            self.indexOID=''
         wprocess=0
         wtabletag=0
         void=''
         aisimage=0
         for i in range(mf):
            v=rs.Fields.Item(i).Value
            s=rs.Fields.Item(i).Name
   #         if type(v)==type(u""):
            if s=='_OID':
               wprocess=1
               void=v.encode('cp1250')
            if s=='_timestamp':
               wprocess=0
            if rs.Fields.Item(i).Type in [adoconst.adDate,adoconst.adDBDate,adoconst.adDBTime,adoconst.adDBTimeStamp]: #adDate,adDBDate,adDBTime,adDBTimeStamp
               if wprocess:
                  try:
                     vadt=(v.year,v.month,v.day,v.hour,v.minute,v.second,v.msec)
                     v1=ICORUtil.tdatetime2fmtstr(vadt)
                  except:
                     vadt=ICORUtil.tzerodatetime()
                     v1=''
                  wtabletag=self.CheckTableTag(wtabletag,void)
                  self.fout.TagOpen('VALUE',{'name':s.encode('cp1250')},anl='')
                  self.fout.write('<![CDATA[%s]]>'%XMLUtil.GetAsXMLStringCDataNoPL(v1))
                  self.fout.TagClose(aindent=0)
            elif rs.Fields.Item(i).Type in [adoconst.adCurrency]:
               if wprocess:
                  try:
                     hi,lo=v
                     if lo<0:
                        lo+=TWO32
                     v='%0.2f'%(((long(hi)<<32)+lo)/10000.0,)
                  except:
                     v=''
                  wtabletag=self.CheckTableTag(wtabletag,void)
                  self.fout.TagOpen('VALUE',{'name':s.encode('cp1250')},anl='',avalue=v)
                  self.fout.TagClose(aindent=0)
            elif rs.Fields.Item(i).Type not in [adoconst.adChapter,adoconst.adLongVarChar,]:
               if wprocess:
                  if type(v)==type(0==1):
                     if v:
                        v='1'
                     else:
                        v='0'
                  if not isinstance(v,types.StringTypes):
                     try:
                        v=v.encode('cp1250')
                     except:
   #                     print '*** unknown conversion type for *** :',rs.Fields.Item(i).Type
                        v=str(v).encode('cp1250')
   #               print ' '*alevel,s,'=',v[:60]
                  if string.strip(v):
                     wtabletag=self.CheckTableTag(wtabletag,void)
                     self.fout.TagOpen('VALUE',{'name':s.encode('cp1250')},anl='',avalue=v)
                     self.fout.TagClose(aindent=0)
            elif rs.Fields.Item(i).Type==adoconst.adLongVarChar:
               if wprocess:
                  if s:
                     if not isinstance(v,types.StringTypes):
                        v=v.encode('cp1250') #XMLUtil.GetAsXMLStringNoPL
   #                  print ' '*alevel,s,'=',v[:60]
                     if string.strip(v):
                        wtabletag=self.CheckTableTag(wtabletag,void)
                        self.fout.TagOpen('VALUE',{'name':s.encode('cp1250')},anl='',avalue=v)
                        self.fout.TagClose(aindent=0)
            else:
               print ' '*alevel,s,'field has other type:',rs.Fields.Item(i).Type
         if wtabletag:
            self.fout.TagClose()
         rs.MoveNext()
                                                                                                                                         
def Main(atableoid,apath):
   ret=1
   afname=MLog.GetLogTempFileName('table')
   alog=MLog.MLog(afname,aconsole=0)
   alog.Log('Main - atableoid: '+str(atableoid)+', apath: '+apath)
   poid=-1
   pythoncom.CoInitialize()
   try:
      try:
         dclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Dotyczy']
         dobj=dclass[atableoid]
         alog.Log('Start generate: oid: %s, tableoid: %s'%(str(poid),str(atableoid),))
         aDataGenerator=DataGenerator(dobj.Projekt,alog)
         aDataGenerator.Process(atableoid,apath)
      except:
         alog.LogException()
         ret=0
   finally:
      pythoncom.CoUninitialize()
      alog.Log('Koniec generowania')
   return ret

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
#   print 'icormain: c:',CID,'f:',FieldName,'o:',OID,'v:',Value,'u:',UID
   OID=35000
   Value='d:/icor/sql/ptest1/out.xml'
   Main(OID,Value)
   return

