# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

import sys
import os
import time
import traceback
import win32api
import win32con

import icorapi
#import CLASSES_Library_ICORBase_Interface_ICORSync as ICORSync

import appplatform.startutil as startutil

MAX_THREAD_COUNT=10

def Main():
   if 0:
      startutil.HideWindow()
   DEFAULT_PROCESS_DAEMON='"'+icorapi.GetVariable(0,'_DEFAULT_PYTHON_TOP_DIR')+'/External/default/daemon.py'+'"' #
   try:
      tcid=1858 # CLASSES_System_SystemDictionary_External_DaemonPID
      rcid=1857 # CLASSES_System_SystemDictionary_External_DaemonParameters
      #asemaphore=ICORSync.allocate_semaphore(MAX_THREAD_COUNT,'__DaemonExternal',aautodelete=1)
      #asemaphore.set_value(MAX_THREAD_COUNT)
      #time.sleep(7)
      ltoids=[]
      toid=icorapi.GetLastFieldValueID(0,tcid,'Status')
      while toid>=0:
         ltoids.append(toid)
         toid=icorapi.GetPrevFieldValueID(0,tcid,'Status',toid)
      for toid in ltoids:
         icorapi.DeleteObject(0,tcid,toid)
      while 1:
         ltoids=[]
         try:
            toid=icorapi.GetLastFieldValueID(0,tcid,'Status')
         except:
            break
         while toid>=0:
            if icorapi.ObjectExists(0,tcid,toid)>=0:
               ltoids.append(toid)
            toid=icorapi.GetPrevFieldValueID(0,tcid,'Status',toid)
         astart=1
         #print
         #print '1:',astart,str(ltoids)
         for toid in ltoids:
            apid=icorapi.GetFieldValueInt(0,tcid,'Name',toid)
            w=0
            try:
               #print '2:',apid
               wexists=startutil.CheckApp('ICOR_Daemon_Instance')
               if wexists:
                  astart=0
               #print '3:',apid,'start=',astart
            except:
               print 'unable to open process:',apid
               w=1
               traceback.print_exc()
            if w:
               print 'delete daemon instance [toid: %d, pid: %d]'%(toid,apid)
               icorapi.DeleteObject(0,tcid,toid)
      
         ltoids=[]
         toid=icorapi.GetLastFieldValueID(0,rcid,'PID')
         while toid>=0:
            apid=icorapi.GetFieldValueInt(0,rcid,'PID',toid)
            if apid>=0:
               ltoids.append([toid,apid])
            toid=icorapi.GetPrevFieldValueID(0,rcid,'PID',toid)
         for toid,apid in ltoids:
            w=0
            try:
               handle=win32api.OpenProcess(win32con.PROCESS_TERMINATE,0,apid)
               win32api.CloseHandle(handle)
            except:
               w=1
            if w:
               print 'delete external method instance [moid: %d, pid: %d]'%(toid,apid)
               icorapi.DeleteObject(0,rcid,toid)
         if astart:
            print 'start new daemon instance'
            os.spawnv(os.P_NOWAIT,sys.executable,['"%s"'%sys.executable,DEFAULT_PROCESS_DAEMON,sys.__dict__.get('ICOR_SERVER','')])
         time.sleep(9)
   except:
      traceback.print_exc()



