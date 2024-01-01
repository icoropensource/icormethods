# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Nazwa',aoid=aoid)
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

class ITSourceTable:
   def __init__(self,aclass,aoid):
      self.ClassItem=aclass
      self.OID=aoid
      self.Fields={}
      self.FieldsID={}
      self.FieldsOIDs={}
      self.EventsOIDs={}
      arefs=self.ClassItem.Pola.GetRefList(aoid)
      while arefs:
         self.Fields[arefs.Nazwa[arefs.OID]]=1
         self.FieldsID[arefs.NazwaID[arefs.OID]]=1
         self.FieldsOIDs[arefs.OID]=1
         arefs.Next()
      arefs=self.ClassItem.TableEvents.GetRefList(aoid)
      while arefs:
         self.EventsOIDs[arefs.OID]=1
         arefs.Next()
   def __repr__(self):
      return str(self.OID)

class ITMain:
   def __init__(self,aobj):
      self.ClassItem=aobj.Class
      self.OID=aobj.OID
      self.DotyczyClass=self.ClassItem.BazyZrodlowe.ClassOfType
      self.BZRTables={}
      self.FieldsOIDs={}
      self.EventsOIDs={}
   def ProcessDuplicates(self,adict,btable,bdict):
      for aid in bdict.keys():
         l=adict.get(aid,[])
         l.append(btable)
         adict[aid]=l
   def GetBZRTable(self,aoid):
      atable=self.BZRTables.get(aoid,None)
      if atable is None:
         if self.DotyczyClass.ObjectExists(aoid):
            atable=ITSourceTable(self.DotyczyClass,aoid)
            self.ProcessDuplicates(self.FieldsOIDs,atable,atable.FieldsOIDs)
            self.ProcessDuplicates(self.EventsOIDs,atable,atable.EventsOIDs)
         self.BZRTables[aoid]=atable
      return atable
   def ProcessTables(self):
      aobj=self.ClassItem[self.OID]
      dobj=aobj.BazyZrodlowe
      while dobj:
         atable=self.GetBZRTable(dobj.OID)
         dobj.Next()

