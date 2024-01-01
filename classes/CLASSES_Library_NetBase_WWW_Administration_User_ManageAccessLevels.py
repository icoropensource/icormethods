# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORSecurity import *
import random

def DoManageAccessLevels(amenu,file):
   file.write('<h1>Wprowad� dane:</h1>')
   file.write("""
<form name="hiddenreportparms1" id="hiddenreportparms1" METHOD="post" ACTION="icormain.asp?jobtype=reportsubmit&OID=%d&ReportOID=%d&RandomValue=%d">
<INPUT TYPE=HIDDEN NAME=edtSelUser ID=edtSelUser Value="">
</form>
<script LANGUAGE="JScript">
<!--
function doSubmit(auid) {
   document.getElementById('edtSelUser').value=auid;
   document.getElementById('hiddenreportparms1').submit();
}
-->
</script>
"""%(amenu.oid,amenu.Reports.OID,random.randint(1,10000000)))
   w,i=0,1
   catdict={}
   asecprofile=ICORSecurityProfile()
   asecprofile.SetByUser(amenu.uid)
   asecprofile.GetUsers()
   ausers=asecprofile.Users.keys()
   ausers.sort()
   file.write('<table class=objectsviewtable>')
   for aname in ausers:
      uref='<a class="fg-button-single ui-state-default ui-corner-all uihover" href="javascript:void(doSubmit(\'%d\'));">%s, %s %s</a>'%(asecprofile.Users[aname].UID,asecprofile.Users[aname].UserName,asecprofile.Users[aname].VCFFirstName,asecprofile.Users[aname].VCFLastName)
      if asecprofile.Users[aname].WWWDisabled:
         uwwwdisabled='<font color="red">Konto nieaktywne</font>'
      else:
         uwwwdisabled='<font color="green">Konto aktywne</font>'
      sgroups=''
      grefs=asecprofile.Users[aname].Groups
      while grefs:
         sgroups=sgroups+grefs.Name[grefs.OID]+'<br>'
         grefs.Next()
      file.write('<tr class=objectsviewrow><td class=objectsviewdataeven NOWRAP>%s</td><td class=objectsviewdataeven NOWRAP>%s</td><td class=objectsviewdataeven NOWRAP>%s</td></tr>\n'%(uref,uwwwdisabled,sgroups))
                      
