# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

import sys
import os
import traceback

import icorapi

import CLASSES_Library_ICORBase_Interface_ICORInterface as ICORInterface

VERBOSE=1

class SysOutWrapper:
   def __init__(self,asstdout):
      self.asstdout = asstdout
      if self.asstdout:
         self.sysout = sys.stdout
         sys.stdout = self
      else:
         self.sysout = sys.stderr
         sys.stderr = self
   def __del__(self):
      try:
         if self.asstdout:
            sys.stdout = self.sysout
         else:
            sys.stderr = self.sysout
      except:
         pass
   def write(self,s):
      if self.asstdout:
         icorapi.OnStdOutPrint(0,s,0)
      else:
         icorapi.OnStdErrPrint(0,s,0)

def Main():
   ret=0
   amdata=None
   try:
      PPID=str(os.getpid())
      saveout=SysOutWrapper(1)
      saveerr=SysOutWrapper(0)
      icnt=int(sys.argv[1])
      if VERBOSE:
         print '  execute method cnt: %d PID: %d'%(icnt,PPID)
      try:
         #ICORInterface.aICORDBEngine.SysBase.ExecutorMethodSetWorking(mid)
         amdata=ICORInterface.aICORDBEngine.SysBase.GetExecutorMethod(pid=PPID)
         aclass=ICORInterface.aICORDBEngine.Classes[amdata['CID']]
         bmethod=aclass.MethodsByName(amdata['Name'])
         mname=bmethod.MethodPath.replace('\\','_')
         mname=mname.replace('/','_')
         amethod=__import__(mname)
         amethod.ICORMain(amdata['CID'],amdata['FieldName'],amdata['OID'],amdata['Value'],amdata['UID'])
      except:
         ret=1
         print 'Error in method: [PID:%d] : %s'%(PPID,str(amdata))
         traceback.print_exc()
   finally:
      ICORInterface.aICORDBEngine.SysBase.SemaphoreRelease('DaemonExternal')
      if amdata:
         ICORInterface.aICORDBEngine.SysBase.ExecutorMethodSetDone(amdata['MID'])
         if not ret:
            ICORInterface.aICORDBEngine.SysBase.RemoveExecutorMethod(amdata['MID'])
   sys.exit(ret)

