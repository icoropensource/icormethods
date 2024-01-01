# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   sum=0.0
   if FieldName=='ObrotyWn':
      sum=aclass.SumBOWn.ValuesAsFloat(OID)+aclass.SumWn.ValuesAsFloat(OID)
   elif FieldName=='ObrotyMa':
      sum=aclass.SumBOMa.ValuesAsFloat(OID)+aclass.SumMa.ValuesAsFloat(OID)
   elif FieldName=='SaldoWn':
      sum=aclass.SumWn.ValuesAsFloat(OID)-aclass.SumMa.ValuesAsFloat(OID)
   elif FieldName=='SaldoMa':
      sum=aclass.SumMa.ValuesAsFloat(OID)-aclass.SumWn.ValuesAsFloat(OID)
   elif FieldName=='SaldoObrotyWn':
      sum=aclass.SumBOWn.ValuesAsFloat(OID)+aclass.SumWn.ValuesAsFloat(OID)-aclass.SumBOMa.ValuesAsFloat(OID)-aclass.SumMa.ValuesAsFloat(OID)
   elif FieldName=='SaldoObrotyMa':
      sum=aclass.SumBOMa.ValuesAsFloat(OID)+aclass.SumMa.ValuesAsFloat(OID)-aclass.SumBOWn.ValuesAsFloat(OID)-aclass.SumWn.ValuesAsFloat(OID)
   return str(sum)



