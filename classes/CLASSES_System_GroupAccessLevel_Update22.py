# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   gclass=aclass.Groups.ClassOfType
   aobj=aclass.GetFirstObject()
   while aobj:
      sgrefs=aobj.Class.Groups[aobj.OID]
      if not sgrefs:
         goid=gclass.Name.Identifiers(aobj.Name)
         if goid<0:
            goid=gclass.AddObject()
            gclass.Name[goid]=aobj.Name
            print 'new:',aobj.Name
         print 'Empty:',aobj.OID,goid,aobj.Name
         aobj.Class.Groups[aobj.OID]=str(goid)+':'+str(gclass.CID)+':'
      aobj.Next()
   return

