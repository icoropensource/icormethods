# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def DoCustomPageByMethod(menu,file):
   aICORDBEngine.Refresh(asystem=1)
   aclass=aICORDBEngine.Classes['CLASSES_Library_NetBase_WWW_Administration_Security']
   aclass.DoWWWClearCache()
   file.write('<h1>Synchronizacja cache uruchomiona</h1>')

