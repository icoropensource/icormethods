# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   import string
#   print 'I: MethodCID:        ',aICORDBEngine.Variables._MethodCID
#   print 'I: MethodName:       ',aICORDBEngine.Variables._MethodName
#   print 'I: MethodOwnerCID:   ',aICORDBEngine.Variables._MethodOwnerCID
#   print 'I: MethodAllowImport:',aICORDBEngine.Variables._AllowMethodImport
   aclass=aICORDBEngine.Classes['CLASSES_System_Security_MethodSecurityInfo']
   if aclass is None:
      print 'Brak klasy MethodSecurityInfo'
      return
   mname=aICORDBEngine.Variables._MethodName
   mcid=int(aICORDBEngine.Variables._MethodOwnerCID)
   mclass=aICORDBEngine.Classes[mcid]
   if mclass is None:
      print 'Brak klasy',mcid
      return
   s=mclass.ClassPath
   aoid=aclass.ItemPath.Identifiers(s+'\\'+mname)
   if aoid<0:
      aoid=aclass.ItemPath.Identifiers(s)
   if aoid>=0:
      sid=aICORDBEngine.SystemID()
      arefs=aclass.AllowImportGroups.GetRefList(aoid)
      w=1
      while arefs.position>=0:
         w=0
         brefs=arefs.SystemIDs.GetRefList(arefs.OID)
         while brefs.position>=0:
            msid=brefs.SystemID[brefs.OID]
            if msid==sid:
               w=1
               break
            brefs.Next()
         if w==1:
            break
         arefs.Next()
      if w==0:
         print 'Method import: Access denied -',mname
         aICORDBEngine.Variables._AllowMethodImport='0'
   return

