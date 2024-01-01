# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
import string
import re

def SearchText(atext,anewtext='',are=1,acase=0):
   aclass=aICORDBEngine.Classes['CLASSES_System_ICORMethod']
   aobj=aclass.GetFirstObject()
   if are==1:
      if not acase:
         atext=strLowerPL(atext)
      p1=re.compile(atext,re.I)
      lret=[]
      while aobj:
         mtext=aobj.aMethodText
         if p1.search(mtext):
            sl=string.split(mtext,'\n')
            i=1
            for s in sl:
               if p1.search(s):
                  break
               i=i+1
            sl=string.split(aobj.aIDClassMethod,'_')
            bclass=aICORDBEngine.Classes[int(sl[0])]
            lret.append('  File "%s\\%s", line %d, in method'%(bclass.ClassPath,aobj.aMethodName,i))
            if anewtext:
               mtext=p1.sub(anewtext,mtext)
               aobj.aMethodText=mtext
         aobj.Next()
   else:
      btext=atext
      if not acase:
         atext=strLowerPL(atext)
      ltext=string.split(atext,'|')
      lret=[]
      while aobj:
         mtext=aobj.aMethodText
         if not acase:
            mtext=strLowerPL(mtext)
         w=1
         for aword in ltext:
            apos=string.find(mtext,aword)
            if apos<0:
               w=0
               break
         if w:
            sl=string.split(mtext,'\n')
            i=1
            for s in sl:
               if string.find(s,ltext[0])>=0:
                  break
               i=i+1
            sl=string.split(aobj.aIDClassMethod,'_')
            bclass=aICORDBEngine.Classes[int(sl[0])]
            lret.append('  File "%s\\%s", line %d, in method'%(bclass.ClassPath,aobj.aMethodName,i))
            if anewtext:
               mtext=string.replace(aobj.aMethodText,btext,anewtext)
               aobj.aMethodText=mtext
         aobj.Next()
   lret.sort()
   for s in lret:
      print s
   return

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if OID<0:
      adialog=InputElementDialog('Wybierz klasę',0,0)
      if not adialog.Show():
         return
      bclass=aICORDBEngine.Classes[adialog.ClassPath]
      if bclass is None:
         return
   else:
      bclass=aICORDBEngine.Classes[OID]
   aoid=aclass.FirstObject()
   if aoid<0:
      aoid=aclass.AddObject()
   if not aclass.EditObject(aoid):
      return
   atext=aclass.SearchText[aoid]
   if atext:
      acasesensitive=str2bool(aclass.CaseSensitiveSearch[aoid])
      are=str2bool(aclass.RegularExpressionSearch[aoid])
      SearchText(atext,'',are=are,acase=acasesensitive)
   return

