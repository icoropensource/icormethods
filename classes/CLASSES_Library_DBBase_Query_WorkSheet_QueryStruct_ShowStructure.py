# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORSecurity import *
from CLASSES_Library_NetBase_WWW_HTML_Tree_SimpleLinks_Main import SimpleLinksHTMLTree
from CLASSES_Library_DBBase_Query_WorkSheet_Main_ICORWorksheetQuery import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import random
import re

def DoProcessQuery2(aclass,aoid,amenu,file,anode,alevel=0):
   arefs=aclass.AccessLevel.GetRefList(aoid)
   w1=CheckAccessLevelForUser(arefs,amenu.uid)
   if not w1:
      return
   sn=aclass.TableID[aoid]+' - '+aclass.TableTitle[aoid]
#   if aclass.Columns[aoid]=='':
#      sh=''
#   else:
   sh='javascript:callbackfunction(\'%d\')'%(aoid)
   bnode=anode.AddNode(sn,sh,aexpanded=1,asorted=0)
   qrefs=aclass.SubQuery.GetRefList(aoid)
   while qrefs:
      DoProcessQuery2(qrefs.Class,qrefs.OID,amenu,file,bnode,alevel+1)
      qrefs.Next()
   return

def DoShowStructure(amenu,file):
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

   atree=SimpleLinksHTMLTree('Dostępne zestawienia')
   aobj=aclass.GetFirstObject()
   while aobj:
      qrefs=aclass.Query.GetRefList(aobj.OID)
      while qrefs:
         DoProcessQuery2(qrefs.Class,qrefs.OID,amenu,file,atree.RootNode)
         qrefs.Next()
      aobj.Next()
   atree.Write(file)

def ProcessSubmitMain(amenu,areport,file,aclass,qclass,zoid,aworksheet):
   if aworksheet is None:
      file.write('<h1>Brak wybranego zestawienia</h1>')
      return
   file.write('<table>')
   file.write('<tr VALIGN=top class=objectseditrow><td class=objectseditdatafieldname>Tytuł:</td><td class="objectseditdatafieldvalue">%s</td></tr>'%aworksheet.TableTitle)
   file.write('<tr VALIGN=top class=objectseditrow><td class=objectseditdatafieldname>Identyfikator:</td><td class="objectseditdatafieldvalue">%s</td></tr>'%aworksheet.TableID)
   file.write('<tr VALIGN=top class=objectseditrow><td class=objectseditdatafieldname>Autor:</td><td class="objectseditdatafieldvalue">%s</td></tr>'%aworksheet.TableAuthor)
   file.write('<tr VALIGN=top class=objectseditrow><td class=objectseditdatafieldname>Opis:</td><td class="objectseditdatafieldvalue">%s</td></tr>'%aworksheet.TableDescription)
   if aworksheet.LastCalculation!=ICORUtil.ZERO_DATE:
      file.write('<tr VALIGN=top class=objectseditrow><td class=objectseditdatafieldname>Ostatnie przeliczenie:</td><td class="objectseditdatafieldvalue">%s</td></tr>'%ICORUtil.tdatetime2fmtstr(aworksheet.LastCalculation))
   file.write('</table>')
   file.write('<ul>')
   aparms={'FileNameModifier':'showashtml_'+str(zoid),'wsqueryoid':str(zoid)}
   aref=amenu.GetMenuRef(asubmit=1,aparms=aparms)
   file.write('<li><a class=reflistoutnavy href="%s">Zestawienie w postaci HTML</a></li>'%aref)
   aparms['FileNameModifier']='showasmsowc_'+str(zoid)
   aref=amenu.GetMenuRef(asubmit=1,aparms=aparms)
   file.write('<li><a class=reflistoutnavy href="%s">Zestawienie w postaci MS Office Windows Control</a></li>'%aref)
   aparms['FileNameModifier']='showasmsowcinfo_'+str(zoid)
   aref=amenu.GetMenuRef(asubmit=1,aparms=aparms)
   file.write('<li><a class=reflistoutnavy href="%s">Parametry zestawienia w postaci MS Office Windows Control</a></li>'%aref)
   file.write('</ul>')

def ProcessShowAsHTML(amenu,areport,file,aclass,qclass,zoid,aworksheet):
   if aworksheet is None:
      file.write('<h1>Brak wybranego zestawienia</h1>')
      return
   aworksheet.DumpHTML(file)
   aparms={'FileNameModifier':'','wsqueryoid':str(zoid)}
   aref=amenu.GetMenuRef(asubmit=1,aparms=aparms)
   file.write('<br><a class=reflistoutnavy href="%s">Powrót do parametrów zestawienia</a>'%aref)

