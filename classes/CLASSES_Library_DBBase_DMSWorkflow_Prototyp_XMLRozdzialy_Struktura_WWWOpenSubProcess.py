# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import subprocess

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   if Value:
      p=subprocess.Popen(Value,shell=False)
   return

