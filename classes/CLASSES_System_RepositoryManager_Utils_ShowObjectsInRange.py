# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil

class Checker:
   def __init__(self):
      pass
   def Start(self):
      oclass=aICORDBEngine.Classes['CLASSES_System_Security_OIDRange']
      orefs=oclass.SelectObjects('Wybierz zakresy OID')
      lrefs=[]
      while orefs:
         lrefs.append([orefs.Name.ValuesAsComp(orefs.OID),orefs.IDMin.ValuesAsComp(orefs.OID),orefs.IDMax.ValuesAsComp(orefs.OID)])
         orefs.Next()
      adialog=ICORUtil.InputElementDialog('Wybierz klasę',0,0)
      if adialog.Show():
         aclass=aICORDBEngine.Classes[adialog.ClassPath]
         aclass.ForEachDerivedClass(self.ShowObjectsInRange,lrefs)
   def ShowObjectsInRange(self,aclass,lrefs):
      ret=[]
      for aname,aoidfrom,aoidto in lrefs:
         l=aclass.GetObjectsInRange(aoidfrom,aoidto)
         if l:
            print '%s|%s|%d|%d|%d'%(aclass.ClassPath,aname,aoidfrom,aoidto,len(l))
            ret.extend(l)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   achecker=Checker()
   achecker.Start()
   return