def ProcessShowAsMSOWC(amenu,areport,file,aclass,qclass,zoid,aworksheet):
   if aworksheet is None:
      file.write('<h1>Brak wybranego zestawienia</h1>')
      return
   aparms={'FileNameModifier':'getwquerydatahtml_'+str(zoid),'wsqueryoid':str(zoid)}
   dref=amenu.GetMenuRef(asubmit=1,aparms=aparms)
   file.write("""
<OBJECT classid=clsid:0002E559-0000-0000-C000-000000000046 id=Spreadsheet1 style="width=100%%;height=85%%;"></OBJECT>

<script language="vbscript">
<!--
Sub Window_onLoad()
   Spreadsheet1.Cells.Clear
   Spreadsheet1.TitleBar.Caption = "%(title)s"
   Spreadsheet1.DataType = "HTMLURL"
   Spreadsheet1.HTMLURL = "%(dref)s"
   Spreadsheet1.Refresh
   Spreadsheet1.ActiveSheet.UsedRange.AutoFitColumns
   Spreadsheet1.Range("A1").Select
End Sub
-->
</script>
<br>
"""%{'dref':dref,'title':aworksheet.TableTitle})
   aparms={'FileNameModifier':'_','wsqueryoid':str(zoid)}
   aref=amenu.GetMenuRef(asubmit=1,aparms=aparms)
   file.write('<br><a class="reflistoutnavy" href="%s">Powrót do parametrów zestawienia</a>'%aref)

def ProcessGetMSOWCHTMLData(amenu,areport,file,aclass,qclass,zoid,aworksheet):
   if aworksheet is None:
      file.write('<h1>Brak wybranego zestawienia</h1>')
      return
   aworksheet.DumpHTML(file)

def ProcessShowAsMSOWCInfo(amenu,areport,file,aclass,qclass,zoid,aworksheet):
   if aworksheet is None:
      file.write('<h1>Brak wybranego zestawienia</h1>')
      return
   aparms={'FileNameModifier':'getwquerydatahtmlinfo_'+str(zoid),'wsqueryoid':str(zoid)}
   dref=amenu.GetMenuRef(asubmit=1,aparms=aparms)
   aparms={'FileNameModifier':'storewsquerydata_'+str(zoid),'wsqueryoid':str(zoid)}
   sref=amenu.GetMenuRef(asubmit=1,aparms=aparms)
   file.write("""
<OBJECT classid=clsid:0002E559-0000-0000-C000-000000000046 id=Spreadsheet1 style="width=100%%;height=85%%;"></OBJECT>

<script language="vbscript">
<!--
Sub Window_onLoad()
   Spreadsheet1.Cells.Clear
   Spreadsheet1.TitleBar.Caption = "%(title)s"
   Spreadsheet1.DataType = "HTMLURL"
   Spreadsheet1.HTMLURL = "%(dref)s"
   Spreadsheet1.Refresh
   Spreadsheet1.Range("A1").Select
End Sub
-->
</script>
<br>
<form name="hiddenreportparms1" METHOD="post" ACTION="%(sref)s">
<INPUT type="hidden" id=wsquerydata name=wsquerydata value="">
</FORM>
<script language="jscript">
<!--
function doWSQuerySubmit() {
   var i,j,mrow,mcol;
   var s="";
   mcol=-1;
   for (i=1;i<250;i++) {
      if (Spreadsheet1.Cells(1,i).Text=="#!TABLECOLUMNEND") {
         mcol=i;
         break;
      }
   }
   if (mcol<0) {
      alert("Tabela nie posiada zaznaczonej ostatniej kolumny.");
      return;
   }
   mrow=-1;
   for (i=1;i<250;i++) {
      if (Spreadsheet1.Cells(i,1).Text=="#!TABLEEND") {
         mrow=i;
         break;
      }
   }
   if (mrow<0) {
      alert("Tabela nie posiada zaznaczonego ostatniego wiersza.");
      return;
   }

   for (i=1;i<=mrow;i++) {
      for (j=1;j<=mcol;j++) {
         s=s+Spreadsheet1.Cells(i,j).Text+'#!_COLUMN';
      }
      s=s+'#!_ROW';
   }
   document.getElementById("wsquerydata").value=s;
   document.getElementById("hiddenreportparms1").submit();
}
-->
</script>

"""%{'dref':dref,'title':aworksheet.TableID,'sref':sref})
   file.write('<br><a class="reflistoutnavy" href="javascript:void(doWSQuerySubmit());">Zapamiętaj zmiany w zestawieniu</a>')
   aparms={'FileNameModifier':'_','wsqueryoid':str(zoid)}
   aref=amenu.GetMenuRef(asubmit=1,aparms=aparms)
   file.write('<br><a class="reflistoutnavy" href="%s">Powrót do parametrów zestawienia</a>'%aref)
   file.write('<hr><PRE>%s</PRE>'%aworksheet.StatusCalculateAsString())

