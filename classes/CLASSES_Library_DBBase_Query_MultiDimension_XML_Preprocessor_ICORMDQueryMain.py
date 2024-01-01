# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import aICORWWWServerInterface
from CLASSES_Library_DBBase_Query_MultiDimension_XML_Preprocessor_ICORMultiDimensionQuery import *
from CLASSES_Library_DBBase_Query_MultiDimension_Main_Iterators import StringRangeIterator
from CLASSES_Library_DBBase_Util_CSVImport import CSVImport
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
from CLASSES_Library_ICORBase_External_MLog import *
import cStringIO
import random
import string
import math
import time
import os
import re
import gc

VERBOSE=1
LOG_FILE=FilePathAsSystemPath(r'%ICOR%\log\log_query2.txt')

class ICORMultidimensionalQueryGroup:
   def __init__(self,adbpath):
      self.FileName=string.replace(FilePathAsSystemPath(adbpath),'\\','/')
      self.DataExists=os.path.exists(self.FileName)
      if not self.DataExists:
         Log('xx The data file does not exists: >%s<\n'%self.FileName)
      self.SRIterator=StringRangeIterator()
      self.Queries=[]
   def __len__(self):
      return len(self.Queries)
   def AppendQuery(self,qobj):
      if not self.DataExists:
         return
#      if not qobj.Class.IsProcessing.ValuesAsInt(qobj.OID):
#         return
#      if string.lower(qobj.Name)=='koszty' or not (string.lower(qobj.Caption)=='katowice' or qobj.Caption==''):
#         print 'skip "%s" "%s"'%(qobj.Name,qobj.Caption,)
#      if len(self.Queries)>2 or not string.find(string.lower(qobj.Name),'koszty')>=0:
#         return
      Log('append query: %s - %s'%(qobj.Name,qobj.Caption,))
      aquery=ICORMultiDimensionQuery(qobj.OID,self.SRIterator)
      self.Queries.append(aquery)
      sobj=qobj.SubQuery
      while sobj:
         self.AppendQuery(sobj)
         sobj.Next()
   def Process(self):
      if not self.DataExists:
         return
      self.SRIterator.Join()
      gmindate=ICORUtil.ZERO_DATE_D_MAX
      gmaxdate=ICORUtil.ZERO_DATE_D
      for afrom,ato,afilters in self.SRIterator.Result:
         mindate=ICORUtil.ZERO_DATE_D_MAX
         maxdate=ICORUtil.ZERO_DATE_D
         for afilter in afilters:
            afilter.InitDane()
            if afilter.DateTo>gmaxdate:
               gmaxdate=afilter.DateTo
            if afilter.DateFrom<gmindate:
               gmindate=afilter.DateFrom
      Log('Start processing, path:'+self.FileName)
      tstart=time.time()
      ret,n=self.Calculate(self.SRIterator.Result,gmindate,gmaxdate)
      tfinish=time.time()
      Log('Process time: %s'%str(tfinish-tstart))
      if ret:
         Log('  ERROR %d - %s'%(ret,n))
      else:
         tstart=time.time()
         for aquery in self.Queries:
            aquery.PostProcess(gmindate,gmaxdate)
         tfinish=time.time()
         Log('PostProcess time: %s'%str(tfinish-tstart))
   def Calculate(self,aplist,gmindate,gmaxdate):
      acsv=CSVImport()
      acsv.Open(self.FileName)
      while not acsv.EOF and aplist:
         akonto=acsv['Konto']
         adata=acsv['Data']
         adata=ICORUtil.getStrAsDate(adata)
         acnt=0
         for afrom,ato,afilters in aplist:
            if akonto>=afrom and akonto<ato:
               for afilter in afilters:
                  if afilter.CheckFK(akonto,adata):
                     v=float(acsv['BOWn'])
                     if v!=0.0:
                        afilter.AcceptBOWn(v,adata)
                     v=float(acsv['Wn'])
                     if v!=0.0:
                        afilter.AcceptWn(v,adata)
                     v=float(acsv['BOMa'])
                     if v!=0.0:
                        afilter.AcceptBOMa(v,adata)
                     v=float(acsv['Ma'])
                     if v!=0.0:
                        afilter.AcceptMa(v,adata)
            acnt=acnt+1
            if akonto<afrom:
               break
         i=0
         while i<len(aplist) and akonto>aplist[i][1]:
            i=i+1
         if i:
            aplist=aplist[i:]
         acsv.Next()
      return 0,''
   def Save(self):
      for aquery in self.Queries:
         if len(aquery.Dimensions)<1:
            continue
         file=cStringIO.StringIO()
         try:
            aquery.DumpFileExcel(file)
            aquery.ClassItem.SourceData[aquery.OID]=file.getvalue()
         finally:
            file.close()

class ICORMultidimensionalQueries:
   def __init__(self,aoid):
      self.ClassItem=aICORDBEngine.Classes['CLASSES_Library_DBBase_Query_MultiDimension_XML_Preprocessor']
      self.OID=aoid
      self.QueryClass=self.ClassItem.Queries.ClassOfType
#      self.QueryClass.SourceData.ClearAllValues()
#      self.QueryClass.LastGenerated.ClearAllValues()
#      self.QueryClass.OutputFileSize.ClearAllValues()
   def Process(self):
      start=time.time()
      aobj=self.ClassItem[self.OID]
      qobj=aobj.Queries
      while qobj:
         qgroup=ICORMultidimensionalQueryGroup(qobj.DBPath)
         qgroup.AppendQuery(qobj)
         qgroup.Process()
         qgroup.Save()
         del qgroup
         gc.collect()
         qobj.Next()
      finish=time.time()
      self.ClassItem.LastGenerated[self.OID]=ICORUtil.tdatetime()
      self.ClassItem.GenerationTime[self.OID]=int(finish-start)
   def Dump(self):
      Log('Query dump:')
      for qdbpath in self.QueryGroups.keys():
         qgroup=self.QueryGroups[qdbpath]
         Log(qgroup.Path+' : '+str(len(qgroup)))

def Main(aoid):
   Log('\n*** Poczatek generowania wszystkich zestawien\n')
   start=time.time()
   try:
      Log('\n*** Inicjacja zestawien\n')
      aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_Query_MultiDimension_Main']
      afield=aclass.FieldsByName('SourceData')
      afield.ClearAllValues()
      if 1:
         aICORMDQueries=ICORMultidimensionalQueries(aoid)
         Log('\n*** Tworzenie zestawien\n')
         aICORMDQueries.Process()
   finally:
      finish=time.time()
      Log('*** koniec generowania wszystkich zestawień, czas: %s\n'%(str(finish-start),))

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   if OID<0:
      OID=2
   Main(OID)


