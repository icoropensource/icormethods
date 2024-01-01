# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import CLASSES_Library_ICORBase_External_MLog as MLog
import os
import re
import sys
import string
import cStringIO
import sha

ALLOWED_TYPES=[
'Ciąg znaków - 1 linia',
'Ciąg znaków - 1 długa linia',
'Data',
'Data i czas',
'EMail',
'Kod pocztowy',
'Liczba',
'Liczba całkowita',
'NIP',
'Nr rachunku bankowego',
'Opis',
'PESEL',
'Pieniądze',
'REGON',
'Tak/Nie',
]

class PMField:
   def __init__(self,aparser,aname,atype,akind,aisobligatory,azwrotne=0):
      self.Parser=aparser
      self.Name=aname
      self.Type=atype
      self.Kind=akind #1-wzorcowe,2-informacyjne,3-z serwera
      self.IsObligatory=aisobligatory
      self.Registered=0
      self.CzyZwrotne=azwrotne
      self.Cnt=-1
   def AcceptValue(self,avalue):
      ret=1
      bvalue=avalue
      try:
         if self.Type=='Ciąg znaków - 1 linia' or self.Type=='Ciąg znaków - 1 długa linia':
            bvalue=avalue
         elif self.Type=='Data':
            bvalue=ICORUtil.getStrAsDate(avalue)
         elif self.Type=='Data i czas':
            pass
         elif self.Type=='EMail':
            pass
         elif self.Type=='Kod pocztowy':
            pass
         elif self.Type=='Liczba':
            bvalue=float(avalue)
         elif self.Type=='Liczba całkowita':
            bvalue=int(avalue)
         elif self.Type=='NIP':
            pass
         elif self.Type=='Nr rachunku bankowego':
            pass
         elif self.Type=='Opis':
            pass
         elif self.Type=='PESEL':
            pass
         elif self.Type=='Pieniądze':
            bvalue=float(avalue)
         elif self.Type=='REGON':
            pass
         elif self.Type=='Tak/Nie':
            bvalue=ICORUtil.str2bool(avalue)
      except:
         ret=0
         bvalue=''
      return ret,bvalue

class PMPlatnosc:
   def __init__(self,aparser,apola,aczyanulowano,aczyjuzzaplacono,aczybezkwoty,aczyplatnoscgrupowa,adataakceptacji,aczyaktualizacjatresci):
      self.Parser=aparser
      if aparser.LastPayment:
         self.NadPlatnosc=aparser.LastPayment[-1]
      else:
         self.NadPlatnosc=None
      self.Pola=apola
      self.CzyAnulowano=aczyanulowano
      self.CzyJuzZaplacono=aczyjuzzaplacono
      self.CzyBezKwoty=aczybezkwoty
      self.CzyPlatnoscGrupowa=aczyplatnoscgrupowa
      self.DataAkceptacji=adataakceptacji
      self.CzyAktualizacjaTresci=aczyaktualizacjatresci
      self.Raty=[]
      self.DigestFields=['Kwota','DataWymagalnosci','IDPlatnika','IDTytulu','Tytulem','Platnik'] # 'TrescPrzelewu'
      self.IDDigestFields=['IDPlatnika','Platnik','PlatnikAdresMiejscowosc','PlatnikAdresUlica','PlatnikAdresNrPosesji','PlatnikAdresNrLokalu']
      self._Digest,self._DigestID=None,None
      self.OID=''
   def __repr__(self):
      ret=''
      for apname in self.DigestFields:
         avalue=self.Pola.get(apname,'')
         if type(avalue)==type(''):
            ret=ret+' | '+avalue
         elif type(avalue)==type(0.0):
            ret=ret+' | %0.2f'%avalue
         else:
            ret=ret+' | '+str(avalue)
      return ret
   def __getattr__(self,name):
      if name=='Digest':
         if self._Digest is None:
            self._Digest=self.CalculateDigest(self.DigestFields)
         return self._Digest
      if name=='DigestID':
         if self._DigestID is None:
            self._DigestID=self.CalculateDigest(self.IDDigestFields)
         return self._DigestID
   def CalculateDigest(self,afields):
      asha=sha.new()
      for apname in afields:
         avalue=self.Pola.get(apname,'')
         if type(avalue)==type(''):
            asha.update(avalue)
         else:
            asha.update(str(avalue))
      return asha.hexdigest()
   def AddRaty(self,aopis):
      self.Raty.append([aopis,[]])
   def AddPlatnosci(self,aplatnosc):
      l=self.Raty[-1]
      l[1].append(aplatnosc)
   def PrintInfo(self,alevel=0):
      aindent='  '*alevel
      print aindent,self.Pola.get('Kwota',0.0),self.Pola['DataWymagalnosci'],self.Pola['IDPlatnika']
      for arata,aplatnosci in self.Raty:
         print aindent,'  *** RATY:',arata
         for aplatnosc in aplatnosci:
            aplatnosc.PrintInfo(alevel+2)

