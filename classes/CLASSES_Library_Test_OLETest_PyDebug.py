# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   import win32com
   from win32com.axdebug import debugger
   aclass=aICORDBEngine.Classes[CID]
   d = debugger.AXDebugger()
#   d.StartDebugger()
#   d.Attach()
   d.Break()
   MessageDialog('aaaa')
   return



