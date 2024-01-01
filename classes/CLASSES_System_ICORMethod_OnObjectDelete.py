# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import os

def DeleteMethodText(bclass,bcid,bmname):
   #print 'DeleteMethodText:',bclass.ClassPathImport,bclass.CID,bcid,bmname,bclass.IsMethodInThisClass(bmname)
   if bclass.CID==bcid:
      pass
   elif bclass.IsMethodInThisClass(bmname):
      return
   fpath=FilePathAsSystemPath('%%ICOR%%/python/methods/%s_%s.py'%(bclass.ClassPathImport,bmname))
   if os.path.exists(fpath):
      try:
         os.unlink(fpath)
      except:
         print 'Cant delete method text: %s'%fpath
   alist=bclass.GetInheritedClassesList()
   for icid in alist:
      dclass=aICORDBEngine.Classes[icid]
      DeleteMethodText(dclass,bcid,bmname)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aidmethod=aclass.aIDClassMethod[OID]
   bcid,bmname=aidmethod.split('_')
   bcid=int(bcid)
   bclass=aICORDBEngine.Classes[bcid]
   DeleteMethodText(bclass,bcid,bmname)
   return

