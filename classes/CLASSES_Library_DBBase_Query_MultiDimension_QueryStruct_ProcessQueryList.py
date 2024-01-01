# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORSecurity import *
from CLASSES_Library_DBBase_Query_MultiDimension_Main_ICORMultiDimensionQuery import GenerateMDQuery,mdqt_HTML,mdqt_Excel
from CLASSES_Library_NetBase_WWW_HTML_Tree_SimpleLinks_Main import SimpleLinksHTMLTree
import CLASSES_Library_ICORBase_Interface_ICORUtil
import string
import random

def DoProcessQuery(aclass,aoid,amenu,file,catdict):
   ret=0
   arefs=aclass.AccessLevel.GetRefList(aoid)
   w1=CheckAccessLevelForUser(arefs,amenu.uid)
   if not w1:
      return 0
   sn=aclass.Name[aoid]
   if aclass.Dimensions[aoid]=='':
      s='<li>%s</li>\n'%(sn)
   else:
      sl=string.split(sn,' ')
      for s1 in sl:
         s2=s1.lower()
         catdict[s2]=1
      ret=ret+1
      s='<li><a class=reflistoutred href="javascript:callbackfunction(\'%d\')">%s</a></li>\n'%(aoid,sn)
   file.write(s)
   qrefs=aclass.SubQuery.GetRefList(aoid)

   file.write('<UL>\n')
   while qrefs:
      ret=ret+DoProcessQuery(qrefs.Class,qrefs.OID,amenu,file,catdict)
      qrefs.Next()
   file.write('</UL>\n')
   return ret

def DoProcessQuery2(aclass,aoid,amenu,file,catdict,anode,alevel=0):
   ret=0
   arefs=aclass.AccessLevel.GetRefList(aoid)
   w1=CheckAccessLevelForUser(arefs,amenu.uid)
   if not w1:
      return 0
   sn=aclass.Caption[aoid]
   if sn=='':
      sn=aclass.Name[aoid]
   if aclass.Dimensions[aoid]=='':
      sh=''
   else:
      sl=string.split(sn,' ')
      for s1 in sl:
         s2=s1.lower()
         catdict[s2]=1
      ret=ret+1
      sh='javascript:callbackfunction(\'%d\')'%(aoid)
   bnode=anode.AddNode(sn,sh,aexpanded=alevel<1)
   qrefs=aclass.SubQuery.GetRefList(aoid)

   while qrefs:
      ret=ret+DoProcessQuery2(qrefs.Class,qrefs.OID,amenu,file,catdict,bnode,alevel+1)
      qrefs.Next()
   return ret

def DoQueryStruct(amenu,file):
   aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_Query_MultiDimension_QueryStruct']

   file.write("""
<form name="hiddenreportparms1" METHOD="post" ACTION="icormain.asp?jobtype=reportsubmit&OID=%d&ReportOID=%d&RandomValue=%d">
<INPUT type="hidden" id=mdqueryoid name=mdqueryoid value="">
</FORM>

<SCRIPT LANGUAGE="JScript">
<!--
function callbackfunction(text) {
   document.getElementById("mdqueryoid").value=text;
   document.getElementById("hiddenreportparms1").submit()
}

function processKeywords() {
   var i,s;
   document.getElementById("keywordslinks1").innerText="";
   s="";
   for (i=0;i<document.getElementById("keywordselection1").options.length;i++) {
      s=s+document.getElementById("keywordselection1").options(i).value+"<br>";
   }
   document.getElementById("keywordslinks1").innerText=s;
}
-->
</SCRIPT>
"""%(amenu.oid,amenu.Reports.OID,random.randint(1,10000000)))
   w,i=0,1
   catdict={}

   atree=SimpleLinksHTMLTree('Dostępne zestawienia')
   ret=0
   aobj=aclass.GetFirstObject()
   while aobj:
      qrefs=aclass.Query.GetRefList(aobj.OID)
      while qrefs:
         ret=ret+DoProcessQuery2(qrefs.Class,qrefs.OID,amenu,file,catdict,atree.RootNode)
         qrefs.Next()
      aobj.Next()
   atree.Write(file)
   file.write('<hr><i>Ilość dostępnych zestawień: %d</i>'%(ret,))
   return

   file.write('<UL>Dostępne zestawienia<BR>\n')
   ret=0
   aobj=aclass.GetFirstObject()
   while aobj:
      qrefs=aclass.Query.GetRefList(aobj.OID)
      while qrefs:
         ret=ret+DoProcessQuery(qrefs.Class,qrefs.OID,amenu,file,catdict)
         qrefs.Next()
      aobj.Next()
   file.write('</UL>\n')
   file.write('<hr><i>Ilość dostępnych zestawień: %d</i>'%(ret,))
   return

   file.write('<hr>')
   knames=catdict.keys()
   knames.sort()
   file.write('<select name=keywordselection1 multiple size=20>')
   for aname in knames:
      file.write('<option value="%s">%s</td>'%(aname,aname))
   file.write('</select>')
   file.write('<button class="fg-button-single ui-state-default ui-corner-all uihover" onclick="processKeywords();">Znajdź zestawienia</button>')
   file.write('<div id=keywordslinks1 name=keywordslinks1></div>')

