# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_DBBase_Util_Excel_HTMLXLSTable as HTMLXLSTable
import string

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
#   awwweditor.RegisterField('Nazwa',aoid=aoid)
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

def GetValueAsInt(avalue):
   if avalue is None or avalue=='':
      return 0
   try:
      v=int(avalue)
   except:
      print 'value:',avalue
      raise
   return 

class Week:
   def __init__(self,adata,anrkolejnytygodnia,aprzesylkiakcje,adostarczenieniepoznijenizxtygodni1,aprzesylkibiezace,adostarczenieniepoznijenizxtygodni2,awydajnosctygodniowagonca):
      self.Data=adata
      self.NrKolejnyTygodnia=GetValueAsInt(anrkolejnytygodnia)
      self.PrzesylkiAkcje=GetValueAsInt(aprzesylkiakcje)
      self.DostarczenieNiePozniejNizXTygodni1=GetValueAsInt(adostarczenieniepoznijenizxtygodni1)
      self.PrzesylkiBiezace=GetValueAsInt(aprzesylkibiezace)
      self.DostarczenieNiePozniejNizXTygodni2=GetValueAsInt(adostarczenieniepoznijenizxtygodni2)
      self.WydajnoscTygodniowaGonca=GetValueAsInt(awydajnosctygodniowagonca)
   def __repr__(self):
      return self.AsString()
   def __str__(self):
      return self.AsString()
   def AsString(self):
      return string.join(map(repr,[self.Data,self.NrKolejnyTygodnia,self.PrzesylkiAkcje,self.DostarczenieNiePozniejNizXTygodni1,self.PrzesylkiBiezace,self.DostarczenieNiePozniejNizXTygodni2,self.WydajnoscTygodniowaGonca]),' ')

class Weeks:
   def __init__(self):
      self.weeks=[]
   def AddWeek(self,aweek):
      self.weeks.append(aweek)
   def Dump(self,afile=None):
      if afile:
         for aweek in self.weeks:
            afile.write(aweek.AsString()+'\n')
      else:
         for aweek in self.weeks:
            print aweek

def PobierzDane(atable):
   afirstrow=2
   aweeks=Weeks()
   for i in range(afirstrow,afirstrow+52):
      adata=atable[1,i].Value
      anrkolejnytygodnia=atable[2,i].Value
      aprzesylkiakcje=atable[3,i].Value
      adostarczenieniepoznijenizxtygodni1=atable[4,i].Value
      aprzesylkibiezace=atable[5,i].Value
      adostarczenieniepoznijenizxtygodni2=atable[6,i].Value
      awydajnosctygodniowagonca=atable[7,i].Value
      aweek=Week(adata,anrkolejnytygodnia,aprzesylkiakcje,adostarczenieniepoznijenizxtygodni1,aprzesylkibiezace,adostarczenieniepoznijenizxtygodni2,awydajnosctygodniowagonca)
      aweeks.AddWeek(aweek)
   return aweeks

def OnWWWAction(aobj,amenu,file):
   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   if amenu.Action=='ObjectApplyMethods':
      atableparser=HTMLXLSTable.MHTMLXLSTableParser()
      atableparser.Process(aobj.Harmonogram)
      aweeks=PobierzDane(atableparser.Table)
      file.write('<pre>')
      aweeks.Dump(file)
      file.write('</pre>')
      awwweditor.WriteObjectView(aobj,asbutton=1)
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


