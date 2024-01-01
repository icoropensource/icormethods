# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil
import string

def OnBeforeWWWAction(aobj,amenu,file):
   return 1

def OnWWWAction(aclass,amenu,file):
   if amenu.Action=='ObjectEdit' and len(amenu.WWWParam)==3:
      pcid,aoid,pfieldname=amenu.WWWParam
      lobj=aclass[aoid]
      aobj=lobj.SourceTable
      robj=lobj.DestinationTable
      asrcfname=lobj.Class.SourceField.Name+'_'+str(lobj.Class.SourceField.FOID)
      adstfname=lobj.Class.DestinationField.Name+'_'+str(lobj.Class.DestinationField.FOID)
      file.write('<table><tr><td valign=top><h3><font color="mediumpurple">Pola w tabeli źródłowej</font></h3><ol>\n')
      if aobj:
         file.write('<li><span onmouseover="javascript:this.style.fontWeight=\'bold\';" onmouseout="javascript:this.style.fontWeight=\'\';" style="cursor:pointer" onclick="javascript:if(document.getElementById(\'%s\').value!=\'\'){document.getElementById(\'%s\').value+=\',\'};document.getElementById(\'%s\').value+=\'%s\'">%s</span></li>\n'%(asrcfname,asrcfname,asrcfname,'_OID','_OID'))
         p1obj=aobj.Pola
         while p1obj:
            file.write('<li><span onmouseover="javascript:this.style.fontWeight=\'bold\';" onmouseout="javascript:this.style.fontWeight=\'\';" style="cursor:pointer" onclick="javascript:if(document.getElementById(\'%s\').value!=\'\'){document.getElementById(\'%s\').value+=\',\'};document.getElementById(\'%s\').value+=\'%s\'">%s</span></li>\n'%(asrcfname,asrcfname,asrcfname,p1obj.Nazwa,p1obj.Nazwa))
            p1obj.Next()
         file.write('</ol></td>\n')
      file.write('<td valign=top><h3><font color="steelblue">Pola w tabeli docelowej</font></h3><ol>\n')
      if robj:
         file.write('<li><span onmouseover="javascript:this.style.fontWeight=\'bold\';" onmouseout="javascript:this.style.fontWeight=\'\';" style="cursor:pointer" onclick="javascript:if(document.getElementById(\'%s\').value!=\'\'){document.getElementById(\'%s\').value+=\',\'};document.getElementById(\'%s\').value+=\'%s\'">%s</span></li>\n'%(adstfname,adstfname,adstfname,'_OID','_OID'))
         p2obj=robj.Pola
         while p2obj:
            file.write('<li><span onmouseover="javascript:this.style.fontWeight=\'bold\';" onmouseout="javascript:this.style.fontWeight=\'\';" style="cursor:pointer" onclick="javascript:if(document.getElementById(\'%s\').value!=\'\'){document.getElementById(\'%s\').value+=\',\'};document.getElementById(\'%s\').value+=\'%s\'">%s</span></li>\n'%(adstfname,adstfname,adstfname,p2obj.Nazwa,p2obj.Nazwa))
            p2obj.Next()
      file.write('</ol></td></tr></table>\n')
   awwweditor=RegisterFields(aclass,amenu,file)
   awwweditor.WWWAction()

def OnWWWActionSubmit(aclass,amenu,areport,file):
   awwweditor=RegisterFields(aclass,amenu,file,-1,areport)
   aoid=awwweditor.WWWActionSubmit()
   if aoid>=0:
      aobj=aclass[aoid]
      if not aobj.LinkName and aobj.DestinationTable:
         aobj.LinkName=aobj.DestinationTable.Nazwa

