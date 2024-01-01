# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

""" FlogThreadQueue..    flognat@fukt.hk-r.se

Third genetion version 1.0

Manage a queue of threads.. well basically, you have for example a
whole lot of webpages you want processed, it is booring getting
them one by one, so why not fetch 10 and process 10 pages in
parallell, works nice because most of the time is waiting for the
pages to come to your computer..

What to do?? Something like:

----------------------------------------

urls[ (many urls here) ]
def processURL(url)
    ... process function ...

import FTHRQueue

queue=FTHRQueue.THRQueue(10) # 10 at a time.. 

for url in urls:
    queue.append(processURL, url) #wroom.. put them all in the Q
                            # the processing of the Q is instantly
                            # started!!

queue.waittilfinished(FTHRQueue.reporter, 30)
             # well if this functioncall weren't here the interpreter
             # would probably exist and kill all threads with it, and
             # it calls the function FTHRQueue.reporter every 30 mins,
             # which prints some info about the queue status.. 

----------------------------------------

it is possible appending stuff to the queue inside a queued item, for
example above..
def processURL(url, queue):
    [...]
    for url in urlsIn(url):
        queue.append(processURL, (url, queue))

for url in urls:
    queue.append(processURL, url)

and we have a threaded web-spider :-)
    
You can also append instances of classes with functionality as the
Thread class to be able to control the thread more, and get status..

The functions that can be used by THRQueue are:
    * kill: send a signal to the thread to die, can for example set a
            flag that is checked in a loop, should return 1 if the
            thread exists gracefully and tells the queue that it
            exits.
            Should return 0 if it can't control the thread, and the
            queue will forget it and continue to the next thread in Q.

 These are report-functions that can be used by the user to monitor
 the queue.. 

    * __str__: return a description of the thread
    * status : return the status of the thread.. 
    
Well to test.. do something like:

>>> from FTHRQueue import *
>>> queue=THRQueue(3)  # starts a queue of the length 3
>>> test(queue)  # insert a bunch of threads into the queue, and start
                 # running
>>> Thread ID: 1, Sleeptime: 10, Counter: 0  #output
Thread ID: 2, Sleeptime: 10, Counter: 0
Thread ID: 3, Sleeptime: 10, Counter: 0
Thread ID: 1, Sleeptime: 10, Counter: 1
Thread ID: 2, Sleeptime: 10, Counter: 1
Thread ID: 3, Sleeptime: 10, Counter: 1
queue.kill(2)  #type THIS, we still got a prompt! 
Thread ID: 1, Sleeptime: 10, Counter: 3  # well the threads has 
Thread ID: 2, Sleeptime: 10, Counter: 3  # to iterate.. 
Thread ID: 3, Sleeptime: 10, Counter: 3
I, 2 don't feel needed anymore.. 
Thread ID: 4, Sleeptime: 10, Counter: 1  # whoah a new thread :-)
Thread ID: 2, Sleeptime: 10, Counter: 4
Thread ID: 3, Sleeptime: 10, Counter: 4

Reference:

    What to do with THRQueue
    ** THRQueue(length, debug=None)
    well the length of the queue, if debug=1 instead of starting new
    threads, the code will be executed immideately by append
    ** status() returns a string with some status info
    ** age(ID) returns the age of the thread with id ID
    ** ages() returns a list of (ID, age) for all the running threads
    ** setthreads(no) changes the size of the queue
    ** append(data) appends data to the end of the queue, where
       data can be either an instance of Thread or similar class
       or function, (args)
    ** kill(ID) send a kill or stop signal to the thread.. it is up to
       the thread itself to catch it!!
       
    ** waittilfinished(reporter=None, gran=5) waits til the queue is finished
       and calls reporter with self as parameter every gran seconds.
       
"""

import sys
import time
import thread

MAXTHREADS=10

# prints queue status and age of the currently running threads
# in the format ID:age(in seconds), ID:age, ID;age,
def reporter(queue):
    str="  "
    for ID, age in queue.ages():
        str=str+("%i:%i, " % (ID, age))
    str=str+"\n"
    sys.stdout.write(time.strftime("%H:%M:%S %m/%d/%y ",
                                   time.localtime(time.time())) + \
                     queue.status()+"\n"+str)

# A locker that can 'snooze' to avoid one possible
# kind of deadlock(?)

SNOOZETIME=3

NONBLOCK=0
BLOCKING=1
SNOOZING=2

class Lock:
    def __init__(self, blocking=BLOCKING, snooze=SNOOZETIME,
                 messenger=None):
        self._blocking=blocking
        self._snooze=snooze
        self._messenger=messenger
        self._lock=thread.allocate_lock()

    def acquire(self, flag=None):
        if flag!=None:
            return self._lock.acquire(flag)

        if self._blocking==NONBLOCK:
            return self._lock.acquire(0)
        if self._blocking==BLOCKING:
            return self._lock.acquire(1)
        if self._blocking==SNOOZING:
            while not self._lock.acquire(0):
                if self._messenger:
                    self._messenger.write("Couldn't acquire lock, snoozing\n")
                time.sleep(self._snooze)
            return 1
            
    def release(self):
        return self._lock.release()
    
    def locked(self):
        return self._lock.locked()

