# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORMDSpace import *
from CLASSES_Library_NetBase_Utils_XMLUtil import GetAsXMLString,GetAsXMLStringNoPL
import types
import string

class ICORMDSpace2HTML(ICORMDSpaceTableIterator):
   def __init__(self,aspace,afile,apage=1,apagetitle='Test',acssfile='icor.css',acsstitle='SOI',askiplastcolumns=0):
      ICORMDSpaceTableIterator.__init__(self,aspace,askiplastcolumns=askiplastcolumns)
      if isinstance(afile,types.StringTypes):
         self.fclose=1
         self.file=open(afile,'wb')
      else:
         self.fclose=0
         self.file=afile
      self.Page=apage
      self.PageTitle=apagetitle
      self.CSSFile=acssfile
      self.CSSTitle=acsstitle
   def __del__(self):
      if self.fclose:
         self.file.close()
   def OnStartPage(self):
      if self.Page:
         self.file.write("""<html>
<head>
<link rel=STYLESHEET type="text/css" href="%s" title="%s">
<meta http-equiv="Content-Type" content="text/html; charset=windows-1250">
<title>%s</title>
<body>
""" % (self.CSSFile,self.CSSTitle,self.PageTitle))
   def OnEndPage(self):
      if self.Page:
         self.file.write('</body></html>\n')
   def OnStart(self,acaption=''):
      self.file.write('<table class=objectsviewtable>\n')
      if acaption!='':
         self.file.write('<caption class=objectsviewcaption>%s</caption>' % (acaption))
   def OnEnd(self):
      self.file.write('</table>\n')
   def OnHeader(self,acol,avalue):
      self.file.write('<TH class=objectsviewheader>'+avalue+'</TH>')
   def OnStartFooter(self):
      self.file.write('<TFOOT><TR>')
   def OnFooter(self,acol,avalue):
      if avalue is None:
         self.file.write('<TD class=objectsviewfooter>&nbsp;</TD>')
         return
      if not isinstance(avalue,types.StringTypes):
         avalue=str(avalue)
      self.file.write('<TD class=objectsviewfooter>'+avalue+'</TD>')
   def OnEndFooter(self):
      self.file.write('</TR></TFOOT>')
   def OnStartRow(self,arow):
      self.file.write('<TR class=objectsviewrow>\n')
   def OnEndRow(self,arow):
      self.file.write('</TR>\n')
   def OnStartCol(self,arow,acol):
      if self.IsOdd:
#         self.file.write('<TD class=objectsviewdataodd NOWRAP>')
         self.file.write('<TD class=objectsviewdataodd>')
      else:
#         self.file.write('<TD class=objectsviewdataeven NOWRAP>')
         self.file.write('<TD class=objectsviewdataeven>')
   def OnEndCol(self,arow,acol):
      self.file.write('</TD>\n')

