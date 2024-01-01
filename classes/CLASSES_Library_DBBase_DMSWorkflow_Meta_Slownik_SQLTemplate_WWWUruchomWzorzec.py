# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import re
import string

def SQLTemplate2Fields(s):
   apatt=re.compile('\<.*?\>')
   l1=apatt.findall(s)
   l2=[]
   d1={}
   for s in l1:
      if d1.has_key(s):
         continue
      d1[s]=1
      ls=string.split(s[1:-1],',')
      try:
         l2.append([s,string.strip(ls[0]),string.strip(ls[1]),string.strip(ls[2]),])
      except:
         print 'error:',s,ls
   return l2

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   l=SQLTemplate2Fields(aclass.Tresc[aoid])
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   for s1,s2,s3,s4 in l:
      awwweditor.RegisterField(s2,adisplayed=s2,atype=mt_String,avalue=s4)
   return awwweditor

def RegisterFieldsStep1(aclass,amenu,file,aoid=-1,areport=None,avalue=''):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
                       
   pclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Struktura']
   pobj=pclass.GetFirstObject()
   while pobj:
      if ICORSecurity.CheckRecursiveAccessLevelForUser(pobj,'AccessLevelView',amenu.uid):
         break
      pobj.Next()
   if pobj:
      awwweditor.RegisterField('Projekt',adisplayed='Projekt',aoid=pobj.OID,aclassitem=pobj.Class)

   awwweditor.RegisterField('tresc',adisplayed='Wzorzec SQL',atype=mt_Memo,avalue=avalue)
#   awwweditor.RegisterField('Field2',adisplayed='Pole I',atype=mt_Integer,avalue='123')
#   awwweditor.RegisterField('Field3',adisplayed='Pole DT',atype=mt_DateTime,avalue='2002/02/02')
   return awwweditor

def OnBeforeWWWAction(aobj,amenu,file):
   w=1
   if 0:
      w=w and ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelView',amenu.uid)
   if 0:
      w=w and ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelEdit',amenu.uid)
   if 0:
      w=w and ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelDelete',amenu.uid)
   return w

def OnWWWAction(aobj,amenu,file):
   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   if amenu.Action=='ObjectApplyMethods':
      awwweditor.Write()
   return 0 # show back reference to main object (1-link, 2-button)

def OnWWWActionSubmit(aobj,amenu,areport,file):
   if not areport['refMode']:
      awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
      atresc=aobj.Tresc
      l=SQLTemplate2Fields(atresc)
      for s1,s2,s3,s4 in l:
         avalue=awwweditor[s2]
         atresc=string.replace(atresc,s1,avalue)
      bwwweditor=RegisterFieldsStep1(aobj.Class,amenu,file,aobj.OID,None,avalue=atresc)
      bwwweditor.Write(arefMode='step1')
   elif areport['refMode']=='step1':
      awwweditor=RegisterFieldsStep1(aobj.Class,amenu,file,aobj.OID,areport)
      file.write('<h1>Step 1</h1>')
      file.write('<h2>Field 1: %s</h2>'%awwweditor['Projekt'])
      file.write('<h2>Field 2: %s</h2>'%awwweditor['tresc'])



