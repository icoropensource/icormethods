# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil

TEST_STR1=['aaa','bbbbbbbbbbbbb','asdasdasdfq1230781239871293120837y10823y917823','12387123987']
TEST_STR2=['ąćęłńóśźż','ĄĆĘŁŃÓŚŹŻ','qąwćeęrłtńyóuśiźożp','abcABC123!@#$%^&*()_+<>"\\umn/']
TEST_FILES=['d:/icor/SQL2005_Sys_Views.pdf','d:/icor/windows-shortcuts-3.pdf','d:/icor/aaaaaaa.bbb']
TEST_DATES=['2010/02/01 12:22:33','2010/02/01','2010-02-01','12:23:33','11/10/2005 17:22:26','11/10/2005 17:44']
TEST_URL=['a%20%21+bcd+efg',]

def TestHash():
   import hashlib
   for s in TEST_STR1:
      sh1=aICORDBEngine.HashString(s)
      sh2=hashlib.md5(s).hexdigest().upper()
      w=1
      if sh1<>sh2:
         w=0
      print w,sh1,sh2

def TestHashFile():
   import hashlib
   for afname in TEST_FILES:
      sh1=aICORDBEngine.HashFile(afname)
      amd5=hashlib.md5()
      try:
         fin=open(afname,'rb')
         try:
            while 1:
               adata=fin.read(65536)
               if not adata:
                  break
               amd5.update(adata)
         finally:
            fin.close()
         sh2=amd5.hexdigest().upper()
      except:
         sh2=''
      w=1
      if sh1<>sh2:
         w=0
      print w,sh1,sh2

def TestStrings():
   for s in TEST_STR2:
      s1=ICORUtil.ICORLowerCase(s)
      s2=ICORUtil.strLowerPL(s)
      print s,s1,s2,ICORUtil.ICORCompareText(s,s1),ICORUtil.ICORCompareText(s+'A',s1),ICORUtil.ICORCompareText(s,s1+'A')

def TestDates():
   for sdt in TEST_DATES:
      s1=ICORUtil.str2DateTime(sdt)
      s2=ICORUtil.getStrAsDateTime(sdt)
      print sdt,s1,s2

def str2HTMLstr(s):
   s=XMLUtil.CP1250_To_UTF8(s)
   ret=''
   for c in s:
      if ord(c)>127:
         ret=ret+'&#'+str(ord(c))+';'
      else:
         ret=ret+c
   return ret

def CP1250_To_Str(s):
   data=re.sub(r'\\u([a-f0-9][a-f0-9][a-f0-9][a-f0-9])',lambda x:'&#'+str(int(x.group(1),16))+';',unicode(s,'cp1250','ignore').encode('raw_unicode_escape','xmlcharrefreplace'))
   return data
#   return unicode(s,'cp1250','ignore').encode('unicode_escape',amode)

def TestHTMLStr():
   for s in TEST_STR2:
      s1=ICORUtil.str2HTMLstr(s)
      s1a=str2HTMLstr(s)
      s1b=CP1250_To_Str(s)
      s2=XMLUtil.GetAsXMLStringNoPL(s)
      s3=XMLUtil.GetAsXMLString(s)
      print '%s | %s | %s | %s | %s | %s<hr>'%(s,s1,s1b,s1a,s2,s3)

def TestURL():
   import urllib
   for s in TEST_URL:
      s1=ICORUtil.URLString2NormalString(s)
      s2=urllib.unquote_plus(s)
      print s,s1,s2

def TestGetFieldProperty():
   attrs=['FieldValueAsString','FieldAccess', \
      'FieldDescription','FieldNameAsDisplayed','FieldFormat','IsAliased','IsContainer', \
      'AllowRead','AllowWrite','FieldPath','FieldType','FID', \
      'IsVirtual','IsCached', \
      'IsFastIndexed','IsIndexed','IsInteractive','IsObligatory', \
      'Alignment','AlignmentStd','FieldEditor', \
      'FieldPosition','FieldLVColWidth','FieldLeft','FieldTop','FieldWidth','FieldHeight',
      'FieldNamePosition','FieldDefaultDblClickAction','FieldSheetID','FieldTabIndex',\
      'IsReadOnly','FieldOwnerClassID','IsReportProtected']
   xattrs=['LastModified','FieldDefaultValueAsString']
   lclasses=['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Projekt']
   for aclasspath in lclasses:
      wc=0
      aclass=aICORDBEngine.Classes[aclasspath]
      for afield in aclass.FieldsIterator():
         wf=0
         for aattr in attrs:
            s1=getattr(afield,aattr)
            s2=getattr(afield,'x'+aattr)
            if s1!=s2:                
               if not wc:
                  print '@@@ CLASS:',aclass.ClassPath
                  wc=1
               if not wf:
                  print '  @@@ FIELD:',afield.FName
                  wf=1
               print '    > [%s] {%s} {%s}'%(aattr,s1,s2)

