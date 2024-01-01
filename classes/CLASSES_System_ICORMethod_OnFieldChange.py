# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil

#ąćęłńóśź ĄĆĘŁŃÓSŹŻ


def SaveMethodText(bclass,bcid,bmname,atext):
   #print 'SaveMethodText:',bclass.ClassPathImport,bclass.CID,bcid,bmname,bclass.IsMethodInThisClass(bmname)
   if bclass.CID==bcid:
      pass
   elif bclass.IsMethodInThisClass(bmname):
      return
   try:
      fpath=FilePathAsSystemPath('%%ICOR%%/python/methods/%s_%s.py'%(bclass.ClassPathImport,bmname))
      fout=open(fpath,'w')
      fout.write(atext)
      fout.close()
   except:
      print 'cant save method: %s'%(fpath,)
   alist=bclass.GetInheritedClassesList()
   for icid in alist:
      dclass=aICORDBEngine.Classes[icid]
      SaveMethodText(dclass,bcid,bmname,atext)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if FieldName=='aMethodText':
      atext=aclass.aMethodText[OID]
      atext=atext.replace(chr(13),'')
      if atext.find('# -*- coding: ')!=0:
         if 1:
            atext='# -*- coding: windows-1250 -*-'+chr(10)+'# saved: '+ICORUtil.tdatetime2fmtstr()+chr(10)+chr(10)+atext
         else:
            atext='# -*- coding: utf-8 -*-'+chr(10)+'# saved: '+ICORUtil.tdatetime2fmtstr()+chr(10)+chr(10)+atext
            atext=XMLUtil.CP1250_To_UTF8(atext)
      aidmethod=aclass.aIDClassMethod[OID]
      bcid,bmname=aidmethod.split('_')
      bcid=int(bcid)
      bclass=aICORDBEngine.Classes[bcid]
      SaveMethodText(bclass,bcid,bmname,atext)
   return

