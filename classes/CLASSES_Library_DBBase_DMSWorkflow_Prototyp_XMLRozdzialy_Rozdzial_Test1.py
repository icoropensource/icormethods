# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import re
import string

def GetChapterGroup(robj):
   ret=''
   nobj=robj.NadRozdzial
   while nobj:
      zobj=robj.GrupaRozdzialow
      if zobj:
         ret=zobj.Nazwa
         break
      nobj=nobj.NadRozdzial
   return ret


def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aobj=aclass.GetFirstObject()
   while aobj:
      print aobj.OID,GetChapterGroup(aobj)
      aobj.Next()
   

   return
   aobj=aclass.GetFirstObject()
   while aobj:
      l=[str(aobj.OID),aobj.Naglowek,str(aobj.ZrodloDanychWzorca.Nazwa).replace("'",''),str(aobj['SGIsTableView',mt_Integer]),str(aobj['IsCustomXSL',mt_Integer]),str(aobj['IsCustomXSLSO',mt_Integer])]
      print string.join(l,'|')
      aobj.Next()                        
   return
                             
