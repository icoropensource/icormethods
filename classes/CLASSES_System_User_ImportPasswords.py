# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORSecurity import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if OID<0:
      arefs=aclass.SelectObjects(acaption='Wybierz użytkownika wzorcowego',adisabletoolbar=0,adisableediting=0)
      if not arefs:
         return
      OID=arefs.OID
   print OID,aclass.UserName[OID]
   aprofile=ICORSecurityProfile()
   aprofile.SetByUser(OID)
   agroups=aclass.Groups[OID]
   fin=open(FilePathAsSystemPath('%ICOR%/tmp/passwords.txt'),'r')
   try:
      l=fin.readline()
      while l:
         boid,buser,bpassword=string.split(l[:-1],',')
         boid=int(boid)
         aoid=aclass.UserName.Identifiers(buser)
         if aoid<0:
            print '* Nowy użytkownik:',buser
            aprofile.AddUser(buser,buser,agroups)
         elif aoid<>boid:
            print ' Użytkownik',buser,'[',boid,'] znajduje się pod innym numerem OID:',aoid
         elif aclass.Password[aoid]!=bpassword:
            print '- Nowe haslo dla uzytkownika: %s %s %s'%(buser,bpassword,aclass.Password[aoid])
            aICORDBEngine.UserVars['PasswordChange']=1
            aclass.Password[aoid]=bpassword
            aICORDBEngine.UserVars['PasswordChange']=0
         l=fin.readline()
   finally:
      fin.close()
   return



