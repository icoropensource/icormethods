# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

import time
import threading
import win32api
import win32event
import win32process
import win32con

class ProcessThread(threading.Thread):
   def __init__(self, aOwner):
      threading.Thread.__init__(self, name="ProcessThread")
      self.pinfo = None
      self.Owner = aOwner
   def run(self):
      self.Execute()
   def IsActive(self):
      return self.pinfo is not None
   def ResetThread(self, force):
      if self.IsActive():
         hProcess,hThread,dwProcessID,dwThreadID=self.pinfo
         dwExitCode = win32process.GetExitCodeProcess( hProcess )
         self.Owner.OnTerminate( dwExitCode )
         if hProcess:
            if force:
               dwExitCode = win32process.TerminateProcess( hProcess, force )
            win32api.CloseHandle( hProcess )
         if hThread:
            win32api.CloseHandle( hThread )
      self.pinfo = None
      self.Owner.Thread = None
   def Execute(self):
      StartupInfo = win32process.STARTUPINFO()
      flags=win32con.CREATE_DEFAULT_ERROR_MODE|win32con.CREATE_NO_WINDOW|win32con.DETACHED_PROCESS
      
      flags=win32con.CREATE_NEW_CONSOLE
#      flags=flags|win32con.IDLE_PRIORITY_CLASS
      flags=flags|win32con.CREATE_DEFAULT_ERROR_MODE

      try:
         self.pinfo=win32process.CreateProcess(
            self.Owner.AppName,   # program
            self.Owner.CommandLine,   # command line
            None,         # process security attributes
            None,         # thread security attributes
            0,         # inherit handles
            flags,         # startup flags
            None,         # environment
            self.Owner.Directory,   # startup directory
            StartupInfo)      # startup info
      except:
         self.pinfo = None
      self.Owner.startevent.set()
      if self.pinfo:
         hProcess,hThread,dwProcessID,dwThreadID=self.pinfo
#         ovReturn = win32api.WaitForInputIdle( hProcess, win32event.INFINITE )
#         self.Owner.OnIdle()
         rc = win32con.WAIT_TIMEOUT
         while (rc != win32con.WAIT_OBJECT_0):
            rc = win32event.WaitForSingleObject( hProcess , 1000 )
      self.ResetThread(0)

class Process:
   def __init__(self):
      self.AppName = None
      self.CmdLine = ''
      self.ShowWindow = 1
      self.Directory = ''
      self.Thread = None
      self.ExitCode = -1
      self.startevent = threading.Event()
   def Execute(self):
      if not self.IsActive():
         self.startevent.clear()
         self.Thread = ProcessThread( self )
         self.Thread.start()
         self.startevent.wait()
   def OnTerminate(self,exitcode):
      self.ExitCode = exitcode
      self.Thread = None
   def OnIdle(self):
      pass
   def IsActive(self):
      return self.Thread is not None