class ICORMDSpace2HTMLSimple(ICORMDSpaceTableIterator):
   def __init__(self,aspace,afile,apage=1,apagetitle='Test',askiplastcolumns=0,asorted=0,aid=0):
      ICORMDSpaceTableIterator.__init__(self,aspace,askiplastcolumns=askiplastcolumns)
      if isinstance(afile,types.StringTypes):
         self.fclose=1
         self.file=open(afile,'wb')
      else:
         self.fclose=0
         self.file=afile
      self.Page=apage
      self.PageTitle=apagetitle
      self.Sorted=asorted
      self.ID=aid
   def __del__(self):
      if self.fclose:
         self.file.close()
   def OnStartPage(self):
      if self.Page:
         self.file.write("""<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=windows-1250">
<title>%s</title>
<body>
""" % (self.PageTitle,))
   def OnEndPage(self):
      if self.Page:
         self.file.write('</body></html>\n')
   def OnStart(self,acaption=''):
      if self.Sorted or 1:
         if acaption!='':
            #self.file.write('<span><font size="-3">%s</font></span>' % (acaption))
            self.file.write('<div class="ui-widget-header">%s</div>' % (acaption))
         if 0:
            self.file.write('<table class="sort-table" cellspacing=0 id="sortedTable%d">\n'%self.ID)
         else:
            self.file.write('<table id="sortedTable%d">\n'%self.ID)
      else:
         if acaption!='':
            self.file.write('<caption><font size="-3">%s</font></caption>' % (acaption))
         self.file.write('<table id="sortedTable%d">\n'%self.ID)
   def OnEnd(self):
      self.file.write('</table>\n')
      if 0:
         if self.Sorted:
            self.WriteSortCall()
      else:
         self.WriteSortCall()
   def OnStartHeader(self):
      if self.Sorted or 1:
         self.file.write('<THEAD><TR>')
   def OnHeader(self,acol,avalue):
      if self.Sorted or 1:
         if 0:
            self.file.write('<TD>'+avalue+'</TD>')
         else:
            self.file.write('<th>'+avalue+'</th>')
      else:
         if 0:
            self.file.write('<TH><font size="-3">'+avalue+'</font></TH>')
         else:
            self.file.write('<th>'+avalue+'</th>')
   def OnEndHeader(self):
      if self.Sorted or 1:
         self.file.write('</TR></THEAD>')
   def OnStartFooter(self):
      if 0:
         self.file.write('<TFOOT><TR>')
   def OnFooter(self,acol,avalue):
      if 0:
         if avalue is None:
            self.file.write('<TD><font size="-3">&nbsp;</font></TD>')
            return
         if not isinstance(avalue,types.StringTypes):
            avalue=str(avalue)
         self.file.write('<TD><font size="-3">'+avalue+'</font></TD>')
   def OnEndFooter(self):
      if 0:
         self.file.write('</TR></TFOOT>')
   def OnStartBody(self):
      if self.Sorted or 1:
         self.file.write('<TBODY>')
   def OnEndBody(self):
      if self.Sorted or 1:
         self.file.write('</TBODY>')
   def OnStartRow(self,arow):
      self.file.write('<TR>\n')
   def OnEndRow(self,arow):
      self.file.write('</TR>\n')
   def OnStartCol(self,arow,acol):
      if 0:
         self.file.write('<TD><font size="-3">')
      else:
         self.file.write('<TD>')
   def OnEndCol(self,arow,acol):
      if 0:
         self.file.write('</font></TD>\n')
      else:
         self.file.write('</TD>\n')
   def WriteSortCall(self):
      d={'ID':str(self.ID)}
      if 0:
         self.file.write("""
<script type="text/javascript">
function addClassName%(ID)s(el, sClassName) {
   var s = el.className;
   var p = s.split(" ");
   var l = p.length;
   for (var i = 0; i < l; i++) {
      if (p[i] == sClassName)
         return;
   }
   p[p.length] = sClassName;
   el.className = p.join(" ");
}

function removeClassName%(ID)s(el, sClassName) {
   var s = el.className;
   var p = s.split(" ");
   var np = [];
   var l = p.length;
   var j = 0;
   for (var i = 0; i < l; i++) {
      if (p[i] != sClassName)
         np[j++] = p[i];
   }
   el.className = np.join(" ");
}
var astvar%(ID)s = new SortableTable(document.getElementById("sortedTable%(ID)s") ); //[]
astvar%(ID)s.onsort = function () {
   var rows = astvar%(ID)s.tBody.rows;
   var l = rows.length;
   for (var i = 0; i < l; i++) {
      removeClassName%(ID)s(rows[i], i %% 2 ? "sort-row-odd" : "sort-row-even");
      addClassName%(ID)s(rows[i], i %% 2 ? "sort-row-even" : "sort-row-odd");
   }
};
astvar%(ID)s.sort(0,1);
</script>
"""%d)
      else:
         self.file.write("""
<script type='text/javascript'>
jQuery(function (){makeTable('#sortedTable%d');});
</script>
"""%(self.ID,))

class ICORMDSpace2HTMLLinks(ICORMDSpaceTableIterator):
   def __init__(self,aspace,afile,askiplastcolumns=0):
      ICORMDSpaceTableIterator.__init__(self,aspace,askiplastcolumns=askiplastcolumns)
      if isinstance(afile,types.StringTypes):
         self.fclose=1
         self.file=open(afile,'wb')
      else:
         self.fclose=0
         self.file=afile
      self.Links=[]
      self.Caption=''
   def __del__(self):
      if self.fclose:
         self.file.close()
   def OnStart(self,acaption=''):
      self.Caption=acaption

class ICORMDSpace2CSV(ICORMDSpaceTableIterator):
   def __init__(self,aspace,afile,adefcolumns=0,adeftypes=0,aheaderfile=0):
      ICORMDSpaceTableIterator.__init__(self,aspace)
      self.HeaderFile=aheaderfile
      if isinstance(afile,types.StringTypes):
         self.fclose=1
         self.file=open(afile,'wb')
         if aheaderfile:
            self.headerfile=open(afile+'h','wb')
      else:
         self.fclose=0
         self.file=afile
      self.DefaultColumns=adefcolumns
      self.DefaultTypes=adeftypes
      self.HeaderTypes={}
      self.FieldDelimiter=','
   def __del__(self):
      if self.fclose:
         self.file.close()
      if self.HeaderFile:
         self.headerfile.close()
   def GetCSVValue(self,astr):
      if string.find(astr,'"')>=0:
         astr=string.replace(astr,'"',"'")
         w=1
      else:
         w=0
      if w or string.find(astr,' ')>=0 or string.find(astr,self.FieldDelimiter)>=0:
         astr='"'+astr+'"'
      return astr
   def OnStartHeader(self):
      self.IsComma=0
   def OnHeader(self,acol,avalue):
      if self.IsComma:
         s=self.FieldDelimiter
         sh=chr(254)
      else:
         s=''
         sh=''
      if self.DefaultColumns:
         s=s+'Column%d'%(acol+1)
      else:
         s=s+avalue
      if self.DefaultTypes:
         s=s+':'+self.HeaderTypes.get(acol,'STRING')
      self.file.write(s)
      if self.HeaderFile:
         sh=sh+avalue
         self.headerfile.write(sh)
      self.IsComma=1
   def OnEndHeader(self):
      self.IsComma=0
      self.file.write('\n')
      if self.HeaderFile:
         self.headerfile.write('\n')
   def OnStartCol(self,arow,acol):
      if self.IsComma:
         self.file.write(self.FieldDelimiter)
      self.IsComma=1
   def OnEndRow(self,arow):
      self.IsComma=0
      self.file.write('\n')

