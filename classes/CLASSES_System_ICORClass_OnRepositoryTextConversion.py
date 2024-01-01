# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_System_SystemDictionary_FieldAutoTextConversion_DoFieldNameConversion import GetFieldNameAutoExpand
import string

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   ret=''
   if FieldName in ['FieldNameAutoExpand','WWWMenuAutoExpand','GeoMenuAutoExpand']:
      ret=GetFieldNameAutoExpand(Value)
   return ret

