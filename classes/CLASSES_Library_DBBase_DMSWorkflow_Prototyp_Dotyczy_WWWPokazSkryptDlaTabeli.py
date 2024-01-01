# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil

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
   anazwa=aobj.Nazwa
   atable=XMLUtil.CP1250_To_ASCII(anazwa)
   atable='aTABELA_%s_OID'%ICORUtil.MakeIdentifier(atable)
   d={
      'nazwa':anazwa,
      'table':atable,
      'aobj.Nazwa':aobj.Nazwa,
      'aobj.NazwaObiektu':aobj.NazwaObiektu,
      'aobj.NazwaTabeli':aobj.NazwaTabeli,
   }
   file.write('''
self.%(table)s=self.CreateTable(tablename='%(aobj.Nazwa)s',aNazwaObiektu='%(aobj.NazwaObiektu)s',aNazwaTabeli='%(aobj.NazwaTabeli)s',aGrupa=None,accessuser=1)
'''%d)
   i=0
   l=[]
   while pobj:
      if not pobj.Nazwa in ['_ChapterID','_OIDDictRef','Informacja opis czynności','Informacja data wytworzenia','Informacja osoba odpowiedzialna','Informacja podmiot udostępniający','InformacjaPodmiotUdostepniajacy','InformacjaOsobaOdpowiedzialna','InformacjaDataWytworzenia','InformacjaOpisCzynnosci',]:
         d['pobj.Nazwa']=pobj.Nazwa
         d['pobj.TypPolaDotyczy.Opis']=pobj.TypPolaDotyczy.Opis
         d['pobj.NazwaWidoczna']=pobj.NazwaWidoczna
         d['pobj.SGIsAliased']=ICORUtil.str2bool(pobj.SGIsAliased)
         d['pobj.SGIsIndexed']=ICORUtil.str2bool(pobj.SGIsIndexed)
         d['pobj.SGIsSearch']=ICORUtil.str2bool(pobj.SGIsSearch)
         d['pobj.SGIsObligatory']=ICORUtil.str2bool(pobj.SGIsObligatory)
         d['pobj.SGIsSingleViewHidden']=ICORUtil.str2bool(pobj.SGIsSingleViewHidden)
         d['pobj.SGIsDictViewHidden']=ICORUtil.str2bool(pobj.SGIsDictViewHidden)
         d['pobj.WartosciSlownika']=XMLUtil.GetAsXMLStringSimple(XMLUtil.GetAsXMLStringSimple(pobj.WartosciSlownika))
         zobj=pobj.ZrodloDanychSlownika
         if zobj:
            d['pobj.ZrodloDanychSlownika']="'%s'"%(zobj.Nazwa,)
         else:
            d['pobj.ZrodloDanychSlownika']='None'
         l.append([pobj['SGTabIndex',mt_Integer],i,'''self.CreateField(self.%(table)s,'%(pobj.Nazwa)s','%(pobj.TypPolaDotyczy.Opis)s',aFieldNameAsDisplayed='%(pobj.NazwaWidoczna)s',aSGIsAliased='%(pobj.SGIsAliased)d',aSGIsIndexed='%(pobj.SGIsIndexed)d',aSGIsSearch='%(pobj.SGIsSearch)d',aSGIsObligatory='%(pobj.SGIsObligatory)d',aSGIsSingleViewHidden='%(pobj.SGIsSingleViewHidden)d',aSGIsDictViewHidden='%(pobj.SGIsDictViewHidden)d',aWartosciSlownika='%(pobj.WartosciSlownika)s',aZrodloDanychSlownika=%(pobj.ZrodloDanychSlownika)s)
'''%d])
         i=i+1
      pobj.Next()
   l.sort()
   for ti,i,s in l:
      file.write(s)
   file.write('''self.AddTableCMSFields(self.%(table)s)
'''%d)
   file.write('</pre>')
   return 2 # show back reference to main object (1-link, 2-button)

