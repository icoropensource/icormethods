# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import string
from CLASSES_Library_ICORBase_Interface_ICORTextFile import TextFile
import time
output_dir='c:/icor/tmp/'

ufields = [
#   ['CLASSES_Library_Dictionary_Named_ReplicationClassPath','IsClassRecursive',mt_Boolean],
#   ['CLASSES_Library_Dictionary_Named_ReplicationClassPath','IsFieldRecursive',mt_Boolean]
]

umethods = []

def FileExists(afpath):
   try:
      f=open(afpath,'rb')
   except:
      return 0
   f.close()
   return 1

def UpdateMethodText(acpath,amname,fname,atext=''):
   fpath=FilePathAsSystemPath(output_dir+fname)
   aclass=aICORDBEngine.Classes[acpath]
   mclass=aICORDBEngine.Classes['CLASSES_System_ICORMethod']
   if aclass is None or mclass is None:
      print 'B��D! Klasa ',acpath,' nie istnieje!'
      return
   moid=mclass.aIDClassMethod.Identifiers(str(aclass.CID)+'_'+amname)
   if moid<0:
      print 'B��D! Metoda ',amname,' nie istnieje!'
      return
   amethod=aclass.MethodsByName(amname)
   if amethod is None:
      print 'B��D! Metoda ',amname,' nie istnieje!'
      return
   if atext=='':
      if not FileExists(fpath):
         print 'B��D! Plik ',fpath,' nie istnieje!'
         return
      try:
         file=TextFile(fpath,'r')
      except RuntimeError,e:
         if e.args[0]=='Not a gzipped file':
            file=open(fpath,'rt')
      try:
         atext=''
         aline=file.readline()
         while aline:
            atext=atext+aline
            aline=file.readline()
      finally:
         file.close()
   mclass.aMethodText[moid]=atext
   mclass.aLastModified.SetValuesAsDateTime(moid,ICORUtil.tdatetime())

def ExportMethods():
   for acname,amname in umethods:
      print 'metoda:',amname
      aclass=aICORDBEngine.Classes[acname]
      if aclass is None:
         print 'B��D! Klasa ',acname,' nie istnieje!'
         continue
      m1=aclass.MethodsByName(amname)
      if m1 is None:
         print 'B��D! Metoda ',amname,' nie istnieje!'
         continue
      afile=FilePathAsSystemPath(output_dir+acname+'_'+amname)
      atext=m1.MethodText
      file=TextFile(afile+'.gz','w')
      try:
         file.write(atext)
      finally:
         file.close()

def SaveRep():
   ExportMethods()
   return

def FFunc(aclass,afield):
   if afield.FieldTID<=MAX_ICOR_SYSTEM_TYPE:
      return
   aoid=aclass.FirstObject()
   while aoid>=0:
      arefstr=afield[aoid]
      if arefstr!='':
         alist=string.split(arefstr,':')
         refs=[]
         k=0
         s=''
         while k<len(alist):
            if alist[k]=='':
               break
            try:
               o=int(alist[k])
               c=int(alist[k+1])
               s=s+str(o)+':'+str(c)+':'
            except:
               print aclass.NameOfClass,afield.Name,aoid
               break
            k=k+2
         afield[aoid]=s
      aoid=aclass.NextObject(aoid)

def CFunc(aclass):
   aclass.ForEachField(FFunc)

