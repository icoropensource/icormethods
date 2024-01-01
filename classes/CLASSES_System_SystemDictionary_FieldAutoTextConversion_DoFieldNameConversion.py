# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil
import re
import string

def GetFieldNameAutoExpand(Value):
   l=[]
   ss=''
   for c in Value:
      if c==' ' and ss:
         l.append(CLASSES_Library_ICORBase_Interface_ICORUtil.strLowerPL(ss))
         ss=''
      elif c in CLASSES_Library_ICORBase_Interface_ICORUtil._STRING_UPPERCASE_PL and ss:
         l.append(CLASSES_Library_ICORBase_Interface_ICORUtil.strLowerPL(ss))
         ss=c
      else:
         ss=ss+c
   if ss:
      l.append(CLASSES_Library_ICORBase_Interface_ICORUtil.strLowerPL(ss))
   aclass=aICORDBEngine.Classes['CLASSES_System_SystemDictionary_FieldAutoTextConversion']
   pdict={}
   aobj=aclass.GetFirstObject()
   while aobj.Exists():
      pdict[aobj.Name]=aobj.ToValue
      aobj.Next()
   for i in range(len(l)):
      aword=l[i]
      for afrom,ato in pdict.items():
#         if ato=='żłob':
#            print 'afrom: %s, ato: %s, aword_b: %s'%(afrom,ato,aword),
         aword=re.sub(afrom,ato,aword)
#         if ato=='żłob':
#            print 'aword_a: %s'%aword
      l[i]=aword
   if l:
      l[0]=CLASSES_Library_ICORBase_Interface_ICORUtil.strCapitalizePL(l[0])
   return string.join(l,' ')

