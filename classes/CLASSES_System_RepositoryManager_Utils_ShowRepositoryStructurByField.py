# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
import string

def ShowClassFields(aclass,aname,arecur,level):
   if (aclass.CID in arecur) and (level>1):
      return arecur
   arecur.append(aclass.CID)
   flist=aclass.GetFieldsList()
   flist.sort()
   print '<LI><OL>%s'%(aname)
   for fname in flist:
      afi=aclass.FieldsByName(fname)
#      if afi.IsInteractive!='1':
#         continue
#      if afi.WWWDisabled=='1':
#         continue
      if afi.FieldTID<=MAX_ICOR_SYSTEM_TYPE:
         print '<LI>%s</LI>'%(afi.FieldNameAsDisplayed)
      else:
         arecur=ShowClassFields(afi.ClassOfType,afi.FieldNameAsDisplayed,arecur,level+1)
   print '</OL></LI>'
   return arecur[:-1]

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   adialog=InputElementDialog('Wybierz klasę',0,0)
   if adialog.Show():
      aclass=aICORDBEngine.Classes[adialog.ClassPath]
      ClearStdOut()
      arecur=[]
      print '<OL>%s'%(aclass.NameOfClass)
      ShowClassFields(aclass,'',arecur,0)
      print '</OL'
   return

