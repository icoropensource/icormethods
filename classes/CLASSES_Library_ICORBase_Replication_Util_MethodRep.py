# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil
import string
from CLASSES_Library_ICORBase_Interface_ICORTextFile import TextFile
import time
#from CLASSES_Library_ICORBase_Replication_Send_GenerateReplication import SendReplicationByFTP
###
output_dir='c:/icor/tmp/'

ufields = [
#   ['CLASSES_Library_Dictionary_Named_ReplicationClassPath','IsClassRecursive',mt_Boolean],
#   ['CLASSES_Library_Dictionary_Named_ReplicationClassPath','IsFieldRecursive',mt_Boolean]
]

umethods = [
   ['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Rozdzial','WWWChapterEdit'],   #(2004, 11, 9, 12, 51, 47, 0)
   ['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Rozdzial','WWWChapterGenerate'],   #(2004, 11, 9, 13, 18, 15, 0)
   ['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Rozdzial','WWWChapterNew'],   #(2004, 11, 9, 12, 51, 37, 0)
   ['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Struktura','Main'],   #(2004, 11, 9, 16, 9, 59, 0)
   ['CLASSES_Library_NetBase_WWW_Server','DoMenuWorkflowRecur'],   #(2004, 11, 9, 13, 23, 49, 0)
]

def FileExists(afpath):
   try:
      f=open(afpath,'rb')
   except:
      return 0
   f.close()
   return 1

def UpdateMethodText(acpath,amname,fname,atext=''):
   fpath=FilePathAsSystemPath(output_dir+fname)
   aclass=aICORDBEngine.Classes[acpath]
   mclass=aICORDBEngine.Classes['CLASSES_System_ICORMethod']
   if aclass is None or mclass is None:
      print 'B��D! Klasa ',acpath,' nie istnieje!'
      return
   moid=mclass.aIDClassMethod.Identifiers(str(aclass.CID)+'_'+amname)
   if moid<0:
      print 'B��D! Metoda ',amname,' nie istnieje!'
      return
   amethod=aclass.MethodsByName(amname)
   if amethod is None:
      print 'B��D! Metoda ',amname,' nie istnieje!'
      return
   if atext=='':
      if not FileExists(fpath):
         print 'B��D! Plik ',fpath,' nie istnieje!'
         return
      try:
         file=TextFile(fpath,'r')
      except RuntimeError,e:
         if e.args[0]=='Not a gzipped file':
            file=open(fpath,'rt')
      try:
         atext=''
         aline=file.readline()
         while aline:
            atext=atext+aline
            aline=file.readline()
      finally:
         file.close()
   mclass.aMethodText[moid]=atext
   mclass.aLastModified.SetValuesAsDateTime(moid,CLASSES_Library_ICORBase_Interface_ICORUtil.tdatetime())

def ExportMethods(agzipped=1):
   for acname,amname in umethods:
      print 'metoda:',amname
      aclass=aICORDBEngine.Classes[acname]
      if aclass is None:
         print 'B��D! Klasa ',acname,' nie istnieje!'
         continue
      m1=aclass.MethodsByName(amname)
      if m1 is None:
         print 'B��D! Metoda ',amname,' nie istnieje!'
         continue
      afile=FilePathAsSystemPath(output_dir+acname+'_'+amname)
      atext=m1.MethodText
      if agzipped:
         afile=afile+'.gz'
      else:
         afile=afile+'.py'
      file=TextFile(afile,'w')
      try:
         file.write(atext)
      finally:
         file.close()

def SaveRep(agzipped=1):
   ExportMethods(agzipped)
   return

def LoadRep():
# aktualizacja pol
   for acname,afname,aftype in ufields:
      print 'pole:',afname
      aclass=aICORDBEngine.Classes[acname]
      f1=aclass.FieldsByName(afname)
      if f1 is None:
         fdef1=ICORFieldDefinition(afname,aftype)
         aclass.AddField(fdef1)

