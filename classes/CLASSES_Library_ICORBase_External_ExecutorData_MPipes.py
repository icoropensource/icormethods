# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

import win32pipe,win32file,win32event,pywintypes,win32api,winerror
import sys, os, types, traceback
import threading, struct
import string, random
import Queue

import win32pipe,win32file,win32event,pywintypes,win32api,winerror
import ntsecuritycon
import sys, os, types, traceback
import threading, struct
import string, random
import Queue

import binascii
import struct

def Log(s):
   amode='a+'
   fname='d:/icor/log/mpipe.log'
   try:
      f=open(fname,amode)
      if s[-1:]!='\n':
         s=s+'\n'
      f.write('['+str(os.getpid())+'] {'+win32api.GetUserName()+'} '+s)
      f.close()
   except:
      pass

def find_in_locals(aname,adefault):
   f=sys._getframe().f_back
   while f is not None:  
      if f.f_locals.has_key(aname):
         return f.f_locals[aname]
      f=f.f_back
   return adefault

def get_caller_names(adepth=0):
   ret=[]
   f=sys._getframe().f_back
   acnt=0
   while f is not None:
      aname=f.f_code.co_name
      if adepth and acnt==adepth:
         return aname      
      ret.append(aname)
      f=f.f_back
      acnt=acnt+1
   return ret

def hex2int(anum):
   return struct.unpack('>i',binascii.unhexlify(anum))[0]

#stale dla typow podstawowych
mt_Integer,mt_Double,mt_DateTime,mt_Boolean,mt_String=0x20,0x40,0x60,0x70,0x90
mt_Bool,mt_Date,mt_Time=0x70,0x60,0x60
mt_Memo=0x91

MAX_REQUEST_QUEUE_SIZE=64
MAX_THREAD_COUNT=4

class MWin32PipeException(Exception):
   pass

class MWin32Pipe:
   def __init__(self,aserver='.',apipename='ICORPipe0'):
#      Log('* init')
      self.server=aserver
      self.pipename=apipename
      self.waitifbusy=27
      self.pipe=None
   def _Open(self,nowait=0):
#      Log('* open 1 ')
      if self.pipe is not None:
#         Log('* open 2')
         self._Close()
      while 1:
#         Log('* open 3')
         try:
            self.pipe = win32file.CreateFile(
               "\\\\%s\\pipe\\%s" % (self.server,self.pipename), 
               win32file.GENERIC_READ + win32file.GENERIC_WRITE, 
               win32file.FILE_SHARE_READ + win32file.FILE_SHARE_WRITE, 
               None, 
               win32file.OPEN_EXISTING, 
               win32file.FILE_ATTRIBUTE_NORMAL, 
               None)
#            Log('* open 4')
            return 1
         except win32file.error,(rc,fnerr,msg):
            if rc==winerror.ERROR_PIPE_BUSY:
#               Log('* open 5')
               if nowait:
                  return 0
               secs=random.randint(self.waitifbusy,self.waitifbusy+10)
               #print 'waits for %3d msecs'%secs
               win32api.Sleep(secs)
               continue
            if self.pipe is not None:
#               Log('* open 6')
               #print 'closehandle in exception'
               win32file.CloseHandle(self.pipe)
            if rc==winerror.ERROR_FILE_NOT_FOUND:
#               Log('* open 7')
               raise MWin32PipeException,'The ICOR process at server "%s" is not accessible'%self.server
#            Log('* open 8 rc: '+str(rc)+' fnerr: '+str(fnerr)+' msg: '+str(msg))
            raise win32file.error,(rc,fnerr,msg)
#      Log('* open 9')
   def _Close(self):
#      Log('* close')
      if self.pipe is not None:
         win32file.CloseHandle(self.pipe)
         self.pipe=None
   def ReadInt(self):
#      Log('* readint')
      hr,data=win32file.ReadFile(self.pipe,4)
      return struct.unpack('i',data)[0]
   def ReadInts(self,acount,astuple=1):
      ret=[]
      for i in range(acount):
         hr,data=win32file.ReadFile(self.pipe,4)
         ret.append(struct.unpack('i',data)[0])
      if astuple:
         ret=tuple(ret)
      return ret
   def ReadString(self,ahexlen=0):