def ProcessGetMSOWCHTMLInfo(amenu,areport,file,aclass,qclass,zoid,aworksheet):
   if aworksheet is None:
      file.write('<h1>Brak wybranego zestawienia</h1>')
      return
   file.write('<table border=1>')
   for arow in range(1,aworksheet.MaxRow+1):
      file.write('<tr height=55>')
      for acol in range(1,aworksheet.MaxCol+1):
         acell=aworksheet[acol,arow]
         if not acell is None:
            file.write('<td width=134>%s</td>'%acell.Formula)
         else:
            file.write('<td width=134></td>')
      if arow==1:
         file.write('<td width=134>#!TABLECOLUMNEND</td>')
      else:
         file.write('<td width=134></td>')
      file.write('</tr>')
   file.write('<tr height=55 >')
   file.write('<td width=134>#!TABLEEND</td>')
   for acol in range(1,aworksheet.MaxCol):
      file.write('<td width=134></td>')
   file.write('</tr>')
   file.write('</table>')

def ProcessStoreWSQueryData(amenu,areport,file,aclass,qclass,zoid,aworksheet):
   if aworksheet is None:
      file.write('<h1>Brak wybranego zestawienia</h1>')
      return
   atext=areport['wsquerydata','']
   atable=[]
   sl=string.split(atext,'#!_ROW')
   for srow in sl:
      sr=string.split(srow,'#!_COLUMN')
      if sr:
         atable.append(sr)
         if sr[0]=='#!TABLEEND':
            break
   w=0
   if atable and atable[0]:
      patt=re.compile('\#\!TABLEID\(\"(.+?)\"\)',re.I)
      m=patt.search(atable[0][0])
      if m:
         w=1
         atableid=m.group(1)
      else:
         astatus='Tabela nie posiada swojego identyfikatora'
   if w:
      arow,acol,maxcol=0,0,0
      astatus=''
      while 1:
         s=atable[arow][maxcol]
         if s=='#!TABLECOLUMNEND':
            break
         if maxcol>=250:
            astatus='Tabela nie posiada ostatniej kolumny (#!TABLECOLUMNEND).'
            w=0
            break
         maxcol=maxcol+1
   if w:
      aworksheet.Clear()
      aworksheet.SetID('')
      ioid=aworksheet.ClassItem.TableID.Identifiers(atableid)
      if ioid>=0:
         w=0
         astatus='Tabela o podanym identyfikatorze już istnieje'
   if w:
      while 1:
         if atable[arow][0]=='#!TABLEEND':
            break
         if arow>2499:
            astatus='tabela posiada ponad 2500 wierszy!'
            w=0
            break
         for i in range(maxcol):
            s=atable[arow][i]
            if s:
#               print 'CELL[%2d,%2d]=>%s<'%(i+1,arow+1,s)
               acell=aworksheet.GetCell(i+1,arow+1)
               acell.SetFormula(s)
         arow=arow+1
   if w:
      aworksheet.Calculate()
      file.write('<h1>Dane zostały poprawnie zapamiętane</h1>')
      file.write('<hr><PRE>%s</PRE>'%aworksheet.StatusCalculateAsString())
   else:
      file.write('<font color="red"><h1>%s</h1></font>'%astatus)
      file.write('<h1>Dane nie zostały poprawnie zapamiętane</h1>')
   aparms={'FileNameModifier':'_','wsqueryoid':str(zoid)}
   aref=amenu.GetMenuRef(asubmit=1,aparms=aparms)
   file.write('<br><a class="reflistoutnavy" href="%s">Powrót do parametrów zestawienia</a>'%aref)
   aWorksheetQueries.Refresh()

def DoShowStructureSubmit(amenu,areport,file):
   aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_Query_WorkSheet_QueryStruct']
   qclass=aclass.Query.ClassOfType
   fnamemodifier=areport['FileNameModifier','']
   aoid=int(areport.get('wsqueryoid','-1'))
   aworksheet=aWorksheetQueries[aoid]
   if fnamemodifier:
      sl=string.split(fnamemodifier,'_')
      fnamemodifier=sl[0]
   if fnamemodifier=='':
      ProcessSubmitMain(amenu,areport,file,aclass,qclass,aoid,aworksheet)
   elif fnamemodifier=='showashtml':
      ProcessShowAsHTML(amenu,areport,file,aclass,qclass,aoid,aworksheet)
   elif fnamemodifier=='showasmsowc':
      ProcessShowAsMSOWC(amenu,areport,file,aclass,qclass,aoid,aworksheet)
   elif fnamemodifier=='getwquerydatahtml':
      ProcessGetMSOWCHTMLData(amenu,areport,file,aclass,qclass,aoid,aworksheet)
   elif fnamemodifier=='showasmsowcinfo':
      ProcessShowAsMSOWCInfo(amenu,areport,file,aclass,qclass,aoid,aworksheet)
   elif fnamemodifier=='getwquerydatahtmlinfo':
      ProcessGetMSOWCHTMLInfo(amenu,areport,file,aclass,qclass,aoid,aworksheet)
   elif fnamemodifier=='storewsquerydata':
      ProcessStoreWSQueryData(amenu,areport,file,aclass,qclass,aoid,aworksheet)



