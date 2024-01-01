# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   arefs=aclass.SelectObjects()
   if not arefs:
      return
   fout=open(FilePathAsSystemPath('%ICOR%/tmp/users.xml'),'w')
   try:
      fout.write('<?xml version="1.0" encoding="windows-1250"?>\n\n')
      fout.write('<PROFILE name="">\n\n')
      while arefs:
#         fout.write('<USER name="%s" password="%s" firstname="%s" lastname="%s" email="%s" uid="%d" hash="%d" >\n'%(arefs.Class.UserName[arefs.OID],arefs.Class.Password[arefs.OID],arefs.Class.VCFFirstName[arefs.OID],arefs.Class.VCFLastName[arefs.OID],'',arefs.OID,1))
         fout.write('<USER uid="%d" name="%s" password="%s" firstname="%s" lastname="%s" email="%s" >\n'%(arefs.OID,arefs.Class.UserName[arefs.OID],arefs.Class.UserName[arefs.OID],arefs.Class.VCFFirstName[arefs.OID],arefs.Class.VCFLastName[arefs.OID],'',))
         brefs=arefs.Class.Groups.GetRefList(arefs.OID)
         while brefs:
                    
            fout.write('  <SECURITYUSERGROUP name="%s" accesslevel="%s" >\n'%(brefs.Class.Name[brefs.OID],brefs.Class.AccessLevel[brefs.OID]))
            grefs=brefs.Class.Groups.GetRefList(brefs.OID)
            while grefs:
               fout.write('    <SECURITYBASEGROUP name="%s" />\n'%(grefs.Class.Name[grefs.OID]))
               grefs.Next()
            fout.write('  </SECURITYUSERGROUP>\n')

            fout.write('  <USERGROUP name="%s" />\n'%(brefs.Class.Name[brefs.OID],))
            brefs.Next()
         fout.write('</USER>\n')
         arefs.Next()
      fout.write('\n</PROFILE>\n')
   finally:
      fout.close()      
   return