class ICORMDSpace2XMLDSO(ICORMDSpaceTableIterator):
   def __init__(self,aspace,afile,apage=1,apagetitle='Test',acssfile='icor.css',acsstitle='SOI'):
      ICORMDSpaceTableIterator.__init__(self,aspace)
      if isinstance(afile,types.StringTypes):
         self.fclose=1
         self.file=open(afile,'wb')
      else:
         self.fclose=0
         self.file=afile
      self.Page=apage
      self.PageTitle=apagetitle
      self.CSSFile=acssfile
      self.CSSTitle=acsstitle
      self.Headers=[]
   def __del__(self):
      if self.fclose:
         self.file.close()
   def OnStartPage(self):
      if self.Page:
         self.file.write("""<html>
<head>
<link rel=STYLESHEET type="text/css" href="%s" title="%s">
<meta http-equiv="Content-Type" content="text/html; charset=windows-1250">
<title>%s</title>
<body>
""" % (self.CSSFile,self.CSSTitle,self.PageTitle))
   def OnEndPage(self):
      if self.Page:
         self.file.write('</body></html>\n')
   def OnStart(self,acaption=''):
      self.file.write('\n\n<XML id=xmldso%s><root>\n'%(self.RandomNameModifier,))
#      self.file.write('<table class=objectsviewtable>\n')
#      if acaption!='':
#         self.file.write('<caption class=objectsviewcaption>%s</caption>' % (acaption))
   def OnEnd(self):
      self.file.write('</root>\n</XML>\n\n')
      self.file.write("""
<script language="javascript" defer>
function settablepositioninfo%(SUID)s() {
   var s=sortabletable%(SUID)s;
   debugger;
   alert(tablepositionid%(SUID)s.innerHTML);
}

var lastcolclicked_%(SUID)s="";
var lastsorttype_%(SUID)s=true;

function headerxmltableclick%(SUID)s(acolid) {
   if (lastcolclicked_%(SUID)s!=acolid) {
      lastsorttype_%(SUID)s=true;
      }
   lastsorttype_%(SUID)s=!lastsorttype_%(SUID)s;
   lastcolclicked_%(SUID)s=acolid;
   xmldso3columnssort%(SUID)s("col"+acolid+"s",lastsorttype_%(SUID)s,"",false,"",false);
}
</script>

"""%{'SUID':self.RandomNameModifier})
      self.file.write('<TABLE ID=sortabletable%s DATASRC="#xmldso%s" class=objectsviewtable>\n'%(self.RandomNameModifier,self.RandomNameModifier,))
      if self.space.Caption!='':
         self.file.write('<caption class=objectsviewcaption>\n')
#      self.file.write('<img style="cursor:pointer" onclick="sortabletable%s.firstPage()" src="images/bullet_navy_first_page.png" alt="pierwsza strona"></a>\n'%(self.RandomNameModifier,))
#      self.file.write('<img style="cursor:pointer" onclick="sortabletable%s.previousPage()" src="images/bullet_navy_previous_page.png" alt="poprzednia strona"></a>\n'%(self.RandomNameModifier,))
#      self.file.write('<img style="cursor:pointer" onclick="sortabletable%s.nextPage()" src="images/bullet_navy_next_page.png" alt="następna strona"></a>\n'%(self.RandomNameModifier,))
#      self.file.write('<img style="cursor:pointer" onclick="sortabletable%s.lastPage()" src="images/bullet_navy_last_page.png" alt="ostatnia strona"></a>&nbsp;&nbsp;\n'%(self.RandomNameModifier,))
#      self.file.write('<small><i>strona:&nbsp;<span id=tablepositionid%s>1/2</span>&nbsp;</i></small>' % (self.RandomNameModifier,))
#      self.file.write('<img style="cursor:pointer" onclick=\'if (document.all.setTableRowsCountDiv1_%s.style.display!="") {document.all.setTableRowsCountDiv1_%s.style.display="";}else{document.all.setTableRowsCountDiv1_%s.style.display="none";};\' src="images/bullet_navy_lines.png" alt="ustaw ilość widocznych wierszy">\n'%(self.RandomNameModifier,self.RandomNameModifier,self.RandomNameModifier,))
#      self.file.write('<img style="cursor:pointer" onclick=\'if (document.all.setTableSortDiv1_%s.style.display!="") {document.all.setTableSortDiv1_%s.style.display="";}else{document.all.setTableSortDiv1_%s.style.display="none";};\' src="images/bullet_navy_table_column.png" alt="sortuj w/g">\n'%(self.RandomNameModifier,self.RandomNameModifier,self.RandomNameModifier,))
#      self.file.write('<img style="cursor:pointer" src="images/bullet_navy_lupe_plus.png" alt="filtruj dane">&nbsp;&nbsp;&nbsp;\n')
      if self.space.Caption!='':
         self.file.write('&nbsp;&nbsp;&nbsp;%s</caption>' % (self.space.Caption,))
      self.file.write('<THEAD>\n')
      for i in range(len(self.space.header)):
         self.file.write('<TH onclick="headerxmltableclick%s(\'%d\');" style="cursor=pointer;" class=objectsviewheader>%s</TH>'%(self.RandomNameModifier,i,self.space.header.values[i],))
      self.file.write('</THEAD><TR class=objectsviewrow>\n')
      for i in range(len(self.space.header)):
