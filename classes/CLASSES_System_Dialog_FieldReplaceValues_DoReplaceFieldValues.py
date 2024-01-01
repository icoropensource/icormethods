# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
import string
import re

def SearchText(bfield,atext,anewtext='',are=1,acase=0):
   aclass=bfield.ClassItem
   aobj=aclass.GetFirstObject()
   acnt=0
   if are==1:
      if not acase:
         atext=strLowerPL(atext)
      p1=re.compile(atext,re.I)
      while aobj:
         mtext=bfield[aobj.OID]
         if p1.search(mtext):
            acnt=acnt+1
            if anewtext:
               mtext=p1.sub(anewtext,mtext)
               bfield[aobj.OID]=mtext
         aobj.Next()
   else:
      btext=atext
      if not acase:
         atext=strLowerPL(atext)
      while aobj:
         mtext=bfield[aobj.OID]
         if not acase:
            mtext=strLowerPL(mtext)
         w=1
         apos=string.find(mtext,atext)
         if apos<0:
            w=0
         if w:
            acnt=acnt+1
            if anewtext:
               mtext=string.replace(bfield[aobj.OID],btext,anewtext)
               bfield[aobj.OID]=mtext
         aobj.Next()
   return acnt

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

   if not aclass.EditObject(aoid):
      return

#   acasesensitive=str2bool(aclass.CaseSensitiveSearch[aoid])
   acasesensitive=1
   are=str2bool(aclass.RegularExpressionSearch[aoid])
   fromvalue=aclass.FromValue[aoid]
   tovalue=aclass.ToValue[aoid]
   count=SearchText(bfield,fromvalue,tovalue,are=are,acase=acasesensitive)
   if count:
      MessageDialog('Ilość zamienionych wartości: '+str(count),mtInformation,mbOK)
   else:
      MessageDialog('Nie znaleziono wartości spełniających zadane założenia.',mtInformation,mbOK)
   return