def TestUmowyNaDni(acount,amax,aname):
   print '%d. %s'%(acount,aname)
   InfoStatus('%d/%d %s'%(acount,amax,aname))
   aclass=aICORDBEngine.Classes['CLASSES_DataBase_ASA_Slownik_UmowyNaOkres_UmowyNaDni']
   aobj=aclass.GetFirstObject()
   totalcount=0
   totalmcount,totalmsum=0,0
   totajbjednostki,totalbjednostkisum=0,0
   pos,max=0,len(aobj)
   while aobj:
      if pos%10==0:
         SetProgress(pos,max)
      pos=pos+1
      i=aobj.Class.IloscSzczegolowa.ValuesAsInt(aobj.OID)
      if i<0:
         totalmcount=totalmcount+1
         totalmsum=totalmsum+i
      jobj=aobj.Jednostki
      if jobj:
         akod=jobj.Kod
         if akod=='':
            totajbjednostki=totajbjednostki+1
            totalbjednostkisum=totalbjednostkisum+i
      else:
         totajbjednostki=totajbjednostki+1
         totalbjednostkisum=totalbjednostkisum+i
      totalcount=totalcount+i
      aobj.Next()
   SetProgress(0,0)
   print '  ilosc zarejestrowanych dni w klasie UmowyNaDni:',aclass.ObjectsCount()
   print '  suma wszystkich umow:',totalcount
   print '  ilosc dni z iloscia umow mniejsza od zera:',totalmcount
   print '  suma wartosci mniejszych od zera:',totalmsum
   print '  ilosc dni z nieprzypisanymi jednostkami:',totajbjednostki
   print '  suma umow w nieprzypisanych dniach:',totalbjednostkisum
   print '  razem ilosc umow dostepnych poprzez zestawienia z poziomu jednostek:',totalcount-totalbjednostkisum

