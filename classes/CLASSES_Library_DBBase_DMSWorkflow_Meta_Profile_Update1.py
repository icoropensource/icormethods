# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORSync as ICORSync

import CLASSES_Library_ICORBase_Interface_ICORSearch as ICORSearch

class Test1:
   def __init__(self,aclass,aoidmin,aoidmax):
      self.objectclass=aclass
      self.oidfrom=aoidmin
      self.oidto=1+aoidmax
   def Process(self):
      self.classreffields=[]
      self.objectclass.ForEachDerivedClass(self.DeleteObjectsInRange,self.oidfrom,self.oidto)
      for afield in self.classreffields:
         aoid=afield.GetFirstValueID()
         while aoid>=0:
            arefs=afield.GetRefList(aoid)
            w=arefs.DelRefsInRange(self.oidfrom,self.oidto)
            if w:
               print '   DELREFS:',aoid,afield.ClassItem.ClassPath,'|',afield.Name
#                  arefs.Store()
            aoid=afield.GetNextValueID(aoid)
   def DeleteObjectsInRange(self,aclass,aoidfrom,aoidto):
      l=aclass.GetObjectsInRange(aoidfrom,aoidto)
      if l:
         print 'DELETEOBJECTS:',aclass.ClassPath,aclass.NameOfClass,aoidfrom,aoidto,l[:10]
         lfields=aclass.GetReferencingFields()
         self.classreffields.extend(lfields)
#         for aoid in l:
#            aclass.DeleteObject(aoid)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]

   sclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow']
   aoidmin=23000
   aoidmax=23999
   ctest1=Test1(sclass,aoidmin,aoidmax)
   ctest1.Process()


   return
   aobj=aclass[2]
   amode='build'
   aobj.Class.DoExecute('',aobj.OID,amode)
   return


