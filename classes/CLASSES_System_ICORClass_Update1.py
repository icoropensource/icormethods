# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import string

def ConvertSheets(aclass,aoid):
   sclass=aICORDBEngine.Classes['CLASSES/System/SystemDictionary/ClassSheet']
   s=aclass.aClassSheets[aoid]
   s=string.replace(s,chr(10),':')
   sl=string.split(s,':')
   sr=''
   for asheet in sl:
      if asheet=='':
         continue
      soid=sclass.AddObject()
      sclass.Name[soid]=asheet
      sr=sr+str(soid)+':'+str(sclass.CID)+':'
   aclass.aEditorSheets[aoid]=sr

def UpdateSummaries(aclass,aoid):
   def fsumfunc(aclass,aoid,acid):
      aclass.OwnerCID[aoid]=str(acid)
   aclass.aSummaries.ForEachRefObject(fsumfunc,aoid,aoid)
   
def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
#   aclass.ForEachObject(ConvertSheets)
   aclass.ForEachObject(UpdateSummaries)
   return
