# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import os

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aobj=aclass.GetFirstObject()
   while aobj:
      print aobj.Grupa,'-',aobj.Nazwa
      aobj.Next()
   
   return
   adir='d:/projects/adoutil/sqltemplates/_good'
   l1=os.listdir(adir)
   for sd1 in l1:
      l2=os.listdir(adir+'/'+sd1)
      for sd2 in l2:
         aoid=aclass.AddObject()
         aclass.Grupa[aoid]=sd1
         aclass.Nazwa[aoid]=sd2[:-4]
         fin=open(adir+'/'+sd1+'/'+sd2)
         s=fin.read()
         fin.close()
         aclass.Tresc[aoid]=s
   return