#      Log('* readstring')
      if ahexlen:
         hr,s=win32file.ReadFile(self.pipe,8)
         alen=hex2int(s)
      else:
         hr,slen=win32file.ReadFile(self.pipe,4)
         alen=struct.unpack('i',slen)[0]
      hr,data=win32file.ReadFile(self.pipe,alen)
      return data
   def ReadStrings(self):
      alen=self.ReadInt()
      sl=[]
      for i in range(alen):
         sl.append(self.ReadString())
      return sl
   def ReadFloat(self):
      hr,data=win32file.ReadFile(self.pipe,8)
      return struct.unpack('d',data)[0]
   def Write(self,avalue,atypeinfo=0,ahexlen=0):
#      Log('* write')
      if type(avalue)==types.IntType:
         try:
            if atypeinfo:
               hr,byteswritten=win32file.WriteFile(self.pipe,struct.pack('<i',mt_Integer))
            hr,byteswritten=win32file.WriteFile(self.pipe,struct.pack('<i',avalue))
         except win32file.error,(rc,fnerr,msg):
            if rc==winerror.ERROR_BROKEN_PIPE:
               pass
      elif type(avalue)==types.StringType:
         try:
            if atypeinfo:
               hr,byteswritten=win32file.WriteFile(self.pipe,struct.pack('<i',mt_String))
            if ahexlen:
               s=hex(len(avalue))
               hr,byteswritten=win32file.WriteFile(self.pipe,'0'*(10-len(s))+s[2:])
            else:
               hr,byteswritten=win32file.WriteFile(self.pipe,struct.pack('<i',len(avalue)))
            hr,byteswritten=win32file.WriteFile(self.pipe,avalue)
         except win32file.error,(rc,fnerr,msg):
            if rc==winerror.ERROR_BROKEN_PIPE:
               pass
      elif type(avalue)==types.FloatType:
         try:
            if atypeinfo:
               hr,byteswritten=win32file.WriteFile(self.pipe,struct.pack('<i',mt_Double))
            hr,byteswritten=win32file.WriteFile(self.pipe,struct.pack('<d',avalue))
         except win32file.error,(rc,fnerr,msg):
            if rc==winerror.ERROR_BROKEN_PIPE:
               pass
      elif type(avalue)==types.ListType:
         try:
            sl=[]
            for v in avalue:
               if type(v)==types.IntType:
                  sl.append(struct.pack('<i',v))
               elif type(v)==types.StringType:
                  sl.append(struct.pack('<i',len(v)))
                  sl.append(v)
               elif type(v)==types.FloatType:
                  sl.append(struct.pack('<d',v))
               else:
                  raise MWin32PipeException,'Unknown type for value: '+v
            hr,byteswritten=win32file.WriteFile(self.pipe,string.join(sl,''))
         except win32file.error,(rc,fnerr,msg):
            if rc==winerror.ERROR_BROKEN_PIPE:
               pass
      else:
         raise MWin32PipeException,'Unknown type for value: '+avalue
   def WriteMessage(self,aformat,arest,*aparameters):
#      Log('* writemessage')
      afuncname=get_caller_names(1)
#      Log('%d'%(aparameters[0],)) # do statystyk
#      try:
      s=apply(struct.pack,('<'+aformat,)+aparameters)
#      except:
#         Log('WriteMessage')
#         Log(aformat)
#         Log(str(arest))
#         Log(str(aparameters))
#         raise
      try:                       
         hr,byteswritten=win32file.WriteFile(self.pipe,s+arest)
      except win32file.error,(rc,fnerr,msg):
         if rc==winerror.ERROR_BROKEN_PIPE:
            pass

class MPipesCollection:
   def __init__(self,aserver='.',apipename='ICORPipe0'):
#      Log('* coll init')
      self.server=aserver
      self.pipename=apipename
      self.pipes=Queue.Queue()
   def Add(self,acount=1):
#      Log('* coll add')
      for i in range(acount):
         apipe=MWin32Pipe(self.server,self.pipename)
         self.pipes.put(apipe)
   def Get(self,nowait=0):
#      Log('* coll get')
#      Log('  '+str(get_caller_names()))
      apipe=self.pipes.get()
      ret=apipe._Open(nowait)
      if not ret:
         self.Release(apipe)
         return None
      return apipe
   def Release(self,apipe):
#      Log('* coll release')
#      Log('  '+str(get_caller_names()))
      apipe._Close()
      self.pipes.put(apipe)