# aktualizacja metod
   for acname,amname in umethods:
      print 'metoda:',amname
      aclass=aICORDBEngine.Classes[acname]
      if aclass is None:
         print 'B��D! Klasa ',acname,' nie istnieje!'
         continue
      m1=aclass.MethodsByName(amname)
      if m1 is None:
         mdef1=ICORMethodDefinition(amname)
         print 'dodaje metode',amname
         aclass.AddMethod(mdef1)
      UpdateMethodText(acname,amname,acname+'_'+amname+'.gz')
   return

def ProcessMajatek(jclass,aclass,jfield):
   aoid=aclass.StanNaDzien.GetFirstValueID()
   d={}
   while aoid>=0:
      aobj=aclass[aoid]
      jobj=aobj.JednostkaOrganizacyjna
      if jobj:
         s=d.get(jobj.OID,'')
         s=s+str(aoid)+':'+str(aclass.CID)+':'
         d[jobj.OID]=s
      aoid=aclass.StanNaDzien.GetNextValueID(aoid)
   for joid in d.keys():
      if jclass.ObjectExists(joid):
         jfield[joid]=d[joid]

def DumpObjects(acpath,afname='Nazwa'):
   aclass=aICORDBEngine.Classes[acpath]
   aobj=aclass.GetFirstObject()
   afield=aobj.Class.FieldsByName(afname)
   i=3
   print '   aclass=aICORDBEngine.Classes["%s"]'%acpath
   print '   afield=aclass.FieldsByName("%s")'%afname
   print '   aobjlist=['
   while aobj:
      print '[%d,"%s"],'%(aobj.OID,afield[aobj.OID]),
      i=i-1
      if not i:
         print
         i=3
      aobj.Next()
   print ']'
   print '   for aoid,aname in aobjlist:'
   print '      aclass.CreateObjectByID(aoid)'
   print '      afield[aoid]=aname'
   print

def UpdateObjects():
   aclass=aICORDBEngine.Classes["CLASSES_DataBase_Miasto_StrukturaRobotWToku"]
   afield=aclass.FieldsByName("Gmina")
   aobjlist=[
[26,"1:1081:"], [27,"1:1081:"], ]
   for aoid,aname in aobjlist:
      aclass.CreateObjectByID(aoid)
      afield[aoid]=aname

   aclass=aICORDBEngine.Classes["CLASSES_DataBase_Miasto_StrukturaRobotWToku"]
   afield=aclass.FieldsByName("Opis")
   aobjlist=[
[26,"Drogi"], [27,"Drogi"], ]
   for aoid,aname in aobjlist:
      aclass.CreateObjectByID(aoid)
      afield[aoid]=aname

   aclass=aICORDBEngine.Classes["CLASSES_DataBase_Miasto_StrukturaRobotWToku"]
   afield=aclass.FieldsByName("PelnaNazwa")
   aobjlist=[
[26,"Inwestycje, Drogi"], [27,"Remonty, Drogi"], ]
   for aoid,aname in aobjlist:
      aclass.CreateObjectByID(aoid)
      afield[aoid]=aname

   aclass=aICORDBEngine.Classes["CLASSES_DataBase_Miasto_StrukturaRobotWToku"]
   afield=aclass.FieldsByName("PodStruktura")
   aobjlist=[
[1,"3:1070:4:1070:5:1070:6:1070:7:1070:8:1070:9:1070:10:1070:11:1070:12:1070:13:1070:26:1070:"], [2,"15:1070:16:1070:17:1070:18:1070:19:1070:20:1070:21:1070:22:1070:23:1070:24:1070:25:1070:27:1070:"],
]
   for aoid,aname in aobjlist:
      aclass.CreateObjectByID(aoid)
      afield[aoid]=aname

   return
   jclass=aICORDBEngine.Classes['CLASSES_DataBase_Miasto_JednostkaOrganizacyjna']
   aclass=aICORDBEngine.Classes['CLASSES_DataBase_Miasto_Slownik_ObrotowyMajatek']
   ProcessMajatek(jclass,aclass,jclass.MajatekObrotowy)
   aclass=aICORDBEngine.Classes['CLASSES_DataBase_Miasto_Slownik_RzeczowyMajatekTrwaly']
   ProcessMajatek(jclass,aclass,jclass.RzeczowyMajatekTrwaly)
   aclass=aICORDBEngine.Classes['CLASSES_DataBase_Miasto_Slownik_PozostalyMajatekTrwaly']
   ProcessMajatek(jclass,aclass,jclass.PozostalyMajatekTrwaly)

