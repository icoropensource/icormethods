# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_Utils_FTPUtil import *
from CLASSES_Library_ICORBase_Replication_Send_GenerateReport import *
from ftplib import FTP
import os

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   ClearStdOut()
#   if aICORDBEngine.SystemOwnerUserID==0:
#      MessageDialog('Server w centrali nie wysyła raportów z zmianach.',mtWarning,mbOK)
#      return
   ftp=GetSystemUserFTP()
   if ftp is None:
      MessageDialog('Błąd podczas nawiązywania komunikacji z serwerem.\nSprawdź, czy serwer jest aktywny.',mtError,mbOK)
      return
   try:
      afmanager=FTPFileManager(ftp)
      try:
         afname=afmanager.GetStdName()
         afilepath=FilePathAsSystemPath(aICORDBEngine.UserProfile.FTPLocalDir[aICORDBEngine.SystemProfileOID])
         adatefrom=aICORDBEngine.User.LastReportDate.ValuesAsDateTime(aICORDBEngine.SystemOwnerUserID)
         GenerateReport(afilepath+afname,adatefrom,afmanager.FileTime)
         afmanager.Upload(afname,afilepath)
         aICORDBEngine.User.LastReportDate.SetValuesAsDateTime(aICORDBEngine.SystemOwnerUserID,afmanager.FileTime)
      finally:
         del afmanager
         ftp.quit()
   finally:
      os.unlink(afilepath+afname)
   MessageDialog('Koniec wysyłania danych o zmianach.',mtInformation,mbOK)
   return



