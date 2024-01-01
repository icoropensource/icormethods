# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
import string

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if OID<0:
      adialog=InputElementDialog('Wybierz klasę',0,0)
      if not adialog.Show():
         return
      bclass=aICORDBEngine.Classes[adialog.ClassPath]
      if bclass is None:
         return
   else:
      bclass=aICORDBEngine.Classes[OID]
   aoid=aclass.FirstObject()
   if aoid<0:
      aoid=aclass.AddObject()
   aclass.NMName[aoid]=''
   aclass.NMDescription[aoid]=''
   aclass.NMIsParallel[aoid]='0'
   aclass.NMIsQueued[aoid]='0'
   aclass.NMWWWDescription[aoid]=''
   aclass.NMWWWMethod[aoid]='0'
   aclass.NMWWWConfirmExecute[aoid]='0'
   aclass.NMAllowReadGroups[aoid]=''
   aclass.NMAllowWriteGroups[aoid]=''
   aclass.NMWWWMenuImageLink[aoid]=''
#   lclass=aICORDBEngine.Classes['CLASSES_System_SystemDictionary_MethodLanguage']
#   aclass.NMLanguage[aoid]=str(lclass.FirstObject())+':'+str(lclass.CID)+':'
   if not aclass.EditObject(aoid):
      return
   mname=aclass.NMName[aoid]
   mdef=ICORMethodDefinition(mname)
   mdef.MDescription=aclass.NMDescription[aoid]
   mdef.MIsParallel=aclass.NMIsParallel.ValuesAsInt(aoid)
   arefs=aclass.NMLanguage.GetRefList(aoid)
   if arefs.position>=0:
      mdef.MLanguage=arefs.Name[arefs.OID]
   amethod=bclass.AddMethod(mdef)
   if amethod is None:
      return
   tclass=aICORDBEngine.Classes['CLASSES/System/MethodTemplate']
   if tclass is None:
      return
   if mdef.MLanguage=='' or mdef.MLanguage=='Python':
      if aclass.NMWWWMethod.ValuesAsInt(aoid):
         tname='OnWWWObjectApplyMethods'
      else:
         tname=mname
      dtname='*'
   else:
      tname=mdef.MLanguage+'_'+mname
      dtname=mdef.MLanguage+'_*'
   toid=tclass.MethodName.Identifiers(tname)
   if toid>=0:
      if tclass.DefaultText.ValuesAsInt(toid)>0:
         toid=-1
   if toid<0:
      toid=tclass.MethodName.Identifiers(dtname)
   if toid>=0:
      ami=bclass.MethodsByName(mname)
      if ami is None:
         return
      ami.MethodText=tclass.MethodText[toid]
   amethod.WWWDescription=aclass.NMWWWDescription[aoid]
   amethod.WWWMethod=aclass.NMWWWMethod[aoid]
   amethod.WWWConfirmExecute=aclass.NMWWWConfirmExecute[aoid]
   amethod.IsQueued=aclass.NMIsQueued.ValuesAsInt(aoid)
   aICORDBEngine.Classes.MetaMethod.aAllowReadGroups[amethod.MOID]=aclass.NMAllowReadGroups[aoid]
   aICORDBEngine.Classes.MetaMethod.aAllowWriteGroups[amethod.MOID]=aclass.NMAllowWriteGroups[aoid]
   aICORDBEngine.Classes.MetaMethod.aWWWMenuImageLink[amethod.MOID]=aclass.NMWWWMenuImageLink[aoid]
   return

