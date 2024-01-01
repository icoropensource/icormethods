# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[Value]
   aclass.IsSystem='1'
   mclass=aICORDBEngine.Classes['CLASSES\System\Security\MethodSecurityInfo']
   aoid=mclass.ItemPath.Identifiers(aclass.Inherited.ClassPath)
   if aoid>0:
      moid=mclass.AddObject()
      mclass.ItemPath[moid]=aclass.ClassPath
      mclass.AllowGetGroups[moid]=mclass.AllowGetGroups[aoid]
      mclass.AllowImportGroups[moid]=mclass.AllowImportGroups[aoid]
      mclass.AllowUpdateGroups[moid]=mclass.AllowUpdateGroups[aoid]
   return