def TestJednostkiOrganizacyjne(acount,amax,aname):
   print '%d. %s'%(acount,aname)
   InfoStatus('%d/%d %s'%(acount,amax,aname))
   aclass=aICORDBEngine.Classes['CLASSES_DataBase_ASA_Slownik_UmowyNaOkres_UmowyNaDni']
   if not aclass.IsFieldInClass('STATUS'):
      fdef=ICORFieldDefinition('STATUS',mt_Integer)
      fdef.FInteractive=0
      aclass.AddField(fdef)
   fstatus=aclass.STATUS
   fstatus.ClearAllValues()
   print '  ilosc zarejestrowanych dni w klasie UmowyNaDni:',aclass.ObjectsCount()
   aclass=aICORDBEngine.Classes['CLASSES_DataBase_ASA_JednostkaOrganizacyjna']
   print '  ilosc jednostek organizacyjnych:',aclass.ObjectsCount()
   aobj=aclass.GetFirstObject()
   totalumowy1829,totalumowy3039,totalumowy4049,totalumowy50n=0,0,0,0
   totaldnisum,totalbaddnirefs=0,0
   totaldiffdnijednostki,totaldiffjednostkisum,totaldiffanddatedni=0,0,0
   totalbadjednostkidni=0
   pos,max=0,len(aobj)
   while aobj:
      if pos%10==0:
         SetProgress(pos,max)
      pos=pos+1
      u1=aobj.Class.UmowyNaWiek1829.ValuesAsInt(aobj.OID)
      u2=aobj.Class.UmowyNaWiek3039.ValuesAsInt(aobj.OID)
      u3=aobj.Class.UmowyNaWiek4049.ValuesAsInt(aobj.OID)
      u4=aobj.Class.UmowyNaWiek50n.ValuesAsInt(aobj.OID)
      totalumowy1829=totalumowy1829+u1
      totalumowy3039=totalumowy3039+u2
      totalumowy4049=totalumowy4049+u3
      totalumowy50n=totalumowy50n+u4
      wsum=u1+u2+u3+u4
      dobj=aobj.UmowyNaDni
      jsum=0
      sref=str(aobj.OID)+':'+str(aobj.CID)+':'
      wref,wdate=0,0
      ldate=()
      while dobj:
         i=dobj.Class.IloscSzczegolowa.ValuesAsInt(dobj.OID)
         adate=dobj.Class.Data.ValuesAsDate(dobj.OID)
         if adate==ldate:
            wdate=1
         jsum=jsum+i
         s=dobj.Class.Jednostki[dobj.OID]
         if s!=sref:
            dobj.Class.Jednostki[dobj.OID]=sref
            totalbaddnirefs=totalbaddnirefs+1
            wref=1
         x=1+fstatus.ValuesAsInt(dobj.OID)
         fstatus[dobj.OID]=str(x)
         dobj.Next()
      if wref:
         totalbadjednostkidni=totalbadjednostkidni+1
      totaldnisum=totaldnisum+jsum
      if jsum!=wsum:
         totaldiffdnijednostki=totaldiffdnijednostki+1
         if wdate:
            totaldiffanddatedni=totaldiffanddatedni+1
         if jsum>wsum:
            x=jsum-wsum
         else:
            x=wsum-jsum
         totaldiffjednostkisum=totaldiffjednostkisum+x
      aobj.Next()
   aclass=aICORDBEngine.Classes['CLASSES_DataBase_ASA_Slownik_UmowyNaOkres_UmowyNaDni']
   aoid=aclass.FirstObject()
   stzero,stjeden,stmore=0,0,0
   sumzero,sumjeden,sumrest=0,0,0
   pos,max=0,aclass.ObjectsCount()
   while aoid>=0:
      if pos%10==0:
         SetProgress(pos,max)
      pos=pos+1
      i=aclass.IloscSzczegolowa.ValuesAsInt(aoid)
      x=fstatus.ValuesAsInt(aoid)
      if x==1:
         stjeden=stjeden+1
         sumjeden=sumjeden+i
      elif x==0:
         stzero=stzero+1
         sumzero=sumzero+i
      else:
         stmore=stmore+1
         sumrest=sumrest+i*x
      aoid=aclass.NextObject(aoid)
   SetProgress(0,0)
   print '  razem umowy na wiek 18-29:',totalumowy1829
   print '  razem umowy na wiek 30-39:',totalumowy3039
   print '  razem umowy na wiek 40-49:',totalumowy4049
   print '  razem umowy na wiek 50-n:',totalumowy50n
   print '  razem umowy na wiek:',totalumowy1829+totalumowy3039+totalumowy4049+totalumowy50n
   print '  ilosc umow w/g przypisanych dni:',totaldnisum
   print '  ilosc jednostek, gdzie suma na dni nie zgadza sie z suma na wiek:',totaldiffdnijednostki
   print '  ilosc jednostek gdzie nie zgadzaja sie powyzsze sumy oraz sa powtorzone daty:',totaldiffanddatedni
   print '  roznica w jednostkach pomiedzy suma na dni a suma na wiek:',totaldiffjednostkisum
   print '  ilosc jednostek ze zlymi przypisaniami zwrotnymi w dniach:',totalbadjednostkidni
   print '  ilosc dni, ktore nie maja zwrotnego przypisania do jednostek:',totalbaddnirefs
   print '  ilosc dni, ktore nie sa przypisane do zadnej jednostki:',stzero
   print '  ilosc dni, ktore sa przypisanie do jednej jednostki:',stjeden
   print '  ilosc dni, ktore sa przypisanie do wiekszej ilosci jednostek:',stmore
   print '  suma umow w dniach nie przypisanych:',sumzero
   print '  suma umow w dniach przypisanych jeden raz:',sumjeden
   print '  suma umow w dniach przypisanych wiecej niz jeden raz:',sumrest

