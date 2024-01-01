# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *

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
   pobj=aobj.Pola
   file.write('<pre>')
   while pobj:
      if not pobj.Nazwa in ['_ChapterID','_OIDDictRef','Informacja opis czynności','Informacja data wytworzenia','Informacja osoba odpowiedzialna','Informacja podmiot udostępniający',]:
         file.write('%s|%s|%s\n'%(pobj.Nazwa,pobj.NazwaWidoczna,pobj.TypPolaDotyczy.Opis))
      pobj.Next()
   file.write('</pre>')
   return 2 # show back reference to main object (1-link, 2-button)



