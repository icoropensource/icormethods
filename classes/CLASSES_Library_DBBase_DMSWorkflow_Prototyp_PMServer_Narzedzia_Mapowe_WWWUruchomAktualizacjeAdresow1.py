# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORSecurity import *
import CLASSES_Library_ICORBase_Interface_ICORSync as ICORSync
import random

def DoGenerate(amenu,file):
   file.write("""
<form name="hiddenreportparms1" METHOD="post" ACTION="icormain.asp?jobtype=reportsubmit&OID=%d&ReportOID=%d&RandomValue=%d">
"""%(amenu.oid,amenu.Reports.OID,random.randint(1,10000000)))
   file.write("""
</form>
<script LANGUAGE="JScript">     
<!--
function doSubmit() {
   document.getElementById("hiddenreportparms1").submit();
}
-->
</script>
<BUTTON onclick="doSubmit();">Aktualizuj wszystkie adresy</BUTTON>
""")
   return

def DoGenerateSubmit(amenu,areport,file):
   aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Narzedzia_Mapowe']
   file.write('<h1><font color="green">W trakcie aktualizacji</font></h1>')
   astate=ICORSync.ICORState(aname='SOK_AKTUALIZACJA_GEO1',avalue='RUN')
   aclass.DoUruchomAktualizacjeAdresow1(str(astate.OID),-1,'')
   file.write("""
<script language="javascript" defer>
getParentFrame('NAVBAR').registerStateBadOK(%d);
</script>
"""%astate.OID)



