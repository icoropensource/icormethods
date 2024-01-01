# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def OnBeforeWWWAction(aobj,amenu,file):
   return 1

def DoReportInstrukcjaDlaPracownikow(pobj,file):
   aobj=pobj.Dokumenty
   while aobj:
      file.write('<h1><center><font color="brown">%s</font></center></h1>\n'%aobj.Nazwa)
      pobj=aobj.Procedury
      lt,lw=[],[]
      while pobj:
         lp=[]
         cobj=pobj.Czynnosci
         while cobj:
            lp.append(cobj.Nazwa)
            cobj.Next()
         if pobj.Symbol=='T':
            lt.append([pobj.Dokument.Symbol,pobj.Dokument.Nazwa,lp])
         else:
            lw.append([pobj.Dokument.Symbol,pobj.Dokument.Nazwa,lp])
         pobj.Next()
      if lt:
         file.write('<h3><font color="navy">Tworząc nowy dokument należy:</font></h3>')
         for asymbol,anazwa,lc in lt:
            file.write('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<font color="green">%s - %s</font><br>'%(asymbol,anazwa))
            for aczynnosc in lc:
               file.write('<input class="checkradio" type="checkbox">%s<br>'%(aczynnosc,))
            file.write('<br>')
      if lw:
         file.write('<h3><font color="navy">Gdy nadejdzie nowy dokument należy:</font></h3>')
         for asymbol,anazwa,lc in lw:
            file.write('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<font color="green">%s - %s</font><br>'%(asymbol,anazwa))
            for aczynnosc in lc:
               file.write('<input class="checkradio" type="checkbox">%s<br>'%(aczynnosc,))
            file.write('<br>')
      file.write('<hr>')
      aobj.Next()
   tobj=pobj.BazyZrodlowe
   while tobj:
      file.write('<h2>%s</h2>\n'%tobj.Nazwa)
      file.write('<b>Pola:</b><br><table border="1">')
      fobj=tobj.Pola
      while fobj:
         file.write('<tr><td>%s</td><td>%s</td><td>%s</td></tr>'%(fobj.Nazwa,fobj.TypPolaDotyczy.Opis,fobj.Opis))
         fobj.Next()
      file.write('</table><br>')
      tobj.Next()

def OnWWWAction(aobj,amenu,file):
   if amenu.Action=='ObjectApplyMethods':
      DoReportInstrukcjaDlaPracownikow(aobj,file)
   return 1

def OnWWWActionSubmit(aobj,amenu,areport,file):
   print aobj.CID,aobj.OID

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]



