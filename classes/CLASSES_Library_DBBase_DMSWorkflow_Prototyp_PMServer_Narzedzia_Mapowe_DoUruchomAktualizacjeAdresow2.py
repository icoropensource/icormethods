# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil
import CLASSES_Library_ICORBase_External_MLog as MLog
import CLASSES_Library_ICORBase_Interface_ICORSync as ICORSync
import string
import os

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   saveout=MLog.MemorySysOutWrapper()
   sok='OK'
   smessage='Import zakończono powodzeniem'
   try:
      try:
         astate=FieldName            
         fname=aICORDBEngine.Variables['_ICOR_BASE_DIR']+'/util/Korespondencja/Adresy/mi2sok2.cmd'
         os.spawnv(os.P_WAIT,fname,['"'+fname+'"',])
      except:
         sok='BAD'
         smessage='Wystąpił błąd podczas importu danych'
         import traceback
         traceback.print_exc()
         import win32api
         try:
            for i in range(100):
               win32api.Beep(500-i*2,2)
         except:
            pass
   finally:
      if astate:
         bstate=ICORSync.ICORState(int(astate))
         bstate.Name=smessage
         bstate.Value=sok
      saveout.Restore()
      import win32api
      try:
         win32api.Beep(5000,100)
         win32api.Beep(3000,150)
      except:
         pass

   return