def WriteUserParameters(amenu,file,auser,asecprofile,auid):
   file.write("""
<form name="hiddenreportparms1" id="hiddenreportparms1" METHOD="post" ACTION="icormain.asp?jobtype=reportsubmit&OID=%d&ReportOID=%d&RandomValue=%d">
<INPUT TYPE=HIDDEN NAME=edtSelUser ID=edtSelUser Value="%d">
<INPUT TYPE=HIDDEN NAME=edtAction ID=edtAction Value="SelectUser">
<INPUT TYPE=HIDDEN NAME=edtParam ID=edtParam Value="SelectUser">
<INPUT TYPE=HIDDEN NAME=edtParam1 ID=edtParam1 Value="">
<INPUT TYPE=HIDDEN NAME=edtParam2 ID=edtParam2 Value="">
</form>
<script LANGUAGE="JScript">
<!--
function doSubmit(aaction,aparam) {
   document.getElementById('edtAction').value=aaction
   if (aaction=="ChangePassword") {
      if (document.getElementById('edtPassword1').value=="") {
         alert('Prosz� wpisa� has�o');
         return;
      }
      if (document.getElementById('edtPassword1').value!=document.getElementById('edtPassword2').value) {
         alert('Wpisane has�a s� r�ne');
         return;
      }
      document.getElementById('edtParam').value=document.getElementById('edtPassword1').value;
   }
   if ((aaction=="GroupRemove") || (aaction=="GroupAdd")) {
      document.getElementById('edtParam').value=aparam;
   }
   if (aaction=="UserDelete") {
      if (!confirm('Czy na pewno chcesz skasowa� tego u�ytkownika?')) {
         return;
      }
   }
   if (aaction=="ChangeVCFData") {
      document.getElementById('edtParam1').value=document.getElementById('edtVCFFirstName').value;
      document.getElementById('edtParam2').value=document.getElementById('edtVCFLastName').value;
   }
   document.getElementById('hiddenreportparms1').submit();
}
-->
</script>
"""%(amenu.oid,amenu.Reports.OID,random.randint(1,10000000),auid))
   file.write('<h1>U�ytkownik: %s</h1>'%(auser.UserName,))
   file.write("""
<table>
<tr><td align="right">Has�o:</td><td><INPUT TYPE=PASSWORD NAME=edtPassword1 ID=edtPassword1 TABINDEX=2 Value=""></td></tr>
<tr><td align="right">Powt�rz has�o:</td><td><INPUT TYPE=PASSWORD NAME=edtPassword2 ID=edtPassword2 TABINDEX=3 Value=""></td></tr>
</table>
<br>
<BUTTON class='fg-button-single ui-state-default ui-corner-all uihover' onclick="doSubmit('ChangePassword',0);">Zmie� has�o</BUTTON>
<hr>
""")
   file.write("""
<table>
<tr><td align="right">Imi�:</td><td><INPUT TYPE=EDIT NAME=edtVCFFirstName ID=edtVCFFirstName TABINDEX=4 Value="%s"></td></tr>
<tr><td align="right">Nazwisko:</td><td><INPUT TYPE=EDIT NAME=edtVCFLastName ID=edtVCFLastName TABINDEX=5 Value="%s"></td></tr>
</table>
<br>
<BUTTON class='fg-button-single ui-state-default ui-corner-all uihover' onclick="doSubmit('ChangeVCFData',0);">Zmie� dane osobowe</BUTTON>
<hr>
"""%(auser.VCFFirstName,auser.VCFLastName))
   if auser.WWWDisabled:
      file.write('<p>U�ytkownik jest zablokowany!</p><BUTTON class="fg-button-single ui-state-default ui-corner-all uihover" onclick="doSubmit(\'WWWEnable\',0);">Odblokuj u�ytkownika</BUTTON><hr>')
   else:
      file.write('<p>U�ytkownik mo�e pracowa� przez WWW.</p><BUTTON class="fg-button-single ui-state-default ui-corner-all uihover" onclick="doSubmit(\'WWWDisable\',0);">Zablokuj u�ytkownika</BUTTON><hr>')
   file.write('<BUTTON class="fg-button-single ui-state-default ui-corner-all uihover" onclick="doSubmit(\'UserDelete\',0);">Skasuj u�ytkownika</BUTTON><hr>')
   agroups=asecprofile.Groups.keys()
   agroups.sort()
   file.write('<br><b>Prawa dost�pu</b><br>\n<table>\n')
   for aname in agroups:
      goid,gname=asecprofile.Groups[aname].OID,asecprofile.Groups[aname].GroupName
      if auser.IsInGroup(goid):
         file.write('<tr><td><font color="green" size="-2">%s</font></td><td><button class="fg-button-single ui-state-default ui-corner-all uihover" onclick="doSubmit(\'GroupRemove\',%d);">Od��cz od tej grupy</button></td></tr>\n'%(gname,goid))
      else:
         file.write('<tr><td><font color="red" size="-2">%s</font></td><td><button class="fg-button-single ui-state-default ui-corner-all uihover" onclick="doSubmit(\'GroupAdd\',%d);">Przy��cz do tej grupy</button></td></tr>\n'%(gname,goid))
   file.write('</table>')
   arefs=auser.WWWLoginLog
   if arefs:
      file.write('<hr><b>Log dost�pu (ostatnie 100 pozycji):</b>\n<table class=objectsviewtable>')
      i=100
      while arefs and i:
         if arefs.Logged.ValuesAsInt(arefs.OID):
            alogged='Zalogowany'
         else:
            alogged='B��dne has�o'
         file.write('<tr class=objectsviewrow><td class=objectsviewdataeven NOWRAP>%s</td><td class=objectsviewdataeven NOWRAP>%s</td><td class=objectsviewdataeven NOWRAP>%s</td><td class=objectsviewdataeven NOWRAP>%s</td><td class=objectsviewdataeven NOWRAP>%s</td></tr>\n'%(arefs.EventDateTime[arefs.OID],arefs.LoginUser[arefs.OID],alogged,arefs.RemoteAddr[arefs.OID],arefs.HttpUserAgent[arefs.OID]))
         arefs.Next()
         i=i-1
      file.write('</table>')

def DoManageAccessLevels(amenu,areport,file):
   aaction=areport['edtAction','']
   auid=int(areport['edtSelUser'])
   asecprofile=ICORSecurityProfile()
   asecprofile.SetByUser(amenu.uid)
   asecprofile.GetUsers()
   auser=asecprofile.UsersID.get(auid,None)
   if auser is None:
      file.write('<h1><font color="red">Wybrany u�ytkownik nie istnieje</font></h1><br><button class="fg-button-single ui-state-default ui-corner-all uihover" onclick="history.back();">Powr�t</button>')
      return
   if aaction=='':
      print 'Brak akcji!'
   elif aaction=='UserDelete':
      if auid==amenu.uid:
         file.write('<h1><font color="red">Nie mo�esz skasowa� sam siebie</font></h1><br><button class="fg-button-single ui-state-default ui-corner-all uihover" onclick="history.back();">Powr�t</button>')
      else:
         auser.Delete()
         file.write('<h1><font color="green">U�ytkownik zosta� skasowany</font></h1>')
      return
   elif aaction=='ChangePassword':
      auser.Password=areport['edtParam']
   elif aaction=='ChangeVCFData':
      auser.VCFFirstName=areport['edtParam1']
      auser.VCFLastName=areport['edtParam2']
   elif aaction=='SelectUser':
      pass
   elif aaction=='WWWEnable':
      auser.WWWDisabled=0
   elif aaction=='WWWDisable':
      auser.WWWDisabled=1
   elif aaction=='GroupRemove':
      goid=int(areport['edtParam'])
      agroup=asecprofile.GroupsID[goid]
      agroup.RemoveUser(auser)
   elif aaction=='GroupAdd':
      goid=int(areport['edtParam'])
      agroup=asecprofile.GroupsID[goid]
      agroup.AddUser(auser)
   WriteUserParameters(amenu,file,auser,asecprofile,auid)
   return


