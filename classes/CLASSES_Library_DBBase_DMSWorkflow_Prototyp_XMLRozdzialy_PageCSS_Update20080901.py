# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]

   if 1:
      aobj=aclass.GetFirstObject()
      while aobj:
         aobj.CSSUser=aobj.CSSUser+aobj.CSSSystem
         aobj.CSSSystem=''
         aobj.Next()

   lfields=[
'CSSSystem',
]
   for afieldname in lfields:
      afield=aclass.FieldsByName(afieldname)
      afield.IsAliased='0'
      afield.IsInteractive='0'
      afield.WWWDefaultInput='0'

   return       
