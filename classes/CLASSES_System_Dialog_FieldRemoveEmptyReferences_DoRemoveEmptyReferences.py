# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
import string

cr_none,cr_leaveunchanged,cr_changecid,cr_remove,cr_deleteobject=0,1,2,3,4

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if OID<0:
      return
   bclass=aICORDBEngine.Classes[OID]
   if bclass is None:
      return
   bfield=bclass.FieldsByName(Value)
   if bfield is None:
      return
   aoid=aclass.FirstObject()
   if aoid<0:
      aoid=aclass.AddObject()
   if not aclass.EditObject(aoid,acaption='Kasowanie pustych referencji w polu '+bfield.Name):
      return

   amode=cr_none
   aobj=aclass[aoid].BadCIDAction
   if aobj:
      if aobj.OID==1:
         amode=cr_leaveunchanged
      elif aobj.OID==2:
         amode=cr_changecid
      elif aobj.OID==3:
         amode=cr_remove
      elif aobj.OID==4:
         amode=cr_deleteobject

   countR,countO=0,0
   ldel=[]
   boid=bclass.FirstObject()
   while boid>=0:
      s,w='',0
      arefs=bfield.GetRefList(boid)
      while arefs:
         if amode==cr_deleteobject:
            if not bfield.ClassOfType.ObjectExists(arefs.OID):
               ldel.append(boid)
               break
         elif (arefs.Class is None) or (bfield.ClassOfType.CID!=arefs.CID):
            if amode in [cr_none,cr_leaveunchanged]:
               s=s+str(arefs.OID)+':'+str(arefs.CID)+':'
            elif amode==cr_changecid:
               if bfield.ClassOfType.ObjectExists(arefs.OID):
                  s=s+str(arefs.OID)+':'+str(bfield.ClassOfType.CID)+':'
               w=1
               countR=countR+1
            elif amode==cr_remove:
               w=1
               countR=countR+1
         else:
            if bfield.ClassOfType.ObjectExists(arefs.OID):
               s=s+str(arefs.OID)+':'+str(bfield.ClassOfType.CID)+':'
            else:    
               w=1
               countR=countR+1
         arefs.Next()
      if w:
         if amode not in [cr_none,cr_leaveunchanged]:
            bfield[boid]=s
         countO=countO+1
      boid=bclass.NextObject(boid)

   if countR:
      MessageDialog('Zmieniono %d referencji w %d obiektach.'%(countR,countO),mtInformation,mbOK)
   elif ldel:
      print 'obiekty do skasowania (%d):'%(len(ldel),),ldel
      bclass.DeleteObject(ldel)
      MessageDialog('Usunięto %d obiektów.'%(len(ldel),),mtInformation,mbOK)
   else:
      MessageDialog('Nie znaleziono pustych referencji.',mtInformation,mbOK)
   return

