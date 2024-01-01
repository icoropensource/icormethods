# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import string,re

class C:
   x=1
   def __init__(self):
      self.a=123

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
#   set_trace()
   s='stack1'+chr(253)+'10'+chr(254)+ \
      'stack2'+chr(253)+'20'+chr(254)+ \
      'stack3'+chr(253)+'30'
   v='varName1'+chr(253)+'varValue1'+chr(253)+'string'+chr(253)+'local'+chr(253)+'pyID1'+chr(254)+ \
      'varName2'+chr(253)+'varValue2'+chr(253)+'int'+chr(253)+'local'+chr(253)+'pyID2'+chr(254)+ \
      'varName3'+chr(253)+'varValue3'+chr(253)+'float'+chr(253)+'global'+chr(253)+'pyID3'+chr(254)+ \
      'varName4'+chr(253)+'varValue4'+chr(253)+'list'+chr(253)+'global'+chr(253)+'pyID4'
   __import__('CLASSES_Library_ICORBase_Debugger_ICORDebugger').set_trace()
#   aICORDBEngine.RepositoryChange('DebuggerCallStack',-1,-1,s)
#   aICORDBEngine.RepositoryChange('DebuggerVariables',-1,-1,v)
   c=C()
   d={}
   d['a,.///\\\\b']=c
   l=[1,2,3,'aaa','bbb',string,re,ICORMain,c]
   a=1
   aclass=aICORDBEngine.Classes[CID]
   aobj=aclass.GetFirstObject()
   b=2
   c=3
   d=4
   e=5
   print 'Nacisnij Ctrl+Break...'
   for i in range(1000000):
      DoEvents()
   return



