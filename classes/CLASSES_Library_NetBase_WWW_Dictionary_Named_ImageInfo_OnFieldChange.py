# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import base64

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if FieldName in ['Location',]:
      alocation=aclass.Location[OID]
      try:
         afname=FilePathAsSystemPath(string.replace(alocation,'/icormanager','%ICOR%/wwwroot'))
         fin=open(afname,'rb')
         atext=fin.read()
         fin.close()
         btext=base64.standard_b64encode(atext)
         aclass.Base64[OID]=btext
      except:
         print 'bad image location:',alocation
   return
                                         
