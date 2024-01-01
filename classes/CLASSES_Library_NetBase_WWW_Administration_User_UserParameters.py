# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
from CLASSES_Library_ICORBase_Interface_ICORSecurity import *
import CLASSES_Library_NetBase_WWW_Administration_User_ManageUsersUserEdit as ManageUsersUserEdit
import string
import random

def DoUserParameters(amenu,file):
   asecprofile=ICORSecurityProfile()
   asecprofile.SetByUser(amenu.uid)
   asecprofile.GetUsers()
   agroups=asecprofile.Groups.keys()
   agroups.sort()

   apasschecker=ManageUsersUserEdit.GetPassPolicyCheckFunction(asecprofile)

   dd={
      'amenuoid':amenu.oid,
      'areportoid':amenu.Reports.OID,
      'arandom':random.randint(1,10000000),
      'apasschecker':apasschecker,
      'username':aICORDBEngine.User.UserName[amenu.uid],
   }

   vp=aICORDBEngine.UserVars[amenu.uid,'DisablePasswordChange']
   if vp!='1':
      file.write('<form name=summForm id=summForm METHOD="post" ACTION="icormain.asp?jobtype=reportsubmit&OID=%d&ReportOID=%d">\n'%(amenu.oid,amenu.Reports.OID))
      s="""
<script LANGUAGE="javascript">
%(apasschecker)s
function doSubmit() {
   jQuery("#mybutton1").attr('disabled','disabled');
   if (document.getElementById('valuepassword1').value=="") {
      alert('Proszę wpisać hasło');
      jQuery("#mybutton1").removeAttr("disabled");
      return;
   }
   if (document.getElementById('valuepassword1').value!=document.getElementById('valuepassword2').value) {
      alert('Wpisane hasła są różne');
      jQuery("#mybutton1").removeAttr("disabled");
      return;
   }
   var s=passwordCheck(document.getElementById('valuepassword1').value);
   if (s!='') {
      alert(s);
      jQuery("#mybutton1").removeAttr("disabled");
      return;
   }
   document.getElementById('summForm').submit();
}
</script>
   <h1>Użytkownik: %(username)s</h1>
<p>
Aby zmienić aktualne hasło wprowadź nowe hasło do poniższych pól. Małe i duże litery
są rozróżniane.
</p>
<TABLE>
<TR><TD align=right>Nowe hasło:</TD>
<TD><INPUT type="password" id=valuepassword1 name=valuepassword1 value=""></TD></TR>
<TR><TD align=right>Powtórz hasło:</TD>
<TD><INPUT type="password" id=valuepassword2 name=valuepassword2 value=""></TD></TR>
</TABLE>
<br>
<BUTTON id=mybutton1 class="fg-button-single ui-state-default ui-corner-all uihover" onclick="doSubmit();">Zmień hasło</BUTTON>
</form>
""" %dd
      file.write(s)

   if amenu.uid>=0:
      arefs=aICORDBEngine.User.WWWLoginLog.GetRefList(amenu.uid)
      if arefs:
         file.write('<hr><b>Log dostępu (ostatnie 100 pozycji):</b>\n<table class=objectsviewtable>')
         i=100
         while arefs and i:
            if arefs.Logged.ValuesAsInt(arefs.OID):
               alogged='Zalogowany'
            else:
               alogged='<font color=red>Błędne hasło</font>'
            file.write('<tr class=objectsviewrow><td class=objectsviewdataeven NOWRAP>%s</td><td class=objectsviewdataeven NOWRAP>%s</td><td class=objectsviewdataeven NOWRAP>%s</td><td class=objectsviewdataeven NOWRAP>%s</td><td class=objectsviewdataeven NOWRAP>%s</td></tr>\n'%(arefs.EventDateTime[arefs.OID],arefs.LoginUser[arefs.OID],alogged,arefs.RemoteAddr[arefs.OID],arefs.HttpUserAgent[arefs.OID]))
            arefs.Next()
            i=i-1
         file.write('</table>')

def DoUserParametersSubmit(amenu,areport,file):
   vp=aICORDBEngine.UserVars[amenu.uid,'DisablePasswordChange']
   if vp!='1':
      ahaslo1=areport['valuepassword1']
      ahaslo2=areport['valuepassword2']
      if ahaslo1!=ahaslo2:
         file.write('<h1><font color="red">Wprowadzone hasła są różne - spróbuj jeszcze raz.</font></h2>')
      else:
         aICORDBEngine.User.Password[amenu.uid]=ahaslo1
         file.write('<h1><font color="green">Hasło dla użytkownika %s zostało zmienione. Następnym razem podczas logowania użyj nowego hasła.</font></h2>'%(aICORDBEngine.User.UserName[amenu.uid],))
   else:
      file.write('<h1><font color="green">Ten użytkownik nie może zmieniać hasła.</font></h2>')

