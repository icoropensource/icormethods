# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
#   print 'OOC1: %s f %s i %s v %s u %s'%(str(CID),FieldName,str(OID),Value,str(UID))
   aclass=aICORDBEngine.Classes[CID]
   zobj=aclass.Zakladki.ClassOfType.NewObject()
#   print 'OOC2: %s'%(str(zobj.OID),)
   zobj.Nazwa='Dane'
#   print 'OOC3'
   zobj.ZakladkaID='10'
#   print 'OOC4'
   aclass.Zakladki[OID]=zobj.AsString()
#   print 'OOC5: %s'%(aclass.Zakladki[OID]),
   return 'C1'



