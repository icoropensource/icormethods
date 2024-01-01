# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

import sys
import gc
import os
import time
import string
import binascii
import struct
import thread
import win32security
import _winreg
import base64
import win32api

def hex2int(anum):
   return struct.unpack('>i',binascii.unhexlify(anum))[0]

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_External_MLog as MLog

LOG=aICORDBEngine.Variables['_ICOR_BASE_DIR']+'/log/iis_batch.log'

class ExecutorMain:
   def __init__(self):
      self.running=0        
      self.returnValue='<h1>ICOR</h1>'
      key=_winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,'SOFTWARE\\Mikroplan\\ICOR\\GeneralOptions')
      try:
         aicorbasedir,atype=_winreg.QueryValueEx(key,'ICORBaseDir')
         auser,atype=_winreg.QueryValueEx(key,'IIS_USER_Name')
         self.user=auser.encode('cp1250')
         apassword,atype=_winreg.QueryValueEx(key,'IIS_USER_Password')
         self.password=base64.decodestring(apassword.encode('cp1250'))
         aWP_IDLE_TIME,atype=_winreg.QueryValueEx(key,'WP_IDLE_TIME')
         aWP_MAX_MEMORY_TERMINATE,atype=_winreg.QueryValueEx(key,'WP_MAX_MEMORY_TERMINATE')
         aWP_MAX_MEMORY_SWAP,atype=_winreg.QueryValueEx(key,'WP_MAX_MEMORY_SWAP')
         aWP_MAX_WORK_TIME,atype=_winreg.QueryValueEx(key,'WP_MAX_WORK_TIME')
         self.WP_IDLE_TIME,self.WP_MAX_MEMORY_TERMINATE,self.WP_MAX_MEMORY_SWAP,self.WP_MAX_WORK_TIME=int(aWP_IDLE_TIME),int(aWP_MAX_MEMORY_TERMINATE),int(aWP_MAX_MEMORY_SWAP),int(aWP_MAX_WORK_TIME)
         try:
            self.WP_IMPERSONATION_DISABLED,atype=_winreg.QueryValueEx(key,'WP_IMPERSONATION_DISABLED')
            self.WP_IMPERSONATION_DISABLED=int(self.WP_IMPERSONATION_DISABLED)
         except:
            self.WP_IMPERSONATION_DISABLED=0
         try:
            self.domain,atype=_winreg.QueryValueEx(key,'IIS_USER_Domain')
            self.domain=adomain.encode('cp1250')
         except:
            self.domain=''
         if not self.domain:
            self.domain=None
         if not self.user:
            self.WP_IMPERSONATION_DISABLED=1
      finally:
         key.Close()
   def starttimer(self):
      self.time=time.time()
      thread.start_new_thread(self.timer,())
   def start(self,afunction,aargs):
      self.returnValue='<h1>ICOR</h1>'
      self.function=afunction
      self.args=aargs
      self.running=1
      thread.start_new_thread(self.run,())
   def login(self):
      if self.user==win32api.GetUserName():
         return
      if not self.WP_IMPERSONATION_DISABLED:
         try:
            uHandle=win32security.LogonUser(self.user,self.domain,self.password,win32security.LOGON32_LOGON_INTERACTIVE,win32security.LOGON32_PROVIDER_DEFAULT)
            win32security.ImpersonateLoggedOnUser(uHandle)
         except:
            raise
   def logout(self):
      if not self.WP_IMPERSONATION_DISABLED:
         win32security.RevertToSelf()
   def run(self):
      self.login()
      try:
         try:
            self.returnValue=apply(self.function,self.args)
            if self.returnValue is None:
               self.returnValue=''
            elif type(self.returnValue)!=type(''):
               self.returnValue=str(self.returnValue)
         except:
            MLog.LogException(fname=LOG,aconsole=1)
      finally:
         self.time=time.time()
         self.running=0
         self.logout()
   def timer(self):
      self.login()
      while 1:
         if not self.running:
            tt=time.time()
            if (tt-self.time)>self.WP_IDLE_TIME:
               try:
                  win32api.Beep(2000,40)
                  win32api.Beep(4000,40)
                  win32api.Beep(4000,40)
                  win32api.Beep(3000,40)
               except:
                  pass
               hProcess=win32api.GetCurrentProcess()
               win32api.TerminateProcess(hProcess,0)
         time.sleep(self.WP_IDLE_TIME/2)

