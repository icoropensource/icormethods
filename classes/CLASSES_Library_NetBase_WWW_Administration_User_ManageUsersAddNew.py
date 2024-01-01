# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORSecurity import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_WWW_Administration_User_ManageUsersUserEdit as ManageUsersUserEdit
import random

def DoManageUsers(amenu,file):
   file.write("""
<form name="hiddenreportparms1" id="hiddenreportparms1" METHOD="post" ACTION="icormain.asp?jobtype=reportsubmit&OID=%d&ReportOID=%d&RandomValue=%d">
<table>
<tr><td align="right">Identyfikator użytkownika:</td><td><INPUT NAME=edtLoginName ID=edtLoginName TABINDEX=1 Value=""></td></tr>
<tr><td align="right">Hasło:</td><td><INPUT TYPE=PASSWORD NAME=edtPassword1 ID=edtPassword1 TABINDEX=2 Value=""></td></tr>
<tr><td align="right">Powtórz hasło:</td><td><INPUT TYPE=PASSWORD NAME=edtPassword2 ID=edtPassword2 TABINDEX=3 Value=""></td></tr>
<tr><td align="right">Hasło wygasa po (dni):</td><td><INPUT NAME=edtPasswordExp ID=edtPasswordExp TABINDEX=4 Value=""></td></tr>

<tr><td align="right">Nazwisko:</td><td><INPUT NAME=edtLastName ID=edtLastName TABINDEX=5 Value=""></td></tr>
<tr><td align="right">Imię:</td><td><INPUT NAME=edtFirstName ID=edtFirstName TABINDEX=6 Value=""></td></tr>
<tr><td align="right">EMail:</td><td><INPUT NAME=edtEMail ID=edtEMail TABINDEX=7 Value=""></td></tr>
<tr><td align="right">Opis:</td><td><INPUT NAME=edtOpis ID=edtOpis TABINDEX=8 Value=""></td></tr>
</table>
"""%(amenu.oid,amenu.Reports.OID,random.randint(1,10000000)))
   asecprofile=ICORSecurityProfile()
   asecprofile.SetByUser(amenu.uid)
   asecprofile.GetUsers()
   agroups=asecprofile.Groups.keys()
   agroups.sort()

   apasschecker=ManageUsersUserEdit.GetPassPolicyCheckFunction(asecprofile)

   file.write('<br><b>Prawa dostępu</b><br>\n')
   for aname in agroups:
      goid,gname=asecprofile.Groups[aname].OID,asecprofile.Groups[aname].GroupName
      file.write('<INPUT class="checkradio" TYPE=CHECKBOX NAME=grpCheck_%d ID=grpCheck_%d >%s<br>\n'%(goid,goid,gname))

   dd={
      'amenuoid':amenu.oid,
      'areportoid':amenu.Reports.OID,
      'arandom':random.randint(1,10000000),
      'apasschecker':apasschecker,
   }
   file.write("""
</form>
<script LANGUAGE="javascript">
%(apasschecker)s
function doSubmit() {
   jQuery("#mybutton1").attr('disabled','disabled');
   if (document.getElementById('edtLoginName').value=="") {
      alert('Proszę wpisać identyfikator użytkownika');
      jQuery("#mybutton1").removeAttr("disabled");
      return;
   }
   if (document.getElementById('edtPassword1').value=="") {
      alert('Proszę wpisać hasło');
      jQuery("#mybutton1").removeAttr("disabled");
      return;
   }
   if (document.getElementById('edtPassword1').value!=document.getElementById('edtPassword2').value) {
      alert('Wpisane hasła są różne');
      jQuery("#mybutton1").removeAttr("disabled");
      return;
   }
   var s=passwordCheck(document.getElementById('edtPassword1').value);
   if (s!='') {
      alert(s);
      jQuery("#mybutton1").removeAttr("disabled");
      return;
   }
   document.getElementById('hiddenreportparms1').submit();
}
</script>
<BUTTON id=mybutton1 class="fg-button-single ui-state-default ui-corner-all uihover" onclick="doSubmit();">Zatwierdź</BUTTON>
"""%dd)
   file.write('<hr><b>Proponowane hasła:</b><br><table border="0" width="100%">')
   for i in range(10):
      file.write('<tr>')
      for j in range(6):
         file.write('<td>%s</td>'%ManageUsersUserEdit.GetPassPolicySuggestedPassword(asecprofile))
      file.write('</tr>')
   file.write('</table>')
   return

def DoManageUsersSubmit(amenu,areport,file):
   auser,apassword,afirstname,alastname,aemail,aexpiration,adescription=areport['edtLoginName'],areport['edtPassword1'],areport['edtFirstName'],areport['edtLastName'],areport['edtEMail'],areport['edtPasswordExp'],areport['edtOpis']
   asecprofile=ICORSecurityProfile()
   asecprofile.SetByUser(amenu.uid)
   asecprofile.GetUsers()
   if asecprofile.UserClass.UserName.Identifiers(auser)>=0:
      file.write('<h1><font color="red">Użytkownik o takiej nazwie już istnieje</font></h1><br><button class="fg-button-single ui-state-default ui-corner-all uihover" onclick="history.back();">Powrót</button>')
      return
   grefs=''
   for agroup in asecprofile.Groups.values():
      if areport.has_key('grpCheck_'+str(agroup.OID)):
         grefs=grefs+str(agroup.OID)+':'+str(agroup.UserGroupClass.CID)+':'
   if grefs=='':
      file.write('<h1><font color="red">Proszę wybrać co najmniej jedną grupę dostępu</font></h1><br><button class="fg-button-single ui-state-default ui-corner-all uihover" onclick="history.back();">Powrót</button>')
      return
   ret=asecprofile.AddUser(auser,apassword,grefs,afirstname=afirstname,alastname=alastname,aemail=aemail,aexpiration=aexpiration,adescription=adescription)
   if ret:
      file.write('<h1><font color="green">Użytkownik został pomyślnie dodany</font></h1><br><button class="fg-button-single ui-state-default ui-corner-all uihover" onclick="history.back();">Powrót</button>')
   else:
      file.write('<h1><font color="red">Użytkownik nie został dodany</font></h1><br><button class="fg-button-single ui-state-default ui-corner-all uihover" onclick="history.back();">Powrót</button>')