def TestGetMethodProperty():
   attrs=('MethodAccess','MethodDescription', \
      'MethodPath','MID','IsMenuHidden','Language','WWWDescription')
   sattrs=['MethodText','AllowRead','AllowWrite','LastModified',]
   xattrs=[]
   lclasses=['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Projekt']
   for aclasspath in lclasses:
      wc=0
      aclass=aICORDBEngine.Classes[aclasspath]
      for amethod in aclass.MethodsIterator():
         wf=0
         for aattr in attrs:
            s1=getattr(amethod,aattr)
            s2=getattr(amethod,'x'+aattr)
            if s1!=s2:                      
               if not wc:
                  print '@@@ CLASS:',aclass.ClassPath
                  wc=1
               if not wf:
                  print '  @@@ METHOD:',amethod.Name
                  wf=1
               print '    > [%s] {%s} {%s} (%s)'%(aattr,s1,s2,type(s1))
            else:
               pass
               print '    = [%s] {%s} {%s} (%s)'%(aattr,s1,s2,type(s1))

def ShowFieldValue():
   aclass=aICORDBEngine.Classes['CLASSES_System_ICORField']
   aoid=8917
   print aclass.aFieldName[aoid],aclass.aFieldAlignment[aoid]

def TestObjects():
   aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Projekt']
   aobj=aclass.GetFirstObject()
   acnt=4
   while aobj and acnt:
      print '##',aobj.OID
      for afield in aclass.FieldsIterator():
         print '  ',aobj.OID,afield.FName,afield[aobj.OID]
      acnt=acnt-1
      aobj.Next()

def TestMethodPath():
   lcpaths=['CLASSES_Library_Test_Struct_Test1','CLASSES_Library_Test_Struct_Test1_Test2','CLASSES_Library_Test_Struct_Test1_Test2_Test3','CLASSES_Library_Test_Struct_Test1_Test2_Test3_Test4']
   for acpath in lcpaths:
      aclass=aICORDBEngine.Classes[acpath]
      amethod=aclass.Metoda1
      print amethod.MOID,amethod.MethodPath,acpath

def TestGetClassProperty():
   attrs=['ClassDescription','IsSystem','IsVirtual', \
         'ClassColIDWidth','ClassFormLeft','ClassFormTop', \
         'ClassFormWidth','ClassFormHeight','ClassFieldsHidden', \
         'ReportClass','MaxOID','IsReadOnly','BaseCID']
   attrs=attrs+['NameOfClass','BasePath','ClassPath',]
   xattrs=['AllowRead','AllowWrite','LastModified',]
   lclasses=['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Projekt','CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Struktura','CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Rozdzial']
   for aclasspath in lclasses:
      wc=0
      aclass=aICORDBEngine.Classes[aclasspath]
      for aattr in attrs:
         s1=getattr(aclass,aattr)
         s2=getattr(aclass,'x'+aattr)
         if s1!=s2:                      
            if not wc:
               print '@@@ CLASS:',aclass.ClassPath
               wc=1
            print '    > [%s] {%s} {%s} (%s)'%(aattr,s1,s2,type(s1))
         else:
            pass
            #print '    = [%s] {%s} {%s} (%s)'%(aattr,s1,s2,type(s1))

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   #TestHash()
   #TestHashFile()
   #TestStrings()
   #TestDates()
   #TestHTMLStr()
   #TestURL()
   #TestGetFieldProperty()
   #ShowFieldValue()
   #TestObjects()
   #TestGetMethodProperty()
   #TestMethodPath()
   TestGetClassProperty()
   return
