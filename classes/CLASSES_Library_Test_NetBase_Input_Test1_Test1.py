# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil

def Test():
   return 1

def TestInsertRef(aclass):
   aoid=aclass.FirstObject()
   arefs=aclass.PoleC.GetRefList(aoid)
   arefs.InsertRef('Test',1,aclass.PoleC.ClassOfType.CID)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aobj=aclass.GetFirstObject()

   vb=aclass.PoleB[1]
   vc=aclass.PoleC[1]
   vd=aclass.PoleD[1]
   vf=aclass.PoleF[1]
   vi=aclass.PoleI[1]
   vm=aclass.PoleM[1]
   vs=aclass.PoleS[1]

   for i in range(2,1000,2):
      if 0:
         aclass.PoleB[i]=vb
         aclass.PoleC[i]=vc
         aclass.PoleF[i]=float(vf)+i
         aclass.PoleI[i]=int(vi)+i
         aclass.PoleM[i]=vm+'\n\n%d'%i
         aclass.PoleS[i]=vs+' - %d'%i
      aclass.PoleD[i]=vd
   return


   while aobj:
      print aobj.OID,aobj.PoleS,aobj.PoleB,aobj.PoleD
      aobj.Next()
   

   return
   aclass=aICORDBEngine.Classes[1862]
   afield=aclass.GenerujSP
   print afield.FOID
   afield[35001]=''
   print '  GG: v:%s'%aICORDBEngine.CacheBase.GetFieldValue(afield.FOID,35001,mt_Bool,1)

   return
   aclass=aICORDBEngine.Classes['CLASSES_Library_Test_NetBase_Input_Test1']

   aclass.PoleB[1]=''
   aclass.PoleB[2]=' '
   return
   v=aclass.SGIsDisabled.Values(1)
   print v,type(v)
   v=aclass.SGIsDisabled.ValuesAsInt(1)
   print v,type(v)
   v=aclass.SGIsDisabled.ValuesAsComp(1)
   print v,type(v)

   return
   print 'CACHE_DISABLE:',CACHE_DISABLE
   print 'ICOR_EXECUTE_EXTERNAL:',ICOR_EXECUTE_EXTERNAL
   aclass=aICORDBEngine.Classes[CID]
   afieldnames=aclass.GetFieldsList()
   for afieldname in afieldnames:
      afield=aclass.FieldsByName(afieldname)
      print afield.Name,afield.FOID

   print 'True',ICORUtil.str2bool('True')
   print 'False',ICORUtil.str2bool('False')
   for s in ['24/06/2011 11:10:12','24/06/2011','11:10:12','2011/06/24 11:10:12','2011/06/24','']:
      v=ICORUtil.getStrAsDateTime(s)
      print s,v,':'.join(map(str,v))

   return
   aclass=aICORDBEngine.Classes[CID]
   OID=1
   iOID=12
   aclass.PoleC.ClassOfType.PoleS[iOID]='BW2'

   arefs=aclass.PoleC.GetRefList(OID)
   arefs.sort(aclass.PoleC.ClassOfType.PoleS)
   ret=arefs.InsertRefEx(aclass.PoleC.ClassOfType.PoleS,iOID,aclass.PoleC.ClassOfType.CID)

   while arefs:
      print arefs.PoleS[arefs.OID]
      arefs.Next()
   return




