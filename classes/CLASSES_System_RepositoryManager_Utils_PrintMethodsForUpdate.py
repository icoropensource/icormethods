# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
import string

def TraverseClasses(aclass):
   class CIterator(ICORRepositoryIterator):
      def __init__(self):
         ICORRepositoryIterator.__init__(self)
      def OnPreMethod(self,aclass,amethodname):
         amethod=aclass.MethodsByName(amethodname)
         print "['%s','%s'],"%(string.replace(aclass.ClassPath,'\\','_'),amethodname)
   CIterator().ForEachClass(aclass)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   adialog=InputElementDialog('Wybierz klas�',0,0)
   if adialog.Show():
      aclass=aICORDBEngine.Classes[adialog.ClassPath]
      ClearStdOut()
      TraverseClasses(aclass)
   return

