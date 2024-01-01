# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

import os
import sys
import traceback
import icorapi
import time
import CLASSES_Library_ICORBase_Interface_FTHRQueue as FTHRQueue
import CLASSES_Library_ICORBase_Interface_ICORSync as ICORSync

cv_eq,cv_le,cv_ge,cv_not=1,2,4,8

MAX_THREAD_COUNT=10
MAX_HANDLES_COUNT=300

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
      if self.asstdout:
         sys.stdout = self.sysout
      else:
         sys.stderr = self.sysout
   def write(self,s):
      if self.asstdout:
         icorapi.OnStdOutPrint(0,s,0)
      else:
         icorapi.OnStdErrPrint(0,s,0)
   def flush(self):
      pass

def ICORMethodRun(aqueue,pcid,poid,ampath,aparallel,aqueued,aexecutor,apid): #   print '  ICORMethodRun %d,%d,%s par: %d, que: %d'%(pcid,poid,ampath,aparallel,aqueued)
   global MAX_HANDLES_COUNT
   try:
      w=icorapi.SetTestFieldValue(0,pcid,'Status',poid,cv_eq,'Ready','Processing')
      if w:
         if aparallel and not aqueued:
            asemaphore=ICORSync.allocate_semaphore(MAX_THREAD_COUNT,'__DaemonExternal')
            asemaphore.acquire()
            ret=os.spawnv(os.P_NOWAIT,sys.executable,['"%s"'%sys.executable,aexecutor,str(poid),sys.__dict__.get('ICOR_SERVER','')]) #         print '    Parallel method stop poid=%d'%(poid,)
            MAX_HANDLES_COUNT=MAX_HANDLES_COUNT-1
         elif aparallel:
            asemaphore=ICORSync.allocate_semaphore(MAX_THREAD_COUNT,'__DaemonExternal')
            asemaphore.acquire()
            ret=os.spawnv(os.P_WAIT,sys.executable,['"%s"'%sys.executable,aexecutor,str(poid),sys.__dict__.get('ICOR_SERVER','')]) #         print '    Parallel method stop poid=%d, ret=%d'%(poid,ret)
            MAX_HANDLES_COUNT=MAX_HANDLES_COUNT-1
         else:
            try:
               amethod=__import__(ampath)
               bcid=int(icorapi.GetFieldValue(0,pcid,'BCID',poid))
               boid=int(icorapi.GetFieldValue(0,pcid,'BOID',poid))
               buid=int(icorapi.GetFieldValue(0,pcid,'BUID',poid))
               bfieldname=icorapi.GetFieldValue(0,pcid,'BFieldName',poid)
               bvalue=icorapi.GetFieldValue(0,pcid,'BValue',poid)
               icorapi.SetFieldValue(0,pcid,'PID',poid,apid)
               amethod.ICORMain(bcid,bfieldname,boid,bvalue,buid)
            finally:
               icorapi.DeleteObject(0,pcid,poid)
   except:
      traceback.print_exc()

def reporter(queue):
    str="  "
    for ID, age in queue.ages():
        str=str+("%i:%i, " % (ID, age))
    str=str+"\n"
    print time.strftime("%H:%M:%S %m/%d/%y ",time.localtime(time.time()))+queue.status()+"\n"+str

def Main():
   DEFAULT_PROCESS_EXECUTOR='"'+icorapi.GetVariable(0,'_ICOR_BASE_DIR')+'/Python/py2.4/External/cluster/main.py'+'"' #
   PPID=str(os.getpid())
   tcid=1858 # CLASSES_System_SystemDictionary_External_DaemonPID
#   toid=icorapi.AddObject(0,tcid)
#   icorapi.SetFieldValue(0,tcid,'Name',toid,PPID)
#   icorapi.SetFieldValue(0,tcid,'Status',toid,'RUN')
   
   aparqueue=FTHRQueue.THRQueue(10)
   dtqueues={}
#   pcid=1857 # CLASSES_System_SystemDictionary_External_DaemonParameters
   try:
      try:
##         saveout=SysOutWrapper(1)
##         saveerr=SysOutWrapper(0)
         print 'Start Daemon [pid=%s]'%(PPID,)
         while MAX_HANDLES_COUNT>0:
            try:
               w=icorapi.GetFieldValue(0,tcid,'Status',toid)!='RUN'
            except:
               w=1
            if w:
               break
   #         print time.ctime(time.time())
            roid=icorapi.GetLastObjectID(0,tcid)
            bpid=icorapi.GetFieldValue(0,tcid,'Name',roid)
            if bpid!=PPID:
               print 'Exit PID=%s, new daemon instance [%s] detected'%(PPID,bpid)
               break
            lpoids=[]
            poid=icorapi.GetLastFieldValueID(0,pcid,'Status')
            while poid>=0:
               astatus=icorapi.GetFieldValue(0,pcid,'Status',poid)
               if astatus!='Ready':
                  break
               lpoids.append(poid)
               poid=icorapi.GetPrevFieldValueID(0,pcid,'Status',poid)
            lpoids.reverse()
            for poid in lpoids:
               ampath=icorapi.GetFieldValue(0,pcid,'Name',poid)
               moid=int(icorapi.GetFieldValue(0,pcid,'MOID',poid))
               mcid=462 # CLASSES_System_ICORMethod
               aparallel=icorapi.GetFieldValueInt(0,mcid,'aIsParallel',moid)
               aqueued=icorapi.GetFieldValueInt(0,mcid,'aIsQueued',moid)
               if aparallel and not aqueued:
                  aparqueue.append(ICORMethodRun,(aparqueue,pcid,poid,ampath,aparallel,aqueued,DEFAULT_PROCESS_EXECUTOR,PPID))
               else:
                  aqueue=dtqueues.get(ampath,None)
                  if aqueue is None:
                     aqueue=FTHRQueue.THRQueue(1)
                     dtqueues[ampath]=aqueue
                  aqueue.append(ICORMethodRun,(aqueue,pcid,poid,ampath,aparallel,aqueued,DEFAULT_PROCESS_EXECUTOR,PPID))
            import gc
#            gc.set_debug(gc.DEBUG_STATS | gc.DEBUG_LEAK)
            gc.collect()
#            print gc.garbage
            time.sleep(7)
      except:
         traceback.print_exc()
   finally:
      icorapi.DeleteObject(0,tcid,toid)
   
   print 'Exit Daemon [toid=%d, pid=%s]'%(toid,PPID)
   
   time.sleep(1)
   aparqueue.waittilfinished(reporter,10)
   for akey,aqueue in dtqueues.items():
      aqueue.waittilfinished(reporter,10)

