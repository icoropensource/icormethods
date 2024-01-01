# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

class DictClassChecker:
   def __init__(self,aremove=0,aignorebackreffields=0,ashowfullreport=0):
      self.remove=aremove
      self.ignorebackreffields=aignorebackreffields
      self.showfullreport=ashowfullreport
   def Process(self,aclass):
      self.ClassItem=aclass
      self.OIDDict={}
      aICORDBEngine.Classes.MetaField.aFieldTypeID.ForEachValueByPattern(self.OnFind,aclass.CID,str(aclass.CID))
      rlist=[]
      aobj=aclass.GetFirstObject()
      print 'not referenced objects:'
      while aobj:
         if not self.OIDDict.has_key(aobj.OID):
            print 'OID:',aobj.OID,aobj.AsColumnValues(amaxcol=5)
            if self.remove:
               rlist.append(aobj.OID)
         aobj.Next()
      if self.showfullreport:
         print
         print '*** referenced objects: ***'
         aobj=aclass.GetFirstObject()
         while aobj:
            if self.OIDDict.has_key(aobj.OID):
               dd=self.OIDDict[aobj.OID]
               lk=dd.keys()
               lk.sort()
               print 'OID:',aobj.OID,aobj.AsColumnValues(amaxcol=5)
               for vk in lk:
                  do=dd[vk]
                  lv=do.keys()
                  lv.sort()
                  print '  %s [%d]:'%(vk,len(lv)),lv
            aobj.Next()
      for roid in rlist:
         aclass.DeleteObject(roid)
   def OnFind(self,afield,aposition,avalue):
      foid=aICORDBEngine.Classes.MetaField.aFieldTypeID.GetValueIDByPosition(aposition)
      bcid=aICORDBEngine.Classes.MetaField.aFieldTypeID.ValuesAsComp(foid)
      fcid=aICORDBEngine.Classes.MetaField.aFieldOwnerClassID.ValuesAsComp(foid)
      fname=aICORDBEngine.Classes.MetaField.aFieldName.ValuesAsComp(foid)
      if bcid!=self.ClassItem.CID:
         print '*** bledny CID dla pozycji',foid,'w klasie o cid:',fcid,'dla pola:',fname
         return
      bclass=aICORDBEngine.Classes[fcid]
      if bclass is None:
         print '*** nie istniejąca klasa CID:',fcid
      bfield=bclass.FieldsByName(fname)
      if bfield is None:
         print '*** nie istniejące pole:',fname,'w klasie:',bclass.ClassPath,'CID:',fcid
         return
      aignore=''
      sbackref=''
      if bfield.WWWBackRefField:
         sbackref=' [BACKREF]'
      if self.ignorebackreffields and sbackref:
         aignore=' ** IGNORE **'
      print bclass.ClassPath,'-',bfield.Name,sbackref,aignore
      if aignore:
         return
      boid=bclass.FirstObject()
      while boid>=0:
         brefs=bfield.GetRefList(boid)
         while brefs:
            dd=self.OIDDict.get(brefs.OID,{})
            dk=bclass.ClassPath+' - '+bfield.Name
            do=dd.get(dk,{})
            do[boid]=1
            dd[dk]=do
            self.OIDDict[brefs.OID]=dd
            brefs.Next()
         boid=bclass.NextObject(boid)
   def Dump(self):
      pass

