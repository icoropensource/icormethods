# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil
import string

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   ClearStdOut()
   aclass=aICORDBEngine.Classes[CID]
   sdate=CLASSES_Library_ICORBase_Interface_ICORUtil.InputDate()
   if sdate=='':
      return
   adate=CLASSES_Library_ICORBase_Interface_ICORUtil.str2DateTime(sdate)
   mclass=aICORDBEngine.Classes['CLASSES_System_ICORMethod']
   aobj=mclass.GetFirstObject()
   mlist=[]
   while aobj:
      mdate=aobj.Class.aLastModified.ValuesAsComp(aobj.OID)
      if mdate>=adate:
         sl=string.split(aobj.aIDClassMethod,'_')
         mcid=int(sl[0])
         rclass=aICORDBEngine.Classes[mcid]
         if rclass is None:
            print 'Klasa:',mcid,'nie istnieje!'
         else:
            mlist.append((rclass.ClassPath,aobj.aMethodName,mdate))
      aobj.Next()
   mlist.sort()
   for aitem in mlist:
      print "   ['%s','%s'],   #%s"%(string.replace(aitem[0],'\\','_'),aitem[1],str(aitem[2]))
   return
