# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:16:53

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import icorlib.projekt.mcrmwwwmenumodel as MCRMWWWMenuModel

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   i=15
   aobj=aclass.GetFirstObject()
   while aobj and i:
      v=aobj['IsCustom']
      w='N'
      if v:
         w='T'
      print aobj.OID,v,w,type(v)
      i=i-1
      aobj.Next()
   
   return
