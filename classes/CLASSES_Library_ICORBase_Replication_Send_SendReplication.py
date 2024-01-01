# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import ICORRepositoryIterator
from CLASSES_Library_NetBase_Utils_XMLUtil import *
from CLASSES_Library_ICORBase_Interface_ICORTextFile import TextFile
import gzip
import string,time

# FTP replication
from CLASSES_Library_NetBase_Utils_FTPUtil import *
from ftplib import FTP
import os

ReplicationException = 'ReplicationException'

class ICORSendReplicationClassIterator(ICORRepositoryIterator):
   def __init__(self,aprofile,atargetuser=-1,acallbackobjectfunc=None):
      ICORRepositoryIterator.__init__(self)
      self.CustomTargetUser=atargetuser
      self.CallbackObjectFunc=acallbackobjectfunc
      self.ProfileClass=aICORDBEngine.Classes['CLASSES/Library/ICORBase/Replication/Send']
      if self.ProfileClass is None:
         raise ReplicationException,'Profile class does not exists'
      if type(aprofile)==type(1):
         self.OID=aprofile
      else:
         self.OID=self.ProfileClass.Name.Identifiers(aprofile)
      if self.OID<0:
         raise ReplicationException,'Profile does not exists'
      self.InitByProfile()
   def InitByProfile(self):
      self.afile=self.ProfileClass.OutputFile[self.OID]
      self.adate=self.ProfileClass.DateFrom.ValuesAsDateTime(self.OID)
      self.adatecreated=self.ProfileClass.DateCreated.ValuesAsDateTime(self.OID)
      if self.adatecreated==ZERO_DATE:
         self.adatecreated=tdatetime()
      arefs=self.ProfileClass.TargetUser.GetRefList(self.OID)
      if arefs.position>=0:
         self.targetuser=arefs.OID
      else:
         self.targetuser=-1
      if self.CustomTargetUser>=0:
         self.targetuser=self.CustomTargetUser
      self.allowsystem=self.ProfileClass.AllowSystem.ValuesAsInt(self.OID)
      self.disableclassmethods=self.ProfileClass.DisableClassMethods.ValuesAsInt(self.OID)
      self.disablefieldmethods=self.ProfileClass.DisableFieldMethods.ValuesAsInt(self.OID)
      self.disableobjectmethods=self.ProfileClass.DisableObjectMethods.ValuesAsInt(self.OID)
      self.isfieldrecursive=self.ProfileClass.IsFieldRecursive.ValuesAsInt(self.OID)
      self.file=None
   def Generate(self,fname=''):
      if fname!='':
         self.afile=fname
      if self.afile=='':
         raise ReplicationException,'No file'
      self.afile=FilePathAsSystemPath(self.afile)
      if self.afile[-3:]!='.gz':
         self.afile=self.afile+'.gz'
      bobj=self.ProfileClass[self.OID]
      cobj=bobj.BaseClasses
      while cobj:
         self.bpath=cobj.Name
         self.bclass=aICORDBEngine.Classes[self.bpath]
         if not self.bclass is None:
            self.ForEachClass(self.bclass,self.isfieldrecursive)
         cobj.Next()
   def OnPreIterate(self):
      self.file=TextFile(self.afile,'w')
      self.file.write('<?xml version="1.0" encoding="Windows-1250"?>\n\n')
      sd=tdatetime2str(self.adate,' ')
      sc=tdatetime2str(self.adatecreated,' ')
      self.file.write('<REPLICATION>\n')
      sheader='<HEADER SourceUser="%d" TargetUser="%d" DateFrom="%s" Created="%s" />\n\n' % (aICORDBEngine.SystemOwnerUserID,self.targetuser,sd,sc)
      self.file.write(sheader)
   def OnPostIterate(self):
      self.file.write('</REPLICATION>\n')
      if not self.file is None:
         self.file.close()
      InfoStatus('')
   def OnBeforeRecursiveField(self,aclass,afield):
      amethod=aclass.MethodsByName('OnRecursiveFieldExport')
      if not amethod is None:
         ret=amethod.Execute(afield.Name)
         if ret!='1':
            return 0
      return 1
   def OnPreClass(self,aclass):
      if not self.allowsystem and aclass.IsSystem=='1':
         return
      if aclass.IsVirtual=='1':
         return
      adt=aclass.GetLastModified()
      if adt<self.adate:
         return
      amethod=aclass.MethodsByName('OnClassExport')
      if not amethod is None and not self.disableclassmethods:
         aICORDBEngine.Variables._AllowClassExport='1'
         amethod.Execute()
         if aICORDBEngine.Variables._AllowClassExport!='1':
            return
      InfoStatus(aclass.NameOfClass)
      sd=tdatetime2str(adt,' ')
      sclass='<CLASS CID="%d" LastModification="%s" ClassPath="%s">\n' % (aclass.CID,sd,aclass.ClassPath)
      aclasswritten=0
      afmethod=aclass.MethodsByName('OnFieldExport')
      aomethod=aclass.MethodsByName('OnObjectExport')
      flist=aclass.GetFieldsList()
      for afname in flist:
         afield=aclass.FieldsByName(afname)
         if afield.IsInteractive=='1' and afield.AllowRead=='1' and afield.IsVirtual!='1' and afield.IsReportProtected!=1:
            ismemo=afield.IsContainer=='1' and afield.FieldTypeID==str(mt_String)
            adt=afield.GetLastModified()
            if adt<self.adate:
               continue
            if not afmethod is None and not self.disablefieldmethods:
               aICORDBEngine.Variables._AllowFieldExport='1'
               afmethod.Execute(afname)
               if aICORDBEngine.Variables._AllowFieldExport!='1':
                  continue
            if not aclasswritten:
               self.file.write(sclass)
               aclasswritten=1
            InfoStatus(aclass.NameOfClass+':'+afield.Name)
            sd=tdatetime2str(adt,' ')
            s='  <FIELD Name="%s" LastModification="%s">\n' % (afname,sd)
            self.file.write(s)
            aoid=afield.GetFirstValueID()
            while aoid>=0:
               adt=afield.GetValueLastModified(aoid)
               if adt<self.adate:
                  aoid=afield.GetNextValueID(aoid)
                  continue
               if self.CallbackObjectFunc:
                  if not self.CallbackObjectFunc(aclass,aoid):
                     aoid=afield.GetNextValueID(aoid)
                     continue
               if not aomethod is None and not self.disableobjectmethods:
                  aICORDBEngine.Variables._AllowObjectExport='1'
                  aomethod.Execute(afname,aoid)
                  if aICORDBEngine.Variables._AllowObjectExport!='1':
                     aoid=afield.GetNextValueID(aoid)
                     continue
               sd=tdatetime2str(adt,' ')
               if ismemo:
                  sv=afield.ValuesAsString(aoid)
                  svl=''
                  for c in sv:
                     if c !='\015':
                        svl = svl + c
                  slist=string.split(svl,'\n')
                  s='    <OBJECT OID="%d" LastModification="%s">\n' % (aoid,sd)
                  self.file.write(s)
                  for sv in slist:
                     self.file.write('      <DATA>'+GetAsXMLString(sv)+'</DATA>\n')
               else:
                  s='    <OBJECT OID="%d" LastModification="%s">\n' % (aoid,sd)
                  self.file.write(s)
                  self.file.write('      <DATA>'+GetAsXMLString(afield.ValuesAsString(aoid))+'</DATA>\n')
               self.file.write('    </OBJECT>\n')
               aoid=afield.GetNextValueID(aoid)
            self.file.write('  </FIELD> <!-- %s -->\n\n' % (afname))
      if aclasswritten:
         self.file.write('</CLASS> <!-- %s -->\n\n\n' % (aclass.NameOfClass))