class ICORPMPackageParser(XMLUtil.ICORBaseXMLParser):
   def Initialize(self):
      self.IsGood=1
      self.Fields={}
      self.FieldNames=[]
      self.FieldCnt=0
      self.Platnosci=[]
      self.IsPolaInformacyjne=0

      self.Aplikacja=''
      self.DataUtworzeniaPaczki=''
      self.IDPaczki=''
      self.AutorPaczki=''
      self.CSVSeparator=';'
      self.CSVOgranicznikTekstu='"'
      self.CSVFormatDaty='rrrr-mm-dd'
      self.CSVSeparatorNaKoncuLinii='0'
      self.CSVZnakNowejLinii='CRLF'

      self.AddField('Kwota','Liczba',1,0)
      self.AddField('DataWymagalnosci','Data',1,0)
      self.AddField('IDTytulu','Ciąg znaków - 1 linia',1,0)
      self.AddField('IDPlatnika','Ciąg znaków - 1 linia',1,1)
      self.AddField('Tytulem','Ciąg znaków - 1 linia',1,0)
      self.AddField('Platnik','Ciąg znaków - 1 linia',1,0)
      self.AddField('PlatnikNip','Ciąg znaków - 1 linia',1,0)
      self.AddField('TrescDecyzji','Opis',1,0)
      self.AddField('TrescPrzelewu','Opis',1,0)
      self.AddField('TrescZwrotki','Opis',1,0)
      self.AddField('ZwrotkaGrupa','Ciąg znaków - 1 linia',1,0)
      self.AddField('PlatnikAdres','Opis',1,0)
      self.AddField('PlatnikAdresUlica','Ciąg znaków - 1 linia',1,0)
      self.AddField('PlatnikAdresNrPosesji','Ciąg znaków - 1 linia',1,0)
      self.AddField('PlatnikAdresNrLokalu','Ciąg znaków - 1 linia',1,0)
      self.AddField('PlatnikAdresKodPocztowy','Ciąg znaków - 1 linia',1,0)
      self.AddField('PlatnikAdresMiejscowosc','Ciąg znaków - 1 linia',1,0)
      self.AddField('PlatnikAdresGmina','Ciąg znaków - 1 linia',1,0)
      self.AddField('PlatnikAdresPowiat','Ciąg znaków - 1 linia',1,0)
      self.AddField('PlatnikAdresWojewodztwo','Ciąg znaków - 1 linia',1,0)
      self.AddField('PlatnikAdresPanstwo','Ciąg znaków - 1 linia',1,0)
      self.AddField('PlatnikAdresInneInformacje','Ciąg znaków - 1 linia',1,0)
      #2008<
      self.AddField('PlatnikAdresCzyKraj','Ciąg znaków - 1 linia',1,0)
      self.AddField('PlatnikAdresNieruchomosciUlica','Ciąg znaków - 1 linia',1,0)
      self.AddField('PlatnikAdresNieruchomosciNrPosesji','Ciąg znaków - 1 linia',1,0)
      self.AddField('PlatnikAdresNieruchomosciNrLokalu','Ciąg znaków - 1 linia',1,0)
      self.AddField('PlatnikAdresKorespondencjiKodPocztowy','Ciąg znaków - 1 linia',1,0)
      self.AddField('PlatnikAdresKorespondencjiMiasto','Ciąg znaków - 1 linia',1,0)
      self.AddField('PlatnikAdresKorespondencjiMiejscowosc','Ciąg znaków - 1 linia',1,0)
      self.AddField('PlatnikAdresKorespondencjiUlica','Ciąg znaków - 1 linia',1,0)
      self.AddField('PlatnikAdresKorespondencjiNrPosesji','Ciąg znaków - 1 linia',1,0)
      self.AddField('PlatnikAdresKorespondencjiNrLokalu','Ciąg znaków - 1 linia',1,0)
      self.AddField('PlatnikAdresKorespondencjiCzyKraj','Ciąg znaków - 1 linia',1,0)
      self.AddField('PlatnikAdresKorespondencjiPanstwo','Ciąg znaków - 1 linia',1,0)
      self.AddField('PlatnikAdresKorespondencjiInneInformacje','Ciąg znaków - 1 linia',1,0)
      #2008>
      self.AddField('PMKwotaZaplaty','Liczba',3,1)
      self.AddField('PMDataZaplaty','Data',3,1)
      self.AddField('PMBank','Ciąg znaków - 1 linia',3,0)
      self.AddField('PMKasa','Ciąg znaków - 1 linia',3,0)
      self.AddField('PMKasjer','Ciąg znaków - 1 linia',3,0)
      self.AddField('PMDataWplywu','Data',3,0)
      self.AddField('PMStatusPlatnosci','Ciąg znaków - 1 linia',3,0)
      self.AddField('PMDataOdbioruDecyzji','Data',3,0)

      self.LastPayment=[]
   def Parse(self,atext):
      self.Initialize()
      XMLUtil.ICORBaseXMLParser.Parse(self,atext)
   def AddField(self,aname,atype,akind,aisobligatory):
      afield=PMField(self,aname,atype,akind,aisobligatory)
      self.Fields[aname]=afield
   def RegisterField(self,aname,atype,akind,azwrotne=0):
      self.FieldNames.append(aname)
      if akind==1 or akind==3:
         if self.Fields.has_key(aname):
            afield=self.Fields[aname]
            afield.Registered=1
            afield.CzyZwrotne=azwrotne
            afield.Cnt=self.FieldCnt
            self.FieldCnt=self.FieldCnt+1
            if afield.IsObligatory and not afield.CzyZwrotne:
               self.IsGood=0
               self.status.append('pole obligatoryjne %s nie jest zaznaczone jako zwrotne'%aname)
            if afield.Type!=atype:
               self.IsGood=0
               self.status.append('pole %s powinno posiadać typ %s a posiada %s'%(aname,afield.Type,atype))
         else:
            self.IsGood=0
            self.status.append('niedopuszczalne pole systemowe: %s'%aname)
      elif akind==2:
         self.IsPolaInformacyjne=1
         if self.Fields.has_key(aname):
            self.IsGood=0
            afield=self.Fields[aname]
            if afield.Kind!=akind:
               self.status.append('niedopuszczalne pole informacyjne: %s'%aname)
            else:
               self.status.append('powtórzone pole informacyjne: %s'%aname)
         else:
            afield=PMField(self,aname,atype,akind,0,azwrotne)
            afield.Registered=1
            afield.Cnt=self.FieldCnt
            self.FieldCnt=self.FieldCnt+1
            self.Fields[aname]=afield
            if not atype in ALLOWED_TYPES:
               self.IsGood=0
               self.status.append('pole %s posiada nieznany typ %s'%(aname,afield.Type))
   def start_PMPACZKA(self,attrs):