def CorrectUmowyJednostki(acount,amax,aname):
   print '%d. %s'%(acount,aname)
   InfoStatus('%d/%d %s'%(acount,amax,aname))
   aclass=aICORDBEngine.Classes['CLASSES_DataBase_ASA_Slownik_UmowyNaOkres_UmowyNaDni']
   totalumowyprocessed,totaldobredni,totalumowynojednostki=0,0,0
   sumdobreumowy,sumumowy,sumumowynojednostki=0,0,0
   djednostki={}
   aobj=aclass.GetFirstObject()
   pos,max=0,len(aobj)
   while aobj:
      if pos%15==0:
         SetProgress(pos,max)
      pos=pos+1
      i=aobj.Class.STATUS.ValuesAsInt(aobj.OID)
      asum=aobj.Class.IloscSzczegolowa.ValuesAsInt(aobj.OID)
      if i!=0:
         totaldobredni=totaldobredni+1
         sumdobreumowy=sumdobreumowy+asum
         aobj.Next()
         continue
      jobj=aobj.Jednostki
      if not jobj:
         totalumowynojednostki=totalumowynojednostki+1
         sumumowynojednostki=sumumowynojednostki+asum
         aobj.Next()
         continue
      totalumowyprocessed=totalumowyprocessed+1
      sumumowy=sumumowy+asum
      akod=jobj.Kod
      udlist=djednostki.get(akod,[])
      udlist.append([aobj.Class.Data.ValuesAsDate(aobj.OID),aobj.OID])
      djednostki[akod]=udlist
      aobj.Next()
   SetProgress(0,0)
   totalbadjednostkikod,sumbadjednostki=0,0
   totalpowtorzonedatywjednostkach,totaljednostkizpowtorzonymidatami,totalpowtorzoneiddatywjednostkach=0,0,0
   totalpowtorzonewartosciwjednostkachrowne,totalpowtorzonewartosciwjednostkachrozne=0,0
   jclass=aICORDBEngine.Classes['CLASSES_DataBase_ASA_JednostkaOrganizacyjna']
   pos,max=0,len(djednostki.keys())
   for akod,udlist in djednostki.items():
      if pos%5==0:
         SetProgress(pos,max)
      pos=pos+1
      aoid=jclass.Kod.Identifiers(akod)
      if aoid<0:
         print '    ## jednostka nie istnieje:',akod
         totalbadjednostkikod=totalbadjednostkikod+1
         for udate,uoid in udlist:
            sumbadjednostki=sumbadjednostki+aclass.IloscSzczegolowa.ValuesAsInt(uoid)
         continue
      arefs=jclass.UmowyNaDni.GetRefList(aoid)
      olist=arefs.AsListOID()
      odlist=[]
      for uoid in olist:
         x=[aclass.Data.ValuesAsDate(uoid),uoid]
         odlist.append(x)
      odlist=odlist+udlist
      odlist.sort()
      w=0
      for i in range(len(odlist)-1):
         x1=odlist[i]
         x2=odlist[i+1]
         if x1[0]==x2[0]:
            w=1
            if x1[1]==x2[1]:
               totalpowtorzoneiddatywjednostkach=totalpowtorzoneiddatywjednostkach+1
            else:
               v1=aclass.IloscSzczegolowa[x1[1]]
               v2=aclass.IloscSzczegolowa[x2[1]]
               if v1==v2:
                  totalpowtorzonewartosciwjednostkachrowne=totalpowtorzonewartosciwjednostkachrowne+1
               else:
                  totalpowtorzonewartosciwjednostkachrozne=totalpowtorzonewartosciwjednostkachrozne+1
            totalpowtorzonedatywjednostkach=totalpowtorzonedatywjednostkach+1
      if w:
         totaljednostkizpowtorzonymidatami=totaljednostkizpowtorzonymidatami+1
      s=''
      s1=':'+str(aclass.CID)+':'
      li=-1
      for i in range(len(odlist)):
         x1=odlist[i]
         if x1[1]==li:
            continue
         li=x1[1]
         s=s+str(li)+s1
      jclass.UmowyNaDni[aoid]=s
   SetProgress(0,0)
   print '  ilosc poprawnie przypisanych dni:',totaldobredni
   print '  ilosc umow w poprawnie przypisanych dniach:',sumdobreumowy
   print '  ilosc dni nie przypisanych do jednostek oraz bez informacji o jednostkach:',totalumowynojednostki
   print '  ilosc umow w tych dniach:',sumumowynojednostki
   print '  ilosc dni nie przypisancych do jednostek:',totalumowyprocessed
   print '  ilosc umow w tych dniach:',sumumowy
   print '  ilosc jednostek o nieistniejacych kodach:',totalbadjednostkikod
   print '  ilosc umow na dni w tych jednostkach:',sumbadjednostki
   print '  ilosc jednostek z powtorzonymi datami:',totaljednostkizpowtorzonymidatami
   print '  ilosc powtorzonych dat w jednostkach:',totalpowtorzonedatywjednostkach
   print '  w tym powtorzone identyfikatory dat:',totalpowtorzoneiddatywjednostkach
   print '  w pozostalych datach rowne ilosci szczegolowe mialo:',totalpowtorzonewartosciwjednostkachrowne
   print '  w pozostalych datach rozne ilosci szczegolowe mialo:',totalpowtorzonewartosciwjednostkachrozne