class Thread:
    def __init__(self, function, args=None, messenger=None):
        self._function=function
        self._endthread=None

        if not args:
            self._args=()
        elif type(args)!=type(()):
            self._args=(args,)
        else:
            self._args=args

        self._messenger=messenger
            
        self._started=0
        self.ID=None
        self._status='WAITING'
        
    def setID(self, ID):
        self.ID=ID

    def go(self, endthread=None):
        if endthread:
            self._endthread=endthread
        sys.stdout.flush()
        self._started=time.time()
        ok=0
        try:
            self._status='RUNNING'
            sys.stdout.flush()
            apply(self._function, self._args)
            self._status='DONE'
            ok=1
        finally:
            if not ok:
                if self._messenger:
                    self._messenger.write("Exception in thread for %s\n"
                                          % str(self))
            if self._endthread:
                self._endthread(self.ID)
        
    def kill(self):
        # Well no thread control, lets just forget about us..
        if self._endthread:
            self._endthread(self)
        self._endthread=None
        
    def __str__(self):
        return str(self._args)
        
    def age(self):
        return not self._started or time.time()-self._started

    def status(self):
        return self._status

class THRQueue:
    def __init__(self, noofthreads=MAXTHREADS, closefunction=None,
                 debug=None, messenger=None):
        self._BLOCK=Lock(SNOOZING)
        self._WORKING=Lock(BLOCKING)

        self._noofthreads=0
        self._maxthreads=noofthreads
        self._debug=debug
        self._messenger=messenger

        self._counter=1
        self._queue=[]
        self._running={}

    def status(self):
        return "Threads left: %i, threads running: %i" % \
               (len(self._queue), len(self._running))
    
    def age(self, ID):
        return self._running[ID].age()
        
    def ages(self):
        list=[]
        for ID, thr in self._running.items():
            list.append((ID,thr.age()))
        return list

    def isempty(self):
        if len(self._queue)==0 and len(self._running)==0:
            return 1
        return 0

    def isalmostempty(self):
        if len(self._queue)==0 and len(self._running)<self._maxthreads:
            return 1
        return 0
    def getstats(self):
        return len(self._queue),len(self._running),self._maxthreads
        
    def deepstatus(self):
        list=[]
        for ID, thr in self._running.items():
            list.append((ID,thr.age(),thr.status()))
        return list
        
    def getthreads(self):
        return self._maxthreads

    def setthreads(self, number):
        self._maxthreads=number

    def append(self, *args):
        if len(args)==1:
            thr=args[0]
        elif len(args)==2:
            thr=Thread(args[0], args[1])
        else:
            raise "ERROR"

        if self._debug:
            thr.go()
        else:
            try:
                self._BLOCK.acquire()
                self._append(thr)
            finally:
                self._BLOCK.release()
            self.startthread()
        
    # wraps an exception block, and lock around append
    def _append(self, thr):
        thr.setID(self._counter)
        self._counter=self._counter+1
        self._queue.append(thr)
        
    def kill(self, ID):
        thr=self._running[ID]
        # well if the thread won't exit gracefully, we just.. forget about it
        if not thr.kill():
            self.endthread(ID)
            
    #wraps an exception block, and lock around startthread
    def startthread(self):
        try:
            self._BLOCK.acquire()
            self._startthread()
        finally:
            self._BLOCK.release()
            
    def _startthread(self):
        if not self._WORKING.locked():
            self._WORKING.acquire()
            
        while len(self._queue)>0 and len(self._running)<self._maxthreads:
            thr=self._queue[0]
            self._queue=self._queue[1:]
            self._running[thr.ID]=thr
            thread.start_new_thread(thr.go, (self.endthread, ))

        if len(self._queue)==0 and len(self._running)==0:
            # Ok we are done
            self._WORKING.release()

    #wraps an exception block, and lock around endthread
    def endthread(self, ID):
        try:
            self._BLOCK.acquire()
            self._endthread(ID)
        finally:
            self._BLOCK.release()
        self.startthread()
        
    def _endthread(self, ID):
        del self._running[ID]

    def waittilfinished(self, callbackfunction=None, gran=5):
        if callbackfunction:
            while self._WORKING.locked():
                # Lets give the system time to get up.. 
                time.sleep(gran)
                callbackfunction(self)
        else:
            self._WORKING.acquire(1)
            self._WORKING.release()

class TestThread(Thread):
    def __init__(self, args=None):
        Thread.__init__(self, self.runner, args)
        self.counter=0
        self.stop=0
        
    def runner(self, sleeptime):
        # Wait for the stop signal.
        while not self.stop and self.counter < 15:
            print "Thread ID: %i, Sleeptime: %i, Counter: %i" % \
                  (self.ID, sleeptime, self.counter)
            self.counter=self.counter+1
            time.sleep(sleeptime)
        if self.stop:
            print "I, %i don't feel needed anymore" % self.ID
        print "Bye"
        
    def kill(self):
        self.stop=1
        return 1

def test1(queue):
    for i in range(10):
        queue.append(TestThread(20))

def testfun(roof, sleeptime):
    counter=0
    while counter < roof:
        print "Counting to %i, at %i, sleeping %i" % \
              (count, counter, sleeptime)
        counter=counter+1
        time.sleep(sleeptime)
    print "Done, roof reached.. bye bye"
  
def test2(queue):
    import rand
    for i in range(20):
        queue.append(testfun, (rand.choice(range(20)),
                               rand.choice(range(5,20))) )
    queue.waittilfinished(reporter, 15)