def Start():
   MLog.Log('START X',fname=LOG,aconsole=0)
   saveout=MLog.MemorySysOutWrapper(asetbinary=1,apidinclude=1,aicorstdoutprint=1)
   try:
      aexception=0
      athread=ExecutorMain()
      if 0:
         try:
            MLog.Log('USER ?: ',fname=LOG,aconsole=0)
            MLog.Log('USER 1: '+str(win32api.GetUserName()),fname=LOG,aconsole=0)
            athread.login()
            MLog.Log('USER 2: '+str(win32api.GetUserName()),fname=LOG,aconsole=0)
         except:
            MLog.Log('EXCEPTION',fname=LOG,aconsole=0)
            MLog.LogException(fname=LOG,aconsole=0)
            raise
      athread.starttimer()
      hProcess=win32api.GetCurrentProcess()

      alrclass=aICORDBEngine.Classes[STARTUP_CLASS_LOCATION]
      alroid=alrclass.FirstObject()
      blastrefreshtime=alrclass.LastProcessPoolRefresh.ValuesAsDateTime(alroid)

      while 1 and not aexception:
         amsg=saveout.sysin.read(8)
         amsgid=hex2int(amsg)
#         MLog.Log('MSGID: '+str(amsgid),fname=LOG,aconsole=0)
         if amsgid==1: # ECHO+SLEEP
#            time.sleep(5)
            alen=hex2int(saveout.sysin.read(8))
            ret=saveout.sysin.read(alen)
            ret='{'+str(os.getpid())+'}['+ret+']'
            saveout.sysout.write('%08x'%len(ret))
            saveout.sysout.write(ret)
         elif amsgid==2 or amsgid==3: # EXECUTE_METHOD OR EXECUTE_METHOD_NO_WAIT
            UID=hex2int(saveout.sysin.read(8))
            alen=hex2int(saveout.sysin.read(8))
            amethodpath=saveout.sysin.read(alen)
            alen=hex2int(saveout.sysin.read(8))
            afieldname=saveout.sysin.read(alen)
            aoid=hex2int(saveout.sysin.read(8))
            alen=hex2int(saveout.sysin.read(8))
            avalue=saveout.sysin.read(alen)
            ret=''
            try:
               amethodpath=string.replace(amethodpath,'\\','_')
               amethodpath=string.replace(amethodpath,'/','_')
               lm=string.split(amethodpath,'_')
               aclasspath=string.join(lm[:-1],'_')

               alrclass=aICORDBEngine.Classes[STARTUP_CLASS_LOCATION]
               alroid=alrclass.FirstObject()
               alastrefreshtime=alrclass.LastProcessPoolRefresh.ValuesAsDateTime(alroid)
               if blastrefreshtime!=alastrefreshtime:
                  blastrefreshtime=alastrefreshtime
                  aICORDBEngine.Refresh(asystem=1)
                  MLog.Log('REFRESH',fname=LOG,aconsole=0)

               mclass=aICORDBEngine.Classes[aclasspath]
               amethodpath=amethodpath.replace('\\','_')
               amethodpath=amethodpath.replace('/','_')
               pagemethod=__import__(amethodpath)
               athread.start(pagemethod.ICORMain,(mclass.CID,afieldname,aoid,avalue,UID))
               tstart=time.time()
               while 1:
                  if athread.running:
                     tfinish=time.time()
                     tt=tfinish-tstart
                     if amsgid==2 and tt>athread.WP_MAX_WORK_TIME:
                        MLog.Log('TIME LIMIT',fname=LOG,aconsole=0)
                        break
                     if amsgid==2:
                        saveout.sysout.write('TIM')
                  else:
                     break
                  time.sleep(0.1)
            except:
               if amsgid==2:
                  saveout.sysout.write('EXC')
               aexception=1
               athread.returnValue='### EXCEPTION ###'
               if amsgid==2:
                  saveout.LogException()
               MLog.LogException(fname=LOG,aconsole=0)
            if amsgid==2:
               saveout.sysout.write('DAT')
               saveout.sysout.write('%08x'%len(athread.returnValue))
               saveout.sysout.write(athread.returnValue)
            if amsgid==3:
               break
         elif amsgid==99: # QUIT
            MLog.Log('QUIT',fname=LOG,aconsole=0)
            break   
         gc.collect()
         time.sleep(0.00001)
   finally:
      saveout.Restore()
      try:
         win32api.Beep(3000,150)
         win32api.Beep(5000,100)
      except:
         pass
      MLog.Log('TERMINATE',fname=LOG,aconsole=0)

def Main():
   try:
      Start()
   except:
      MLog.LogException(fname=LOG,aconsole=0)