#         self.file.write('<TD class=objectsviewdataeven NOWRAP><DIV DATAFLD="col%d" DATAFORMATAS=HTML></DIV></TD>'%(i,))
         self.file.write('<TD class=objectsviewdataeven><DIV DATAFLD="col%d" DATAFORMATAS=HTML></DIV></TD>'%(i,))
      self.file.write('</TR></TABLE>\n')
      self.file.write("""
<SCRIPT LANGUAGE=javascript defer>
function aDataPageSizeSelect_%(SUID)s_onchange() {
   var si=document.all.aDataPageSizeSelect_%(SUID)s.selectedIndex;
   sortabletable%(SUID)s.dataPageSize = document.all.aDataPageSizeSelect_%(SUID)s.options(si).value;
   document.all.setTableRowsCountDiv1_%(SUID)s.style.display='none';
}
</SCRIPT>
<DIV ID=setTableRowsCountDiv1_%(SUID)s STYLE="display:none">
<BR>
<TABLE bgcolor="silver" cellspacing=0 cellpadding=0>
<TR>
<TD bgcolor="ACTIVECAPTION"><FONT face="Arial" size="-2" color="white"><b>&nbsp;&nbsp;Ustaw ilość wierszy&nbsp;&nbsp;</b><font></TD>
<TD bgcolor="ACTIVECAPTION"><IMG alt="ukryj" style="cursor:pointer" src="images/caption_button_minimize.gif" onclick="document.all.setTableRowsCountDiv1_%(SUID)s.style.display='none';"></TD>
<TD bgcolor="ACTIVECAPTION"><IMG alt="pokaż" style="cursor:pointer" src="images/caption_button_maximize.gif" onclick="document.all.setTableRowsCountDiv1_%(SUID)s.style.display='';/*document.all.setTableRowsCountDiv1_%(SUID)s.scrollIntoView(0);*/"></TD>
<!-- <TD bgcolor="ACTIVECAPTION"><IMG src="images/caption_button_close.gif"></TD> -->
</TR>
<TR><TD>

<TABLE bgcolor="BUTTONFACE" cellspacing=10>
<TR>
<TD>Ilość&nbsp;wierszy&nbsp;w&nbsp;tabeli:</TD><TD><SELECT ID=aDataPageSizeSelect_%(SUID)s name=aDataPageSizeSelect_%(SUID)s LANGUAGE=javascript onchange="return aDataPageSizeSelect_%(SUID)s_onchange()">
<OPTION value=5>5</OPTION>
<OPTION value=10>10</OPTION>
<OPTION value=15 Selected>15</OPTION>
<OPTION value=20>20</OPTION>
<OPTION value=25>25</OPTION>
<OPTION value=50>50</OPTION>
<OPTION value=75>75</OPTION>
<OPTION value=100>100</OPTION>
<OPTION value=200>200</OPTION>
<OPTION value=500>500</OPTION>
<OPTION value=1000>1000</OPTION>
<OPTION value=0>wszystkie</OPTION>
</SELECT></TD>
</TR></TABLE>

</TD></TR></TABLE>

</DIV>

"""%{'SUID':self.RandomNameModifier})
#************************
      self.file.write("""
<BR>

<SCRIPT LANGUAGE=javascript defer>
function ReplaceChar_%(SUID)s(s,ch,rc) {
   var r="",i;
   for (i=0;i<s.length;i++) {
      c=s.substr(i,1)
      if (c==ch) {
         r=r+rc;
         } else {
         r=r+c;
         }
      }
   return(r);
}
function aFielNameSelect_%(SUID)s_onchange() {
   var sv;
   var va;
   var sf = "";
   
   va=document.all.aFielNameSelect1_%(SUID)s.options(document.all.aFielNameSelect1_%(SUID)s.selectedIndex).value;
   if (va!="-1") {
      va="Column"+va;
      sv=document.all.aFieldValue1_%(SUID)s.value;
      if (sv.indexOf(" ",0)>=0 || sv=="")
         sv='"'+sv+'"';
      if (sf!="")
         sf=sf+" & ";
      sf=sf+va+document.all.aFieldConditionSelect1_%(SUID)s.options(document.all.aFieldConditionSelect1_%(SUID)s.selectedIndex).value+sv;
      }

   va=document.all.aFielNameSelect2_%(SUID)s.options(document.all.aFielNameSelect2_%(SUID)s.selectedIndex).value;
   if (va!="-1") {
      va="Column"+va;
      sv=document.all.aFieldValue2_%(SUID)s.value;
      if (sv.indexOf(" ",0)>=0 || sv=="")
         sv='"'+sv+'"';
      if (sf!="")
         sf=sf+" & ";
      sf=sf+va+document.all.aFieldConditionSelect2_%(SUID)s.options(document.all.aFieldConditionSelect2_%(SUID)s.selectedIndex).value+sv;
      }

   va=document.all.aFielNameSelect3_%(SUID)s.options(document.all.aFielNameSelect3_%(SUID)s.selectedIndex).value;
   if (va!="-1") {
      va="Column"+va;
      sv=document.all.aFieldValue3_%(SUID)s.value;
      if (sv.indexOf(" ",0)>=0 || sv=="")
         sv='"'+sv+'"';
      if (sf!="")
         sf=sf+" & ";
      sf=sf+va+document.all.aFieldConditionSelect3_%(SUID)s.options(document.all.aFieldConditionSelect3_%(SUID)s.selectedIndex).value+sv;
      }

   va=document.all.aFielNameSelect4_%(SUID)s.options(document.all.aFielNameSelect4_%(SUID)s.selectedIndex).value;
   if (va!="-1") {
      va="Column"+va;
      sv=document.all.aFieldValue4_%(SUID)s.value;
      if (sv.indexOf(" ",0)>=0 || sv=="")
         sv='"'+sv+'"';
      if (sf!="")
         sf=sf+" & ";
      sf=sf+va+document.all.aFieldConditionSelect4_%(SUID)s.options(document.all.aFieldConditionSelect4_%(SUID)s.selectedIndex).value+sv;
      }

   va=document.all.aFielNameSelect5_%(SUID)s.options(document.all.aFielNameSelect5_%(SUID)s.selectedIndex).value;
   if (va!="-1") {
      va="Column"+va;
      sv=document.all.aFieldValue5_%(SUID)s.value;
      if (sv.indexOf(" ",0)>=0 || sv=="")
         sv='"'+sv+'"';
      if (sf!="")
         sf=sf+" & ";
      sf=sf+va+document.all.aFieldConditionSelect5_%(SUID)s.options(document.all.aFieldConditionSelect5_%(SUID)s.selectedIndex).value+sv;
      }
   xmldso%(SUID)s.recordset.Filter = sf;
   xmldso%(SUID)s.recordset.Reset();
   document.all.setTableFilterDiv1_%(SUID)s.style.display='none';
}
function aClearAllConditions_%(SUID)s() {
   document.all.aFielNameSelect1_%(SUID)s.selectedIndex=0;
   document.all.aFielNameSelect2_%(SUID)s.selectedIndex=0;
   document.all.aFielNameSelect3_%(SUID)s.selectedIndex=0;
   document.all.aFielNameSelect4_%(SUID)s.selectedIndex=0;
   document.all.aFielNameSelect5_%(SUID)s.selectedIndex=0;
   document.all.aFieldValue1_%(SUID)s.value="";
   document.all.aFieldValue2_%(SUID)s.value="";
   document.all.aFieldValue3_%(SUID)s.value="";
   document.all.aFieldValue4_%(SUID)s.value="";
   document.all.aFieldValue5_%(SUID)s.value="";
   document.all.aFieldConditionSelect1_%(SUID)s.selectedIndex=0;
   document.all.aFieldConditionSelect2_%(SUID)s.selectedIndex=0;
   document.all.aFieldConditionSelect3_%(SUID)s.selectedIndex=0;
   document.all.aFieldConditionSelect4_%(SUID)s.selectedIndex=0;
   document.all.aFieldConditionSelect5_%(SUID)s.selectedIndex=0;
   xmldso%(SUID)s.recordset.Filter = "";
   xmldso%(SUID)s.recordset.Reset();
}
function xmldsocolumnssortfunc%(SUID)s(a,b) {
   var v1=a[0].text;
   var v2=b[0].text;
   var res=0;
   if (v1<v2)
      res=-1;
   if (v1>v2)
      res=1;
   if (a[1])
      res=-res;
   if (res==0 && a[2]) {
      v1=a[2].text;
      v2=b[2].text;
      if (v1<v2)
         res=-1;
      if (v1>v2)
         res=1;
      if (a[3])
         res=-res;
      if (res==0 && a[4]) {
         v1=a[4].text;
         v2=b[4].text;
         if (v1<v2)
            res=-1;
         if (v1>v2)
            res=1;
         if (a[5])
            res=-res;
      }
   }
   return res;
}
</script>
<script LANGUAGE=javascript defer>
function xmldso3columnssort%(SUID)s(acol1,acol1desc,acol2,acol2desc,acol3,acol3desc) {
   var xmld, fc, nc,nc2,nc3, colid1,colid2,colid3, as, ap, i;
   xmld = xmldso%(SUID)s.XMLDocument.documentElement;
   fc = xmld.firstChild;
   colid1=-1;
   colid2=-1;
   colid3=-1;
   if (fc) {
      i=0;
      nc=fc.firstChild;
      while (nc) {
         if (nc.nodeName==acol1)
            colid1=i;
         if (nc.nodeName==acol2)
            colid2=i;
         if (nc.nodeName==acol3)
            colid3=i;
         nc=nc.nextSibling;
         i++;
         }
   }
   if ((colid1<0) && (colid2<0) && (colid3<0))
      return;
   as=new Array()
   i=0;
   while (fc) {          
      nc=false;
      nc2=false;
      nc3=false;
      if (colid1>=0)
         nc=fc.childNodes(colid1);
      if (colid2>=0)
         nc2=fc.childNodes(colid2);
      if (colid3>=0)
         nc3=fc.childNodes(colid3);
      ap=new Array(nc,acol1desc,nc2,acol2desc,nc3,acol3desc);
      as[i]=ap;
      fc=fc.nextSibling;
      i++;
   }
   as.sort(xmldsocolumnssortfunc%(SUID)s);
   for (i in as) {
      xmld.appendChild(as[i][0].parentNode);
   }
}
</script>

<script language="javascript" event="onclick" for="onsortformbuttonxmlchart%(SUID)s" defer>
//function aSortButtonClick_%(SUID)s(){
   var col1,col2,col3,col1sd,col2sd,col3sd;
   
   col1="col"+document.all.aFieldSortSelect1_%(SUID)s.options(document.all.aFieldSortSelect1_%(SUID)s.selectedIndex).value+"s";
   col1sd=document.all.aFieldSortCond1_%(SUID)s.options(document.all.aFieldSortCond1_%(SUID)s.selectedIndex).value=="+";
   col2="col"+document.all.aFieldSortSelect2_%(SUID)s.options(document.all.aFieldSortSelect2_%(SUID)s.selectedIndex).value+"s";
   col2sd=document.all.aFieldSortCond2_%(SUID)s.options(document.all.aFieldSortCond2_%(SUID)s.selectedIndex).value=="+";
   col3="col"+document.all.aFieldSortSelect3_%(SUID)s.options(document.all.aFieldSortSelect3_%(SUID)s.selectedIndex).value+"s";
   col3sd=document.all.aFieldSortCond3_%(SUID)s.options(document.all.aFieldSortCond3_%(SUID)s.selectedIndex).value=="+";
   xmldso3columnssort%(SUID)s(col1,col1sd,col2,col2sd,col3,col3sd);
   document.all.setTableSortDiv1_%(SUID)s.style.display='none';
//}
</script>
<script language="javascript" defer>
function aClearSortClick_%(SUID)s(){
   document.all.aFieldSortSelect1_%(SUID)s.selectedIndex=0;
   document.all.aFieldSortCond1_%(SUID)s.selectedIndex=0;
   document.all.aFieldSortSelect2_%(SUID)s.selectedIndex=0;
   document.all.aFieldSortCond2_%(SUID)s.selectedIndex=0;
   document.all.aFieldSortSelect3_%(SUID)s.selectedIndex=0;
   document.all.aFieldSortCond3_%(SUID)s.selectedIndex=0;
}
</SCRIPT>

<DIV ID=setTableFilterDiv1_%(SUID)s STYLE="display:none">
<TABLE bgcolor="silver" cellspacing=0 cellpadding=0>
<TR>
<TD bgcolor="ACTIVECAPTION"><FONT face="Arial" size="-2" color="white"><b>&nbsp;&nbsp;Parametry filtrowania&nbsp;&nbsp;</b><font></TD>
<TD bgcolor="ACTIVECAPTION"><IMG alt="ukryj" style="cursor:pointer" src="images/caption_button_minimize.gif" onclick="document.all.setTableFilterDiv1_%(SUID)s.style.display='none';"></TD>
<TD bgcolor="ACTIVECAPTION"><IMG alt="pokaż" style="cursor:pointer" src="images/caption_button_maximize.gif" onclick="document.all.setTableFilterDiv1_%(SUID)s.style.display='';/*document.all.setTableFilterDiv1_%(SUID)s.scrollIntoView(0);*/"></TD>
<!-- <TD bgcolor="ACTIVECAPTION"><IMG src="images/caption_button_close.gif"></TD> -->
</TR>
<TR><TD>
<TABLE bgcolor="BUTTONFACE" cellspacing=10>
<TR>
<TD>
Poniżej możesz wybrać warunki, którymi ograniczysz wyświetlane dane. Dla pól tekstowych możesz napisać
na końcu znak '*' aby znaleźć wszystkie wartości rozpoczynające się od wpisanego słowa np. 'b*' uwzględni
tylko 'Biłgoraj','Bydgoszcz' itd. Jeśli chcesz pozbyć się pustych komórek możesz ograniczyć widok stosując
operator '<' np. pole 'Ilość' ma być mniejsze od 100000. Wynika to z faktu, że puste komórki są traktowane podczas
porównań jako większe od dowolnych komórek wypełnionych wartością.
</TD></TR>
<TR>
"""%{'SUID':self.RandomNameModifier})
      self.file.write("""
<TABLE>
<TR><TD>Kolumna:</TD><TD><SELECT ID=aFielNameSelect1_%(SUID)s>
<OPTION SELECTED value="-1">brak warunku</OPTION>
"""%{'SUID':self.RandomNameModifier})
      for i in range(1,len(self.space.header)-2):
         self.file.write('<OPTION value="%d">%s</OPTION>'%(i+1,self.space.header[i]))
      s="""
</SELECT></TD><TD>
<SELECT ID=aFieldConditionSelect1_%(SUID)s>
<OPTION value=" = " SELECTED> = </OPTION><OPTION value=" > "> > </OPTION><OPTION value=" >= "> >= </OPTION><OPTION value=" < "> < </OPTION><OPTION value=" <= "> <= </OPTION><OPTION value=" <> "> <> </OPTION>
</SELECT></TD><TD>
<INPUT ID=aFieldValue1_%(SUID)s TYPE=TEXT VALUE=""></TD></TR>
<TR><TD>Kolumna:</TD><TD><SELECT ID=aFielNameSelect2_%(SUID)s>
<OPTION SELECTED value="-1">brak warunku</OPTION>
"""%{'SUID':self.RandomNameModifier}
      self.file.write(s)
      for i in range(1,len(self.space.header)-2):
         self.file.write('<OPTION value="%d">%s</OPTION>'%(i+1,self.space.header[i]))
      s="""
</SELECT></TD><TD>
<SELECT ID=aFieldConditionSelect2_%(SUID)s>
<OPTION value=" = " SELECTED> = </OPTION><OPTION value=" > "> > </OPTION><OPTION value=" >= "> >= </OPTION><OPTION value=" < "> < </OPTION><OPTION value=" <= "> <= </OPTION><OPTION value=" <> "> <> </OPTION>
</SELECT></TD><TD>
<INPUT ID=aFieldValue2_%(SUID)s TYPE=TEXT VALUE=""></TD></TR>
<TR><TD>Kolumna:</TD><TD><SELECT ID=aFielNameSelect3_%(SUID)s>
<OPTION SELECTED value="-1">brak warunku</OPTION>
"""%{'SUID':self.RandomNameModifier}
      self.file.write(s)
      for i in range(1,len(self.space.header)-2):
         self.file.write('<OPTION value="%d">%s</OPTION>'%(i+1,self.space.header[i]))
      s="""
</SELECT></TD><TD>
<SELECT ID=aFieldConditionSelect3_%(SUID)s>
<OPTION value=" = " SELECTED> = </OPTION><OPTION value=" > "> > </OPTION><OPTION value=" >= "> >= </OPTION><OPTION value=" < "> < </OPTION><OPTION value=" <= "> <= </OPTION><OPTION value=" <> "> <> </OPTION>
</SELECT></TD><TD>
<INPUT ID=aFieldValue3_%(SUID)s TYPE=TEXT VALUE=""></TD></TR>
<TR><TD>Kolumna:</TD><TD><SELECT ID=aFielNameSelect4_%(SUID)s>
<OPTION SELECTED value="-1">brak warunku</OPTION>
"""%{'SUID':self.RandomNameModifier}
      self.file.write(s)
      for i in range(1,len(self.space.header)-2):
         self.file.write('<OPTION value="%d">%s</OPTION>'%(i+1,self.space.header[i]))
      s="""
</SELECT></TD><TD>
<SELECT ID=aFieldConditionSelect4_%(SUID)s>
<OPTION value=" = " SELECTED> = </OPTION><OPTION value=" > "> > </OPTION><OPTION value=" >= "> >= </OPTION><OPTION value=" < "> < </OPTION><OPTION value=" <= "> <= </OPTION><OPTION value=" <> "> <> </OPTION>
</SELECT></TD><TD>
<INPUT ID=aFieldValue4_%(SUID)s TYPE=TEXT VALUE=""></TD></TR>
<TR><TD>Kolumna:</TD><TD><SELECT ID=aFielNameSelect5_%(SUID)s>
<OPTION SELECTED value="-1">brak warunku</OPTION>
"""%{'SUID':self.RandomNameModifier}
      self.file.write(s)
      for i in range(1,len(self.space.header)-2):
         self.file.write('<OPTION value="%d">%s</OPTION>'%(i+1,self.space.header[i]))
      s="""
</SELECT></TD><TD>
<SELECT ID=aFieldConditionSelect5_%(SUID)s>
<OPTION value=" = " SELECTED> = </OPTION><OPTION value=" > "> > </OPTION><OPTION value=" >= "> >= </OPTION><OPTION value=" < "> < </OPTION><OPTION value=" <= "> <= </OPTION><OPTION value=" <> "> <> </OPTION>
</SELECT></TD><TD>
<INPUT ID=aFieldValue5_%(SUID)s TYPE=TEXT VALUE=""></TD></TR>
</TABLE>
<br>
<TABLE><TR>
<TD>&nbsp;&nbsp;<BUTTON class='fg-button-single ui-state-default ui-corner-all uihover' onclick="return aFielNameSelect_%(SUID)s_onchange()">Uwzględnij warunki</BUTTON></TD>
<TD><BUTTON class='fg-button-single ui-state-default ui-corner-all uihover' onclick="return aClearAllConditions_%(SUID)s()">Skasuj warunki</BUTTON></TD>
</TR></TABLE>
"""%{'SUID':self.RandomNameModifier}
      self.file.write(s)
