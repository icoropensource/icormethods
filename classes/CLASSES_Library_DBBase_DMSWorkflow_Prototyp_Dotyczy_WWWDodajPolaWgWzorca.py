# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import string

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Pola',adisplayed='Pola',atype=mt_Memo,avalue='')
   return awwweditor

def RegisterFieldsStep1(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Field1',adisplayed='Pole S',atype=mt_String,avalue='ABC')
   awwweditor.RegisterField('Field2',adisplayed='Pole I',atype=mt_Integer,avalue='123')
   awwweditor.RegisterField('Field3',adisplayed='Pole DT',atype=mt_DateTime,avalue='2002/02/02')
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
      tclass=aobj.Class.Pola.ClassOfType.TypPolaDotyczy.ClassOfType
      file.write('<hr><h3>Format opisu danych</h3>nazwa_pola|[nazwa_widoczna]|typ_pola<br>nazwa_pola|[nazwa_widoczna]|typ_pola<br>nazwa_pola|[nazwa_widoczna]|typ_pola<br><hr><h3>Typy pól</h3>')
      toid=tclass.Opis.GetFirstValueID()
      while toid>=0:
         file.write('%s<br>'%tclass.Opis[toid])
         toid=tclass.Opis.GetNextValueID(toid)
   return 2 # show back reference to main object (1-link, 2-button)

def OnWWWActionSubmit(aobj,amenu,areport,file):
   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
   lpola=string.split(string.replace(awwweditor['Pola'],'\r',''),'\n')
   pclass=aobj.Class.Pola.ClassOfType
   tclass=pclass.TypPolaDotyczy.ClassOfType
   file.write('<h2>Dodane pola</h2>')
   w=1
   for aline in lpola:
      ldane=string.split(aline,'|')
      toid=tclass.Opis.Identifiers(ldane[2])
      if toid<=0:
         file.write('<font color="red">Nieznany typ pola: "%s" dla pola "%s"</font><br>'%(ldane[2],ldane[1]))
         w=0
   if w:
      atabid=0
      pobj=aobj.Pola
      while pobj:
         aid=pobj.Class.SGTabIndex.ValuesAsInt(pobj.OID)
         if aid>atabid:
            atabid=aid
         pobj.Next()
      atabid=atabid+10
      prefs=[]
      for aline in lpola:
         ldane=string.split(aline,'|')
         if not ldane[1]:
            ldane[1]=ldane[0]
         toid=tclass.Opis.Identifiers(ldane[2])
         if toid<=0:
            file.write('<font color="red">Nieznany typ pola: "%s" dla pola "%s"</font><br>'%(ldane[2],ldane[1]))
         else:
            poid=pclass.AddObject(arefobject=aobj)
            pclass.Nazwa[poid]=ldane[0]
            pclass.NazwaWidoczna[poid]=ldane[1]
            pclass.TypPolaDotyczy[poid]=[toid,tclass.CID]
            pclass.SGTabIndex[poid]=str(atabid)
            if ldane[2] in ['HTML','Opis','OID']:
               pclass.SGIsAliased[poid]='0'
            else:
               pclass.SGIsAliased[poid]='1'
            pclass.SGIsIndexed[poid]='1'
            pclass.SGIsSearch[poid]='1'
            prefs.append([poid,pclass.CID])
            atabid=atabid+10
            file.write('Dodano pole: %s<br>'%ldane[1])
      aobj.Class.Pola.AddRefs(aobj.OID,prefs,asortedreffield=pclass.SGTabIndex)
   awwweditor.WriteObjectView(aobj,asbutton=1)



