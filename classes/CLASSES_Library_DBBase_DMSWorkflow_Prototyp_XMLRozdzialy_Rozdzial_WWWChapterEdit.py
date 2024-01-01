# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Naglowek',aoid=aoid)
   awwweditor.RegisterField('NaglowekMenu',aoid=aoid)
   awwweditor.RegisterField('TabelaZrodlowa',aoid=aoid)
#   awwweditor.RegisterField('ZrodloDanychWzorca',aoid=aoid)
#   awwweditor.RegisterField('PageTemplate',aoid=aoid)
#   awwweditor.RegisterField('GrupaRozdzialow',aoid=aoid)
   awwweditor.RegisterField('SGIsTableView',aoid=aoid)
   awwweditor.RegisterField('SGShowAsTable',aoid=aoid)
#   awwweditor.RegisterField('Galeria',aoid=aoid)
   awwweditor.RegisterField('SGHref',aoid=aoid)
   awwweditor.RegisterField('SGHrefParams',aoid=aoid)
   awwweditor.RegisterField('SGHrefApp',aoid=aoid)
   awwweditor.RegisterField('SGTarget',aoid=aoid)
   awwweditor.RegisterField('RodzajZaglebienia',aoid=aoid)
   awwweditor.RegisterField('SGIsMenuDisabled',aoid=aoid)
   awwweditor.RegisterField('IsAutoGenerate',aoid=aoid)
   awwweditor.RegisterField('ScheduledGenerate',aoid=aoid)
   awwweditor.RegisterField('IsGenerateDisabled',aoid=aoid)
   awwweditor.RegisterField('Priorytet',aoid=aoid)
   awwweditor.RegisterField('SGIsIndexDisabled',aoid=aoid)
   awwweditor.RegisterField('RSSDisabled',aoid=aoid)
   awwweditor.RegisterField('RSSOpis',aoid=aoid)
   awwweditor.RegisterField('ChapterParams',aoid=aoid)
   awwweditor.RegisterField('AccessLevelView',aoid=aoid)
   awwweditor.RegisterField('AccessLevelEdit',aoid=aoid)
   awwweditor.RegisterField('AccessLevelTableEdit',aoid=aoid)
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
      awwweditor.Write(anoreturnbutton=1)
   return 0 # show back reference to main object (1-link, 2-button)

def OnWWWActionSubmit(aobj,amenu,areport,file):
   amenu.SetAction('ObjectEdit')
   try:
      awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
      awwweditor.WWWActionSubmit(anoobjectview=1)
   finally:
      amenu.RestoreAction()
   file.write('<h3><font color="green">Dane zostały zmienione. Pamiętaj o odświeżeniu odpowiedniej pozycji w menu</font</h3>')



