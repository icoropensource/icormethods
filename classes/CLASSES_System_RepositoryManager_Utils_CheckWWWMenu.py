# -*- coding: windows-1250 -*-
# saved: 2021/06/08 16:37:27

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
from icorlib.wwwmenu.menuutil as MenuUtil import ICORWWWMenuItem

class CIterator(ICORRepositoryIterator):
   def __init__(self):
      ICORRepositoryIterator.__init__(self)
   def OnPreClass(self,aclass):
      fclasses=[aclass.ClassPath.replace('\\','_'),]
      for afield in aclass.FieldsIterator():
         if afield.ClassOfType is not None:
            fclasses.append(afield.ClassOfType.ClassPath.replace('\\','_'))
      w=0
      mrefs=aclass.GetWWWMenuRefs()
      while mrefs:
         amenu=ICORWWWMenuItem(0,mrefs.OID)
         fparamitem=amenu.ParamItem.replace('\\','_')
         if fparamitem not in fclasses:
            if not w:
               print aclass.ClassPath
               w=1
            print '   %s  - "%s"  - [%s]'%(amenu.Action,amenu.Caption,fparamitem)
         mrefs.Next()

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   sclass='CLASSES_DataBase'
   aclass=aICORDBEngine.Classes[sclass]
   aiterator=CIterator()
   aiterator.ForEachClass(aclass)

