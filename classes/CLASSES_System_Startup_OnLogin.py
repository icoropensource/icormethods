# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   return
   aICORDBEngine.Variables['_LoginUser']='User'
   aICORDBEngine.Variables['_LoginPassword']=''
   ret=InputPassword()
   if ret!='-1':
      print 'User:',aICORDBEngine.Variables['_LoginUser']
      print 'Password:',aICORDBEngine.Variables['_LoginPassword']
   aICORDBEngine.Variables['_LoginPassword']=''
   return
