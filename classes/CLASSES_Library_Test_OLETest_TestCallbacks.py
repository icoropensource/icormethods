# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

import copy_reg
from CLASSES_Library_ICORBase_Interface_ICORInterface import *

import pythoncom
from win32com.server import util,dispatcher
from win32com.client import gencache,Dispatch,dynamic

#Microsoft Script Control 1.0
scLib=gencache.EnsureModule("{0E59F1D2-1FBE-11D0-8FF2-00A0D10038BC}", 0, 1, 0)

class function:
   _public_methods_ = [
      ]
   def __init__(self,cb):
      self.cb=cb
   def _invokeex_(self, dispid, lcid, wFlags, args, kwargs, serviceProvider):
#      print '_invokeex_',args,kwargs
      if len(args)==0:
         return self.cb()
      else:
         return apply(self.cb,args)

def wrapFunction(cb):
   obj=util.wrap(
      function(cb),
      useDispatcher=dispatcher.DispatcherBase
      )
   return dynamic.Dispatch(
      obj
      )

def myproc():
   print 'in myproc'
   return 1

def main():
   cbMyProc=wrapFunction(myproc)
   sc=scLib.ScriptControl()
   sc.Language = "VBScript"
   vbCode="""
function NameMe()
   Dim strName 'As String
   strName = InputBox("Name?")
   MsgBox "Your name is " & strName
   NameMe=strName
end function 
function IGetref(outproc)
   MsgBox "IGetref"
   outproc
   set IGetref=getref("NameMe")
end function
"""
   sc.AddCode(vbCode)
#   sc.Run("NameMe")
   x=sc.CodeObject.IGetref(cbMyProc)
#   print x
   rc=x()
   print 'x()=',rc

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   main()
   return


