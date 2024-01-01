# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import str2ProperID
import string

def GetProperFieldsID(s):
   lret=[]
   sl=string.split(s,',')
   for s in sl:
      if s[:1]!='_':
         lret.append(str2ProperID(s))
      else:
         lret.append(s)
   return string.join(lret,',')

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if FieldName=='SourceField':
      s=aclass.SourceField[OID]
      aclass.SourceFieldID[OID]=GetProperFieldsID(s)
   if FieldName=='DestinationField':
      s=aclass.DestinationField[OID]
      aclass.DestinationFieldID[OID]=GetProperFieldsID(s)
   return



