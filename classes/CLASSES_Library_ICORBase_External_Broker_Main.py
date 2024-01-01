# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

import os
import time
import threading
import win32api,win32security,win32con
import CLASSES_Library_ICORBase_External_Broker_Communicator
import CLASSES_Library_ICORBase_External_Broker_Config
import CLASSES_Library_ICORBase_External_Broker_Process
brokercommunicator=CLASSES_Library_ICORBase_External_Broker_Communicator
brokerinfo=CLASSES_Library_ICORBase_External_Broker_Config
brokerprocess=CLASSES_Library_ICORBase_External_Broker_Process

class Impersonate:
   def __init__(self,user,password,domain=None):
      self.domain=domain or '.'
      self.user=user
      self.password=password
   def logon(self):
      self.handel=win32security.LogonUser(
         self.user,
         self.domain,
         self.password,
         #win32security.LOGON32_LOGON_NETWORK, #
         win32con.LOGON32_LOGON_INTERACTIVE,
         win32con.LOGON32_PROVIDER_DEFAULT)
      win32security.ImpersonateLoggedOnUser(self.handel)
   def logoff(self):
      win32security.RevertToSelf() #terminates impersonation
      self.handel.Close() #guarantees cleanup

class Runner(threading.Thread):
   def __init__(self,broker,no):
      threading.Thread.__init__(self,name='Runner')
      self.no = no
      self.broker = broker
      self.pipename = self.broker.procpip %no
      # ustawic jezeli ma sie uruchomic
      self.evtRunning= threading.Event()
      self.evtRunning.clear()
      # ustawic jezeli proces ma byc zabity
      self.evtQuit = threading.Event()
      self.evtQuit.clear()
      # ustawiony jezeli wystartowal
      self.evtStarted = threading.Event()
      self.evtStarted.clear()
   def startProcess(self):
      self.evtRunning.set()
   def isRunning(self):
      return self.evtRunning.isSet()
   def stopProcess(self):
      self.evtQuit.set()
   def doquit(self,p):
      if p.IsActive():
         p.Thread.ResetThread(199)
         while p.IsActive():
            time.sleep(0.1)
   def run(self):
      p = brokerprocess.Process()
      p.CommandLine='%s %s' %(self.broker.procapp, self.pipename)
      p.Directory=os.getcwd()
      times = 0
      while 1:
         self.evtStarted.clear()
         self.evtRunning.clear()
         self.evtRunning.wait()
         if self.evtQuit.isSet():
            self.doquit()
            return
         p.Execute()
         self.evtStarted.set()
         if not p.IsActive():
            print 'startup failed! rc=',p.ExitCode,'commandline:',p.CommandLine
            return
         while p.IsActive():
            time.sleep(0.1)
            if self.evtQuit.isSet():
               self.doquit()
               return
         print p.CommandLine,'down with rc=',p.ExitCode

def handle(c,cmd,cond):
   r = None
   while not r:
      cond.acquire()
      for t in threading.enumerate():
         if t.getName() == 'Runner':
            if t.isRunning() or t.broker.proccmd != cmd:
               continue
            if not r:
               r = t
            elif t.no < r.no:
               r = t
      if not r:
         cond.release()
#         print 'brak wolnych slotow dla',cmd
         time.sleep(0.1)
#   print 'start:',r.broker.procapp, r.pipename
   r.evtRunning.set()
   r.evtStarted.wait()
#   time.sleep(2)
   c.Output('\\\\.\\pipe\\%s' %r.pipename,1)
   c.Close()
   cond.release()

def server():
   for k,v in brokerinfo.brokers.items():
      for i in range(v.procmin):
         r=Runner(v,i)
         r.start()
   cond = threading.Semaphore()
#   a=Impersonate('icorisapi','icorisapi','.')
#   a.logon() #become the user
#   print 'whoami?',win32api.GetUserName() #show you're someone else
   while 1:
      c=brokercommunicator.CommunicatorServer('ICORPROCESSBROKER')
      try:
         cmd = c.Input()
         print 'cmd=',cmd
         if cmd == "PING":
            c.Output('PONG',1)
         elif cmd[:5] == 'DONE ':
            cond.acquire()
            cmd = cmd[5:]
            for t in threading.enumerate():
               if t.getName() == 'Runner':
                  if t.pipename == cmd:
                     t.evtRunning.clear()
                     break
            cond.release()
         elif cmd == 'INFO':
            cond.acquire()
            for t in threading.enumerate():
               if t.getName() == 'Runner':
                  print t.isRunning(), t.broker.procapp, t.pipename
            cond.release()
         else:
            broker = brokerinfo.brokers.get(cmd,None)
            if not broker:
               print 'what?: %s' %cmd
            else:
               t=threading.Thread(target=handle,args=(c,cmd,cond))
               t.start()
               continue
         c.Close()
      except:
         c.Close()
         return

def main():
   th = threading.Thread(target=server,name='server')
   th.start()

#main()




