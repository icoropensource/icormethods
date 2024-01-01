# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

import sys
import icorapi
import os
import time
import traceback
import subprocess
import win32api
import win32con

def Main():
   DEFAULT_PROCESS_DAEMON='"'+icorapi.GetVariable(0,'_ICOR_BASE_DIR')+'/Python/py2.4/External/cluster/daemon.py'+'"' #
   try:
      tcid=1858 # CLASSES_System_SystemDictionary_External_DaemonPID
      time.sleep(7)
      apid=-1
      while 1:
         try:
            toid=icorapi.GetLastFieldValueID(0,tcid,'Status')
         except:
            break
         astart=1
         if apid>0:
            w=0
            try:
               handle=win32api.OpenProcess(win32con.PROCESS_TERMINATE,0,apid)
               win32api.CloseHandle(handle)
               astart=0
            except:
               print 'unable to open process:',apid
               w=1
               traceback.print_exc()
            if w:
               print 'delete daemon instance [pid: %d]'%(apid,)
         if astart:
            print 'start new daemon instance'
            apid=subprocess.Popen([sys.executable, DEFAULT_PROCESS_DAEMON,sys.__dict__.get('ICOR_SERVER','')]).pid
         time.sleep(11)
   except:
      traceback.print_exc()

