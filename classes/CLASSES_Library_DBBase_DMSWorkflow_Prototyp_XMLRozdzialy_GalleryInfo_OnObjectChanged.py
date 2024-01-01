# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import os

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   pclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Projekt']
   pobj=pclass.GetFirstObject()
   while pobj:
      apath=pobj.WWWDataPath
      if apath:
         apath=FilePathAsSystemPath(apath)+'/sqlimages/'+str(OID)+'/'
         try:
            ldir=os.listdir(apath)
         except:
            ldir=[]
         for afname in ldir:
            try:
               os.unlink(apath+afname)
            except:
               pass
      pobj.Next()
   return



