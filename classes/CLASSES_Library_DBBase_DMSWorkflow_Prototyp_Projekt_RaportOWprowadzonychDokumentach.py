# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def OnBeforeWWWAction(aobj,amenu,file):
   file.write('<hr>')
   return 1

def GetBR(s,acut=60):
   if not s:
      return ''
   sr=string.split(s,' ')
   sr.reverse()
   sl=[]
   slen=0
   while sr:
      sw=string.strip(sr.pop())
      if not sw:
         continue
      if slen+len(sw)>acut:
         slen=len(sw)
         sw='<br>'+sw
      else:
         slen=slen+len(sw)
      sl.append(sw)
   return string.join(sl,' ')

def DoRaportODokumentach(pobj,file):
   aobj=pobj.Dokumenty
   sum=0
   while aobj:
      file.write('<h1><font color="green">%s</font> - %s</h1>'%(aobj.Symbol,aobj.Nazwa))
      file.write("""
<table>
<tr VALIGN=top class="objectseditrow">
<td class="objectseditdatafieldname"> Dotyczy:</td>
<td class="objectseditdatafieldvalue"> %s</td></tr>

<tr VALIGN=top class="objectseditrow">
<td class="objectseditdatafieldname"> Cel dokumentu:</td>
<td class="objectseditdatafieldvalue"> %s</td></tr>

<tr VALIGN=top class="objectseditrow">
<td class="objectseditdatafieldname"> Osoby odpowiedzialne:</td>
<td class="objectseditdatafieldvalue"> %s</td></tr>

<tr VALIGN=top class="objectseditrow">
<td class="objectseditdatafieldname"> Źródło danych:</td>
<td class="objectseditdatafieldvalue"> %s</td></tr>

<tr VALIGN=top class="objectseditrow">
<td class="objectseditdatafieldname"> Adresat:</td>
<td class="objectseditdatafieldvalue"> %s</td></tr>

<tr VALIGN=top class="objectseditrow">
<td class="objectseditdatafieldname"> Zdarzenia:</td>
<td class="objectseditdatafieldvalue"> %s</td></tr>

<tr VALIGN=top class="objectseditrow">
<td class="objectseditdatafieldname"> Inne czynności:</td>
<td class="objectseditdatafieldvalue"> %s</td></tr>

<tr VALIGN=top class="objectseditrow">
<td class="objectseditdatafieldname"> Przewidywana ilość:</td>
<td class="objectseditdatafieldvalue"> %s/%s</td></tr>

</table>
"""%(GetBR(aobj.Dotyczy.Nazwa),GetBR(aobj.Cel),GetBR(aobj.OsobyOdpowiedzialne),GetBR(aobj.ZrodloDanych),GetBR(aobj.Adresat),GetBR(aobj.Zdarzenia),GetBR(aobj.InneCzynnosci),GetBR(aobj.PrzewidywanaIloscDokumentow),GetBR(aobj.IloscDokumentowNaOkres.Nazwa)))

      bobj=aobj.Pola
      file.write('<table class=objectsviewtable>')
      file.write('<th class=objectsviewheader>Pole</th>\n')
      file.write('<th class=objectsviewheader>Rodzaj</th>\n')
      file.write('<th class=objectsviewheader>Wartości słownika</th>\n')
      file.write('<th class=objectsviewheader>Warunki poprawności</th>\n')
      file.write('<th class=objectsviewheader>Opis</th>\n')
      file.write('<th class=objectsviewheader>Źródło danych</th>\n')
      while bobj:
         file.write('<tr class=objectsviewrow>')
         file.write('<td class=objectsviewdataeven>%s</td>\n'%GetBR(bobj.Nazwa,24))
         file.write('<td class=objectsviewdataeven>%s</td>\n'%bobj.TypPolaDotyczy.Opis)
         file.write('<td class=objectsviewdataeven>%s</td>\n'%GetBR(bobj.WartosciSlownika,24))
         file.write('<td class=objectsviewdataeven>%s</td>\n'%GetBR(bobj.WarunkiPoprawnosci,24))
         file.write('<td class=objectsviewdataeven>%s</td>\n'%GetBR(bobj.Opis,24))
         file.write('<td class=objectsviewdataeven>%s</td>\n'%GetBR(bobj.ZrodloDanych,24))
         file.write('</tr>')
         bobj.Next()
      file.write('</table>\n')
      file.write('<hr>\n')
      sum=sum+aobj.Class.PrzewidywanaIloscDokumentow.ValuesAsInt(aobj.OID)
      aobj.Next()
   file.write('<hr>\n')
   file.write('<h3><font color="blue">Razem ilość dokumentów na miesiąc: %d</font></h3>'%sum)
   dmin=2
   sumh=sum*dmin/60.0
   file.write('<h3><font color="blue">Zakładając %d minuty na dokument daje to: %0.2f godzin</font></h3>'%(dmin,sumh))
   file.write('<h3><font color="blue">Ilość osobodni (8h/dzień): %0.2f</font></h3>'%(sumh/8,))

def OnWWWAction(aobj,amenu,file):
   if amenu.Action=='ObjectApplyMethods':
      DoRaportODokumentach(aobj,file)
   return 1

def OnWWWActionSubmit(aobj,amenu,areport,file):
   print aobj.CID,aobj.OID

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]



