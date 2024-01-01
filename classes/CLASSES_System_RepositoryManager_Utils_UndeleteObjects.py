# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *

class CIterator(ICORRepositoryIterator):
   def __init__(self):
      ICORRepositoryIterator.__init__(self)
   def GetFieldOIDs(self,afield,loids):
      aoid=afield.GetFirstValueID()
      while aoid>=0:
         loids.add(aoid)
         aoid=afield.GetNextValueID(aoid)
   def GetFieldOIDsDeleted(self,afield,loids):
      aoff=afield.GetFirstDeletedOffset()
      while aoff>=0:
         aoid=afield.GetRecOID(aoff)
         if aoid>=0:
            loids.add(aoid)
         aoff=afield.GetNextDeletedOffset(aoff)
   def OnPreClass(self,aclass):
      afields=aclass.GetFieldsList()
      lso=set()
      for afname in afields:
         afield=aclass.FieldsByName(afname)
         self.GetFieldOIDs(afield,lso)
         self.GetFieldOIDsDeleted(afield,lso)
      lsc=set()
      aobj=aclass.GetFirstObject()
      while aobj:
         lsc.add(aobj.OID)
         aobj.Next()
      lx=[aoid for aoid in lso if (not aoid in lsc) and (aoid<10000000)]
      lfields=aclass.GetFieldsList()
      if lfields and lx:
         afield=aclass.FieldsByName(lfields[0])
         for aoid in lx:
            st=afield[aoid]
            afield[aoid]='>>x<<'
            afield[aoid]=st
            nt=afield[aoid]
            if nt!=st:
               print aoid,aclass.CID,afield.Name,aclass.ClassPath
      if lx:
         fout=open('d:/icor/tmp/h/do_%06d_%s.txt'%(aclass.CID,aclass.ClassPath.replace('\\','_')),'w')
         fout.write(str(lx))
         fout.close()

def TraverseClasses(aclass):
   CIterator().ForEachClass(aclass)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_API_Parameter']
   TraverseClasses(aclass)