#      print 'STACK:',self.stack
      l=self.CheckAttrs(attrs,['wersja'])
      if l:
         self.IsGood=0
         self.status.append('nieznane atrybuty w tagu <PMPACZKA>: %s'%str(l))
   def end_PMPACZKA(self):
      pass
   def start_DANEPACZKI(self,attrs):
#      print 'STACK:',self.stack
      pass
   def end_DANEPACZKI(self):
      pass
   def start_DANE(self,attrs):
#      print 'STACK:',self.stack
      l=self.CheckAttrs(attrs,['nazwa','wartosc','czyzwrotne'])
      if l:
         self.IsGood=0
         self.status.append('nieznane atrybuty w tagu <DANE>: %s'%str(l))
      anazwa=attrs.get('nazwa','')
      awartosc=attrs.get('wartosc','')
      if not anazwa in ['Aplikacja','DataUtworzeniaPaczki','IDPaczki','AutorPaczki','CSVSeparator','CSVOgranicznikTekstu','CSVFormatDaty','CSVSeparatorNaKoncuLinii','CSVZnakNowejLinii']:
         self.IsGood=0
         self.status.append('nieznana wartość atrybutu "nazwa" w tagu <DANE>: %s'%anazwa)
      else:
         self.__dict__[anazwa]=awartosc
      if anazwa=='Aplikacja':
         if not awartosc:
            self.IsGood=0
            self.status.append('brak opisu aplikacji w tagu <DANE>: %s'%awartosc)
      elif anazwa=='DataUtworzeniaPaczki':
         if not re.match('^\d{4}\-\d{1,2}-\d{1,2}$',awartosc,re.I) and not re.match('^\d{4}\-\d{1,2}-\d{1,2} \d{1,2}\:\d{1,2}\:\d{1,2}$',awartosc,re.I):
            self.IsGood=0
            self.status.append('błędna data utworzenia paczki w tagu <DANE>: %s'%awartosc)
      elif anazwa=='IDPaczki':
         if not awartosc:
            self.IsGood=0
            self.status.append('brak opisu IDPaczki w tagu <DANE>: %s'%awartosc)
      elif anazwa=='AutorPaczki':
         if not awartosc:
            self.IsGood=0
            self.status.append('brak opisu AutorPaczki w tagu <DANE>: %s'%awartosc)
      elif anazwa=='CSVSeparator':
         pass
      elif anazwa=='CSVOgranicznikTekstu':
         pass
      elif anazwa=='CSVFormatDaty':
         awartosc=awartosc.lower()
         if not awartosc in ['','rrrr-mm-dd','dd-mm-rrrr','rrrrmmdd','ddmmrrrr','rrrr/mm/dd','dd/mm/rrrr',]:
            self.IsGood=0
            self.status.append('błędny opis CSVFormatDaty w tagu <DANE>: %s'%awartosc)
      elif anazwa=='CSVSeparatorNaKoncuLinii':
         if not awartosc in ['','0','1']:
            self.IsGood=0
            self.status.append('błędny opis CSVSeparatorNaKoncuLinii w tagu <DANE>: %s'%awartosc)
      elif anazwa=='CSVZnakNowejLinii':
         awartosc=awartosc.lower()
         if not awartosc in ['','crlf','lf']:
            self.IsGood=0
            self.status.append('błędny opis CSVZnakNowejLinii w tagu <DANE>: %s'%awartosc)
   def end_DANE(self):
      pass
   def start_POLAWZORCOWE(self,attrs):
