# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *

def TraverseClasses(aclass):
   class CIterator(ICORRepositoryIterator):
      def __init__(self):
         ICORRepositoryIterator.__init__(self)
      def OnPreClass(self,aclass):
         InfoStatus(aclass.ClassPath)
         aobj=aclass.GetFirstObject()
         while aobj:
            aICORDBEngine.RepositoryChange('ClassRefreshObject',aclass.CID,aobj.OID,asubitem='',avalue1='',avalue2='')
            aobj.Next()
   CIterator().ForEachClass(aclass)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   adialog=InputElementDialog('Wybierz klasę',0,0)
   if adialog.Show():
      aclass=aICORDBEngine.Classes[adialog.ClassPath]
      ClearStdOut()
      TraverseClasses(aclass)
   return

