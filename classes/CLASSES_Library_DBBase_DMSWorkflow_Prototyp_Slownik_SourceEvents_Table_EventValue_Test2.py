# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   OID=37000
   eobj=aclass[OID]
   tobj=eobj.Dotyczy
   kobj=eobj.EventKind
   print 'EventKind:',kobj.OID #18


   afieldname='TableEvents'
   afield=tobj.Class.FieldsByName(afieldname)
   arefs=afield.GetRefList(tobj.OID)

   arfieldname='EventKind'

   rfield=afield.ClassOfType.FieldsByName(arfieldname)
   arvalue='18'

   aasoidsearch=0
   if not rfield.ClassOfType is None:
      aasoidsearch=1
      arvalue=int(arvalue)
   print 'AsOIDSearch:',aasoidsearch

   apos,afind=arefs.FindRefByValue(arfieldname,arvalue,aasoidsearch=aasoidsearch)
   if afind:
      print 'FIND:',apos
   else:
      print 'NOT FIND'
   return
