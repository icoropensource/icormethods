# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil

def SearchText(ltext1,ltext2):
   aclass=aICORDBEngine.Classes['CLASSES_System_ICORMethod']
   aobj=aclass.GetFirstObject()
   ltext1l=[ICORUtil.strLowerPL(x) for x in ltext1]
   ltext2l=[ICORUtil.strLowerPL(x) for x in ltext2]
   lret=[]
   while aobj:
      mtext=ICORUtil.strLowerPL(aobj.aMethodText)
      apos=string.find(mtext,ltext1l[0])
      if apos>=0:
         slm=string.split(aobj.aIDClassMethod,'_')
         bclass=aICORDBEngine.Classes[int(slm[0])]
         sl=string.split(mtext,'\n')
         i=0
         for s in sl:
            i=i+1
            w=1
            for ss in ltext1l:
               if string.find(s,ss)<0:
                  w=0
                  break
            if not w:
               continue
            for ss in ltext2l:
               if string.find(s,ss)>=0:
                  w=0
                  break
            if not w:
               continue
            lret.append([bclass.ClassPath,aobj.aMethodName,i,'  File "%s\\%s", line %d, in method'%(bclass.ClassPath,aobj.aMethodName,i)])
      aobj.Next()
   lret.sort()
   print 'ilosc wpisow:',len(lret)
   for sc,sm,si,sl in lret:
      print sl
   return

def SearchTerm(spatt):
   apatt=re.compile(spatt,re.I)
   aclass=aICORDBEngine.Classes['CLASSES_System_ICORMethod']
   aobj=aclass.GetFirstObject()
   dret={}
   while aobj:
      mtext=aobj.aMethodText
      lm=apatt.findall(mtext)
      for s in lm:
         dret[s]=1
      aobj.Next()
   ltext=dret.keys()
   ltext.sort()
   for s in ltext:
      print s

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
#   SearchText([' name=','<'],[' id=','<meta','<param','<font'])
   SearchTerm('icorapi.(.*?)\W')
   return
