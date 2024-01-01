# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORSecurity as ICORSecurity

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if FieldName=='AccessLevelView':
      aobj=aclass[OID]
      arefs=ICORSecurity.GetRecursiveAccessLevelRefs(aobj,'AccessLevelView')
      if arefs:
         return arefs.AsString()
      return ''
   if FieldName=='IsTableView':
      w=aclass.SGIsTableView.ValuesAsInt(OID)
      if w:
         return '1'
      return '0'
   if FieldName=='Naglowek':
      return aclass.Naglowek[OID]
   if FieldName=='CMSID':
      ret='-1'
      aobj=aclass[OID]
      bobj=aobj.AsObject()
      wobj=None
      while not wobj and bobj:
         wobj=bobj.Struktura
         if wobj:
            ret=str(wobj.OID)
         bobj=bobj.NadRozdzial
      return ret
   return ''




