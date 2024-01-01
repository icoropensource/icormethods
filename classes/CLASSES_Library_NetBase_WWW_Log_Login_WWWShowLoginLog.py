# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_ICORBase_Interface_ICORSearch as ICORSearch
import random

def DoGenerate(amenu,file):
   file.write("""
<SCRIPT LANGUAGE=javascript>

var dselectedelement=0;

function condselect_onchange(aelement,aelement2) {
   if (aelement.selectedIndex==0) {
      document.getElementById(aelement2).style.visibility="visible";
      } else {
      document.getElementById(aelement2).style.visibility="hidden";
      }
}

var drPopup = null;

if (isIE()) {
   drPopup = window.createPopup();
}

function showPopupDR(asrc,aelement)
{
   dselectedelement=asrc;
   if (isIE()) {
      drPopup.document.body.innerHTML = oContextHTML.innerHTML;
      drPopup.show(0, 0, 300, 200, aelement);
   }
}

function showPopupPR(asrc,aelement,asrcelement,dh)
{
   dselectedelement=asrc;
   if (isIE()) {
      drPopup.document.body.innerHTML = asrcelement.innerHTML;
      drPopup.show(0, 0, 300, dh, aelement);
   }
}

</SCRIPT>

<form name="hiddenreportparms1" id="hiddenreportparms1" METHOD="post" ACTION="icormain.asp?jobtype=reportsubmit&OID=%d&ReportOID=%d&RandomValue=%d">
<table>
<tr><td align="right">Data od (>=):</td><td>
"""%(amenu.oid,amenu.Reports.OID,random.randint(1,10000000)))
   file.write("""
<INPUT class=datepicker type="text" id=rulevalue0 name=rulevalue0 size="24" value="">
</td></tr>
<tr><td align="right">Data do (<):</td><td>
<INPUT class=datepicker type="text" id=rulevalue1 name=rulevalue1 size="24" value="">
</td></tr>
<tr><td align="right">Użytkownik:</td><td>
<INPUT type="text" id=rulevalue2 name=rulevalue2 size="44" value="">
</td></tr>
</table>
""")
   file.write("""
</form>
<script LANGUAGE="JScript">
function doSubmit() {
   document.getElementById('hiddenreportparms1').submit();
}
</script>
<BUTTON class="fg-button-single ui-state-default ui-corner-all uihover" onclick="jQuery(this).attr('disabled','disabled');doSubmit();">Zatwierdź</BUTTON>
""")
   return

def DoGenerateSubmit(amenu,areport,file):
   sdataod=areport['rulevalue0']
   sdatado=areport['rulevalue1']
   suzytkownik=ICORUtil.strLowerPL(areport['rulevalue2'])
   adataod=ICORUtil.getStrAsDateTime(sdataod)
   adatado=ICORUtil.getStrAsDateTime(sdatado)
   lmessage=[]
   if adataod==ICORUtil.ZERO_DATE_TZ:
      lmessage.append('Proszę wprowadzić datę początkową')
   if adatado==ICORUtil.ZERO_DATE_TZ:
      lmessage.append('Proszę wprowadzić datę końcową')
   if adataod>adatado:
      lmessage.append('Data początkowa jest późniejsza od daty końcowej')
   if lmessage:
      for s in lmessage:
         file.write('<h3><font color=red>'+s+'</font></h3>')
      DoGenerate(amenu,file)
      return
   file.write('<b>Od daty: '+ICORUtil.tdate2fmtstr(adataod)+'</b><br>')
   file.write('<b>Do daty: '+ICORUtil.tdate2fmtstr(adatado)+'</b><br>')
   if suzytkownik:
      file.write('<b>Użytkownik: '+suzytkownik+'</b></br>')
   file.write('<hr>')
   lclass=aICORDBEngine.Classes['CLASSES_Library_NetBase_WWW_Log_Login']
   aedtfield=lclass.EventDateTime
   asearch=ICORSearch.ICORRepositorySearch(aedtfield)
   apos=asearch.FindLeft(adatado)
   aoid=aedtfield.GetValueIDByPosition(apos)
   file.write("""
<table id="sortedTable0">
<THEAD>
   <TR>
      <TH>Data i czas</TH>
      <TH>Użytkownik</TH>
      <TH>Zalogowany</TH>
      <TH>Adres IP</TH>
      <TH>Cookie</TH>
   </TR>
</THEAD>
<TBODY>
""")
   while 1:
      aoid=aedtfield.GetPrevValueID(aoid)
      if aoid<0:
         break
      v=aedtfield.ValuesAsComp(aoid)
      if v<adataod:
         break
      aloginuser=lclass.LoginUser[aoid]
      if suzytkownik:
         buzytkownik=ICORUtil.strLowerPL(aloginuser)
         if string.find(buzytkownik,suzytkownik)<0:
            continue
      file.write('<tr>')
      file.write('<td><a href="icormain.asp?jobtype=objectedit&CID=%d&OID=%d">'%(lclass.CID,aoid)+lclass.EventDateTime[aoid]+'</a></td>')
      file.write('<td>'+aloginuser+'</td>')
      alogged=lclass.Logged.ValuesAsInt(aoid)
      if alogged:
         file.write('<td>tak</td>')
      else:
         file.write('<td><font color=red>nie</font></td>')
      file.write('<td>'+lclass.RemoteAddr[aoid]+'</td>')
      file.write('<td>'+lclass.HttpCookie[aoid]+'</td>')
      file.write('</tr>')
   file.write("""
</TR>
</TBODY></table>
<script type="text/javascript">
jQuery(function (){makeTable('#sortedTable0');});
</script>
""")

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   adataod=(2007, 2, 1, 0, 0, 0, 0)
   adatado=(2007, 2, 6, 0, 0, 0, 0)
   suzytkownik=''

   lclass=aICORDBEngine.Classes['CLASSES_Library_NetBase_WWW_Log_Login']
   aedtfield=lclass.EventDateTime
   asearch=ICORSearch.ICORRepositorySearch(aedtfield)
   apos=asearch.FindLeft(adatado)
   aoid=aedtfield.GetValueIDByPosition(apos)
   while 1:
      aoid=aedtfield.GetPrevValueID(aoid)
      if aoid<0:
         break
      v=aedtfield.ValuesAsComp(aoid)
      if v<adataod:
         break
      print '  ',aoid,lclass.EventDateTime[aoid]
      print lclass.EventDateTime[aoid]+' | '+lclass.LoginUser[aoid]+' | '+lclass.RemoteAddr[aoid]+' | '+lclass.HttpCookie[aoid]


