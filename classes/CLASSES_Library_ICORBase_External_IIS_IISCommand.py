# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

import win32event,win32file,win32pipe,win32api,winerror,win32security
import sys
import string
import struct
import types
import CLASSES_Library_ICORBase_External_IIS_ASPObjects
ASPObjects=CLASSES_Library_ICORBase_External_IIS_ASPObjects
from CLASSES_Library_ICORBase_External_MLog import Log,LogException

class Communicator:
   def __init__(self,apipename):
      self.PipeName=apipename
      self.CreatePipe()
   def CreatePipe(self):
      sa=self.CreatePipeSecurityObject()
      self.pipe = win32pipe.CreateNamedPipe('\\\\.\\pipe\\'+self.PipeName,win32pipe.PIPE_ACCESS_DUPLEX,win32pipe.PIPE_TYPE_MESSAGE+win32pipe.PIPE_READMODE_MESSAGE+win32pipe.PIPE_WAIT,win32pipe.PIPE_UNLIMITED_INSTANCES, 0, 0, 150, sa)
      if self.pipe==win32file.INVALID_HANDLE_VALUE:
         print 'Error!',GetLastError
   def Open(self):
      while 1:
         try:
            Log('connecting...\n')
            hr = win32pipe.ConnectNamedPipe(self.pipe)
            Log('connected!\n')
            break
         except win32file.error, (rc,fnerr,msg):
            win32file.CloseHandle(self.pipe)
            if rc==winerror.ERROR_NO_DATA:
               self.CreatePipe()
            else:
               raise
   def Close(self):
      try:
         win32file.FlushFileBuffers(self.pipe);
         win32pipe.DisconnectNamedPipe(self.pipe);
         win32file.CloseHandle(self.pipe)
      except:
         pass
   def CreatePipeSecurityObject(self):
      sa=win32security.SECURITY_ATTRIBUTES()
      sa.bInheritHandle=1
      sa.SetSecurityDescriptorDacl(1,None,0)
      return sa
   def Input(self):
#      Log('  Input 1:')
      while 1:
         try:
            hr,slen=win32file.ReadFile(self.pipe,4)
            alen=struct.unpack('i',slen)[0]
#            Log('    Input 3: '+str(alen))
            if alen>0:
               hr,data=win32file.ReadFile(self.pipe,alen)
            else:
               hr,data=0,''
            break
         except win32file.error, (rc,fnerr,msg):
            if rc in [winerror.ERROR_PIPE_LISTENING,winerror.ERROR_BROKEN_PIPE]:
               self.Open()
            else:
               raise
#      Log('    Input 2: '+data[:60])
      return data
   def Output(self,avalue,aflush=1):
#      Log('  Output 1: '+avalue[:60])
      try:
         hr,byteswritten=win32file.WriteFile(self.pipe,struct.pack('<i',len(avalue)))
#         Log('    Output 2:')
         if len(avalue)>0:
            hr,byteswritten=win32file.WriteFile(self.pipe,avalue)
#         Log('    Output 3:')
         if aflush:
            win32file.FlushFileBuffers(self.pipe);
#         Log('    Output 4:')
      except win32file.error,(rc,fnerr,msg):
#         Log('    Output 5:')
         if rc==winerror.ERROR_BROKEN_PIPE:
            pass
#      Log('    Output 6:')
   def CallMethod(self,abase,amethod,avalue):
#      Log('CALLMETHOD %s %s %d\n'%(abase,amethod,len(avalue)))
      if type(avalue)==types.TupleType:
         if len(avalue)==2:
            self.Output('CALLMETHOD2 %s %s'%(abase,amethod),0)
            self.Output(avalue[0],0)
            self.Output(avalue[1])
         elif len(avalue)==3:
            self.Output('CALLMETHOD2 %s %s'%(abase,amethod),0)
            self.Output(avalue[0],0)
            self.Output(avalue[1],0)
            self.Output(avalue[2])
      else:
         self.Output('CALLMETHOD %s %s'%(abase,amethod),0)
         self.Output(avalue)
#      Log('Wait for method result\n')
      res=self.Input()
#      Log('Method result: %s\n'%res)
      return res
   def GetProperty(self,abase,aname):
#      Log('GETPROPERTY %s %s\n'%(abase,aname))
      self.Output('GETPROPERTY %s %s'%(abase,aname))
#      Log('Wait for getproperty result\n')
      res=self.Input()
#      Log('Property result: %s\n'%res)
      return res
   def SetProperty(self,abase,aname,avalue):
#      Log('SETPROPERTY %s %s=%s\n'%(abase,aname,avalue))
      self.Output('SETPROPERTY %s %s'%(abase,aname),0)
      self.Output(avalue)
      return
   def GetCollection(self,abase,aname):
#      Log('GETCOLLECTION %s %s\n'%(abase,aname))
      self.Output('GETCOLLECTION %s %s'%(abase,aname))
#      Log('Wait for getcollection result\n')
      res=self.Input()
#      Log('COLLECTION result: %s\n'%res)
      return res
   def SetCollectionItem(self,abase,aname,iname,ivalue):
#      Log('SETCOLLECTIONITEM %s %s %s\n'%(abase,aname,iname))
      self.Output('SETCOLLECTIONITEM %s %s %s'%(abase,aname,iname),0)
      self.Output(ivalue)
      res=self.Input()
      return

class ICORPyExecutor:
   def __init__(self,apipename):
      self.communicator=Communicator(apipename)
   def Close(self):
      self.communicator.Close()
   def Process(self):
#      Log('start\n')
      while 1:
         Log("before Input\n")
         s=self.communicator.Input()
         Log("Input: %s\n"%s)
         if not s:
            continue
         sl=string.split(s)
         command=sl[0]
         if command=="START":
            self.DoStart(sl[1])
         elif command=="STOP":
            break
   def DoStart(self,aiid):
      Log("START: %s\n"%aiid)
      try:
         amodule=__import__('CLASSES_Library_ICORBase_External_IIS_IISInterface')
         amodule=reload(amodule)

         asession=ASPObjects.Session('SESSION',self.communicator)
         aserver=ASPObjects.Server('SERVER',self.communicator)
         aapplication=ASPObjects.Application('APPLICATION',self.communicator)
         arequest=ASPObjects.Request('REQUEST',self.communicator)
         aresponse=ASPObjects.Response('RESPONSE',self.communicator)

         amodule.Session=asession
         amodule.Server=aserver
         amodule.Application=aapplication
         amodule.Request=arequest
         amodule.Response=aresponse

#         Log("module start\n")
         amodule.DoStart(Log,aiid)
#         Log("module end\n")

         amodule.Session=None
         amodule.Server=None
         amodule.Application=None
         amodule.Request=None
         amodule.Response=None
      except:
         LogException()
         self.communicator.Output('ERROR')
      Log("before finish\n")
      self.communicator.Output('FINISH')
      Log("after finish\n")

def ProcessIISCommands(apipename="ICORIISPipe0"):
   aexecutor=ICORPyExecutor(apipename)
   try:
      aexecutor.Process()
   finally:
      aexecutor.Close()



