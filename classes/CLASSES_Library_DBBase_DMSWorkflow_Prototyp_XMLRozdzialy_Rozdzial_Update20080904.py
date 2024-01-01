# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   efieldname='ChapterEvents'
   lfields=[
'OnASPPageAfter',
'OnASPPageBefore',
'OnASPPageTop',
'OnRSSGetDescription',
'OnRSSGetLink',
'OnRSSGetTitle',
#'SQLData',
#'XSLData',
#'XSLDataSO',
]

   efield=aclass.FieldsByName(efieldname)
   eclass=efield.ClassOfType
   kclass=eclass.EventKind.ClassOfType
   for afieldname in lfields:
      koid=kclass.EventName.Identifiers(afieldname)
      if koid<0:
         koid=kclass.AddObject()
         kclass.EventName[koid]=afieldname

   for afieldname in lfields:
      afield=aclass.FieldsByName(afieldname)
      afield.IsAliased='0'
      afield.IsInteractive='0'
      afield.WWWDefaultInput='0'

   aobj=aclass.GetFirstObject()
   wb=0
   while aobj and not wb:
      d={}
      eobj=aobj.GetFieldValue(efieldname)
      while eobj:
         d[eobj.EventKind.EventName]=1
         wb=1
         eobj.Next()
      for afieldname in lfields:
         if d.has_key(afieldname):
            continue
         afield=aclass.FieldsByName(afieldname)
         avalue=afield[aobj.OID]
         s=string.replace(avalue,chr(13),'')
         s=string.replace(avalue,chr(10),'')
         s=string.replace(avalue,' ','')
         if s:
            koid=kclass.EventName.Identifiers(afieldname)
            eoid=eclass.GetNextFreeObjectID(aobj.OID,aobj.OID+1000)
            eclass.CreateObjectByID(eoid)
            eclass.EventKind[eoid]=[koid,kclass.CID]
            eclass.EventSource[eoid]=avalue
            efield.AddRefs(aobj.OID,[eoid,eclass.CID])
      aobj.Next()
   return