def TestGrupyObslugi(acount,amax,aname):
   print '%d. %s'%(acount,aname)
   InfoStatus('%d/%d %s'%(acount,amax,aname))
   aclass=aICORDBEngine.Classes['CLASSES_DataBase_ASA_JednostkaOrganizacyjna']
   aobj=aclass.GetFirstObject()
   pos,max=0,len(aobj)
   totalsum,countgrupy,countdni=0,0,0
   totaljednostkibadgrupydiff=0
   while aobj:
      if pos%5==0:
         SetProgress(pos,max)
      pos=pos+1
      u1=aobj.Class.UmowyNaWiek1829.ValuesAsInt(aobj.OID)
      u2=aobj.Class.UmowyNaWiek3039.ValuesAsInt(aobj.OID)
      u3=aobj.Class.UmowyNaWiek4049.ValuesAsInt(aobj.OID)
      u4=aobj.Class.UmowyNaWiek50n.ValuesAsInt(aobj.OID)
      wsum=u1+u2+u3+u4
      jednostkasum=0
      gobj=aobj.GrupyObslugi
      while gobj:
         countgrupy=countgrupy+1
         uobj=gobj.Umowy
         while uobj:
            countdni=countdni+1
            i=uobj.Class.Ilosc.ValuesAsInt(uobj.OID)
            totalsum=totalsum+i
            jednostkasum=jednostkasum+i
            uobj.Next()
         gobj.Next()
      if wsum!=jednostkasum:
         totaljednostkibadgrupydiff=totaljednostkibadgrupydiff+1
      aobj.Next()
   SetProgress(0,0)
   dclass=aICORDBEngine.Classes['CLASSES_DataBase_ASA_Slownik_UmowyNaOkres_UmowyNaGrupyObslugi']
   print '  ilosc umow w podziale na grupy:',totalsum
   print '  ilosc jednostek z roznica pomiedzy umowami na wiek a umowami na grupy:',totaljednostkibadgrupydiff
   print '  ilosc grup obslugi:',countgrupy
   print '  ilosc dni przypisanych do grup obslugi:',countdni
   print '  ilosc dni w klasie UmowyNaGrupy:',dclass.ObjectsCount()

def TestTypyAkwizytorow(acount,amax,aname):
   print '%d. %s'%(acount,aname)
   InfoStatus('%d/%d %s'%(acount,amax,aname))
   aclass=aICORDBEngine.Classes['CLASSES_DataBase_ASA_JednostkaOrganizacyjna']
   aobj=aclass.GetFirstObject()
   pos,max=0,len(aobj)
   totalsum,countgrupy,countdni=0,0,0
   totaljednostkibadgrupydiff=0
   while aobj:
      if pos%5==0:
         SetProgress(pos,max)
      pos=pos+1
      u1=aobj.Class.UmowyNaWiek1829.ValuesAsInt(aobj.OID)
      u2=aobj.Class.UmowyNaWiek3039.ValuesAsInt(aobj.OID)
      u3=aobj.Class.UmowyNaWiek4049.ValuesAsInt(aobj.OID)
      u4=aobj.Class.UmowyNaWiek50n.ValuesAsInt(aobj.OID)
      wsum=u1+u2+u3+u4
      jednostkasum=0
      gobj=aobj.Agenci
      while gobj:
         countgrupy=countgrupy+1
         uobj=gobj.Umowy
         while uobj:
            countdni=countdni+1
            i=uobj.Class.IloscSzczegolowa.ValuesAsInt(uobj.OID)
            totalsum=totalsum+i
            jednostkasum=jednostkasum+i
            uobj.Next()
         gobj.Next()
      if wsum!=jednostkasum:
         totaljednostkibadgrupydiff=totaljednostkibadgrupydiff+1
      aobj.Next()
   SetProgress(0,0)
   dclass=aICORDBEngine.Classes['CLASSES_DataBase_ASA_Slownik_UmowyNaOkres_UmowyNaTypAkwizytora']
   print '  ilosc umow w podziale na typy agentow:',totalsum
   print '  ilosc jednostek z roznica pomiedzy umowami na wiek a umowami na typy:',totaljednostkibadgrupydiff
   print '  ilosc typow agentow:',countgrupy
   print '  ilosc dni przypisanych do typow agentow:',countdni
   print '  ilosc dni w klasie UmowyNaTypAkwizytora:',dclass.ObjectsCount()

