# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import string,re

def ChangeMain(aclass):
   aobj=aclass.GetFirstObject()
   s1="def ICORMain\(CID\=\-1\, FieldName\=\'\'\, OID\=\-1\, Value\=\'\'\)\:"
   s2="[^ ]ICORMain"
   s3="ICORMain"
   p1=re.compile(s1,re.I)
   p2=re.compile(s2,re.I)
   p3=re.compile(s3,re.I)
   i=1
   while aobj and i<=10000:
      atext=aobj.aMethodText
      if p1.search(atext):
         atext=string.replace(atext,"def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):","def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):")
         aobj.aMethodText=atext
         if p2.search(atext):
            print i,'S1:',aobj.aIDClassMethod
      elif p3.search(atext):
         print i,'   S2:',aobj.aIDClassMethod
      i=i+1
      aobj.Next()
   return

def SearchTextAndView(aclass,amax=1000,afname=''):
#   atext=ICORUtil.strLowerPL(atext)
   aobj=aclass.GetFirstObject()
   lret=[]
   acnt=0
   while aobj:
      w=0
      mtext=aobj.aMethodText
      mtext=string.replace(mtext,chr(13),'')
      sl=string.split(mtext,chr(10))
      ll=[]
      for s in sl:
         spos=string.find(s,'=')
         if s and spos>0 and s[:4]!='def ' and s[:6]!='class ' and s[:5]!='from ' and s[:7]!='import ' and s[:3]!='if ' and s[:4]!='var ' and not s[:1] in [' ','#','>','<','-','%','\\','/','"',"'",]:
            w=1
            ll.append(s)
            acnt=acnt+1
            if acnt>amax:
               break
      if w:
         sl=string.split(aobj.aIDClassMethod,'_')
         bclass=aICORDBEngine.Classes[int(sl[0])]
         lret.append(['%s\\%s'%(bclass.ClassPath,aobj.aMethodName),ll])
      if acnt>amax:
         break
      aobj.Next()
   lret.sort()
   fout=open(afname,'w')
   try:
      for s,ll in lret:
         fout.write('\n############################################################\n#%s\n'%s)
         for s1 in ll:
            s1=string.replace(s1,'"""','')
            s1=string.replace(s1,"'''",'')
            fout.write('   %s\n'%s1)
   finally:
      fout.close()
   return

def SaveTexts(aclass):
   aobj=aclass.GetFirstObject()
   while aobj:
      if aobj.aMethodName=='OnWWWAction':
         dt=string.replace(aobj.aLastModified,':','_')
         dt=string.replace(dt,' ','_')
         dt=string.replace(dt,'/','_')
         fout=open('c:/icor/tmp/OnWWWAction_'+dt+' '+str(aobj.OID)+'.py','w')
         fout.write(string.replace(aobj.aMethodText,chr(13),''))
         fout.close()
      aobj.Next()

def SearchText(aclass,atext,anewtext=''):
   atext=ICORUtil.strLowerPL(atext)
   aobj=aclass.GetFirstObject()
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
   lret.sort()
   for s in lret:
      print s
   return

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   SearchText(aclass,'\.addobject\(.+?\,.+?\)','')
#   SaveTexts(aclass)
#   return
#   ChangeMain(aclass)
#   SearchText(aclass,'self\.[^ ]*?\(.*?\).*? or ','')
#   SearchTextAndView(aclass,amax=10000000,afname='c:/icor/globals.py')

   return
   aobj=aclass.GetFirstObject()
   alen=0
   while aobj.Exists():
      blen=len(aobj.aMethodText)
      if blen>alen:
         sl=string.split(aobj.aIDClassMethod,'_')
         bclass=aICORDBEngine.Classes[int(sl[0])]
#         print 'len:',alen
         print '  File "%s\\%s", line %d, in method'%(bclass.ClassPath,aobj.aMethodName,1)
         alen=blen
      aobj.Next()
   return

   print '{}'
   SearchText(aclass,'def.*\(.*\=.*\{.*\}.*\)')
   print '[]'
   SearchText(aclass,'def.*\(.*\=.*\[.*\].*\)')

