# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORSecurity import *
from CLASSES_Library_DBBase_Query_WorkSheet_Main_ICORWorksheetQuery import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import random
import re

def DoProcessQuery2(aclass,aoid,amenu,file,alevel=0):
   arefs=aclass.AccessLevel.GetRefList(aoid)
   w1=CheckAccessLevelForUser(arefs,amenu.uid)
   if not w1:
      return
   aquery=aWorksheetQueries[aoid]
   sn=aclass.TableID[aoid]+' - '+aclass.TableTitle[aoid]
   sh='javascript:callbackfunction(\'%d\')'%(aoid)
   sc=aquery.StatusCalculateAsString()
   if sc:
      file.write('<h2>%s</h2><pre>%s</pre><hr>\n'%(sn,sc))
   qrefs=aclass.SubQuery.GetRefList(aoid)
   while qrefs:
      DoProcessQuery2(qrefs.Class,qrefs.OID,amenu,file,alevel+1)
      qrefs.Next()
   return

def DoStatusList(amenu,file):
   aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_Query_WorkSheet_QueryStruct']
   file.write("""
<form name="hiddenreportparms1" METHOD="post" ACTION="icormain.asp?jobtype=reportsubmit&OID=%d&ReportOID=%d&RandomValue=%d">
<INPUT type="hidden" id=wsqueryoid name=wsqueryoid value="">
</FORM>

<SCRIPT LANGUAGE="JScript">
<!--
function callbackfunction(text) {
   document.getElementById("wsqueryoid").value=text;
   document.getElementById("hiddenreportparms1").submit()
}
-->
</SCRIPT>
"""%(amenu.oid,amenu.Reports.OID,random.randint(1,10000000)))

   aobj=aclass.GetFirstObject()
   while aobj:
      qrefs=aclass.Query.GetRefList(aobj.OID)
      while qrefs:
         DoProcessQuery2(qrefs.Class,qrefs.OID,amenu,file)
         qrefs.Next()
      aobj.Next()



