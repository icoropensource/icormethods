# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
from CLASSES_Library_ICORBase_Interface_ICORSecurity import *
import CLASSES_Library_NetBase_WWW_Server_ICORWWWInterfaceUtil as ICORWWWInterfaceUtil
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import random

def GetPassPolicySuggestedPassword(asecprofile):
   apasswordpolicy=asecprofile.GetParam('PASSWORD_POLICY')
   if apasswordpolicy=='ustawa8':
      apasschecker=ICORUtil.GetRandomPassword(8)
   elif apasswordpolicy=='ustawa6':
      apasschecker=ICORUtil.GetRandomPassword(6)
   elif apasswordpolicy=='min6':
      apasschecker=ICORUtil.GetReadablePasswordPL()
   elif apasswordpolicy=='min8':
      apasschecker=ICORUtil.GetReadablePasswordPL()
   else:
      apasschecker=ICORUtil.GetReadablePasswordPL()
   return apasschecker

def GetPassPolicyCheckFunction(asecprofile):
   apasswordpolicy=asecprofile.GetParam('PASSWORD_POLICY')
   if apasswordpolicy=='ustawa8':
      apasschecker='''
function passwordCheck(apass) {
   if (apass.length<8) {
      return 'wymagane hasło o co najmniej 8 znakach';
   }
   if (apass.search(/[a-z]/)<0) {
      return 'wymagana co najmniej jedna mała litera';
   }
   if (apass.search(/[A-Z]/)<0) {
      return 'wymagana co najmniej jedna duża litera';
   }
   if (apass.search(/[0-9]/)<0) {
      return 'wymagana co najmniej jedna cyfra';
   }
   return '';
}
   '''
   elif apasswordpolicy=='ustawa6':
      apasschecker='''
function passwordCheck(apass) {
   if (apass.length<6) {
      return 'wymagane hasło o co najmniej 6 znakach';
   }
   if (apass.search(/[a-z]/)<0) {
      return 'wymagana co najmniej jedna mała litera';
   }
   if (apass.search(/[A-Z]/)<0) {
      return 'wymagana co najmniej jedna duża litera';
   }
   if (apass.search(/[0-9]/)<0) {
      return 'wymagana co najmniej jedna cyfra';
   }
   return '';
}
   '''
   elif apasswordpolicy=='min6':
      apasschecker='''
function passwordCheck(apass) {
   if (apass.length<6) {
      return 'wymagane hasło o co najmniej 6 znakach';
   }
   return '';
}
   '''
   elif apasswordpolicy=='min8':
      apasschecker='''
function passwordCheck(apass) {
   if (apass.length<8) {
      return 'wymagane hasło o co najmniej 8 znakach';
   }
   return '';
}
   '''
   else:
      apasschecker='''
function passwordCheck(apass) {
   return '';
}
   '''
   return apasschecker

def DoManageUsers(amenu,file):
   if 0:
      aclass=aICORDBEngine.Classes['CLASSES_System_User']
      afield=aclass.UserName
      aoid=afield.GetFirstValueID()
      while aoid>=0:
         if not aclass.ObjectExists(aoid):
            s=aclass.Description[aoid]
            aclass.Description[aoid]='XXXXX'
            aclass.Description[aoid]=s
         aoid=afield.GetNextValueID(aoid)

   w,i=0,1
   catdict={}
   asecprofile=ICORSecurityProfile()
   asecprofile.SetByUser(amenu.uid)
   asecprofile.GetUsers()

   apasschecker=GetPassPolicyCheckFunction(asecprofile)

   ausers=asecprofile.Users.keys()
   ausers.sort(cmp=lambda x,y: cmp(x.lower(), y.lower()))
#   file.write('<select id=usersselect onchange="alert(this.options[this.selectedIndex].value);">')
   file.write('<select class=searchableselect id=usersselect>')
   file.write('<option value="">*** wybierz użytkownika ***</option>')
   for aname in ausers:
      if asecprofile.Users[aname].WWWDisabled:
         uwwwdisabled='<font color="red">'
      else:
         uwwwdisabled='<font color="green">'
      adesc=asecprofile.Users[aname].Description
      if adesc:
         adesc=' - '+adesc
      file.write('<option value="%d">%s%s, %s %s%s</font></option>'%(asecprofile.Users[aname].UID,uwwwdisabled,asecprofile.Users[aname].UserName,asecprofile.Users[aname].VCFFirstName,asecprofile.Users[aname].VCFLastName,adesc))
   file.write('</select>')

   file.write('<br><br>')

   dd={
      'amenuoid':amenu.oid,
      'areportoid':amenu.Reports.OID,
      'arandom':random.randint(1,10000000),
      'apasschecker':apasschecker,
   }
