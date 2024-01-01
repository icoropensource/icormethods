# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def DoManageUsers(amenu,file):
   aclass=aICORDBEngine.Classes['CLASSES_System_User']
   file.write('%d : %s<br>'%(amenu.uid,aclass.UserName[amenu.uid]))
   aobj=aclass.GetFirstObject()
   file.write('<pre>\n')
   while aobj.Exists():
      file.write('%d,%s,%s\n'%(aobj.OID,aobj.UserName,aobj.Password))
      aobj.Next()
   file.write('</pre>\n')