def SendReplicationByFTP(aprofile,auserid=-1,adatefrom=(),abyftp=1,acallbackobjectfunc=None):
#   if achecksystemuser and aICORDBEngine.SystemOwnerUserID==0:
#      MessageDialog('Server w centrali nie wysyła raportów z zmianach.',mtWarning,mbOK)
#      return
   citerator=ICORSendReplicationClassIterator(aprofile,auserid,acallbackobjectfunc)
   arefs=citerator.ProfileClass.FTPProfile.GetRefList(citerator.OID)
   if abyftp:
      ftp=GetReplicationFTP(arefs)
      if ftp is None:
         MessageDialog('Błąd podczas nawiązywania komunikacji z serwerem.\nSprawdź, czy serwer jest aktywny.',mtError,mbOK)
         return
   else:
      ftp=None
   try:
      afmanager=FTPFileManager(ftp)
      try:
         afname=afmanager.GetStdName(auserid)
         afilepath=FilePathAsSystemPath(arefs.FTPLocalDir[arefs.OID])
         afpath=afilepath+'\\'+afname
         if auserid<0:
            auserid=aICORDBEngine.SystemOwnerUserID
         if not (adatefrom==() or adatefrom==tzerodatetime()):
            citerator.adate=adatefrom
         else:
            citerator.adate=aICORDBEngine.User.LastReportDate.ValuesAsDateTime(auserid)
         citerator.adatecreated=afmanager.FileTime
         citerator.Generate(afpath)
         afmanager.Upload(afname,afilepath)
         aICORDBEngine.User.LastReportDate.SetValuesAsDateTime(auserid,afmanager.FileTime)
      finally:
         del afmanager
         if ftp:
            ftp.quit()
   finally:
      pass
#      os.unlink(afpath)
   if abyftp:
      MessageDialog('Koniec wysyłania danych o zmianach.',mtInformation,mbOK)
   else:
      MessageDialog('Koniec wysyłania danych o zmianach. Plik z raportem znajduje się w:'+chr(10)+afpath+chr(10)+'teraz możesz przegrać go np. na dyskietkę i wykonać procedurę pobrania raportu na serwerze w Centrali',mtInformation,mbOK)
   return 

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   ClearStdOut()
#   SendReplicationByFTP('Test')
#   return
   if OID>=0:
      citerator=ICORSendReplicationClassIterator(OID)
   else:
      MessageDialog('Aby wysłać informacje o zmianach należy wybrać profil.',mtError,mbOK)
      return
   citerator.Generate()


