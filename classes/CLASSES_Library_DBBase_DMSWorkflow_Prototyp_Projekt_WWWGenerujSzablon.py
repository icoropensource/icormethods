# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORSecurity import *
import CLASSES_Library_ICORBase_Interface_ICORSync as ICORSync
import random

def DoGenerate(amenu,file):
   file.write("""
<form name="hiddenreportparms1" id="hiddenreportparms1" METHOD="post" ACTION="icormain.asp?jobtype=reportsubmit&OID=%d&ReportOID=%d&RandomValue=%d">
<table>
<tr><td align="right">Wybierz projekt:</td><td><SELECT NAME=edtProject ID=edtProject TABINDEX=1>
"""%(amenu.oid,amenu.Reports.OID,random.randint(1,10000000)))
   aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Projekt']
   aobj=aclass.GetFirstObject('Nazwa')
   while aobj:
      if not aobj['SGIsDisabled'] and CheckRecursiveAccessLevelForUser(aobj,'AccessLevelView',amenu.uid):
         bobj=aobj.SzablonyGenerowania
         while bobj:
            if CheckRecursiveAccessLevelForUser(bobj,'AccessLevelView',amenu.uid):
               file.write('<option value="%d">%s - %s</option>'%(bobj.OID,aobj.Nazwa,bobj.Nazwa))
            bobj.Next()
      aobj.Next('Nazwa')
   file.write("""
</SELECT></td></tr>
</table>
""")
   file.write("""
</form>
<script LANGUAGE="JScript">
<!--
function doSubmit() {
   document.getElementById("hiddenreportparms1").submit();
}
-->
</script>
<BUTTON class='fg-button-single ui-state-default ui-corner-all uihover' onclick="jQuery(this).attr('disabled','disabled');doSubmit();">Zatwierdź</BUTTON>
""")
   return

def DoGenerateSubmit(amenu,areport,file):
   soid=areport['edtProject']
   try:
      aoid=int(soid)
   except:
      aoid=-1
   aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_SzablonGenerowania']
   aobj=aclass[aoid]
   if not aobj:
      file.write('<h1><font color="red">Wybrano nieprawidłowy projekt.</font></h1><br><button onclick="history.back();">Powrót</button>')
      return
   file.write('<h1><font color="green">Szablon "%s" jest w trakcie generowania</font></h1><br><button onclick="history.back();">Powrót</button>'%aobj.Nazwa)
   astate=ICORSync.ICORState(aname='STRUKTURY',avalue='RUN')
   aobj.Class.Main('0!'+str(astate.OID),aobj.OID,'')
   file.write("""
<script language="javascript" defer>
getParentFrame('NAVBAR').registerStateBadOK(%d);
</script>
"""%astate.OID)
#   file.write('&nbsp;&nbsp;<button onclick="javascript:window.location=\'icormain.asp?jobtype=objectedit&CID=%d&OID=%d&menuoid=%d\';" tabIndex=%d>Przejdź do szablonu</button>'%(aobj.CID,aobj.OID,amenu.oid,2))



