# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aclass.Tabela.UpdateReferencedObjects(OID,adeleterefs=1,aupdaterefs=1)
   aobj=aclass[OID]
   robj=aobj.ListaWysylkowa
   while robj:
      robj.Class.Elementy.DeleteRefs(robj.OID,[OID,CID])
      robj.Next()
   return

