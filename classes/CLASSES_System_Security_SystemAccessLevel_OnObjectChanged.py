# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

import sys
try:
   import ICORDelphi
   icorapi=ICORDelphi
   ICOR_EXECUTE_EXTERNAL=0
except:
   import icorapi
   ICOR_EXECUTE_EXTERNAL=1

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   import string
   acclevel=string.atof(icorapi.GetFieldValue(UID,CID,'AccessLevel',OID))
   if acclevel<0:
      acclevel=0
   if acclevel>8:
      acclevel=8
   res=icorapi.SetFieldValue(UID,CID,'AccessLevel',OID,str(acclevel))
   return