#      print 'STACK:',self.stack
      pass
   def end_POLAWZORCOWE(self):
      pass
   def start_POLEWZORCOWE(self,attrs):
#      print 'STACK:',self.stack
      l=self.CheckAttrs(attrs,['nazwa','typ','czyzwrotne'])
      if l:
         self.IsGood=0
         self.status.append('nieznane atrybuty w tagu <POLEWZORCOWE>: %s'%str(l))
      anazwa=attrs.get('nazwa','')
      atyp=attrs.get('typ','')
      szwrotne=attrs.get('czyzwrotne','0')
      if not szwrotne in ['0','1']:
         self.IsGood=0
         self.status.append('błędny wartość atrybutu czyzwrotne (%s) dla pola wzorcowego: %s'%(szwrotne,anazwa))
         szwrotne='0'
      self.RegisterField(anazwa,atyp,1,int(szwrotne))
   def end_POLEWZORCOWE(self):
      pass
   def start_POLAINFORMACYJNE(self,attrs):
      pass
   def end_POLAINFORMACYJNE(self):
      pass
   def start_POLEINFORMACYJNE(self,attrs):
      l=self.CheckAttrs(attrs,['nazwa','typ','czyzwrotne'])
      if l:
         self.IsGood=0
         self.status.append('nieznane atrybuty w tagu <POLEINFORMACYJNE>: %s'%str(l))
      anazwa=attrs.get('nazwa','')
      atyp=attrs.get('typ','')
      szwrotne=attrs.get('czyzwrotne','0')
      if not szwrotne in ['0','1']:
         self.IsGood=0
         self.status.append('błędny wartość atrybutu czyzwrotne (%s) dla pola informacyjnego: %s'%(szwrotne,anazwa))
         szwrotne='0'
      self.RegisterField(anazwa,atyp,2,int(szwrotne))
      bfield=self.Fields[anazwa]
   def end_POLEINFORMACYJNE(self):
      pass
   def start_POLAZSERWERA(self,attrs):
      pass
   def end_POLAZSERWERA(self):
      pass
   def start_POLEZSERWERA(self,attrs):
      l=self.CheckAttrs(attrs,['nazwa','typ'])
      if l:
         self.IsGood=0
         self.status.append('nieznane atrybuty w tagu <POLEZSERWERA>: %s'%str(l))
      anazwa=attrs.get('nazwa','')
      atyp=attrs.get('typ','')
      self.RegisterField(anazwa,atyp,3,1)
   def end_POLEZSERWERA(self):
      pass
   def start_PLATNOSCI(self,attrs):
      self.CheckFields()
      if not self.IsGood:
         self.status.append('*** błędy w definicji XML uniemożliwiają import danych o płatnościach ***')
      self.OnStartPlatnosci()
   def end_PLATNOSCI(self):
      self.OnEndPlatnosci()
   def start_PLATNOSC(self,attrs):
      if not self.IsGood:
         return
      if attrs.has_key('Tytylem'):
         attrs['Tytulem']=attrs['Tytylem']
         del attrs['Tytylem']
      if not attrs.has_key('Platnik'):
         attrs['Platnik']=''
      if not attrs.has_key('PlatnikAdresInneInformacje'):
         attrs['PlatnikAdresInneInformacje']=''
      if not attrs.has_key('PlatnikAdresKorespondencjiInneInformacje'):
         attrs['PlatnikAdresKorespondencjiInneInformacje']=''
      l=self.CheckAttrs(attrs,self.FieldNames+['czybezkwoty','czyanulowano','czyjuzzaplacono','czyplatnoscgrupowa','dataakceptacji','czyaktualizacjatresci']+['PlatnikAdresKorespondencjiInneInformacje',])
      if l:
         self.IsGood=0
         self.status.append('nieznane atrybuty w tagu <PLATNOSC>: %s'%str(l))
         return
      s=attrs.get('czyanulowano','0')
      if not s in ['0','1']:
         self.IsGood=0
         self.status.append('błędna wartość atrybutu czyanulowano (%s) dla platnosci'%s)
         return
      aczyanulowano=int(s)
      s=attrs.get('czyjuzzaplacono','0')
      if not s in ['0','1']:
         self.IsGood=0
         self.status.append('błędna wartość atrybutu czyjuzzaplacono (%s) dla platnosci'%s)
         return
      aczyjuzzaplacono=int(s)
      s=attrs.get('czybezkwoty','0')
      if not s in ['0','1']:
         self.IsGood=0
         self.status.append('błędna wartość atrybutu czybezkwoty (%s) dla platnosci'%s)
         return
      aczybezkwoty=int(s)
      s=attrs.get('czyplatnoscgrupowa','0')
      if not s in ['0','1']:
         self.IsGood=0
         self.status.append('błędna wartość atrybutu czyplatnoscgrupowa (%s) dla platnosci'%s)
         return
      aczyplatnoscgrupowa=int(s)
      s=attrs.get('czyaktualizacjatresci','0')
      if not s in ['0','1']:
         self.IsGood=0
         self.status.append('błędna wartość atrybutu czyaktualizacjatresci (%s) dla platnosci'%s)
         return
      aczyaktualizacjatresci=int(s)
      adataakceptacji=ICORUtil.getStrAsDate(attrs.get('dataakceptacji',''))
      apola={}
      for apole,awartosc in attrs.items():
         if apole in ['czybezkwoty','czyanulowano','czyjuzzaplacono','czyplatnoscgrupowa','dataakceptacji','czyaktualizacjatresci']:
            continue
         afield=self.Fields[apole]
         aaccept,avalue=afield.AcceptValue(awartosc)
         if aaccept:
            apola[apole]=avalue
         else:
            self.IsGood=0
            self.status.append('błędna wartość atrybutu %s dla platnosci: %s'%(apole,awartosc[:80]))
      if not self.IsGood:
         return
      aplatnoscclass=self.OnGetPlatnoscClass()
      aplatnosc=aplatnoscclass(self,apola,aczyanulowano,aczyjuzzaplacono,aczybezkwoty,aczyplatnoscgrupowa,adataakceptacji,aczyaktualizacjatresci)
      if self.LastPayment:
         pplatnosc=self.LastPayment[-1]
         pplatnosc.AddPlatnosci(aplatnosc)
      else:
         self.OnPaymentAdd(aplatnosc)
      self.LastPayment.append(aplatnosc)
   def end_PLATNOSC(self):
      if not self.IsGood:
         return
      self.LastPayment.pop()
   def start_RATY(self,attrs):
      if not self.IsGood:
         return
      l=self.CheckAttrs(attrs,['opis'])
      if l:
         self.IsGood=0
         self.status.append('nieznane atrybuty w tagu <PLATNOSC>: %s'%str(l))
         return
      pplatnosc=self.LastPayment[-1]
      pplatnosc.AddRaty(attrs.get('opis',''))
   def end_RATY(self):
      pass
   def syntax_error(self,message):
      self.IsGood=0
      self.status.append('błąd w danych XML w linii %d: %s'%(self.lineno,message))
   def unknown_starttag(self,tag,attrs):
      self.IsGood=0
      self.status.append('nieznany tag początkowy w linii %d: %s'%(self.lineno,tag))
   def unknown_endtag(self,tag):
      self.IsGood=0
      self.status.append('nieznany tag końcowy w linii %d: %s'%(self.lineno,tag))
   def unknown_entityref(self,ref):
      self.IsGood=0
      self.status.append('nieznany wielkość referencyjna w linii %d: %s'%(self.lineno,ref))
   def unknown_charref(self,ref):
      self.IsGood=0
      self.status.append('nieznany wartość referencyjna w linii %d: %s'%(self.lineno,ref))
   def CheckFields(self):
      for afield in self.Fields.values():
         if afield.IsObligatory and not afield.Registered:
            self.IsGood=0
            self.status.append('pole obligatoryjne %s nie zostało dołączone do pliku XML'%afield.Name)
   def PrintPlatnosci(self):
      for aplatnosc in self.Platnosci:
         aplatnosc.PrintInfo()
   def OnGetPlatnoscClass(self):
      return PMPlatnosc
   def OnPaymentAdd(self,aplatnosc):
      self.Platnosci.append(aplatnosc)
   def OnStartPlatnosci(self):
      pass
   def OnEndPlatnosci(self):
      pass

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   ret='Wystąpił nieoczekiwany błąd - treść XML jest najprawdopodobniej bez sensu.'
   saveout=MLog.MemorySysOutWrapper()
   try:
      try:
         aclass=aICORDBEngine.Classes[CID]
         if Value=='':
            fin=open('k:/icor/tmp/paczka2.xml','r')
            Value=fin.read()
            fin.close()
         aparser=ICORPMPackageParser()
         aparser.Parse(Value)
         if aparser.IsGood:
            print '****** PACZKA WYGLĄDA OK!!! *********'
            print
            l=[]
            for s in aparser.FieldNames:
               afield=aparser.Fields[s]
               if afield.CzyZwrotne:
                  l.append('%s%s%s'%(aparser.CSVOgranicznikTekstu,s,aparser.CSVOgranicznikTekstu))
            print '*** NAGŁÓWEK CSV ***'
            print string.join(l,aparser.CSVSeparator)
            print
            print '*** DANE Z PACZKI ***'
            aparser.PrintPlatnosci()
         else:
            aparser.Dump()
      except:
         import traceback
         traceback.print_exc()
   finally:
      ret=saveout.read()
      saveout.Restore()
   return ret