def OnWWWAction(aobj,amenu,file):
#   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   if amenu.Action=='ObjectApplyMethods':
#      awwweditor.Write()
      lstatus=[]
      if not aobj.AppPath:
         lstatus.append([0,'Wpisz ścieżkę generowania projektu do pola AppPath'])
      if not aobj.BaseNameModifier:
         lstatus.append([0,'Wpisz modyfikator nazwy w polu BaseNameModifier'])
      if not aobj.DBAccess:
         lstatus.append([0,'Wybierz ścieżkę dostępu do bazy danych w projekcie'])
      if not aobj.HTTPServerParameters:
         lstatus.append([0,'Wybierz parametry serwera WWW'])
      aitmain=ITMain(aobj)

      aitmain.ProcessTables()
      for afieldid,ltables in aitmain.FieldsOIDs.items():
         if len(ltables)>1:
            lstatus.append([0,'Pole: %d występuje w więcej niż jednej tabeli: %s'%(afieldid,str(ltables))])
      for afieldid,ltables in aitmain.EventsOIDs.items():
         if len(ltables)>1:
            lstatus.append([0,'Zdarzenie: %d występuje w więcej niż jednej tabeli: %s'%(afieldid,str(ltables))])

      dobj=aobj.BazyZrodlowe
      if not dobj:
         lstatus.append([0,'Projekt nie posiada zdefiniowanych tabel'])
      else:
         while dobj:
            if not dobj.Class.ObjectExists(dobj.OID):
               lstatus.append([0,'Projekt posiada przypisaną skasowaną tabelę OID: %d'%dobj.OID])
            else:

               zd={}
               zobj=dobj.Zakladki
               if not zobj:
                  lstatus.append([0,'Tabela %s nie posiada zdefiniowanych zakładek OID: %d'%(dobj.Nazwa,dobj.OID)])
               else:
                  while zobj:
                     if zd.has_key(zobj.ZakladkaID):
                        lstatus.append([0,'Tabela %s posiada zakładkę o powtórzonym identyfikatorze OID: %d, ZOID: %d'%(dobj.Nazwa,dobj.OID,zobj.OID)])
                     if zobj.Nazwa in zd.values():
                        lstatus.append([0,'Tabela %s posiada zakładkę o powtórzonej nazwie OID: %d, ZOID: %d'%(dobj.Nazwa,dobj.OID,zobj.OID)])
                     zd[zobj.ZakladkaID]=zobj.Nazwa
                     if not zobj.ZakladkaID:
                        lstatus.append([0,'Tabela %s posiada zakładkę bez identyfikatora OID: %d, ZOID: %d'%(dobj.Nazwa,dobj.OID,zobj.OID)])
                     if not zobj.Nazwa:
                        lstatus.append([0,'Tabela %s posiada zakładkę bez nazwy OID: %d, ZOID: %d'%(dobj.Nazwa,dobj.OID,zobj.OID)])
                     zobj.Next()
               pobj=dobj.Pola
               if not pobj:
                  lstatus.append([0,'Tabela %s nie posiada zdefiniowanych pól OID: %d'%(dobj.Nazwa,dobj.OID)])
               lobj=dobj.PolaczeniaDoTabel
               while lobj:
                  lsobj=lobj.SourceTable
                  ldobj=lobj.DestinationTable
                  ssl=string.split(lobj.SourceFieldID,',')
                  if not lsobj:
                     lstatus.append([0,'Połączenie do tabeli nie posiada zdefiniowanej tabeli. Tabela: "%s", OID: %d, LOID: %d'%(dobj.Nazwa,dobj.OID,lobj.OID)])
                  else:
                     stable=aitmain.GetBZRTable(lsobj.OID)
                     if stable is None:
                        lstatus.append([0,'Połączenie do tabeli posiada zdefiniowaną tabelę - skasowaną. Tabela: "%s", OID: %d, LOID: %d'%(dobj.Nazwa,dobj.OID,lobj.OID)])
                     else:
                        for afname in ssl:
                           if not stable.FieldsID.has_key(afname) and not afname in ['_OID',]:
                              lstatus.append([0,'Połączenie do tabeli posiada zdefiniowane pole nieistniejące w tabeli źródłowej. Tabela: "%s", OID: %d, LOID: %d, Field: %s'%(dobj.Nazwa,dobj.OID,lobj.OID,afname)])
                  sdl=string.split(lobj.DestinationFieldID,',')
                  if not ldobj:
                     lstatus.append([0,'Połączenie do tabeli nie posiada zdefiniowanej tabeli docelowej. Tabela: "%s", OID: %d, LOID: %d'%(dobj.Nazwa,dobj.OID,lobj.OID)])
                  else:
                     dtable=aitmain.GetBZRTable(ldobj.OID)
                     if dtable is None:
                        lstatus.append([0,'Połączenie do tabeli posiada zdefiniowaną tabelę docelową - skasowaną. Tabela: "%s", OID: %d, LOID: %d'%(dobj.Nazwa,dobj.OID,lobj.OID)])
                     else:
                        for afname in sdl:
                           if not dtable.FieldsID.has_key(afname) and not afname in ['_OID',]:
                              lstatus.append([0,'Połączenie do tabeli posiada zdefiniowane pole docelowe nieistniejące w tabeli. Tabela: "%s", OID: %d, LOID: %d, Field: %s'%(dobj.Nazwa,dobj.OID,lobj.OID,afname)])
                  if not zd.has_key(lobj.LinkTabID):
                     lstatus.append([0,'Połączenie do tabeli nie posiada zdefiniowanej zakładki. Tabela: "%s", OID: %d, LOID: %d'%(dobj.Nazwa,dobj.OID,lobj.OID)])
                  lobj.Next()
            dobj.Next()
      file.write('<h1>Status projektu</h1>')
      file.write('<pre>')
      for apriority,aline in lstatus:
         file.write(aline+'\n')
      file.write('</pre>')
   return 2 # show back reference to main object (1-link, 2-button)

def OnWWWActionSubmit(aobj,amenu,areport,file):
   if not areport['refMode']:
      awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
      file.write('<h1>Step 0</h1>')
      file.write('<h2>Field : %s</h2>'%awwweditor['Nazwa'])
      bwwweditor=RegisterFieldsStep1(aobj.Class,amenu,file,aobj.OID,None)
      bwwweditor.Write(arefMode='step1')
   elif areport['refMode']=='step1':
      awwweditor=RegisterFieldsStep1(aobj.Class,amenu,file,aobj.OID,areport)
      file.write('<h1>Step 1</h1>')
      file.write('<h2>Field 1: %s</h2>'%awwweditor['Field1'])
      file.write('<h2>Field 2: %s</h2>'%awwweditor['Field2'])
      file.write('<h2>Field 3: %s</h2>'%awwweditor['Field3'])


