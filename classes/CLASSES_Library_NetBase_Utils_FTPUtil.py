# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
from ftplib import FTP
import string

class FTPFileManager:
   def __init__(self,aftp):
      self.FTP=aftp
      self.file=None
      self.FileTime=()
   def __del__(self):
      self.CloseFile()
   def GetStdName(self,auid=0):
      self.FileTime=tdatetime()
      if auid<0:
         auid=0
      return str(auid)+'_'+tdatetime2str(self.FileTime,'_')+'_.gz'
   def GetFileList(self,adir=None):
      if not self.FTP:
         return
      if adir:
         self.FTP.cwd(adir)
      return self.FTP.nlst()
   def CloseFile(self):
      if not self.file is None:
         self.file.close()
   def Download(self,afilename,adownloadpath):
      self.CloseFile()
      if not self.FTP:
         return
      if adownloadpath[-1]!='\\':
         adownloadpath=adownloadpath+'\\'
      self.file=open(adownloadpath+afilename,'wb')
      self.FTP.retrbinary('RETR '+afilename,self.DownloadCallback)
   def DownloadCallback(self,adata):
      self.file.write(adata)
   def Upload(self,afilename,auploadpath):
      self.CloseFile()
      if not self.FTP:
         return
      if auploadpath[-1]!='\\':
         auploadpath=auploadpath+'\\'
      self.file=open(auploadpath+afilename,'rb')
      self.FTP.storbinary('STOR '+afilename,self.file,4096)
   def Move(self,afilename,apath):
      if not self.FTP:
         return
      if apath[-1]!='/':
         apath=apath+'/'
      self.FTP.rename(afilename,apath+afilename)

def GetSystemUserFTP():
   aprofile=aICORDBEngine.UserProfile
   poid=aICORDBEngine.SystemProfileOID
   try:
      aftp=FTP()
      aport=aprofile.FTPPort[poid]
      if aport=='':
         aftp.connect(aprofile.FTPServer[poid])
      else:
         aftp.connect(aprofile.FTPServer[poid],int(aport))
      auser=aprofile.FTPUser[poid]
      if auser!='':
         aftp.login(auser,aprofile.FTPPassword[poid])
      else:
         aftp.login()
      adir=aprofile.FTPBaseDir[poid]
      if adir!='':
         aftp.cwd(adir)
      return aftp
   except:
      return None

def GetReplicationFTP(arefs):
   if arefs.position<0:
      return
   try:
      aftp=FTP()
      aport=arefs.FTPPort[arefs.OID]
      if aport=='':
         aftp.connect(arefs.FTPServer[arefs.OID])
      else:
         aftp.connect(arefs.FTPServer[arefs.OID],int(aport))
      auser=arefs.FTPUser[arefs.OID]
      if auser!='':
         aftp.login(auser,arefs.FTPPassword[arefs.OID])
      else:
         aftp.login()
      adir=arefs.FTPBaseDir[arefs.OID]
      if adir!='':
         aftp.cwd(adir)
      return aftp
   except:
      return None


