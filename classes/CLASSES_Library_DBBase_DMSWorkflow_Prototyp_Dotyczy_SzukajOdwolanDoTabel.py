# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def Func2(aclass,afield,bclass,brefs):
   if not afield.ClassOfType is None:
      if afield.ClassOfType.CID==bclass.CID:
         aoid=afield.GetFirstValueID()
         while aoid>=0:
            arefs=afield.GetRefList(aoid)
            if arefs.RefsExists(brefs):
               aclass.EditObject(aoid,acaption='%s : %s'%(aclass.ClassPath,afield.Name),atoolbar=1)
            aoid=afield.GetNextValueID(aoid)

def Func1(aclass,bclass,brefs):
#   print aclass.MaxOID,aclass.ClassPath
   aclass.ForEachField(Func2,bclass,brefs)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp']
   bclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Dotyczy']
   brefs=bclass.SelectObjects()
   if not brefs:
      return
   aclass.ForEachDerivedClass(Func1,bclass,brefs)
   return