def QueryDefDimensionFunc(aclass,aoid,anode,alevel=0):
   aref='icormain.asp?jobtype=objectedit&CID=%d&OID=%d'%(aclass.CID,aoid)
   bnode=anode.AddNode(aclass.Name[aoid],aref,aexpanded=alevel<2)
   aclass.SubDimensions.ForEachRefObject(QueryDefDimensionFunc,aoid,bnode,alevel+1)

def DoQueryStructSubmit(amenu,areport,file):
   aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_Query_MultiDimension_QueryStruct']
   qclass=aclass.Query.ClassOfType
   fnamemodifier=areport.get('FileNameModifier','')
   if fnamemodifier:
      sl=string.split(fnamemodifier,'_')
      fnamemodifier=sl[0]
   zoid=int(areport.get('mdqueryoid','-1'))
   print 'fnamemodifier',fnamemodifier
   if fnamemodifier=='':
      fsize=qclass.OutputFileSize.ValuesAsInt(zoid)
      if fsize>0:
         adt=qclass.LastGenerated.ValuesAsDateTime(zoid)
#         infostr=' (<small><i>%s, %s</i></small>)'%(CLASSES_Library_ICORBase_Interface_ICORUtil.tdatetime2fmtstr(adt),CLASSES_Library_ICORBase_Interface_ICORUtil.GetKBSize(fsize))
         infostr='Stan na dzień: <i>%s</i>, rozmiar zestawienia: <i>%s</i><br><br>'%(CLASSES_Library_ICORBase_Interface_ICORUtil.tdatetime2fmtstr(adt),CLASSES_Library_ICORBase_Interface_ICORUtil.GetKBSize(fsize))
      else:
         infostr=''
      qname=qclass.Name[zoid]
      qcaption=qclass.Caption[zoid]
      if qcaption:
         qfname=qcaption+' '+qname
         qname=qcaption+'<br>'+qname
      else:
         qfname=qname
      qfname=qfname+'.xls'
      file.write("""

<table><tr>
   <td><img src="images/BS00877A.gif" width="50" height="75"></td>
   <td><P class=menuaspagecaption>%s</p></td>
</tr></table>

<form name="hiddenreportparms1" METHOD="post" ACTION="icormain.asp?jobtype=reportsubmit&OID=%d&ReportOID=%d&RandomValue=%d">
<INPUT type="hidden" id=mdqueryoid name=mdqueryoid value="%d">
<INPUT TYPE=HIDDEN NAME=FileNameModifier ID=FileNameModifier VALUE="">
<INPUT TYPE=HIDDEN NAME=UseLoggedCached ID=UseLoggedCached VALUE="1">
<INPUT TYPE=HIDDEN NAME=noscripttags ID=noscripttags VALUE="1" CHECKED>
<INPUT TYPE=HIDDEN NAME=nobodytags ID=noscripttags VALUE="1" CHECKED>
<INPUT TYPE=HIDDEN NAME=MIMEClass ID=MIMEClass VALUE="">
<INPUT TYPE=HIDDEN NAME=MIMEExcel ID=MIMEExcel VALUE=1 CHECKED><!--Pokaż zestawienie w formacie MS Excel 2000.<BR>-->
<INPUT TYPE=HIDDEN NAME=MIMEContentFileName ID=MIMEContentFileName VALUE="%s">
<!--
<INPUT class=checkradio TYPE=CHECKBOX NAME=OpenInNewWindow ID=OpenInNewWindow VALUE=1>Pokaż zestawienie w nowym oknie.<BR>
-->
<!-- <INPUT TYPE=HIDDEN NAME=UseCached ID=UseCached1 VALUE="0"> Wygeneruj zestawienie na podstawie aktualnych danych z FK (może być czasochłonne)<BR> -->
<INPUT TYPE=HIDDEN NAME=UseCached ID=UseCached2 VALUE="1" CHECKED> <!--Pokaż ostatnio generowane zestawienie <BR> -->
%s
<INPUT class=checkradio TYPE=CHECKBOX NAME=DoSaveReport ID=DoSaveReport VALUE=1>Nagraj zestawienie na swój dysk<BR>
</FORM>

<!--
<p><font color="brown"><i>
Uwaga - generowanie nowego zestawienia może być czasochłonne.
</i></font></p>
<P>
<FONT color="red">Uwaga:</FONT><BR>
Pamiętaj, że na końcu nazwy pliku, który nagrywasz na swój dysk, musisz dopisać rozszerzenie <i>xls</i>, np. <i>raport1.xls</i>
</P>
-->

<BUTTON class="fg-button-single ui-state-default ui-corner-all uihover" onclick="javascript:callbackfunction('mdquery');">
Uruchom
</BUTTON>

<P>
Kliknij na poniższy przycisk aby zobaczyć, kto ostatnio oglądał to zestawienie.
</P>
<BUTTON class="fg-button-single ui-state-default ui-corner-all uihover" onclick="javascript:document.getElementById("UseCached").checked=false;document.getElementById("MIMEExcel").checked=false;callbackfunction('lastusers');">
Pokaż
</BUTTON>

<SCRIPT LANGUAGE="JScript"><!--

document.getElementById("UseCached2").checked=true;

function callbackfunction(text) {
   if ((text!="lastusers") && (document.getElementById("DoSaveReport").checked)) {
      text="mdquerySave";
   }
   if (text=="mdquerySave") {
      document.getElementById("MIMEClass").value="application/save";
      text="mdquery";
   } else {
      document.getElementById("MIMEClass").value="";
   }
   if (text=="mdquery") {
      document.getElementById("MIMEExcel").value="1";
      document.getElementById("noscripttags").value="1";
      document.getElementById("nobodytags").value="1";
      text="mdqueryExcel";
   }
   document.getElementById("UseCached2").value="1";
   if (text=="lastusers") {
      document.getElementById("UseCached2").value="0";
      document.getElementById("MIMEClass").value="";
      document.getElementById("MIMEExcel").value="0";
      document.getElementById("noscripttags").value="0";
      document.getElementById("nobodytags").value="0";
   }
   document.getElementById("FileNameModifier").value=text+"_"+document.getElementById("mdqueryoid").value;
   document.getElementById("hiddenreportparms1").submit()
}
--></SCRIPT>
"""%(qname,amenu.oid,amenu.Reports.OID,random.randint(1,10000000),zoid,qfname,infostr))

