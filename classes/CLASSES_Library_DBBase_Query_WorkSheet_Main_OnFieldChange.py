# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_ICORBase_Interface_ICORSecurity as ICORSecurity
import string

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if FieldName in ['Columns','SheetItems']:
      afield=aclass.FieldsByName(FieldName)
      afield.UpdateReferencedObjects(OID)
   if FieldName=='SubQuery':
      aclass.SubQuery.UpdateReferencedObjects(OID,aclass.ParentQuery)
      aobj=aclass[OID]
      dobj=aobj.SubQuery
      sqref=aobj.QueryStruct.AsString()
      while dobj:
         dobj.QueryStruct=sqref
         dobj.Next()
   if FieldName=='TableID':
      afield=aclass.FieldsByName(FieldName)
      fv=afield[OID]
      if fv:
         nv,cnt=fv,1
         nv=ICORUtil.strUpperPL(nv)
         nv=string.replace(nv,' ','_')
         while 1:
            doid=afield.Identifiers(nv)
            if doid<0 or doid==OID:
               break
            nv=fv+'_'+str(cnt)
            cnt=cnt+1
         if nv!=fv:
            afield[OID]=nv
   if FieldName=='SourceData':
      mclass=aclass.SheetItems.ClassOfType
      arefs=aclass.SheetItems.GetRefList(OID)
      if arefs:
         if arefs.SourceData[arefs.OID]==aclass.SourceData[OID]:
            return
      moid=mclass.AddObject()
      mclass.LastModification.SetValuesAsDateTime(moid,ICORUtil.tdatetime())
      auser=ICORSecurity.ICORSecurityUser(UID)
      mclass.UserName[moid]=auser.UserName
      mclass.SourceData[moid]=aclass.SourceData[OID]
      aclass.SheetItems.AddRefs(OID,[moid,mclass.CID],asortedreffield=mclass.LastModification,adescending=1)
   return



