# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import string
from CLASSES_Library_ICORBase_Interface_ICORTextFile import TextFile

output_dir='c:/icor/tmp/'

ufields = [
   ['CLASSES_System_SummaryItem','LastCreated',mt_DateTime],
   ['CLASSES_System_ICORMethod','aLanguage',mt_String],
   ['CLASSES_Library_NetBase_WWW_Server','ServerAppPath',mt_String],
   ['CLASSES_Library_NetBase_WWW_Server','ServerOutputPath',mt_String],
   ['CLASSES_Library_NetBase_WWW_Server','ServerAppOutputPath',mt_String]
]

umethods = [
   ['CLASSES_Library_ICORBase_Interface','ICORIterators'],
   ['CLASSES_Library_ICORBase_Interface','ICORUtil'],
   ['CLASSES_Library_ICORBase_Interface','ICORInterface'],
   ['CLASSES_Library_ICORBase_Interface','ICORMDSpace'],
   ['CLASSES_Library_ICORBase_Interface','ICORObjectsViewer'],
   ['CLASSES_Library_ICORBase_Interface','ICORFSM'],
   ['CLASSES_Library_ICORBase_Interface','ICORChart'],
   ['CLASSES_Library_ICORBase_Interface','ICORSearch'],
   ['CLASSES_Library_ICORBase_Interface','ICORSummary'],
   ['CLASSES_Library_ICORBase_Interface','ICORSecurity'],
   ['CLASSES_Library_ICORBase_Interface','DocTest'],
   ['CLASSES_Library_NetBase_Utils','FTPUtil'],
   ['CLASSES_Library_NetBase_Utils','XMLUtil'],
   ['CLASSES_Library_NetBase_Utils','MDSpaceUtil'],
   ['CLASSES_Library_NetBase_Utils','MimeTypes'],
   ['CLASSES_Library_NetBase_Utils','HTMLUtil'],
   ['CLASSES_Library_NetBase_Utils','WWWColors'],
   ['CLASSES_Library_NetBase_Utils','Col2Delphi'],
   ['CLASSES_Library_NetBase_WWW','ICORHTMLReporter'],
   ['CLASSES_Library_NetBase_WWW_Server','IISInterface'],
   ['CLASSES_Library_NetBase_WWW_Server','ApacheInterface'],
   ['CLASSES_Library_NetBase_WWW_Server','ServerUtil'],
   ['CLASSES_Library_NetBase_WWW_Server','DoObjectsView'],
   ['CLASSES_Library_NetBase_WWW_Server','DoContentsView'],
   ['CLASSES_Library_NetBase_WWW_Server','DoObjectEdit'],
   ['CLASSES_Library_NetBase_WWW_Server','DoMenuPageView'],
   ['CLASSES_Library_NetBase_WWW_Server','DoCustomPageByMethodView'],
   ['CLASSES_Library_NetBase_WWW_Server','DoReportSubmit'],
   ['CLASSES_Library_NetBase_WWW_Server','DoSummaryList'],
   ['CLASSES_Library_NetBase_WWW_Server','DoSummaryExecute'],
   ['CLASSES_Library_NetBase_WWW_Server','ICORExists'],
   ['CLASSES_Library_NetBase_WWW_Server','WWWLogin'],
   ['CLASSES_Library_NetBase_WWW_Server','DoSummaryRecur'],
   ['CLASSES_Library_NetBase_WWW_Server','DoSheetGet'],
   ['CLASSES_Library_NetBase_WWW_Server','DoSummaryParameters'],
   ['CLASSES_Library_NetBase_WWW_Server','ICORWWWInterface'],
   ['CLASSES_Library_NetBase_WWW_Dictionary_Menu','MenuUtil'],
   ['CLASSES_Library_NetBase_WWW_Dictionary_Menu','OnObjectDelete'],
   ['CLASSES_Library_NetBase_WWW_Dictionary_Menu','Update1'],
   ['CLASSES_Library_Win32_OLE','ICORExcel'],
   ['CLASSES_Library_Win32_OLE','MDSpaceUtil'],
   ['CLASSES_Library_Geo_GD','DoExport'],
   ['CLASSES_Library_Geo_GD','GDUtil'],
   ['CLASSES_DataBase_ASA_WWW_PageDef','OnSearchPageGet'],
   ['CLASSES_DataBase_ASA_WWW_PageDef','InputUmowa']
]

def FileExists(afpath):
   try:
      f=open(afpath,'rb')
   except:
      return 0
   f.close()
   return 1

def UpdateMethodText(acpath,amname,fname):
   fpath=FilePathAsSystemPath(output_dir+fname)
   aclass=aICORDBEngine.Classes[acpath]
   if aclass is None:
      print 'BŁĄD! Klasa ',acpath,' nie istnieje!'
      return
   amethod=aclass.MethodsByName(amname)
   if amethod is None:
      print 'BŁĄD! Metoda ',amname,' nie istnieje!'
      return
   if not FileExists(fpath):
      print 'BŁĄD! Plik ',fpath,' nie istnieje!'
      return
   file=TextFile(fpath,'r')
   try:
      atext=''
      aline=file.readline()
      while aline:
         atext=atext+aline
         aline=file.readline()
      amethod.MethodText=atext
   finally:
      file.close()

def ExportMethods():
   for acname,amname in umethods:
      print 'metoda:',amname
      aclass=aICORDBEngine.Classes[acname]
      if aclass is None:
         print 'BŁĄD! Klasa ',acname,' nie istnieje!'
         continue
      m1=aclass.MethodsByName(amname)
      if m1 is None:
         print 'BŁĄD! Metoda ',amname,' nie istnieje!'
         continue
      afile=FilePathAsSystemPath(output_dir+amname)
      atext=m1.MethodText
      file=TextFile(afile+'.gz','w')
      try:
         file.write(atext)
      finally:
         file.close()

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   ClearStdOut()
#   ExportMethods()
#   return
   for acname,afname,aftype in ufields:
      print 'pole:',afname
      aclass=aICORDBEngine.Classes[acname]
      f1=aclass.FieldsByName(afname)
      if f1 is None:
         fdef1=ICORFieldDefinition(afname,aftype)
         aclass.AddField(fdef1)
   aclass=aICORDBEngine.Classes['CLASSES_Library_NetBase_WWW_Server']
   aobj=aclass.GetFirstObject()
   aobj.ServerAppPath=r'%ICOR%/wwwroot'
   aobj.ServerOutputPath=r'%ICOR%/html/output'
   aobj.ServerAppOutputPath=r'%ICOR%/wwwroot/output'
   for acname,amname in umethods:
      print 'metoda:',amname
      aclass=aICORDBEngine.Classes[acname]
      if aclass is None:
         print 'BŁĄD! Klasa ',acname,' nie istnieje!'
         continue
      m1=aclass.MethodsByName(amname)
      if m1 is None:
         mdef1=ICORMethodDefinition(amname)
         print 'dodaje metode',amname
         aclass.AddMethod(mdef1)
      UpdateMethodText(acname,amname,amname+'.gz')
   return



