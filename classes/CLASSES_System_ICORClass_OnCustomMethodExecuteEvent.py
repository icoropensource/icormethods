# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil
import string

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   plist=string.split(FieldName,':')
   if len(plist)<3:
      return ''
   bcid=int(plist[0])
   bmethod=plist[1]
   bfield=plist[2]
   bclass=aICORDBEngine.Classes[bcid]
   if bclass is None:
      return ''
   bmi=bclass.MethodsByName(bmethod)
   if bmi is None:
      return ''
   if bmi.Language in ['Python','']:
      bmi(bfield,OID,Value,UID)
      return
   if bmi.Language=='JavaScript':
      print 'm1'
      import PyV8
      print 'm2'
      class Global(object):
         def Adder(self,a,b):
            return a+b
         def hello(self):
            print "Hello World"
         def echo(self,s):
            print s
         def Print(self,s):
            print s
      g=Global()
      print 'm3'
      engine=PyV8.JSEngine(g)
      print 'm4'
      ret=engine.eval(bmi.MethodText)
      print 'm5'
      print 'r',ret
      return ret
   print bmi.Language,'- method language not implemented'
   return ''