def SaveMenuPageHTML(adate):
   mclass=aICORDBEngine.Classes['CLASSES_Library_NetBase_WWW_Dictionary_Menu']
   mfield=mclass.PageHTML
   aoid=mclass.FirstObject()
   recordseparator=chr(0)+chr(1)+chr(0)
   fieldseparator=chr(0)+chr(2)+chr(0)
   file=TextFile('c:/icor/tmp/menufile.gz','w')
   try:
      while aoid>=0:
         lmd=mfield.GetValueLastModified(aoid)
         if lmd>=adate:
            file.write(str(aoid))
            file.write(fieldseparator)
            s=CLASSES_Library_ICORBase_Interface_ICORUtil.tdatetime2str(lmd,'_')
            file.write(s)
            file.write(fieldseparator)
            file.write(mfield[aoid])
            file.write(recordseparator)
         aoid=mclass.NextObject(aoid)
   finally:
      file.close()

def GetMenuPath(aobj,res):
   res.insert(0,aobj.Caption)
   bobj=aobj.ParentMenu
   if bobj:
      GetMenuPath(bobj,res)

def LoadMenuPageHTML():
   mclass=aICORDBEngine.Classes['CLASSES_Library_NetBase_WWW_Dictionary_Menu']
   mfield=mclass.PageHTML
   recordseparator=chr(0)+chr(1)+chr(0)
   fieldseparator=chr(0)+chr(2)+chr(0)
   file=TextFile('c:/icor/tmp/menufile.gz','r')
   try:
      recs=string.split(file.read(),recordseparator)
      for i in range(len(recs)):
         recs[i]=string.split(recs[i],fieldseparator)
      i=1
      for soid,adate,atext in recs[:-1]:
         aoid=int(soid)
         ld=string.split(adate,'_')
         ld=map(int,ld)
         bdate=tuple(ld)
         res=[]
         GetMenuPath(mclass[aoid],res)
         apath=string.join(res,'/')
         alen=len(atext)
         print i,aoid,bdate,alen,apath
         if alen<619000:
            mfield[aoid]=atext
            mfield.SetValueLastModified(aoid,bdate)
         i=i+1
   finally:
      file.close()

#def SendReplication():
#   SendReplicationByFTP('MiastoAll',auserid=0,adatefrom=(-1,1,1),abyftp=0,aprompt=0)

def ZmienUzytkownikow():
   aclass=aICORDBEngine.Classes['CLASSES_System_User']
   aoid=aclass.UserName.Identifiers('SSlodczyk')
   if aoid>=0:
      aclass.UserName[aoid]='AFabisiak'
      aclass.Password[aoid]='AFabisiak'
   aclass=aICORDBEngine.Classes['CLASSES_System_SummaryRule']
   aobj=aclass.GetFirstObject()
   while aobj.Exists():
      if aobj.Value=='S�odczyk':
         aobj.Value='Fabisiak'
      aobj.Next()
   aclass=aICORDBEngine.Classes['CLASSES_System_ICORField']
   aoid=aclass.aFieldNameAsDisplayed.Identifiers('S�awomir S�odczyk')
   if aoid>=0:
      aclass.aFieldNameAsDisplayed[aoid]='Andrzej Fabisiak'

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   ClearStdOut()
#   DumpObjects('CLASSES_DataBase_Miasto_StrukturaRobotWToku','Gmina')

   SaveRep(agzipped=1)
#   LoadRep()
#   UpdateObjects()

#   SaveMenuPageHTML((2000,3,21))
#   LoadMenuPageHTML()
#   SendReplication()
#   ZmienUzytkownikow()
   MessageDialog('Koniec pobierania aktualizacji. Zamknij program i uruchom ponownie aby zako�czy� proces aktualizacji.',mtInformation,mbOK)
#   MessageDialog('Koniec pobierania aktualizacji.',mtInformation,mbOK)
   return
