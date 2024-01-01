# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORSync as ICORSync
import CLASSES_Library_DBBase_DMSWorkflow_Meta_Profile_ProfileLib as ProfileLib
import cPickle

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('tryb',atype=mt_String,avalue='check',ahidden=1,adefaultcheck=1)
   pparser=ProfileLib.ProfileParser(amenu.uid,'build')
   aobj=aclass[aoid]
   pparser.ParseParameters(aobj.XMLParameters)
   for afieldname,afieldprettyname in pparser.InputVariables:
      awwweditor.RegisterField(afieldname,adisplayed=afieldprettyname,atype=mt_String,avalue=pparser[afieldname])
   return awwweditor,pparser

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
   awwweditor,pparser=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   if amenu.Action=='ObjectApplyMethods':
      file.write('''
<table><tr><td><b>Tryb:&nbsp;</b></td><td>
<select onchange="javascript:jQuery('#tryb').val(this.value);" id=stryb name=stryb tabindex=1>
<option value="check" SELECTED>Sprawdzenie
<option value="build">Tworzenie
<option value="undo">Usunięcie
</select>
</td></tr>
</table>
''')
      awwweditor.Write()
   return 0 # show back reference to main object (1-link, 2-button)

def OnWWWActionSubmit(aobj,amenu,areport,file):
   if not areport['refMode']:
      awwweditor,pparser=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
      amode=awwweditor['tryb']
      file.write('<h1>'+amode+' - w trakcie generowania.</h1>\n')
      astate=ICORSync.ICORState(aname='STRUKTURY',avalue='RUN')
      d={'_mode':amode}
      for afieldname,afieldprettyname in pparser.InputVariables:
         d[afieldname]=awwweditor[afieldname]
      aobj.Class.DoExecute('!'+str(astate.OID),aobj.OID,cPickle.dumps(d))
      file.write("""
<script language="javascript">
getParentFrame('NAVBAR').registerStateBadOK(%d);
</script>
"""%astate.OID)
   return 2 # show back reference to main object (1-link, 2-button)



