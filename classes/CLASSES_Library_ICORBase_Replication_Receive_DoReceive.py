# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_Utils_FTPUtil import *
from CLASSES_Library_ICORBase_Replication_Receive_ReceiveData import *
from ftplib import FTP
import string
import os

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   ClearStdOut()
   afilepath=FilePathAsSystemPath(aICORDBEngine.UserProfile.FTPLocalDir[aICORDBEngine.SystemProfileOID])
   ftp=GetSystemUserFTP()
   if ftp is None:
      MessageDialog('Błąd podczas nawiązywania komunikacji z serwerem.\nSprawdź, czy serwer jest aktywny.',mtError,mbOK)
      return
   try:
      afmanager=FTPFileManager(ftp)
      flist=afmanager.GetFileList()
      for afile in flist:
         fnl=string.split(afile,'_')
         if len(afile)>2 and afile[-3:]=='.gz' and (fnl[0]==str(aICORDBEngine.SystemOwnerUserID) or fnl[0]=='-1'):
            afmanager.Download(afile,afilepath)
            afmanager.Move(afile,'archive/')
            afmanager.CloseFile()
            try:
               ReceiveData(afilepath+afile)
            finally:
               try:
                  os.unlink(afilepath+afile)
               except:
                  pass
   finally:
      del afmanager
      ftp.quit()
   MessageDialog('Koniec pobierania danych.',mtInformation,mbOK)   


