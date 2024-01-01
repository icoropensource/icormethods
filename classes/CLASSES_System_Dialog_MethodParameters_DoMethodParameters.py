# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
import string

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   if OID<0:
      return
   aclass=aICORDBEngine.Classes[CID]
   bclass=aICORDBEngine.Classes[OID]
   if bclass is None:
      return
   amethod=bclass.MethodsByName(Value)
   if amethod is None:
      return
   aoid=aclass.FirstObject()
   if aoid<0:
      aoid=aclass.AddObject()
   aclass.NMDescription[aoid]=amethod.MethodDescription
   aclass.NMIsParallel[aoid]=str(amethod.IsParallel)
   aclass.NMIsQueued[aoid]=str(amethod.IsQueued)
   aclass.NMIsMenuHidden[aoid]=amethod.IsMenuHidden
   aclass.NMWWWDescription[aoid]=amethod.WWWDescription
   aclass.NMWWWMethod[aoid]=str(amethod.WWWMethod)
   aclass.NMWWWConfirmExecute[aoid]=str(amethod.WWWConfirmExecute)
   aclass.NMAllowReadGroups[aoid]=aICORDBEngine.Classes.MetaMethod.aAllowReadGroups[amethod.MOID]
   aclass.NMAllowWriteGroups[aoid]=aICORDBEngine.Classes.MetaMethod.aAllowWriteGroups[amethod.MOID]
   aclass.NMWWWMenuImageLink[aoid]=aICORDBEngine.Classes.MetaMethod.aWWWMenuImageLink[amethod.MOID]
   if not aclass.EditObject(aoid):
      return
   amethod.MethodDescription=aclass.NMDescription[aoid]
   amethod.IsParallel=aclass.NMIsParallel.ValuesAsInt(aoid)
   amethod.IsQueued=aclass.NMIsQueued.ValuesAsInt(aoid)
   amethod.IsMenuHidden=aclass.NMIsMenuHidden[aoid]
   amethod.WWWDescription=aclass.NMWWWDescription[aoid]
   amethod.WWWMethod=aclass.NMWWWMethod[aoid]
   amethod.WWWConfirmExecute=aclass.NMWWWConfirmExecute[aoid]
   aICORDBEngine.Classes.MetaMethod.aAllowReadGroups[amethod.MOID]=aclass.NMAllowReadGroups[aoid]
   aICORDBEngine.Classes.MetaMethod.aAllowWriteGroups[amethod.MOID]=aclass.NMAllowWriteGroups[aoid]
   aICORDBEngine.Classes.MetaMethod.aWWWMenuImageLink[amethod.MOID]=aclass.NMWWWMenuImageLink[aoid]

