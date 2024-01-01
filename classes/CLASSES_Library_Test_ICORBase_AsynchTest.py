# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

import random
import thread
import time
import os

running = 0
next_ident = 0
numtasks = 10

def task(ident,mutex,whmutex,done):
        global running,aoutput
        whmutex.acquire()
        delay = random.random() * numtasks
        print 'task '+str(ident)+'will run for '+str(round(delay,1))+' sec'
        whmutex.release()
        time.sleep(delay)
        mutex.acquire()
        print 'task '+str(ident)+' done'
        running = running - 1
        if running == 0:
                done.release()
        mutex.release()

def newtask(mutex,whmutex,done):
        global next_ident, running,aoutput
        mutex.acquire()
        next_ident = next_ident + 1
        print 'creating task '+str(next_ident)+''
        thread.start_new_thread(task, (next_ident,mutex,whmutex,done))
        running = running + 1
        mutex.release()

def RunTest():
   global aoutput
   mutex = thread.allocate_lock()
   whmutex = thread.allocate_lock() # for calls to random
   done = thread.allocate_lock()
   done.acquire()
   
   for i in range(numtasks):
           newtask(mutex,whmutex,done)
   
   print 'waiting for all tasks to complete'
   done.acquire()
   print 'all tasks done'

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
#   import ICORDelphi
#   DEFAULT_PROCESS_DAEMON='"'+ICORDelphi.GetVariable(0,'_DEFAULT_PYTHON_TOP_DIR')+'/External/default/redaemon.py'+'"' #
#   DEFAULT_PROCESS_EXECUTOR=ICORDelphi.GetVariable(0,'_DEFAULT_PROCESS_EXECUTOR')
#   os.spawnv(os.P_NOWAIT,DEFAULT_PROCESS_EXECUTOR,['"'+DEFAULT_PROCESS_EXECUTOR+'"',DEFAULT_PROCESS_DAEMON]) #
#   return
   aclass=aICORDBEngine.Classes[CID]
#   RunTest()
   for i in range(30):
#      aclass.QueuedTest1(OID=i)
      aclass.ParallelAccess(OID=i+1)
   print 'KONIEC'
   return
