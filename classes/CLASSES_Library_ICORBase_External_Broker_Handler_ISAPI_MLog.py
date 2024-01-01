# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import win32api
import cStringIO
import string
import random
import time
import sys
import os

LOG_FILE=FilePathAsSystemPath(r'%ICOR%\log\info_log.txt')
_TMP_CNT=0

def Log(s='',amode='a+',fname=LOG_FILE,aconsole=1):
   if not s or s=='\n':
      return
   if aconsole:
      print string.replace(s,'\n','')
   try:
      f=open(fname,amode)
      if s[-1:]!='\n':
         s=s+'\n'
      f.write('['+str(os.getpid())+'] {'+win32api.GetUserName()+'} '+ICORUtil.tdatetime2fmtstr(ICORUtil.tdatetime())+': '+s)
      f.close()
   except:
      pass

def LogException(amode='a+',fname=LOG_FILE,aconsole=1):
   try:
      f=open(fname,amode)
      import traceback
      if aconsole:
         traceback.print_exc()
      f.write('['+str(os.getpid())+'] {'+win32api.GetUserName()+'} '+ICORUtil.tdatetime2fmtstr(ICORUtil.tdatetime())+': Exception!\n')
      traceback.print_exc(file=f)
      f.close()
   except:
      pass

def GetLogTempFileName(adir,aprefix='log',asufix='',avalue=None,atrace=0,aext='txt'):
   global _TMP_CNT
   adir=FilePathAsSystemPath(r'%ICOR%/log/'+adir)
   if not os.path.exists(adir):
      os.makedirs(adir)
   afname=aprefix
   if afname:
      afname=afname+'_'
   afname=afname+ICORUtil.tdatetime2fmtstr(noms=0,adelimiter='',atimedelimiter='',apartdelimiter='_',amsdelimiter=' ')
   if asufix:
      afname=afname+'_'+asufix
   afname=adir+'/'+afname+'_%05d.%s'%(_TMP_CNT,aext,)
   _TMP_CNT=_TMP_CNT+1
   if _TMP_CNT>99999:
      _TMP_CNT=0
   if not avalue is None:
      fout=open(afname,'w')
      fout.write(avalue)
      if atrace:
         l=ICORUtil.dumpstack(aslist=1)
         fout.write('\n\n===================================================\n')
         for s in l:
            fout.write(s)
      fout.close()
   return afname

class MLog:
   def __init__(self,afname,aconsole=1):
      self.FName=afname
      self.Console=aconsole
   def Log(self,s,aconsole=None):
      if aconsole is None:
         aconsole=self.Console
      Log(s,fname=self.FName,aconsole=aconsole)
   def LogException(self,s=''):
      if s:
         Log(s,fname=self.FName,aconsole=self.Console)
      LogException(fname=self.FName,aconsole=self.Console)
   def write(self,s):
      self.Log(s)
   def flush(self):
      pass
   def close(self):
      pass

class MemoryLog:
   def __init__(self,aconsole=0):
      self.file=cStringIO.StringIO()
      self.Console=aconsole
   def Log(self,s):
      self.write(s)
   def LogException(self,s=''):
      self.write(s)
      import traceback
      traceback.print_exc(file=self.file)
      if self.Console:
         traceback.print_exc()
   def write(self,s):
      self.file.write(s)
      if self.Console:
         print s
   def flush(self):
      pass
   def close(self):
      self.file.close()
   def read(self):
      return self.file.getvalue()

class MemorySysOutWrapper(MemoryLog):
   def __init__(self,atimeinclude=1,asetbinary=0,apidinclude=1,aicorstdoutprint=0,fout2=None):
      MemoryLog.__init__(self)
      self.restored=0
      self.TimeInclude=atimeinclude
      self.PIDInclude=apidinclude
      self.ICORStdOutPrint=aicorstdoutprint
      self.PID=os.getpid()
      self.UserName=win32api.GetUserName()
      self.sysin=sys.stdin
      if asetbinary:
         import msvcrt
         msvcrt.setmode(sys.stdout.fileno(),os.O_BINARY)
         msvcrt.setmode(sys.stdin.fileno(),os.O_BINARY)
         msvcrt.setmode(sys.stderr.fileno(),os.O_BINARY)
      self.sysout=sys.stdout
      self.syserr=sys.stderr
      self.sysin=sys.stdin
      sys.stdout=self
      sys.stderr=self
      sys.stdin=self
      self.fout2=fout2
      spid=''
      if self.PIDInclude:
         spid='[%d] '%self.PID+' {'+self.UserName+'} '
      if self.TimeInclude:
         self.file.write(spid+ICORUtil.tdatetime2fmtstr(ICORUtil.tdatetime())+': ')
   def __del__(self):
      self.Restore()
   def Restore(self):
      if self.restored:
         return
      sys.stdout=self.sysout
      sys.stderr=self.sysout
      sys.stdin=self.sysin
      self.restored=1
   def LogException(self):
      self.write('')
      import traceback
      if self.ICORStdOutPrint:
         traceback.print_exc()
      else:
         MemoryLog.LogException(self)
   def write(self,s):
      spid=''
      if self.PIDInclude:
         spid='[%d] '%self.PID+' {'+self.UserName+'} '
      if self.TimeInclude:
         spid=spid+ICORUtil.tdatetime2fmtstr(ICORUtil.tdatetime())+': '
      if self.ICORStdOutPrint:
         icorapi.OnStdOutPrint(0,s,0)
      s1=s
      if spid:
         s1=string.replace(s,'\n','\n'+spid)
      MemoryLog.write(self,s1)
      if self.fout2:
         Log(s,fname=self.fout2,aconsole=0)
   def Dump(self):
      Log(self.read(),aconsole=0)





