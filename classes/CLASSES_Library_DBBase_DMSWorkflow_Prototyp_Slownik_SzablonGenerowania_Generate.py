# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil
import CLASSES_Library_ICORBase_Interface_ICORSync as ICORSync

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
#   awwweditor.RegisterField('FieldGenerateTables',adisplayed='Czy generować tabele w SQL',atype=mt_Boolean,avalue='0')
   return awwweditor

def RegisterFieldsStep1(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
#   awwweditor.RegisterField('Field1',adisplayed='Pole S',atype=mt_String,avalue='ABC')
#   awwweditor.RegisterField('Field2',adisplayed='Pole I',atype=mt_Integer,avalue='123')
#   awwweditor.RegisterField('Field3',adisplayed='Pole DT',atype=mt_DateTime,avalue='2002/02/02')
   return awwweditor

def OnBeforeWWWAction(aobj,amenu,file):
   return 1

def OnWWWAction(aobj,amenu,file):
   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   if amenu.Action=='ObjectApplyMethods':
      awwweditor.Write()
   return 0 # show back reference to main object

def OnWWWActionSubmit(aobj,amenu,areport,file):
   if not areport['refMode']:
      awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
#      w=CLASSES_Library_ICORBase_Interface_ICORUtil.str2bool(awwweditor['FieldGenerateTables'])
      w=0
      file.write('<h2>Generowanie w toku</h2>')
      astate=ICORSync.ICORState(aname='STRUKTURY',avalue='RUN')
      aobj.Class.Main(str(w)+'!'+str(astate.OID),aobj.OID,'')
      file.write("""
<script language="javascript">
getParentFrame('NAVBAR').registerStateBadOK(%d);
</script>
"""%astate.OID)
      file.write('<h3>Zlecenie publikacji szablonu zostało dołączone do kolejki.</h3><br>')
      awwweditor.WriteObjectView(aobj,asbutton=1)
#      bwwweditor=RegisterFieldsStep1(aobj.Class,amenu,file,aobj.OID,None)
#      bwwweditor.Write(arefMode='step1')



