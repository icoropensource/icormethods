# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import InputElementDialog

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   adialog=InputElementDialog('Wybierz zestawienie',ashowsummaries=1)
   ret=adialog.Show()
   print 'ret:',ret
   print 'ItemClass:',adialog.ItemClass
   print 'ClassPath:',adialog.ClassPath
   print 'FieldName:',adialog.FieldName
   print 'MethodName:',adialog.MethodName
   print 'Value:',adialog.Value
   return



