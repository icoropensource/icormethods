# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def SetSingleDateObj(aobj):
   dobj=aobj.Dimensions
   if dobj:
      fobj=dobj.FKFilters
      if not fobj:
         fclass=dobj.Class.FKFilters.ClassOfType
         foid=fclass.AddObject()
         fclass.FromDate.SetValuesAsDate(foid,(2000,1,1))
         fclass.ToDate.SetValuesAsDate(foid,(2001,1,1))
         dobj.Class.FKFilters[dobj.OID]=str(foid)+':'+str(fclass.CID)+':'

def SetAllDateObj(aclass):
   aobj=aclass.GetFirstObject()
   while aobj.Exists():
      SetSingleDateObj(aobj)
      aobj.Next()

def SetSelectedDateObj(aclass):
   arefs=aclass.SelectObjects()
   while arefs:
      aobj=aclass[arefs.OID]
      print arefs.Name[arefs.OID]
      SetSingleDateObj(aobj)
      arefs.Next()

def PrintSelectedObj(aclass):
   arefs=aclass.SelectObjects()
   while arefs:
      aobj=aclass[arefs.OID]
      print arefs.Name[arefs.OID]
      arefs.Next()

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   SetSelectedDateObj(aclass)
   return



