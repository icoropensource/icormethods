# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import string
import os

def OnBeforeWWWAction(aobj,amenu,file):
   return 1

def OnWWWAction(aclass,amenu,file):
   awwweditor=RegisterFields(aclass,amenu,file)
   awwweditor.WWWAction()

def OnWWWActionSubmit(aclass,amenu,areport,file):
   awwweditor=RegisterFields(aclass,amenu,file,-1,areport)
   awwweditor.WWWActionSubmit()

def OnWWWMenuObjRecur(xmlfile,aobj,UID):
   apath=FilePathAsSystemPath(aobj.SciezkaAplikacji)
   if not apath:
      return
   d={'text':XMLUtil.GetAsXMLStringNoPL(apath)}
   d['icon']='/icormanager/images/icons/silk/icons/folder_link.png'
   d['openIcon']=d['icon']
   d['action']='icormain.asp?jobtype=menuobjrecuraction&CID=%d&OID=%d&type=dir&param=%s'%(aobj.CID,aobj.OID,'')
   d['src']='icormain.asp?jobtype=menuclassrecuraction&CID=%d&OID=%d&type=dir&param=%s&XMLData=1'%(aobj.CID,aobj.OID,'')
   xmlfile.TagOpen('tree',d,aclosetag=1)

def OnWWWMenuClassRecurAction(xmlfile,aobj,brobj,atype,aparam,acontext,UID):
   if atype=='dir':
      abasepath=FilePathAsSystemPath(aobj.SciezkaAplikacji)
      apath=string.replace(aparam,'..','')
      try:
         l=os.listdir(abasepath+apath)
      except:
         return
      for afilename in l:
         if os.path.isdir(abasepath+apath+'\\'+afilename):
            d={'text':XMLUtil.GetAsXMLStringNoPL(afilename)}
            d['icon']='/icormanager/images/icons/silk/icons/folder_page.png'
            d['openIcon']=d['icon']
            d['action']='icormain.asp?jobtype=menuobjrecuraction&CID=%d&OID=%d&type=dir&param=%s'%(aobj.CID,aobj.OID,apath+'\\'+afilename)
            d['src']='icormain.asp?jobtype=menuclassrecuraction&CID=%d&OID=%d&type=dir&param=%s&XMLData=1'%(aobj.CID,aobj.OID,apath+'\\'+afilename)
            xmlfile.TagOpen('tree',d,aclosetag=1)

def OnWWWMenuObjRecurAction(file,aobj,atype,aparam,UID):
   file.write('<body topmargin="10">') #<base target="TEXT">
   if atype=='dir':
      abasepath=FilePathAsSystemPath(aobj.SciezkaAplikacji)
      apath=string.replace(aparam,'..','')
      try:
         l=os.listdir(abasepath+apath)
      except:
         file.write('<h1>Brak plików</h1>')
         return
      wheader=0
      i=1
      awwwpath=aobj.AdresZewnetrznyWWW+'/'+aobj.KatalogWirtualny
      for afilename in l:
         afilepath=apath+'\\'+afilename
         if not os.path.isdir(abasepath+afilepath):
            if not wheader:
               file.write("""<script type='text/javascript' src='/icormanager/inc/sortabletable.js'></script>
<TABLE class='sort-table' cellspacing=0 id='sortedTable0'>
<COL style='text-align: right'></COL>
<COL></COL>
<COL></COL>
<COL style='text-align: right'></COL>
<THEAD><TR>
<TD>Lp</TD>
<TD>Nazwa</TD>
<TD>Typ</TD>
<TD>Rozmiar</TD>
<TD>Modyfikacja</TD>
<TD>Link</TD>
</TR></THEAD><TBODY>
""")
               wheader=1
            lf=os.path.splitext(afilename)
            aname,atype,asize=lf[0],lf[1][1:],os.path.getsize(abasepath+afilepath)
            amtime=ICORUtil.tdatetime2fmtstr(tdatetime(os.path.getmtime(abasepath+afilepath)))
            file.write("<TR style='BACKGROUND-COLOR: window;'>")
            file.write("<TD>"+str(i)+"</TD>")
            file.write("<TD>"+aname+"</TD>")
            file.write("<TD>"+atype+"</TD>")
            file.write("<TD>"+str(int(asize))+"</TD>")
            file.write("<TD>"+amtime+"</TD>")
            asrc='icormain.asp?jobtype=menuobjrecuraction&CID=%d&OID=%d&type=source&param=%s'%(aobj.CID,aobj.OID,afilepath)
            file.write("<TD><a href='"+awwwpath+afilepath+"' target='_new'>plik</a> <a href='"+asrc+"'>źródło</a></TD>")
            file.write("</TR>")
            i=i+1
      if wheader:
         file.write("""</TBODY></TABLE>
<script type='text/javascript'>
var astvar0 = new SortableTable(document.getElementById('sortedTable0'),['Number','CaseInsensitiveString','CaseInsensitiveString','Number','Date','String'] );
astvar0.sort(0,1);
</script>
""")
      else:
         file.write('<h1>Brak plików</h1>')
   if atype=='source':
      abasepath=FilePathAsSystemPath(aobj.SciezkaAplikacji)
      awwwpath=aobj.AdresZewnetrznyWWW+'/'+aobj.KatalogWirtualny
      apath=string.replace(aparam,'..','')
      try:
         fin=open(abasepath+apath,'r')
         try:
            atext=fin.read()
         finally:
            fin.close()
      except:
         file.write('<h1>Brak plików</h1>')
         return
      file.write('<p>%s<br><a target="_new" href="%s">%s</a></p>'%(abasepath+apath,awwwpath+apath,awwwpath+apath))
      file.write('<textarea style="width:100%;" rows=32 wrap=off>')
      file.write(XMLUtil.GetAsXMLStringNoPL(atext))
      file.write('</textarea>')

