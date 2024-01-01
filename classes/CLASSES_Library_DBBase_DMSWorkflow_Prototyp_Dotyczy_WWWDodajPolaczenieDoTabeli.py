# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil

def RegisterFieldsOld(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   l=''
   if areport is None:
      aobj=aclass[aoid]
      pobj=aobj.Projekt
      dobj=pobj.BazyZrodlowe
      l=[]
      while dobj:
         if dobj.OID!=aoid:
            l.append(string.strip(dobj.Grupa+' / '+dobj.Nazwa))
         dobj.Next()
      l.sort()
   awwweditor.RegisterField('TabelaDocelowa',adisplayed='Tabela docelowa',atype=mt_String,avalue=l)
   return awwweditor

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   l=''
   if areport is None:
      dobj=aclass.GetFirstObject()
      l=[]
      lh=[]
      while dobj:
         if dobj.OID!=aoid and ICORSecurity.CheckRecursiveAccessLevelForUser(dobj,'AccessLevelView',amenu.uid):
            l.append(dobj.Grupa+' / '+dobj.Nazwa)
            lh.append([dobj.Grupa,dobj.Nazwa,dobj.Grupa+' / '+dobj.Nazwa])
         dobj.Next()
      l.sort()
      lh.sort()
      afid='myfield1'
      wlg=0
      slg=''
      file.write('<h3>Wybierz tabelę docelową:</h3>\n')
      file.write('<select id=%s name=%s tabindex=0>\n'%(afid,afid,))
      for sg,sn,sv in lh:
         if sg!=slg:
            if wlg:
               file.write('</optgroup>')
            wlg=1
            slg=sg
            file.write('<optgroup label="%s">'%(sg.replace('"','&quot')))
         file.write('<option value="%s">%s\n'%(sv.replace('"','&quot'),sn))
      if wlg:
         file.write('</optgroup>')
      file.write('</select>')
      file.write('''
<script language="javascript">
jQuery(function() {
   jQuery("#TabelaDocelowa").parent().parent().parent().hide();
   jQuery("#myfield1").change(function(){
      jQuery("#TabelaDocelowa").val(jQuery("#myfield1").val());
   });
});
</script>
''')
   #awwweditor.RegisterField('TabelaDocelowa',adisplayed='Tabela docelowa',atype=mt_String,avalue=l)
   awwweditor.RegisterField('TabelaDocelowa',adisplayed='Tabela docelowa',atype=mt_String,ahidden=1)
   return awwweditor

def RegisterFieldsStep1(aclass,amenu,file,aoid=-1,areport=None,atabela=''):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('TabelaDocelowa',atype=mt_String,ahidden=1,avalue=atabela)
   awwweditor.RegisterField('LinkName',adisplayed='Nazwa połączenia',atype=mt_String,avalue='')
   awwweditor.RegisterField('SrcFields',adisplayed='Pola w tabeli źródłowej',atype=mt_String,avalue='')
   awwweditor.RegisterField('DstFields',adisplayed='Pola w tabeli docelowej',atype=mt_String,avalue='')
   awwweditor.RegisterField('LinkConstraint',adisplayed='Warunek łączenia danych',atype=mt_String,avalue='')
   awwweditor.RegisterField('IsExtension',adisplayed='Czy rozszerzenie tabeli',atype=mt_Bool,avalue='')
   awwweditor.RegisterField('IsTableView',adisplayed='Czy widok tabelaryczny',atype=mt_Bool,avalue='')
   awwweditor.RegisterField('WWWDisabledTable',adisplayed='Czy tabela wyłączona dla potrzeb WWW',atype=mt_Bool,avalue='')
   awwweditor.RegisterField('LinkHrefCaptionNewItem',adisplayed='Nazwa wyświetlana dla nowych pozycji',atype=mt_String,avalue='')
   awwweditor.RegisterField('LinkHrefCaptionEditItem',adisplayed='Nazwa wyświetlana dla istniejących pozycji',atype=mt_String,avalue='')
   awwweditor.RegisterField('TabID',adisplayed='ID Zakładki',atype=mt_String,avalue='10')
   awwweditor.RegisterField('IsInternalTab',adisplayed='Czy wewnętrzna zakładka',atype=mt_Bool,avalue='')
   awwweditor.RegisterField('TabName',adisplayed='Nazwa zakładki',atype=mt_String,avalue='')
   return awwweditor

def OnBeforeWWWAction(aobj,amenu,file):
   w=1
   if 0:
      w=w and ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelView',amenu.uid)
   if 0:
      w=w and ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelEdit',amenu.uid)
   if 0:
      w=w and ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelDelete',amenu.uid)
   return w

def OnWWWAction(aobj,amenu,file):
   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   if amenu.Action=='ObjectApplyMethods':
      awwweditor.Write()
   return 0 # show back reference to main object (1-link, 2-button)

def OnWWWActionSubmit(aobj,amenu,areport,file):
   if not areport['refMode']:
      awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
      file.write('\n\n<h2><font color="green">%s</font></h2>'%awwweditor['TabelaDocelowa'])
      if 0:
         pobj=aobj.Projekt
         dobj=pobj.BazyZrodlowe
      else:
         aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Dotyczy']
         dobj=aclass.GetFirstObject()
      robj=None
      l=[]
      sname1=string.strip(awwweditor['TabelaDocelowa'])
      while dobj:
         sname2=string.strip(dobj.Grupa+' / '+dobj.Nazwa)
         if sname2==sname1:
            robj=dobj
            break
         dobj.Next()
      if robj is None:
         file.write('<h1><font color="red">Podana tabela nie istnieje.</font></h1>')
         return
      p1obj=aobj.Pola
      p2obj=robj.Pola
      file.write('<table><tr><td valign=top><h3><font color="mediumpurple">Pola w tabeli źródłowej</font></h3><ol>\n')
      file.write('<li><span onmouseover="javascript:this.style.fontWeight=\'bold\';" onmouseout="javascript:this.style.fontWeight=\'\';" style="cursor:pointer;" onclick="javascript:if(document.getElementById(\'SrcFields\').value!=\'\'){document.getElementById(\'SrcFields\').value+=\',\'};document.getElementById(\'SrcFields\').value+=\'%s\'">%s</span></li>\n'%('_OID','_OID'))
      while p1obj:
         file.write('<li><span onmouseover="javascript:this.style.fontWeight=\'bold\';" onmouseout="javascript:this.style.fontWeight=\'\';" style="cursor:pointer;" onclick="javascript:if(document.getElementById(\'SrcFields\').value!=\'\'){document.getElementById(\'SrcFields\').value+=\',\'};document.getElementById(\'SrcFields\').value+=\'%s\'">%s</span></li>\n'%(p1obj.Nazwa,p1obj.Nazwa))
         p1obj.Next()
      file.write('</ol></td><td valign=top><h3><font color="steelblue">Pola w tabeli docelowej</font></h3><ol>\n')
      file.write('<li><span onmouseover="javascript:this.style.fontWeight=\'bold\';" onmouseout="javascript:this.style.fontWeight=\'\';" style="cursor:pointer;" onclick="javascript:if(document.getElementById(\'DstFields\').value!=\'\'){document.getElementById(\'DstFields\').value+=\',\'};document.getElementById(\'DstFields\').value+=\'%s\'">%s</span></li>\n'%('_OID','_OID'))
      while p2obj:
         file.write('<li><span onmouseover="javascript:this.style.fontWeight=\'bold\';" onmouseout="javascript:this.style.fontWeight=\'\';" style="cursor:pointer;" onclick="javascript:if(document.getElementById(\'DstFields\').value!=\'\'){document.getElementById(\'DstFields\').value+=\',\'};document.getElementById(\'DstFields\').value+=\'%s\'">%s</span></li>\n'%(p2obj.Nazwa,p2obj.Nazwa))
         p2obj.Next()
      file.write('</ol></td></tr></table>\n')
      bwwweditor=RegisterFieldsStep1(aobj.Class,amenu,file,aobj.OID,None,awwweditor['TabelaDocelowa'])
      bwwweditor.Write(arefMode='step1')
   elif areport['refMode']=='step1':
      awwweditor=RegisterFieldsStep1(aobj.Class,amenu,file,aobj.OID,areport)
      if 0:
         pobj=aobj.Projekt
         dobj=pobj.BazyZrodlowe
      else:
         aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Dotyczy']
         dobj=aclass.GetFirstObject()
      l=[]
      robj=None
      sname1=string.strip(awwweditor['TabelaDocelowa'])
      while dobj:
         sname2=string.strip(dobj.Grupa+' / '+dobj.Nazwa)
         if sname2==sname1:
            robj=dobj
            break
         dobj.Next()
      if robj is None:
         file.write('<h1><font color="red">Podana tabela docelowa nie istnieje.</font></h1>')
         return
      tclass=aobj.Class.PolaczeniaDoTabel.ClassOfType
      toid=tclass.AddObject(arefobject=aobj)
      aname=awwweditor['LinkName']
      if not aname:
         aname=robj.Nazwa
      tclass.LinkName[toid]=aname
      tclass.DestinationField[toid]=awwweditor['DstFields']
      tclass.DestinationTable[toid]=robj.AsRefString()
      tclass.LinkConstraint[toid]=awwweditor['LinkConstraint']
      tclass.LinkTabID[toid]=awwweditor['TabID']
      tclass.SourceField[toid]=awwweditor['SrcFields']
      tclass.IsExtension[toid]=ICORUtil.str2bool(awwweditor['IsExtension'])
      tclass.IsTableView[toid]=ICORUtil.str2bool(awwweditor['IsTableView'])
      tclass.WWWDisabledTable[toid]=ICORUtil.str2bool(awwweditor['WWWDisabledTable'])
      tclass.IsInternalTab[toid]=ICORUtil.str2bool(awwweditor['IsInternalTab'])
      tclass.LinkHrefCaptionNewItem[toid]=awwweditor['LinkHrefCaptionNewItem']
      tclass.LinkHrefCaptionEditItem[toid]=awwweditor['LinkHrefCaptionEditItem']
      aobj.Class.PolaczeniaDoTabel.AddRefs(aobj.OID,[toid,tclass.CID])
      if awwweditor['TabID']:
         zrefs=aobj.Class.Zakladki.GetRefList(aobj.OID)
         apos,afind=zrefs.FindRefByValue('ZakladkaID',awwweditor['TabID'])
         if not afind:
            zclass=aobj.Class.Zakladki.ClassOfType
            zoid=zclass.AddObject(arefobject=aobj)
            if awwweditor['TabName']:
               zname=awwweditor['TabName']
            else:
               zname='Zakładka '+awwweditor['TabID']
            zclass.Nazwa[zoid]=zname
            zclass.ZakladkaID[zoid]=awwweditor['TabID']
            aobj.Class.Zakladki.AddRefs(aobj.OID,[zoid,zclass.CID],asortedreffield=zclass.ZakladkaID)
      file.write('<h1>Połączenie do tabeli zostało dodane.</h1>')
      return 1


