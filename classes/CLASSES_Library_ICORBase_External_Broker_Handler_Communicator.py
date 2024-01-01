# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

import random
import pywintypes
import win32api
import win32file
import win32pipe
import winerror
import struct
import ntsecuritycon
import win32security

class CommunicatorException(Exception):
   pass

def CreatePipeSecurityObject():
   sa=win32security.SECURITY_ATTRIBUTES()
   sa.bInheritHandle=1
   sa.SetSecurityDescriptorDacl(1,None,0)
   return sa

class CommunicatorServer:
   def __init__(self,apipename):
      self.PipeName = apipename
      self.CreatePipe()
   def CreatePipe(self):
      pname="\\\\.\\PIPE\\"+self.PipeName
      self.pipe = win32pipe.CreateNamedPipe(
         pname,
         win32pipe.PIPE_ACCESS_DUPLEX,
         win32pipe.PIPE_TYPE_MESSAGE+win32pipe.PIPE_READMODE_MESSAGE+win32pipe.PIPE_WAIT,
         win32pipe.PIPE_UNLIMITED_INSTANCES,
         0,
         0,
         150,
         CreatePipeSecurityObject())
      if self.pipe==win32file.INVALID_HANDLE_VALUE:
         raise CommunicatorException('Create pipe %d' %win32api.GetLastError())
   def Open(self):
      while 1:
         try:
            hr = win32pipe.ConnectNamedPipe(self.pipe)
            break
         except win32file.error, (rc,fnerr,msg):
            win32file.CloseHandle(self.pipe)
            if rc==winerror.ERROR_NO_DATA:
               self.CreatePipe()
            else:
               raise
   def Close(self):
      try:
         win32file.FlushFileBuffers(self.pipe)
         win32pipe.DisconnectNamedPipe(self.pipe)
         win32file.CloseHandle(self.pipe)
      except:
         pass
   def Input(self):
      while 1:
         try:
            data=''
            while 1:
               hr,slen=win32file.ReadFile(self.pipe,4)
               alen=struct.unpack('<i',slen)[0]
               if alen:
                  hr,data1=win32file.ReadFile(self.pipe,alen)
                  data=data+data1
               else:
                  return data
         except win32file.error, (rc,fnerr,msg):
            if rc in [winerror.ERROR_PIPE_LISTENING,winerror.ERROR_BROKEN_PIPE]:
               self.Open()
            else:
               raise
      raise CommunicatorException("niemozliwe!")
   def Output(self,avalue,last=0,flush=1):
      if type(avalue)==type(1):
         avalue=struct.pack('<i',avalue)
      wlen=len(avalue)
      hr,byteswritten=win32file.WriteFile(self.pipe,struct.pack('<i',wlen))
      if wlen:
         hr,byteswritten=win32file.WriteFile(self.pipe,avalue)
      if last:
         hr,byteswritten=win32file.WriteFile(self.pipe,struct.pack('<i',0))
      elif flush:
         win32file.FlushFileBuffers(self.pipe)

class CommunicatorClient:
   def __init__(self,aserver='.',apipename=''):
      self.server=aserver
      self.pipename=apipename
      self.waitifbusy=23
      self.maxtries = 50
      self.pipe=None
   def Open(self):
      if self.pipe is not None:
         self.Close()
      tries = self.maxtries
      if '\\' in self.server:
         pname = self.server
      else:
         pname = "\\\\%s\\PIPE\\%s" % (self.server,self.pipename)
      while tries:
         try:
            self.pipe = win32file.CreateFile(
               pname, 
               win32file.GENERIC_READ + win32file.GENERIC_WRITE, 
               win32file.FILE_SHARE_READ + win32file.FILE_SHARE_WRITE, 
               None, 
               win32file.OPEN_EXISTING, 
               win32file.FILE_ATTRIBUTE_NORMAL, 
               0)
            return
         except win32api.error,(rc,fnerr,msg):
            tries = tries - 1
            if rc in [winerror.ERROR_PIPE_BUSY, winerror.ERROR_FILE_NOT_FOUND]:
               secs=random.randint(self.waitifbusy,self.waitifbusy+10)
               win32api.Sleep(secs)
               continue
      raise CommunicatorException('Open')

   def Close(self):
      if self.pipe is not None:
         try:
            win32file.FlushFileBuffers(self.pipe)
            win32file.CloseHandle(self.pipe)
         except:
            pass
         self.pipe=None

   def Input(self):
      while 1:
         try:
            data=''
            while 1:
               hr,slen=win32file.ReadFile(self.pipe,4)
               alen=struct.unpack('<i',slen)[0]
               if alen:
                  hr,data1=win32file.ReadFile(self.pipe,alen)
                  data=data+data1
               else:
                  return data
         except win32file.error, (rc,fnerr,msg):
            if rc in [winerror.ERROR_PIPE_LISTENING,winerror.ERROR_BROKEN_PIPE]:
               self.Open()
               continue
            raise
   def Output(self,avalue,last=0,flush=1):
      wlen=len(avalue)
      hr,byteswritten=win32file.WriteFile(self.pipe,struct.pack('<i',wlen))
      if wlen:
         hr,byteswritten=win32file.WriteFile(self.pipe,avalue)
      if last:
         hr,byteswritten=win32file.WriteFile(self.pipe,struct.pack('<i',0))
#      elif flush:
#         win32file.FlushFileBuffers(self.pipe)

def SendCmd(cmd,server='.',withrecv=1):
   bpipe='ICORPROCESSBROKER'
   c=CommunicatorClient(server,bpipe)
   c.Open()
   try:
      c.Output(cmd,1)
      if withrecv:
         return c.Input()
   finally:
      c.Close()



