# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORSecurity import *

def Update1(aclass):
   aoid=aclass.FirstObject()
   print aICORDBEngine.SystemID()
   while aoid>=0:
      s=aclass.Password[aoid]
      p=aICORDBEngine.HashString(s+'_'+str(aoid))
      print aclass.UserName[aoid],s,p
      aclass.Password[aoid]=p
      aoid=aclass.NextObject(aoid)


def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]

   if 1:
      RepairUsersInUserGroups()
      RepairUserGroupsInUsers()
      RepairGroupsInUserGroups()
      RepairUserGroupsInGroups()
      RepairItemGroupsInGroups()
      RepairGroupsInItemGroups()
      RepairProfileInUserGroups()
      RepairProfileInItemGroups()
      RepairUserGroupsInProfile()
      RepairItemGroupsInProfile()

   return