#      aref='icormain.asp?jobtype=objectedit&CID=%d&OID=%d'%(qclass.CID,zoid)
#      atree=SimpleLinksHTMLTree('Definicja zestawienia',aref)
#      qclass.Dimensions.ForEachRefObject(QueryDefDimensionFunc,zoid,atree.RootNode)
#      atree.Write(file)

   elif fnamemodifier=='lastusers':
      file.write('<table><tr><td><img src="images/investigating.png"></td><td><h3>Użytkownicy ostatnio przeglądający zestawienie:</h3></td></tr></table>')
      qname=qclass.Name[zoid]
      qcaption=qclass.Caption[zoid]
      if qcaption:
         qname=qcaption+'<br>'+qname
      file.write('<P class=menuaspagecaption>%s</p>'%(qname))
      aobj=qclass[zoid]
      uobj=aobj.UserLogInfo
      file.write('<table cellspacing="4">')
      uobj.Last()
      while uobj:
         file.write('<tr><td><font size="-2">%s</font></td><td><font size="-2" color="navy">%s</font></td></tr>\n'%(uobj.Date,uobj.UserName))
         uobj.Prev()
      file.write('</table>')
   elif fnamemodifier in ['mdquery','mdqueryExcel']:
      if zoid<0:
         if file:
            file.write('<h1>Zestawienie nie istnieje!</h1>')
      else:
         uclass=qclass.UserLogInfo.ClassOfType
         uoid=uclass.AddObject()
         uclass.UserName[uoid]=aICORDBEngine.User.UserName[amenu.uid]
         adt=CLASSES_Library_ICORBase_Interface_ICORUtil.tdatetime()
         uclass.Date.SetValuesAsDateTime(uoid,adt)
         qclass.UserLogInfo.AddRefs(zoid,[uoid,uclass.CID])
         mimeexcel=areport.get('MIMEExcel','0')
         atype=mdqt_HTML
         if mimeexcel=='1':
            atype=mdqt_Excel
         if file:
            print 'generate query:',zoid,mimeexcel
            GenerateMDQuery(file,zoid,atype)
         else:
            print 'empty file - get from cache'



