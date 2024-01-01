# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_NetBase_Utils_ImageUtil as ImageUtil
import os

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   asrcfname=FieldName+'SQLFiles/'+Value+'.dat'
   adstfname=FieldName+'SQLImages/'+str(OID)+'/'+Value+'.jpg'
   aisimage=ImageUtil.IsImage(asrcfname,aignoreext=1)
   if not os.path.exists(FieldName+'SQLImages/'+str(OID)):
      os.makedirs(FieldName+'SQLImages/'+str(OID))
   gobj=aclass[OID]
   if aisimage:
      try:
         ImageUtil.ResizeImageByConstraint(asrcfname,adstfname,gobj['RozmiarX'],gobj['RozmiarY'],gobj['MaksymalnyRozmiarKB'],gobj['Przycinanie',mt_Integer])
      except:
         return 'BAD'
   else:
      return 'BAD'                
#   print 'thumb:',OID,Value,FieldName
   return 'OK'



