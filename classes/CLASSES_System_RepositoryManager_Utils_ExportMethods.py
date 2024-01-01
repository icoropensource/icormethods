# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
import string

def TraverseClasses(aclass,adir):
   class CIterator(ICORRepositoryIterator):
      def __init__(self,adir):
         ICORRepositoryIterator.__init__(self)
         self.Directory=adir
      def OnPreMethod(self,aclass,amethodname):
         amethod=aclass.MethodsByName(amethodname)
         aname=string.replace(aclass.ClassPath,'\\','_')+'_'+amethodname+'.py'
         print aname
         afile=open(self.Directory+'\\'+aname,'w')
         try:
            afile.write(amethod.MethodText)
         finally:
            afile.close()
   CIterator(adir).ForEachClass(aclass)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   adialog=InputElementDialog('Wybierz klasę',0,0)
   if adialog.Show():
      aclass=aICORDBEngine.Classes[adialog.ClassPath]
      adir=InputDirectory()
      if adir=='':
         return
      ClearStdOut()
      TraverseClasses(aclass,FilePathAsSystemPath(adir))
   return
