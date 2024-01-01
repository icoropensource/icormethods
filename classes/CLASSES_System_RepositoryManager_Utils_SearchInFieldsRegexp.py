# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
import os
import re

BASE_DIR='d:/icor/tmp/'

def TraverseClasses(aclass):
   class CIterator(ICORRepositoryIterator):
      def __init__(self):
         ICORRepositoryIterator.__init__(self)
         #self.patt=re.compile('(session|ICOR_TCP_SERVER|ICOR_TCP_SERVER2|ICOR_TCP_SERVER_PORT|ICOR_TCP_SERVER_PORT2|ICOR_TCP_SERVER_PAGE|ICOR_TCP_SERVER_PAGE2|ICOR_TRANSPORT|ICOR_PATH|CONNECTION_STRING_BASE|CONNECTION_STRING|CONNECTION_STRING_PG|WWWDataPath|WWWUserFiles|WWWUserImages|DefaultTempPath|DefaultOutputPath|DEFAULT_EXECUTOR)',re.I+re.S+re.M)
         self.patt=re.compile('(session)',re.I+re.S+re.M)
      def OnPreField(self,aclass,afieldname):
         afield=aclass.FieldsByName(afieldname)
         if (afield.FieldTID==mt_Memo) or ((afield.FieldTID==mt_String) and int(afield.IsContainer)):
            spath='%s,%s'%(aclass.ClassPath.replace('\\','_'),afieldname)
            aobj=aclass.GetFirstObject()
            w=1
            while aobj:
               s=afield[aobj.OID]
               l=self.patt.findall(s)
               if l:
                  if w:
                     print spath,aobj.OID,l
                     w=0
                  fout=open('%sk1/%s,%d.py'%(BASE_DIR,spath,aobj.OID),'w')
                  fout.write(s)
                  fout.close()
                  #fout=open('%sk2/%s,%d.py'%(BASE_DIR,spath,aobj.OID),'w')
                  #fout.write(' '.join(l))
                  #fout.close()
               aobj.Next()
   CIterator().ForEachClass(aclass)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   if 1==0:
      l=os.listdir(BASE_DIR+'k1')
      for s in l:
         sclass,sfield,soid=os.path.splitext(s)[0].split(',')
         print sclass,sfield,soid
         aclass=aICORDBEngine.Classes[sclass]
         afield=aclass.FieldsByName(sfield)
         fin=open(BASE_DIR+'k1/'+s,'r')
         atext=fin.read()
         fin.close()
         afield[int(soid)]=atext
   else:
      adialog=InputElementDialog('Wybierz klasę',0,0)
      if adialog.Show():
         aclass=aICORDBEngine.Classes[adialog.ClassPath]
         ClearStdOut()
         TraverseClasses(aclass)
   return