def LoadRep():
# aktualizacja pol
   for acname,afname,aftype in ufields:
      print 'pole:',afname
      aclass=aICORDBEngine.Classes[acname]
      f1=aclass.FieldsByName(afname)
      if f1 is None:
         fdef1=ICORFieldDefinition(afname,aftype)
         aclass.AddField(fdef1)

#   aICORDBEngine.Classes.ForEachClass(CFunc)

   totaltime=0
   amax=6
   acount,aname=1,'Sprawdzenie klasy UmowyNaDni'
   start=time.clock()
   TestUmowyNaDni(acount,amax,aname)
   finish=time.clock()
   totaltime=totaltime+finish-start
   print 'czas wykonania:',finish-start

   acount,aname=2,'Sprawdzenie klasy JednostkiOrganizacyjne'
   start=time.clock()
   TestJednostkiOrganizacyjne(acount,amax,aname)
   finish=time.clock()
   totaltime=totaltime+finish-start
   print 'czas wykonania:',finish-start

   acount,aname=3,'Aktualizacja przypisa�'
   start=time.clock()
   CorrectUmowyJednostki(acount,amax,aname)
   finish=time.clock()
   totaltime=totaltime+finish-start
   print 'czas wykonania:',finish-start

   acount,aname=4,'Test po uaktualnieniu JednostekOrganizacyjnych'
   start=time.clock()
   TestJednostkiOrganizacyjne(acount,amax,aname)
   finish=time.clock()
   totaltime=totaltime+finish-start
   print 'czas wykonania:',finish-start

   acount,aname=5,'Sprawdzenie grup obslugi'
   start=time.clock()
   TestGrupyObslugi(acount,amax,aname)
   finish=time.clock()
   totaltime=totaltime+finish-start
   print 'czas wykonania:',finish-start

   acount,aname=6,'Sprawdzenie akwizytorow w/g typu'
   start=time.clock()
   TestTypyAkwizytorow(acount,amax,aname)
   finish=time.clock()
   totaltime=totaltime+finish-start
   print 'czas wykonania:',finish-start

   print 'calkowity czas wykonania:',totaltime

# aktualizacja metod
   for acname,amname in umethods:
      print 'metoda:',amname
      aclass=aICORDBEngine.Classes[acname]
      if aclass is None:
         print 'B��D! Klasa ',acname,' nie istnieje!'
         continue
      m1=aclass.MethodsByName(amname)
      if m1 is None:
         mdef1=ICORMethodDefinition(amname)
         print 'dodaje metode',amname
         aclass.AddMethod(mdef1)
      UpdateMethodText(acname,amname,acname+'_'+amname+'.gz')
   return

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   ClearStdOut()
#   SaveRep()
   LoadRep()
   MessageDialog('A teraz wy�lij log do mnie a nastepnie wyjdz i wejdz do ICORa.',mtInformation,mbOK)
#   MessageDialog('Koniec pobierania aktualizacji. Zamknij program i uruchom ponownie aby zako�czy� proces aktualizacji.',mtInformation,mbOK)
   return



