# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
from CLASSES_Library_NetBase_WWW_Server_ServerUtil import ICORReport
import CLASSES_Library_NetBase_WWW_Server_ICORWWWInterfaceUtil as ICORWWWInterfaceUtil
from CLASSES_Library_ICORBase_Interface_ICORSecurity import *
import CLASSES_Library_NetBase_WWW_Administration_User_ManageUsersUserEdit as ManageUsersUserEdit
import time
import string
import random

def GetPass(apass,auid):
   return aICORDBEngine.HashString(apass+'_'+str(auid))

def GetPasswordForm(amessage,UID):

   asecprofile=ICORSecurityProfile()
   asecprofile.SetByUser(UID)
   asecprofile.GetUsers()
   agroups=asecprofile.Groups.keys()
   agroups.sort()

   apasschecker=ManageUsersUserEdit.GetPassPolicyCheckFunction(asecprofile)

   dd={
      'arandom':random.randint(1,10000000),
      'apasschecker':apasschecker,
      'username':aICORDBEngine.User.UserName[UID],
   }

   if not amessage:
      amessage='Zmiana has�a'
   aresponse=ICORUtil.Response()
   aresponse.write('<html><head>')
   ICORWWWInterfaceUtil.WriteDefIncMeta(aresponse)
   aresponse.write('''
<title>Zmiana has�a</title>
</head>
<body>
<h1><font color="navy">Wprowad� nowe has�o:</font></h1>
<script LANGUAGE="javascript">
%s
function doSubmit() {
   jQuery("#mybutton1").attr('disabled','disabled');
   if (document.getElementById('password1').value=="") {
      alert('Prosz� wpisa� has�o');
      jQuery("#mybutton1").removeAttr("disabled");
      return;
   }
   if (document.getElementById('password1').value!=document.getElementById('password2').value) {
      alert('Wpisane has�a s� r�ne');
      jQuery("#mybutton1").removeAttr("disabled");
      return;
   }
   var s=passwordCheck(document.getElementById('password1').value);
   if (s!='') {
      alert(s);
      jQuery("#mybutton1").removeAttr("disabled");
      return;
   }
   document.getElementById('summForm').submit();
}
</script>
<form name="summForm" id="summForm" METHOD="post" ACTION="icormain.asp">
<table width="523" height="145" border="0">
<tr>
<td rowspan=2><div align="center"><center><p><IMG align=right src="images/icor_znak2.gif"></p></center></div></td>
<td align="right" class="objectseditdatafieldname">Has�o:</td>
<td ></td>
<td ><input TYPE="password" NAME="password1" id="password1" VALUE="" size="22" maxLength=128 tabIndex=1 REQUIRED=1 REGEXP='......+'></td>
</tr>
<tr>
<td align="right" class="objectseditdatafieldname">Powt�rz&nbsp;has�o:</td>
<td ></td>
<td ><input TYPE="password" NAME="password2" id="password2" size="22" maxLength=128 tabIndex=2 REQUIRED=1 REGEXP='......+'></td>
</tr>
<tr>
<td colspan=4 ><div align="center"><center><p>
<BUTTON id=mybutton1 class="fg-button-single ui-state-default ui-corner-all uihover" onclick="doSubmit();">Zmie� has�o</BUTTON>
</p></center></div> </td>
</tr>
</table>
</form>
<hr>
<i>Has�o musi mie� co najmniej 6 znak�w. Mo�e zawiera� litery i cyfry. Du�e i ma�e litery s� rozpoznawane.
Has�a trywialne czyli takie same jak nazwa konta b�d� jego skr�t s� odrzucane. System nie pozwoli tak�e na wprowadzenie
has�a, kt�re by�o ju� wykorzystane w przesz�o�ci.</i>
<hr>
<h3><font color="red">UWAGA: %s</font></h3>
'''%(apasschecker,amessage))
   if 0:
      aresponse.write('<hr><b><font color=navy>Proponowane has�a:</font></b><br><table border="0" width="100%">')
      for i in range(10):
         aresponse.write('<tr>')
         for j in range(6):
            aresponse.write('<td>%s</td>'%ICORUtil.GetReadablePasswordPL())
         aresponse.write('</tr>')
      aresponse.write('</table>')
   aresponse.write('''
<SCRIPT LANGUAGE=javascript>
jQuery(function() {
   jQuery("#password1").focus();
});
</SCRIPT>
<!--
<SCRIPT src='/icormanager/inc/icor_validation.js' language='JScript'></SCRIPT>
-->
</body>
</html>
''')
   return aresponse.AsText(aashtmlstring=0)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   ret='OK'
   uobj=aICORDBEngine.User[UID]
   apassword=uobj.Password
   ausername=uobj.UserName
   if OID==0:
      achange=0
      amessage=''
      for s in ['',ausername,ICORUtil.strUpperPL(ausername),ICORUtil.strLowerPL(ausername),ausername[:2],ICORUtil.strUpperPL(ausername[:2]),ICORUtil.strLowerPL(ausername[:2])]:
         if apassword==GetPass(s,UID):
            achange=1
            amessage='Has�o jest trywialne'
            break
      if not achange:
         if uobj['PasswordMustChange']:
            achange=1
            amessage='Has�o musi zosta� zmienione'
      if not achange:
         aexpiry=uobj['PasswordExpiration']
         if aexpiry>0:
            alastchanged=uobj['PasswordLastChanged']
            if ICORUtil.DateDiff(alastchanged)>aexpiry:
               achange=1
               amessage='Has�o wygas�o'
      if achange:
         ret=GetPasswordForm(amessage,UID)
   elif OID==1:
      aparms=ICORReport(Value,adefPost=1)
      apass1=aparms['password1','']
      apass2=aparms['password2','']
      achange=0
      amessage=''
      if apass1!=apass2:
         achange=1
         amessage='Wprowadzone has�a s� r�ne'
      if not achange and len(apass1)<6:
         achange=1
         amessage='Wprowadzone has�o jest za kr�tkie'
      if not achange:
         for s in [ausername,ICORUtil.strUpperPL(ausername),ICORUtil.strLowerPL(ausername),]:
            if apass1==GetPass(s,UID):
               achange=1
               amessage='Wprowadzone has�o jest trywialne'
               break
      if not achange:
         l=string.split(string.replace(uobj.PasswordHistory,chr(13),''),chr(10))
         bpass1=GetPass(apass1,UID)
         for bpass2 in l:
            if bpass1==bpass2:
               achange=1
               amessage='Wprowadzone has�o by�o ju� wykorzystane'
               break
      if achange:
         ret=GetPasswordForm(amessage,UID)
      else:
         uobj.Password=apass1
   return ret