# sort
      s="""

</TR></TABLE>

</TD></TR></TABLE>
</DIV>

<BR>

<DIV ID=setTableSortDiv1_%(SUID)s STYLE="display:none">
<TABLE bgcolor="silver" cellspacing=0 cellpadding=0>
<TR>
<TD bgcolor="ACTIVECAPTION"><FONT face="Arial" size="-2" color="white"><b>&nbsp;&nbsp;Parametry sortowania&nbsp;&nbsp;</b><font></TD>
<TD bgcolor="ACTIVECAPTION"><IMG alt="ukryj" style="cursor:pointer" src="images/caption_button_minimize.gif" onclick="document.all.setTableSortDiv1_%(SUID)s.style.display='none';"></TD>
<TD bgcolor="ACTIVECAPTION"><IMG alt="pokaż" style="cursor:pointer" src="images/caption_button_maximize.gif" onclick="document.all.setTableSortDiv1_%(SUID)s.style.display='';/*document.all.setTableSortDiv1_%(SUID)s.scrollIntoView(0);*/"></TD>
<!-- <TD bgcolor="ACTIVECAPTION"><IMG src="images/caption_button_close.gif"></TD> -->
</TR>
<TR><TD>
<TABLE bgcolor="BUTTONFACE" cellspacing=10>
<TR>

<TD>Poniżej możesz wybrać kolumny, według których chcesz sortować dane. Kliknięcie na nagłówek
kolumny także powoduje sortowanie tej kolumny, klikając ponownie zmieni się sposób sortowania z
rosnącego na malejący.
</TD></TR>
<TR>
"""%{'SUID':self.RandomNameModifier}
      self.file.write(s)
      s="""
<TABLE>
<TR><TD align=right>I&nbsp;sortowanie&nbsp;w/g:</TD><TD><SELECT ID=aFieldSortSelect1_%(SUID)s>
<OPTION SELECTED value="-1">nie sortuj</OPTION>
"""%{'SUID':self.RandomNameModifier}
      self.file.write(s)
      for i in range(0,len(self.space.header)):
         self.file.write('<OPTION value="%d">%s</OPTION>'%(i,self.space.header[i]))
      s="""
</SELECT></TD><TD>
<SELECT ID=aFieldSortCond1_%(SUID)s>
<OPTION value="+" SELECTED> rosnąco </OPTION><OPTION value="-"> malejąco </OPTION>
</SELECT></TD></TR>
"""%{'SUID':self.RandomNameModifier}
      self.file.write(s)
      s="""
<TR><TD align=right>II&nbsp;sortowanie&nbsp;w/g:</TD><TD><SELECT ID=aFieldSortSelect2_%(SUID)s>
<OPTION SELECTED value="-1">nie sortuj</OPTION>
"""%{'SUID':self.RandomNameModifier}
      self.file.write(s)
      for i in range(0,len(self.space.header)):
         self.file.write('<OPTION value="%d">%s</OPTION>'%(i,self.space.header[i]))
      s="""
</SELECT></TD><TD>
<SELECT ID=aFieldSortCond2_%(SUID)s>
<OPTION value="+" SELECTED> rosnąco </OPTION><OPTION value="-"> malejąco </OPTION>
</SELECT></TD></TR>
"""%{'SUID':self.RandomNameModifier}
      self.file.write(s)
      s="""
<TR><TD align=right>III&nbsp;sortowanie&nbsp;w/g:</TD><TD><SELECT ID=aFieldSortSelect3_%(SUID)s>
<OPTION SELECTED value="-1">nie sortuj</OPTION>
"""%{'SUID':self.RandomNameModifier}
      self.file.write(s)
      for i in range(0,len(self.space.header)):
         self.file.write('<OPTION value="%d">%s</OPTION>'%(i,self.space.header[i]))
      s="""
</SELECT></TD><TD>
<SELECT ID=aFieldSortCond3_%(SUID)s>
<OPTION value="+" SELECTED> rosnąco </OPTION><OPTION value="-"> malejąco </OPTION>
</SELECT></TD></TR>
</TABLE>
<BR>
<TABLE><TR>
<TD>&nbsp;&nbsp;<BUTTON class='fg-button-single ui-state-default ui-corner-all uihover' id=onsortformbuttonxmlchart%(SUID)s>Sortuj</BUTTON></TD> <!-- onclick="return aSortButtonClick_%(SUID)s()" -->
<TD><BUTTON class='fg-button-single ui-state-default ui-corner-all uihover' onclick="return aClearSortClick_%(SUID)s()">Skasuj sortowanie</BUTTON></TD>
</TR></TABLE>         
</TR></TABLE>

</TD></TR></TABLE>
</DIV>

"""%{'SUID':self.RandomNameModifier}
      self.file.write(s)


