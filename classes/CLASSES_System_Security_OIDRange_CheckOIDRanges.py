# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

class OIDRangesChecker:
   def __init__(self,aclass):
      self.ClassItem=aclass
      self.lranges=[]
      self.dranges={}
      aobj=aclass.GetFirstObject()
      while aobj:
         aname=aobj.Name
         if aname:
            aidmin=aobj['IDMin',mt_Integer]
            aidmax=aobj['IDMax',mt_Integer]
            self.lranges.append([aname,aidmin,aidmax])
            self.dranges[aname]=[aidmin,aidmax]
         aobj.Next()
   def Check(self,bclass):
      bclass.ForEachDerivedClass(self.OnClass)
   def OnClass(self,bclass):
      aobj=bclass.GetFirstObject()
      d={}
      while aobj:
         aoid=aobj.OID
         for aname,aidmin,aidmax in self.lranges:
            if aoid>=aidmin and aoid<aidmax:
               acnt=d.get(aname,0)
               acnt=acnt+1
               d[aname]=acnt
               break
         aobj.Next()
      if d:
         w=1
         for aname,acnt in d.items():
            aidmin,aidmax=self.dranges[aname]
            adiff=aidmax-aidmin
            if acnt+100>=adiff:
               if w:
                  print '=============================================================='
                  print 'KLASA:',bclass.NameOfClass,bclass.CID
                  w=0
               print aname,acnt,aidmin,aidmax,aidmax-aidmin

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   achecker=OIDRangesChecker(aclass)
   bclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp']
   achecker.Check(bclass)
   return
