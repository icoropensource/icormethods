# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import os

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   fname=aICORDBEngine.Variables['_ICOR_REPOSITORY_DIR']+'/MIDD/'+str(OID)+'.mfd'
   try:
      if os.path.exists(fname):
         os.unlink(fname)
   except:
      print 'plik',fname,'nie został skasowany'
   return