#************************
   def OnHeader(self,acol,avalue):
      pass
#      self.file.write('<TH class=objectsviewheader>'+avalue+'</TH>')
   def OnStartFooter(self):
      pass
#      self.file.write('<TFOOT><TR>')
   def OnFooter(self,acol,avalue):
      pass
#      if avalue is None:
#         self.file.write('<TD class=objectsviewfooter>&nbsp;</TD>')
#         return
#      if type(avalue)!=type(''):
#         avalue=str(avalue)
#      self.file.write('<TD class=objectsviewfooter>'+avalue+'</TD>')
   def OnEndFooter(self):
      pass
#      self.file.write('</TR></TFOOT>')
   def OnStartRow(self,arow):
      self.file.write('<row>')
      self.file.write('<rowid>%d</rowid>\n'%(arow,))
#      self.file.write('<TR class=objectsviewrow>\n')
   def OnEndRow(self,arow):
      self.file.write('</row>\n')
#      self.file.write('</TR>\n')
   def OnStartCol(self,arow,acol):
      self.file.write('<col%d>'%(acol,))
#      if self.IsOdd:          
#         self.file.write('<TD class=objectsviewdataodd NOWRAP>')
#      else:
#         self.file.write('<TD class=objectsviewdataeven NOWRAP>')
   def OnEndCol(self,arow,acol):
      self.file.write('</col%d>\n'%(acol,))
      if self.Value:
         s=self.Value.AsString()
         s=GetAsXMLStringNoPL(s)
      else:
         s=''
      self.file.write('<col%ds>%s</col%ds>\n'%(acol,s,acol))
#      self.file.write('</TD>\n')



