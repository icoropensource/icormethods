# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def TestSet(afield,aoid,aoperator,atekst):
   afield[aoid]=100
   ret=afield.SetTestValues(aoid,aoperator,50,333)
   print '1. %s 100- 50 [%d] new: %s'%(atekst,ret,afield[aoid])
   afield[aoid]=100
   ret=afield.SetTestValues(aoid,aoperator,100,333)
   print '2. %s 100-100 [%d] new: %s'%(atekst,ret,afield[aoid])
   afield[aoid]=100
   ret=afield.SetTestValues(aoid,aoperator,200,333)
   print '3. %s 100-200 [%d] new: %s'%(atekst,ret,afield[aoid])
   print

def TestInc(afield,aoid,aoperator,atekst):
   afield[aoid]=100
   ret=afield.SetTestIncValues(aoid,aoperator,50)
   print '1. %s 100- 50 [%d] new: %s'%(atekst,ret,afield[aoid])
   afield[aoid]=100
   ret=afield.SetTestIncValues(aoid,aoperator,100)
   print '2. %s 100-100 [%d] new: %s'%(atekst,ret,afield[aoid])
   afield[aoid]=100
   ret=afield.SetTestIncValues(aoid,aoperator,200)
   print '3. %s 100-200 [%d] new: %s'%(atekst,ret,afield[aoid])
   print

def TestDec(afield,aoid,aoperator,atekst):
   afield[aoid]=100
   ret=afield.SetTestDecValues(aoid,aoperator,50)
   print '1. %s 100- 50 [%d] new: %s'%(atekst,ret,afield[aoid])
   afield[aoid]=100
   ret=afield.SetTestDecValues(aoid,aoperator,100)
   print '2. %s 100-100 [%d] new: %s'%(atekst,ret,afield[aoid])
   afield[aoid]=100
   ret=afield.SetTestDecValues(aoid,aoperator,200)
   print '3. %s 100-200 [%d] new: %s'%(atekst,ret,afield[aoid])
   print

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes['CLASSES_Library_Test_Struct_Test1']
   afield=aclass.PoleS
   aoffset=afield.GetFirstDeletedOffset()
   while aoffset>=0:
      aoid=afield.GetRecOID(aoffset)
      if aoid==10:
         adt=afield.GetRecLastModification(aoffset)
         avalue=afield.GetRecValueAsString(aoffset)
         print aoffset,adt,avalue
      aoffset=afield.GetNextDeletedOffset(aoffset)
   return
   CID=1407
   aclass=aICORDBEngine.Classes[CID]
   aoid=1
   TestDec(aclass.PoleI,aoid,cv_leeq,'cv_leeq')
   TestDec(aclass.PoleI,aoid,cv_ge,'cv_ge')
   TestDec(aclass.PoleI,aoid,cv_le,'cv_le')
   TestDec(aclass.PoleI,aoid,cv_neq,'cv_neq')
   TestDec(aclass.PoleI,aoid,cv_eq,'cv_eq')
   return
   TestInc(aclass.PoleI,aoid,cv_leeq,'cv_leeq')
   TestInc(aclass.PoleI,aoid,cv_ge,'cv_ge')
   TestInc(aclass.PoleI,aoid,cv_le,'cv_le')
   TestInc(aclass.PoleI,aoid,cv_neq,'cv_neq')
   TestInc(aclass.PoleI,aoid,cv_eq,'cv_eq')
   return
   TestSet(aclass.PoleI,aoid,cv_leeq,'cv_leeq')
   TestSet(aclass.PoleI,aoid,cv_ge,'cv_ge')
   TestSet(aclass.PoleI,aoid,cv_le,'cv_le')
   TestSet(aclass.PoleI,aoid,cv_neq,'cv_neq')
   TestSet(aclass.PoleI,aoid,cv_eq,'cv_eq')
   return



