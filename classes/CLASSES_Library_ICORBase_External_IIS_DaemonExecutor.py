# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

import sys
import os
import traceback

import icorapi
import CLASSES_Library_ICORBase_Interface_ICORSync as ICORSync

MAX_THREAD_COUNT=10

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
   poid=int(sys.argv[1])
   pcid=1857 # CLASSES_System_SystemDictionary_External_DaemonParameters
   ret=0
   try:
      try:
         saveout=SysOutWrapper(1)
         saveerr=SysOutWrapper(0)
#         print 'parms: %s'%str(sys.argv)
         ampath=icorapi.GetFieldValue(0,pcid,'Name',poid)
#         print 'ampath: %s'%ampath
         ampath=ampath.replace('\\','_')
         ampath=ampath.replace('/','_')
         amethod=__import__(ampath)
         bcid=int(icorapi.GetFieldValue(0,pcid,'BCID',poid))
         boid=int(icorapi.GetFieldValue(0,pcid,'BOID',poid))
         buid=int(icorapi.GetFieldValue(0,pcid,'BUID',poid))
         bfieldname=icorapi.GetFieldValue(0,pcid,'BFieldName',poid)
         bvalue=icorapi.GetFieldValue(0,pcid,'BValue',poid)
         icorapi.SetFieldValue(0,pcid,'PID',poid,str(os.getpid()))
         amethod.ICORMain(bcid,bfieldname,boid,bvalue,buid)
      except:
         print 'Error in method:',ampath
         traceback.print_exc()
         ret=1
   finally:
      asemaphore=ICORSync.allocate_semaphore(MAX_THREAD_COUNT,'__DaemonExternal')
      asemaphore.release()
      icorapi.DeleteObject(0,pcid,poid)
   sys.exit(ret)



