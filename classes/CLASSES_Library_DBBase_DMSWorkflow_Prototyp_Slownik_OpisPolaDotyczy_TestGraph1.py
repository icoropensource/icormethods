# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_OpisPolaDotyczy_OnFieldChange as OnFieldChange

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   OID=35360 # dlugie
   OID=35616 # graf
   OnFieldChange.GraphCreate(aclass[OID])
   return

