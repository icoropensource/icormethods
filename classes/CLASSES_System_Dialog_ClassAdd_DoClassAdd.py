# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
import string

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   ClearStdOut()
   if OID==-1:
      adialog=InputElementDialog('Wybierz klasę',0,0)
      if not adialog.Show():
         return
      bclass=aICORDBEngine.Classes[adialog.ClassPath]
      if bclass is None:
         return
      OID=bclass.CID
   if Value=='':
      Value=InputString('Nowa klasa','Nazwa:','')
      if Value=='':
         return
   if OID!=-1 and Value!='':
      aICORDBEngine.Classes.AddClass(OID,Value)
   return
