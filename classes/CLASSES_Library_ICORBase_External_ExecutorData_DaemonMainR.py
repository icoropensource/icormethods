# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

import os
import sys
import traceback
import time

import icorapi
import appplatform.startutil as startutil

import CLASSES_Library_ICORBase_Interface_ICORInterface as ICORInterface
import CLASSES_Library_ICORBase_Interface_FTHRQueue as FTHRQueue

MAX_HANDLES_COUNT=500
VERBOSE=1

def ICORMethodRun(aqueue,i,aexecutor):
   global MAX_HANDLES_COUNT
   try:
      ICORInterface.aICORDBEngine.SysBase.SemaphoreAcquire('DaemonExternal')
      if VERBOSE:
         print '    spawn process %d'%i
      os.spawnv(os.P_NOWAIT,sys.executable,['"%s"'%sys.executable,aexecutor,str(i),sys.__dict__.get('ICOR_SERVER','')])
      MAX_HANDLES_COUNT=MAX_HANDLES_COUNT-1
   except:
      traceback.print_exc()

def reporter(queue):
    str="  "
    for ID, age in queue.ages():
        str=str+("%i:%i, " % (ID, age))
    str=str+"\n"
    print time.strftime("%H:%M:%S %m/%d/%y ",time.localtime(time.time()))+queue.status()+"\n"+str

def Main():
   global MAX_HANDLES_COUNT
   DEFAULT_PROCESS_EXECUTOR='"'+icorapi.GetVariable(0,'_DEFAULT_PYTHON_TOP_DIR')+'/External/default/main2.py'+'"'
   PPID=str(os.getpid())
   MAX_THREAD_COUNT=startutil.icorconfig.MaxDaemonExecutors
   aparqueue=FTHRQueue.THRQueue(MAX_THREAD_COUNT)
   try:
      print 'Start Daemon [pid=%s]'%(PPID,)
      ICORInterface.aICORDBEngine.SysBase.SemaphoreSet('DaemonExternal',MAX_THREAD_COUNT)
      ICORInterface.aICORDBEngine.SysBase.ExecutorMethodCheckProcessing()
      while 1:
         if MAX_HANDLES_COUNT<=0:
            if ICORInterface.aICORDBEngine.SysBase.SemaphoreInfo('DaemonExternal')==MAX_THREAD_COUNT:
               time.sleep(2.5)
               if ICORInterface.aICORDBEngine.SysBase.SemaphoreInfo('DaemonExternal')==MAX_THREAD_COUNT:
                  break
         amcount=ICORInterface.aICORDBEngine.SysBase.GetExecutorMethodReadyCount()
         if VERBOSE:
            if amcount:
               print '  register %d methods'%amcount
         for i in range(amcount):
            aparqueue.append(ICORMethodRun,(aparqueue,i,DEFAULT_PROCESS_EXECUTOR))
         time.sleep(0.05)
   except:
      traceback.print_exc()
   print 'Exit Daemon [pid=%s]'%(PPID,)
   time.sleep(1)
   aparqueue.waittilfinished(reporter,5)

