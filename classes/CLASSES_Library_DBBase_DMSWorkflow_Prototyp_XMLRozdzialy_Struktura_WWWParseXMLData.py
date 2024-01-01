# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:19:11

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
from icorlib.projekt.mcrmwwwmenu import *
import cStringIO

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None,astructxml=''):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Tabele',adisplayed='Kod XML dla tabel',atype=mt_Memo,afieldeditor='XML')
   if astructxml:
      awwweditor.RegisterField('Rozdzialy',adisplayed='Kod XML dla rozdziałów',atype=mt_Memo,afieldeditor='XML',avalue=astructxml)
   else:
      awwweditor.RegisterField('Rozdzialy',adisplayed='Kod XML dla rozdziałów',atype=mt_Memo,afieldeditor='XML')
   return awwweditor

def RegisterFieldsStep1(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Field1',adisplayed='Pole S',atype=mt_String,avalue='ABC')
   awwweditor.RegisterField('Field2',adisplayed='Pole I',atype=mt_Integer,avalue='123')
   awwweditor.RegisterField('Field3',adisplayed='Pole DT',atype=mt_DateTime,avalue='2002/02/02')
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
   aparser=ICORBIPStructXMLParser()
   astructxml=aparser.StoreXMLSource(aobj)
   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None,astructxml=astructxml)
   if amenu.Action=='ObjectApplyMethods':
      awwweditor.Write(anoreturnbutton=1)
   return 0 # show back reference to main object (1-link, 2-button)

def OnWWWActionSubmit(aobj,amenu,areport,file):
#   amenu.SetAction('ObjectEdit')
#   try:
   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
   sstruct=awwweditor['Rozdzialy']
   stables=awwweditor['Tabele']
   if 1:
      fout=cStringIO.StringIO()
      fsql=cStringIO.StringIO()
      fout.write('*** TABELE ***\n')
      bparser=ICORBIPTablesXMLParser()
      bparser.Parse(stables,astructobj=aobj)
      bparser.Dump(fout,anoprint=1)
      fout.write('\n\n*** STRUKTURA ***\n')
      aparser=ICORBIPStructXMLParser()
      aparser.Parse(sstruct,bparser.Tables,bparser.ExistingTables)
      aparser.Dump(fout,anoprint=1)
      aparser.IsGood=1
      if aparser.IsGood and bparser.IsGood:
         fout=cStringIO.StringIO()
         ret1=bparser.Store(aobj,fout,fsql)
         ret1=1
         if ret1:
            file.write('<h1><font color="green">Tabele XML zaimportowane</font></h1>')
         else:
            file.write('<h1><font color="red">Wystąpiły błędy podczas importowania danych o tabelach z XML</font></h1>')
         ret2=aparser.Store(aobj,fout,fsql)
         ret2=1
         if ret2:
            file.write('<h1><font color="green">Struktura XML zaimportowana</font></h1>')
         else:
            file.write('<h1><font color="red">Wystąpiły błędy podczas importowania danych o strukturze z XML</font></h1>')
#         if ret1 and ret2:
#            aparser.StoreXMLSource(aobj)
#            bparser.StoreXMLSource(aobj)
      else:
         file.write('<h1><font color="red">Popraw dane XML przed aktualizacją projektu:</font></h1>')
      file.write('<pre>')
      file.write(fout.getvalue())
      file.write('</pre>')
      fout.close()
      asql=fsql.getvalue()
      if asql:
         file.write('\n<br><h1>SQL update</h1><br>\n')
         file.write('<pre>')
         file.write(asql)
         file.write('</pre>')
      fsql.close()

#      awwweditor.WWWActionSubmit(anoobjectview=1)
#   finally:
#      amenu.RestoreAction()

def OnWWWAction_Old(aobj,amenu,file):
#   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   if amenu.Action=='ObjectApplyMethods':
      sstruct=aobj.WWWMenuStructXML
      stables=aobj.WWWMenuDataXML
      fout=cStringIO.StringIO()
      fsql=cStringIO.StringIO()
      fout.write('*** TABELE ***\n')
      bparser=ICORBIPTablesXMLParser()
#      bparser.ClearTables(aobj) # clear?
      bparser.Parse(stables,astructobj=aobj)
      bparser.Dump(fout,anoprint=1)
      fout.write('\n\n*** STRUKTURA ***\n')
      aparser=ICORBIPStructXMLParser()
      aparser.Parse(sstruct,bparser.Tables,bparser.ExistingTables)
      aparser.Dump(fout,anoprint=1)
      aparser.IsGood=1
      if aparser.IsGood and bparser.IsGood:
         fout=cStringIO.StringIO()
         ret1=bparser.Store(aobj,fout,fsql)
         if ret1:
            file.write('<h1><font color="green">Tabele XML zaimportowane</font></h1>')
         else:
            file.write('<h1><font color="red">Wystąpiły błędy podczas importowania danych o tabelach z XML</font></h1>')
         ret2=aparser.Store(aobj,fout,fsql)
         ret2=1
         if ret2:
            file.write('<h1><font color="green">Struktura XML zaimportowana</font></h1>')
         else:
            file.write('<h1><font color="red">Wystąpiły błędy podczas importowania danych o strukturze z XML</font></h1>')
         if ret1 and ret2:
            aparser.StoreXMLSource(aobj)
            bparser.StoreXMLSource(aobj)
      else:
         file.write('<h1><font color="red">Popraw dane XML przed aktualizacją projektu:</font></h1>')
      file.write('<pre>')
      file.write(fout.getvalue())
      file.write('</pre>')
      fout.close()
      aobj.SQLUpdate=fsql.getvalue()
      fsql.close()
#      awwweditor.Write()
   return 2 # show back reference to main object (1-link, 2-button)

def OnWWWActionSubmit_Old(aobj,amenu,areport,file):
   if not areport['refMode']:
      awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
      file.write('<h1>Step 0</h1>')
      file.write('<h2>Field : %s</h2>'%awwweditor['Nazwa'])
      bwwweditor=RegisterFieldsStep1(aobj.Class,amenu,file,aobj.OID,None)
      bwwweditor.Write(arefMode='step1')
   elif areport['refMode']=='step1':
      awwweditor=RegisterFieldsStep1(aobj.Class,amenu,file,aobj.OID,areport)
      file.write('<h1>Step 1</h1>')
      file.write('<h2>Field 1: %s</h2>'%awwweditor['Field1'])
      file.write('<h2>Field 2: %s</h2>'%awwweditor['Field2'])
      file.write('<h2>Field 3: %s</h2>'%awwweditor['Field3'])