#   file.write(ICORWWWInterfaceUtil.GetScriptHeader())
#   file.write(ICORWWWInterfaceUtil.GetScriptInit())
   file.write('''
<style>
.groupin {
   color: green;
   font-weight: bold;
}
.groupout {
   color: black;
   font-weight: normal;
}
</style>

<script type="text/javascript">
var auid;
$(function() {
   $('#usersselect').change(function() {
      auid=$(this).val();
      if (auid=="") {
         $("#container-1").hide();
      } else {
         $("#fragment-1").empty();
         $("#fragment-2").empty();
         $("#fragment-3").empty();
         $("#container-1").show();
         $("#fragment-1").load("icormain.asp?jobtype=reportsubmit&OID=%(amenuoid)d&ReportOID=%(areportoid)d&RandomValue=%(arandom)d&amode=t1&nobodytags=1&auid="+auid);
         $("#fragment-2").load("icormain.asp?jobtype=reportsubmit&OID=%(amenuoid)d&ReportOID=%(areportoid)d&RandomValue=%(arandom)d&amode=t2&nobodytags=1&auid="+auid,function(responseText,textStatus,XMLHttpRequest) {
            $("input[gtype='1']").each(function(i){
                  $(this).click(function(e) {
                     var acheck=$(this);
                     var aspan=acheck.next()
                     if (acheck.attr("checked")) {
                        $.post("icormain.asp?jobtype=reportsubmit&OID=%(amenuoid)d&ReportOID=%(areportoid)d&RandomValue=%(arandom)d&amode=t1g&nobodytags=1&auid="+auid,
                           {'gid':acheck.attr("goid")}
                        );
                        aspan.removeClass("groupout");
                        aspan.addClass("groupin");
                     } else {
                        $.post("icormain.asp?jobtype=reportsubmit&OID=%(amenuoid)d&ReportOID=%(areportoid)d&RandomValue=%(arandom)d&amode=t1f&nobodytags=1&auid="+auid,
                           {'gid':acheck.attr("goid")}
                        );
                        aspan.removeClass("groupin");
                        aspan.addClass("groupout");
                     }
                  });
            });
         });
         $("#fragment-3").load("icormain.asp?jobtype=reportsubmit&OID=%(amenuoid)d&ReportOID=%(areportoid)d&RandomValue=%(arandom)d&amode=t3&nobodytags=1&auid="+auid);
      }
   });
   $('#container-1').tabs({selected:1});
});
function zmianaDanych1() {
   var afirstname=$("input[name='edtVCFFirstName']").val();
   var alastname=$("input[name='edtVCFLastName']").val();
   var aemail=$("input[name='edtVCFEMail']").val();
   var aphone=$("input[name='edtVCFPhone']").val();
   var aopis=$("input[name='edtOpis']").val();
   $("#fragment-1").load("icormain.asp?jobtype=reportsubmit&OID=%(amenuoid)d&ReportOID=%(areportoid)d&RandomValue=%(arandom)d&amode=t1a&nobodytags=1&auid="+auid,
      {'firstname':afirstname,'lastname':alastname,'email':aemail,'phone':aphone,'opis':aopis}
   );
}
%(apasschecker)s
function zmianaDanych2() {
   var apass1=$("input[name='edtPassword1']").val();
   var apass2=$("input[name='edtPassword2']").val();
      if (apass1=="") {
         alert('Proszę wpisać hasło');
         return;
      }
      if (apass1!=apass2) {
         alert('Wpisane hasła są różne');
         return;
      }
   var s=passwordCheck(apass1);
   if (s!='') {
      alert(s);
      return;
   }
   $("#fragment-1").load("icormain.asp?jobtype=reportsubmit&OID=%(amenuoid)d&ReportOID=%(areportoid)d&RandomValue=%(arandom)d&amode=t1b&nobodytags=1&auid="+auid,
      {'password':apass1},
      function(responseText,textStatus,XMLHttpRequest) {
         alert("Hasło zostało zmienione");
      }
   );
}
function zmianaDanych2b() {
   var apass1=$("input[name='edtZmianaDni']").val();
   $("#fragment-1").load("icormain.asp?jobtype=reportsubmit&OID=%(amenuoid)d&ReportOID=%(areportoid)d&RandomValue=%(arandom)d&amode=t1b2&nobodytags=1&auid="+auid,
      {'passwordexp':apass1},
      function(responseText,textStatus,XMLHttpRequest) {
         alert("Reguły zostały zmienione");
      }
   );
}
function zmianaDanych3() {
   $("#fragment-1").load("icormain.asp?jobtype=reportsubmit&OID=%(amenuoid)d&ReportOID=%(areportoid)d&RandomValue=%(arandom)d&amode=t1c&nobodytags=1&auid="+auid,
      function(responseText,textStatus,XMLHttpRequest) {
         alert("Użytkownik został odblokowany.");
      }
   );
}
function zmianaDanych4() {
   $("#fragment-1").load("icormain.asp?jobtype=reportsubmit&OID=%(amenuoid)d&ReportOID=%(areportoid)d&RandomValue=%(arandom)d&amode=t1d&nobodytags=1&auid="+auid,
      function(responseText,textStatus,XMLHttpRequest) {
         alert("Użytkownik został zablokowany.");
      }
   );
}
function zmianaDanych5() {
   if (!confirm('Czy na pewno chcesz skasować tego użytkownika?')) {
      return;
   }
   $("#fragment-1").load("icormain.asp?jobtype=reportsubmit&OID=%(amenuoid)d&ReportOID=%(areportoid)d&RandomValue=%(arandom)d&amode=t1e&nobodytags=1&auid="+auid);
}
</script>

<div style="display:none;" id="container-1">
   <ul>
       <li><a href="#fragment-1"><span>Parametry</span></a></li>
       <li><a href="#fragment-2"><span>Prawa dostępu</span></a></li>
       <li><a href="#fragment-3"><span>Ostatnie logowania</span></a></li>
   </ul>
   <div id="fragment-1">
   </div>
   <div id="fragment-2">
   </div>
   <div id="fragment-3">
   </div>
</div>
'''%dd)


   if 0:
      file.write('<h1>Wybierz użytkownika:</h1>')
      file.write("""
<form name="hiddenreportparms1" id="hiddenreportparms1" METHOD="post" ACTION="icormain.asp?jobtype=reportsubmit&OID=%d&ReportOID=%d&nobodytags=1&RandomValue=%d">
<INPUT TYPE=HIDDEN NAME=edtSelUser ID=edtSelUser Value="">
<INPUT TYPE=HIDDEN NAME=edtAction ID=edtAction Value="SelectUser">
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
         uref='<a class="fg-button-single ui-state-default ui-corner-all uihover" href="javascript:void(doSubmit(\'%d\'));">%s, %s %s %s</a>'%(asecprofile.Users[aname].UID,asecprofile.Users[aname].UserName,asecprofile.Users[aname].VCFFirstName,asecprofile.Users[aname].VCFLastName,asecprofile.Users[aname].Description)
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
      file.write('</table>')
                      
def WriteUserParameters(amenu,file,auser,asecprofile,auid):
   file.write("""
<form name="hiddenreportparms1" id="hiddenreportparms1" METHOD="post" ACTION="icormain.asp?jobtype=reportsubmit&OID=%d&ReportOID=%d&RandomValue=%d">
<INPUT TYPE=HIDDEN NAME=edtSelUser ID=edtSelUser Value="%d">
<INPUT TYPE=HIDDEN NAME=edtAction ID=edtAction Value="SelectUser">
<INPUT TYPE=HIDDEN NAME=edtParam ID=edtParam Value="SelectUser">
<INPUT TYPE=HIDDEN NAME=edtParam1 ID=edtParam1 Value="">
<INPUT TYPE=HIDDEN NAME=edtParam2 ID=edtParam2 Value="">
<INPUT TYPE=HIDDEN NAME=edtParam3 ID=edtParam3 Value="">
<INPUT TYPE=HIDDEN NAME=edtParam4 ID=edtParam4 Value="">
<INPUT TYPE=HIDDEN NAME=edtParam5 ID=edtParam5 Value="">
</form>
<script LANGUAGE="JScript">
<!--
function doSubmit(aaction,aparam) {
   document.getElementById('edtAction').value=aaction
   if (aaction=="ChangePassword") {
      if (document.getElementById('edtPassword1').value=="") {
         alert('Proszę wpisać hasło');
         return;
      }
      if (document.getElementById('edtPassword1').value!=document.getElementById('edtPassword2').value) {
         alert('Wpisane hasła są różne');
         return;
      }
      document.getElementById('edtParam').value=document.getElementById('edtPassword1').value;
   }
   if ((aaction=="GroupRemove") || (aaction=="GroupAdd")) {
      document.getElementById('edtParam').value=aparam;
   }
   if (aaction=="UserDelete") {
      if (!confirm('Czy na pewno chcesz skasować tego użytkownika?')) {
         return;
      }
   }
   if (aaction=="ChangeVCFData") {
      document.getElementById('edtParam1').value=document.getElementById('edtVCFFirstName').value;
      document.getElementById('edtParam2').value=document.getElementById('edtVCFLastName').value;
      document.getElementById('edtParam3').value=document.getElementById('edtVCFEMail').value;
      document.getElementById('edtParam4').value=document.getElementById('edtOpis').value;
      document.getElementById('edtParam5').value=document.getElementById('edtVCFPhone').value;
   }
   document.getElementById('hiddenreportparms1').submit();
}
-->
</script>
"""%(amenu.oid,amenu.Reports.OID,random.randint(1,10000000),auid))
   file.write('<h1>Użytkownik: %s</h1>'%(auser.UserName,))
   file.write("""
<table>
<tr><td align="right">Hasło:</td><td><INPUT TYPE=PASSWORD NAME=edtPassword1 ID=edtPassword1 TABINDEX=2 Value=""></td></tr>
<tr><td align="right">Powtórz hasło:</td><td><INPUT TYPE=PASSWORD NAME=edtPassword2 ID=edtPassword2 TABINDEX=3 Value=""></td></tr>
</table>
<br>
<BUTTON class="fg-button-single ui-state-default ui-corner-all uihover" onclick="doSubmit('ChangePassword',0);">Zmień hasło</BUTTON>
<hr>
""")
   file.write("""
<table>
<tr><td align="right">Imię:</td><td><INPUT TYPE=EDIT NAME=edtVCFFirstName ID=edtVCFFirstName TABINDEX=4 Value="%s"></td></tr>
<tr><td align="right">Nazwisko:</td><td><INPUT TYPE=EDIT NAME=edtVCFLastName ID=edtVCFLastName TABINDEX=5 Value="%s"></td></tr>
<tr><td align="right">EMail:</td><td><INPUT TYPE=EDIT NAME=edtVCFEMail ID=edtVCFEMail TABINDEX=6 Value="%s"></td></tr>
<tr><td align="right">Telefon:</td><td><INPUT TYPE=EDIT NAME=edtVCFPhone ID=edtVCFPhone TABINDEX=7 Value="%s"></td></tr>
<tr><td align="right">Opis:</td><td><INPUT TYPE=EDIT NAME=edtOpis ID=edtOpis TABINDEX=8 Value="%s"></td></tr>
</table>
<br>
<BUTTON class="fg-button-single ui-state-default ui-corner-all uihover" onclick="doSubmit('ChangeVCFData',0);">Zmień dane osobowe</BUTTON>
<hr>
"""%(auser.VCFFirstName,auser.VCFLastName,auser.VCFEMail,auser.VCFPhone,auser.Description))
   if auser.WWWDisabled:
      file.write('<p>Użytkownik jest zablokowany!</p><BUTTON class="fg-button-single ui-state-default ui-corner-all uihover" onclick="doSubmit(\'WWWEnable\',0);">Odblokuj użytkownika</BUTTON><hr>')
   else:
      file.write('<p>Użytkownik może pracować przez WWW.</p><BUTTON class="fg-button-single ui-state-default ui-corner-all uihover" onclick="doSubmit(\'WWWDisable\',0);">Zablokuj użytkownika</BUTTON><hr>')
   file.write('<BUTTON class="fg-button-single ui-state-default ui-corner-all uihover" onclick="doSubmit(\'UserDelete\',0);">Skasuj użytkownika</BUTTON><hr>')
   agroups=asecprofile.Groups.keys()
   agroups.sort()
   file.write('<br><b>Prawa dostępu</b><br>\n<table>\n')
   dg={}
   for aname in agroups:
      goid,gname=asecprofile.Groups[aname].OID,asecprofile.Groups[aname].GroupName
      dg[goid]=gname
      if auser.IsInGroup(goid):
         file.write('<tr><td><font color="green" size="-2">%s</font></td><td><button class="fg-button-single ui-state-default ui-corner-all uihover" onclick="doSubmit(\'GroupRemove\',%d);">Odłącz od tej grupy</button></td></tr>\n'%(gname,goid))
      else:
         file.write('<tr><td><font color="red" size="-2">%s</font></td><td><button class="fg-button-single ui-state-default ui-corner-all uihover" onclick="doSubmit(\'GroupAdd\',%d);">Przyłącz do tej grupy</button></td></tr>\n'%(gname,goid))
   buser=ICORSecurityUser(amenu.uid)
   bgroups=buser.Groups
   whr=1
   while bgroups:
      goid=bgroups.OID
      gname=bgroups.Name[goid]
      if not dg.has_key(goid):
         if whr:
            file.write('<tr><td colspan=2><hr></td></tr>\n')
            whr=0
         gname=bgroups.Name[goid]
         if auser.IsInGroup(goid):
            file.write('<tr><td><font color="green" size="-2">%s</font></td><td><button class="fg-button-single ui-state-default ui-corner-all uihover" onclick="doSubmit(\'GroupRemove\',%d);">Odłącz od tej grupy</button></td></tr>\n'%(gname,goid))
         else:
            file.write('<tr><td><font color="red" size="-2">%s</font></td><td><button class="fg-button-single ui-state-default ui-corner-all uihover" onclick="doSubmit(\'GroupAdd\',%d);">Przyłącz do tej grupy</button></td></tr>\n'%(gname,goid))
      bgroups.Next()
   file.write('</table>')
   arefs=auser.WWWLoginLog
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

def DoManageUsersSubmit(amenu,areport,file):
   amode=areport['amode']
   try:
      auid=int(areport['auid'])
   except:
      auid=-1
   if auid<0:
      return
   asecprofile=ICORSecurityProfile()
   asecprofile.SetByUser(amenu.uid)
   asecprofile.GetUsers()
   auser=asecprofile.UsersID.get(auid,None)
   if auser is None:
      file.write('<h1><font color="red">Wybrany użytkownik nie istnieje</font></h1>')
      return
   if amode=='t1a':
      amode='t1'
      auser.VCFFirstName=XMLUtil.UTF8_To_CP1250(areport['firstname'])
      auser.VCFLastName=XMLUtil.UTF8_To_CP1250(areport['lastname'])
      auser.VCFEMail=XMLUtil.UTF8_To_CP1250(areport['email'])
      auser.VCFPhone=XMLUtil.UTF8_To_CP1250(areport['phone'])
      auser.Description=XMLUtil.UTF8_To_CP1250(areport['opis',''])
   if amode=='t1b':
      amode='t1'
      auser.Password=XMLUtil.UTF8_To_CP1250(areport['password'])
   if amode=='t1b2':
      amode='t1'
      auser.UserClass.PasswordExpiration[auser.UID]=XMLUtil.UTF8_To_CP1250(areport['passwordexp'])
   if amode=='t1c':
      amode='t1'
      auser.WWWDisabled=0
   if amode=='t1d':
      amode='t1'
      auser.WWWDisabled=1
   if amode=='t1e':
      if auid==amenu.uid:
         amode='t1'
         file.write('<h1><font color="red">Nie możesz skasować sam siebie</font></h1><hr>')
      else:
         auser.Delete()
         file.write('<h1><font color="green">Użytkownik został skasowany</font></h1>')
         return

   if amode=='t1f':
      try:
         goid=int(areport['gid'])
         agroup=ICORSecurityUserGroup(goid)
         agroup.RemoveUser(auser)
      except:
         print 'Invalid F group',areport['gid']
      return
   if amode=='t1g':
      try:
         goid=int(areport['gid'])
         agroup=ICORSecurityUserGroup(goid)
         agroup.AddUser(auser)
      except:
         print 'Invalid G group',areport['gid']
      return

   if amode=='t1':
      file.write("""
<table>
<tr><td align="right">Imię:</td><td><INPUT TYPE=EDIT NAME=edtVCFFirstName ID=edtVCFFirstName TABINDEX=4 Value="%s"></td></tr>
<tr><td align="right">Nazwisko:</td><td><INPUT TYPE=EDIT NAME=edtVCFLastName ID=edtVCFLastName TABINDEX=5 Value="%s"></td></tr>
<tr><td align="right">EMail:</td><td><INPUT TYPE=EDIT NAME=edtVCFEMail ID=edtVCFEMail TABINDEX=6 Value="%s"></td></tr>
<tr><td align="right">Telefon:</td><td><INPUT TYPE=EDIT NAME=edtVCFPhone ID=edtVCFPhone TABINDEX=7 Value="%s"></td></tr>
<tr><td align="right">Opis:</td><td><INPUT TYPE=EDIT NAME=edtOpis ID=edtOpis TABINDEX=8 Value="%s"></td></tr>
</table>
<br>
<BUTTON class="fg-button-single ui-state-default ui-corner-all uihover" onclick="javascript:zmianaDanych1();">Zmień dane osobowe</BUTTON>
<hr>
<table>
<tr><td align="right">Hasło:</td><td><INPUT TYPE=PASSWORD NAME=edtPassword1 ID=edtPassword1 TABINDEX=8 Value=""></td></tr>
<tr><td align="right">Powtórz hasło:</td><td><INPUT TYPE=PASSWORD NAME=edtPassword2 ID=edtPassword2 TABINDEX=9 Value=""></td></tr>
</table>
<br>
<BUTTON class="fg-button-single ui-state-default ui-corner-all uihover" onclick="javascript:zmianaDanych2();">Zmień hasło</BUTTON>
<hr>
<table>
<tr><td align="right">Ostatnia zmiana hasła:</td><td>%s</td></tr>
<tr><td align="right">Wymuszaj zmianę hasła co x dni:</td><td><INPUT TYPE=EDIT NAME=edtZmianaDni ID=edtZmianaDni TABINDEX=10 Value="%s"></td></tr>
</table>
<br>
<BUTTON class="fg-button-single ui-state-default ui-corner-all uihover" onclick="javascript:zmianaDanych2b();">Zmień reguły</BUTTON>
<hr>
"""%(auser.VCFFirstName,auser.VCFLastName,auser.VCFEMail,auser.VCFPhone,auser.Description,auser.UserClass.PasswordLastChanged[auser.UID],auser.UserClass.PasswordExpiration[auser.UID],))
      if auser.WWWDisabled:
         file.write('<p>Użytkownik jest zablokowany!</p><BUTTON class="fg-button-single ui-state-default ui-corner-all uihover" onclick="javascript:zmianaDanych3();">Odblokuj użytkownika</BUTTON><hr>')
      else:
         file.write('<p>Użytkownik może pracować przez WWW.</p><BUTTON class="fg-button-single ui-state-default ui-corner-all uihover" onclick="javascript:zmianaDanych4();">Zablokuj użytkownika</BUTTON><hr>')
      file.write('<BUTTON class="fg-button-single ui-state-default ui-corner-all uihover" onclick="javascript:zmianaDanych5();">Skasuj użytkownika</BUTTON>')
   elif amode=='t2':
      agroups=asecprofile.Groups.keys()
      agroups.sort(cmp=lambda x,y: cmp(x.lower(), y.lower()))
      file.write('<br><fieldset><legend>Prawa dostępu użytkownika:</legend>\n')
      dg={}
      dlg={}
      for aname in agroups:
         agroup=asecprofile.Groups[aname]
         goid,gname=agroup.OID,agroup.GroupName
         acategory,akind=agroup.Category,agroup.Kind
         dg[goid]=gname
         if auser.IsInGroup(goid):
            schecked=" checked=1"
            sclass='groupin'
         else:
            schecked=""
            sclass='groupout'
         lg=dlg.get((acategory,akind),[])
         lg.append('<input type=checkbox gtype="1" class="checkradio" goid="%d" id=sg%d name=sg%d%s><span class="%s">%s</span><br>\n'%(goid,goid,goid,schecked,sclass,gname))
         dlg[(acategory,akind)]=lg
      ldgk=dlg.keys()
      ldgk.sort()
      for acategory,akind in ldgk:
         if acategory or akind:
            file.write('<br><fieldset><legend>%s %s:</legend>\n'%(acategory,akind))
         lg=dlg[acategory,akind]
         for s in lg:
            file.write(s)
         if acategory or akind:
            file.write('</fieldset>\n')
      buser=ICORSecurityUser(amenu.uid)
      bgroups=buser.Groups
      whr=1
      while bgroups:
         goid=bgroups.OID
         gname=bgroups.Name[goid]
         if not dg.has_key(goid):
            if whr:
               file.write('</fieldset><br><fieldset><legend>Prawa dostępu operatora:</legend>\n')
               whr=0
            gname=bgroups.Name[goid]
            if auser.IsInGroup(goid):
               schecked=" checked=1"
               sclass='groupin'
            else:
               schecked=""
               sclass='groupout'
            file.write('<input type=checkbox gtype="1" class="checkradio" goid="%d" id=sg%d name=sg%d%s><span class="%s">%s</span><br>\n'%(goid,goid,goid,schecked,sclass,gname))
         bgroups.Next()
      file.write('</fieldset>\n')
   elif amode=='t3':
      arefs=auser.WWWLoginLog
      if arefs:
         file.write('<hr><b>Log dostępu (ostatnie 100 pozycji):</b>\n<table class=objectsviewtable>')
         i=100
         while arefs and i:
            if arefs.Logged.ValuesAsInt(arefs.OID):
               alogged='Zalogowany'
            else:
               alogged='<font color=red>Nie zalogowany</font>'
            file.write('<tr class=objectsviewrow><td class=objectsviewdataeven NOWRAP>%s</td><td class=objectsviewdataeven NOWRAP>%s</td><td class=objectsviewdataeven NOWRAP>%s</td><td class=objectsviewdataeven NOWRAP>%s</td><td class=objectsviewdataeven NOWRAP>%s</td></tr>\n'%(arefs.EventDateTime[arefs.OID],arefs.LoginUser[arefs.OID],alogged,arefs.RemoteAddr[arefs.OID],arefs.HttpUserAgent[arefs.OID]))
            arefs.Next()
            i=i-1
         file.write('</table>')
   return
   aaction=areport['edtAction','']
   auid=int(areport['edtSelUser'])
   asecprofile=ICORSecurityProfile()
   asecprofile.SetByUser(amenu.uid)
   asecprofile.GetUsers()
   auser=asecprofile.UsersID.get(auid,None)
   if auser is None:
      file.write('<h1><font color="red">Wybrany użytkownik nie istnieje</font></h1><br><button class="fg-button-single ui-state-default ui-corner-all uihover" onclick="history.back();">Powrót</button>')
      return
   if aaction=='':
      print 'Brak akcji!'
   elif aaction=='UserDelete':
      if auid==amenu.uid:
         file.write('<h1><font color="red">Nie możesz skasować sam siebie</font></h1><br><button class="fg-button-single ui-state-default ui-corner-all uihover" onclick="history.back();">Powrót</button>')
      else:
         auser.Delete()
         file.write('<h1><font color="green">Użytkownik został skasowany</font></h1>')
      return
   elif aaction=='ChangePassword':
      auser.Password=areport['edtParam']
   elif aaction=='ChangeVCFData':
      auser.VCFFirstName=areport['edtParam1']
      auser.VCFLastName=areport['edtParam2']
      auser.VCFEMail=areport['edtParam3']
      auser.Description=areport['edtParam4']
      auser.VCFPhone=areport['edtParam5']
   elif aaction=='SelectUser':
      pass
   elif aaction=='WWWEnable':
      auser.WWWDisabled=0
   elif aaction=='WWWDisable':
      auser.WWWDisabled=1
   elif aaction=='GroupRemove':
      goid=int(areport['edtParam'])
      agroup=ICORSecurityUserGroup(goid)
#      agroup=asecprofile.GroupsID[goid]
      agroup.RemoveUser(auser)
   elif aaction=='GroupAdd':
      goid=int(areport['edtParam'])
      agroup=ICORSecurityUserGroup(goid)
#      agroup=asecprofile.GroupsID[goid]
      agroup.AddUser(auser)
   WriteUserParameters(amenu,file,auser,asecprofile,auid)
   return




