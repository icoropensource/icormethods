# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
#   afields=aclass.GetFieldsList()
   afields=('TPrac',)
   oid=aclass.FirstObject()
   x=0
   ClearStdOut()
   while (oid>=0) and (x>=0):
      print 'Object#',oid
      for afield in afields:
         ifi=aclass.FieldsByName(afield)
         s=ifi[oid]
         if (s!='') and (s!='30/12/1999'):
            print '   ',ifi.FName,':',s
            aclass.Pracownik[oid]=s
      x=x+1
      oid=aclass.NextObject(oid)
   return


