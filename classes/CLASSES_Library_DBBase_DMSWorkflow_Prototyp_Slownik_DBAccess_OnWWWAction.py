# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import icordbmain.adoutil as ADOLibInit
import string

def OnBeforeWWWAction(aobj,amenu,file):
   return 1

def OnWWWAction(aclass,amenu,file):
   awwweditor=RegisterFields(aclass,amenu,file)
   awwweditor.WWWAction()

def OnWWWActionSubmit(aclass,amenu,areport,file):
   awwweditor=RegisterFields(aclass,amenu,file,-1,areport)
   awwweditor.WWWActionSubmit()

def OnWWWMenuClassRecur(xmlfile,bclass,afieldname,aoid,UID):
   return
   import win32api
#   print win32api.GetUserName()
#   print 'c:',bclass.CID,'f:',afieldname,'o:',aoid,'u:',UID

"""
-- tables
--SELECT name FROM sysobjects WHERE xtype = 'U' order by name

-- stored procedures
--SELECT name FROM sysobjects WHERE xtype='P' order by name

-- fields
--SELECT name FROM syscolumns WHERE ID = (SELECT id FROM sysobjects WHERE name='TMP_BZR_18000') ORDER BY name

-- fields and types
/*
SELECT syscolumns.name AS ColumnName, systypes.name AS Datatype --, systypes.length as Length, systypes.*
        FROM sysobjects, syscolumns, systypes
        WHERE sysobjects.id = syscolumns.id AND
        syscolumns.xtype = systypes.xtype AND 
        sysobjects.name = 'TMP_BZR_18000' order by syscolumns.name
*/

-- sp source (more than 1 record)
--SELECT text FROM syscomments WHERE id = (SELECT id FROM sysobjects WHERE name = 'sp_TMP_BZR_18000_DefaultSearch' AND xtype='P');

--exec sp_help
--exec sp_help TMP_BZR_18000
--exec sp_helptext 'sp_TMP_BZR_18000_DefaultSearch'
"""

def OnWWWMenuObjRecur(xmlfile,aobj,UID):
   d={'text':XMLUtil.GetAsXMLStringNoPL(aobj.ConnectionString)}
   d['icon']='/icormanager/images/icons/silk/icons/database_edit.png'
   d['openIcon']=d['icon']
   d['action']='icormain.asp?jobtype=menuobjrecuraction&CID=%d&OID=%d&type=dir&param=%s'%(aobj.CID,aobj.OID,'')
   d['src']='icormain.asp?jobtype=menuclassrecuraction&CID=%d&OID=%d&type=dir&param=%s&XMLData=1'%(aobj.CID,aobj.OID,'')
   xmlfile.TagOpen('tree',d,aclosetag=1)

def OnWWWMenuClassRecurAction(xmlfile,aobj,brobj,atype,aparam,acontext,UID):
   if atype!='dir':
      return
   import win32api
#   print win32api.GetUserName()
#   print 'obj - c:',aobj.Class.CID,aobj.Class.NameOfClass,'o:',aobj.OID,'u:',UID
   try:
      aado=ADOLibInit.ADOUtil(acnt=1,acominitialize=1,dbaccessobj=aobj)
   except Exception,v:
      print 'Exception:',v
      ADOLibInit.handle_com_error(v)
      import traceback
      traceback.print_exc()
      return
   do={}
   lo=['TABLE','VIEW','STORED PROCEDURE']
   for s in lo:
      do[s]=[]
   try:
      rs=aado.SQL2RS("exec sp_tables @table_owner='dbo'")
      try:
         while not rs.EOF and not rs.BOF:
            aobjname=ADOLibInit.GetRSValueAsStr(rs,'TABLE_NAME')
            aobjtype=ADOLibInit.GetRSValueAsStr(rs,'TABLE_TYPE')
            if aobjtype in lo:
               do[aobjtype].append(aobjname)
            rs.MoveNext()
      finally:
         rs=aado.CloseRS(rs)
      rs=aado.SQL2RS("exec sp_stored_procedures @sp_owner='dbo'")
      try:
         while not rs.EOF and not rs.BOF:
            aobjname=ADOLibInit.GetRSValueAsStr(rs,'PROCEDURE_NAME')
            sl=string.split(aobjname,';')
            do['STORED PROCEDURE'].append(sl[0])
            rs.MoveNext()
      finally:
         rs=aado.CloseRS(rs)
   finally:
      aado.Close()

   ll=do['TABLE']
   if ll:
      d={'text':XMLUtil.GetAsXMLStringNoPL('Tabele użytkownika')}
      d['icon']='/icormanager/images/icons/silk/icons/folder_database.png'
      d['openIcon']=d['icon']
      xmlfile.TagOpen('tree',d)
      ll.sort()
      for aobjname in ll:
         d={'text':XMLUtil.GetAsXMLStringNoPL(aobjname)}
         d['action']='icormain.asp?jobtype=menuobjrecuraction&CID=%d&OID=%d&type=table&param=%s'%(aobj.CID,aobj.OID,aobjname)
         d['icon']='/icormanager/images/icons/silk/icons/table_edit.png'
         d['openIcon']=d['icon']
   #      d['src']='icormain.asp?jobtype=menuclassrecur&CID=%d&OID=%d&field=%s&XMLData=1'%(acid,aoid,bfield.Name)
   #               if wcontext:
   #      d['context']='icormain.asp?jobtype=menuclassrecurcontext&CID=%d&OID=%d&field=%s&XMLData=1'%(acid,aoid,bfield.Name)
   #                  print 'Context 2:',d['context']
         xmlfile.TagOpen('tree',d,aclosetag=1)
      xmlfile.TagClose('tree')

   ll=do['VIEW']
   if ll:
      d={'text':XMLUtil.GetAsXMLStringNoPL('Widoki')}
      d['icon']='/icormanager/images/icons/silk/icons/folder_table.png'
      d['openIcon']=d['icon']
      xmlfile.TagOpen('tree',d)
      ll.sort()
      for aobjname in ll:
         d={'text':XMLUtil.GetAsXMLStringNoPL(aobjname),}
         d['action']='icormain.asp?jobtype=menuobjrecuraction&CID=%d&OID=%d&type=view&param=%s'%(aobj.CID,aobj.OID,aobjname)
         d['icon']='/icormanager/images/icons/silk/icons/table_gear.png'
         d['openIcon']=d['icon']
   #      d['src']='icormain.asp?jobtype=menuclassrecur&CID=%d&OID=%d&field=%s&XMLData=1'%(acid,aoid,bfield.Name)
   #               if wcontext:
   #      d['context']='icormain.asp?jobtype=menuclassrecurcontext&CID=%d&OID=%d&field=%s&XMLData=1'%(acid,aoid,bfield.Name)
   #                  print 'Context 2:',d['context']
         xmlfile.TagOpen('tree',d,aclosetag=1)
      xmlfile.TagClose('tree')

   ll=do['STORED PROCEDURE']
   if ll:
      d={'text':XMLUtil.GetAsXMLStringNoPL('Procedury')}
      d['icon']='/icormanager/images/icons/silk/icons/folder_page.png'
      d['openIcon']=d['icon']
      xmlfile.TagOpen('tree',d)
      ll.sort()
      for aobjname in ll:
         d={'text':XMLUtil.GetAsXMLStringNoPL(aobjname),}
         d['action']='icormain.asp?jobtype=menuobjrecuraction&CID=%d&OID=%d&type=sp&param=%s'%(aobj.CID,aobj.OID,aobjname)
         d['icon']='/icormanager/images/icons/silk/icons/script_gear.png'
         d['openIcon']=d['icon']
   #      d['src']='icormain.asp?jobtype=menuclassrecur&CID=%d&OID=%d&field=%s&XMLData=1'%(acid,aoid,bfield.Name)
   #               if wcontext:
   #      d['context']='icormain.asp?jobtype=menuclassrecurcontext&CID=%d&OID=%d&field=%s&XMLData=1'%(acid,aoid,bfield.Name)
   #                  print 'Context 2:',d['context']
         xmlfile.TagOpen('tree',d,aclosetag=1)
      xmlfile.TagClose('tree')

def OnWWWMenuObjRecurAction(file,aobj,atype,aparam,UID):
#   print 't:',atype,'p:',aparam
   try:
      aado=ADOLibInit.ADOUtil(acnt=1,acominitialize=1,dbaccessobj=aobj)
   except Exception,v:
      print 'Exception:',v
      ADOLibInit.handle_com_error(v)
      import traceback
      traceback.print_exc()
      return
   try:
      file.write('<body topmargin="10">') #<base target="TEXT">
      if atype=='table':
         file.write('<h1>%s</h1>'%aparam)
         rs=aado.GetRS("select ordinal_position,column_name,data_type,column_default,character_maximum_length,numeric_precision,numeric_precision_radix,numeric_scale,datetime_precision,is_nullable,character_set_name,collation_name from information_schema.columns where table_name='%s' order by ORDINAL_POSITION"%aparam)
         try:
            aado.GetRSAsTable(rs,file,'Kolumny')
         finally:
            rs=aado.CloseRS(rs)
         rs=aado.GetRS("SELECT indid,name,status,minlen,keycnt,groupid,dpages,used,rowcnt,rowmodctr,xmaxlen,maxirow,maxlen,rows FROM sysindexes where id=object_id('%s','U') and not name like '_WA_SYS_%%' order by indid"%aparam)
         try:
            aado.GetRSAsTable(rs,file,'Indeksy')
         finally:
            rs=aado.CloseRS(rs)
         rs=aado.GetRS("SELECT parent_column_id,d.name,definition,d.type,d.type_desc,d.create_date,d.modify_date,is_system_named FROM sys.default_constraints as d JOIN sys.objects as o ON o.object_id = d.parent_object_id WHERE o.name='%s' ORDER BY parent_column_id"%aparam)
         try:
            aado.GetRSAsTable(rs,file,'Reguły')
         finally:
            rs=aado.CloseRS(rs)
         rs=aado.GetRS("SELECT TOP 100 * FROM %s"%aparam)
         try:
            aado.GetRSAsTable(rs,file,'Dane',amaxvaluelen=400,acounter=1)
         finally:
            rs=aado.CloseRS(rs)
         if 0:
            aado.OpenADOX()
            atable=aado.catalog.Tables(aparam)
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
</TR></THEAD><TBODY>
""")
            i=1
            for acolumn in atable.Columns:
               aname,atype,asize=acolumn.Name,aado.ADOTypes[acolumn.Type],acolumn.DefinedSize
               if asize>10000:
                  asize=0
               file.write("<TR style='BACKGROUND-COLOR: window;'>")
               file.write("<TD>"+str(i)+"</TD>")
               file.write("<TD>"+aname+"</TD>")
               file.write("<TD>"+atype+"</TD>")
               if asize:
                  file.write("<TD>"+str(asize)+"</TD>")
               else:
                  file.write("<TD>&nbsp;</TD>")
               file.write("</TR>")
               i=i+1
            file.write("""</TBODY></TABLE>
<script type='text/javascript'>
var astvar0 = new SortableTable(document.getElementById('sortedTable0'),['Number','String','String','Number'] );
astvar0.sort(0,1);
</script>
""")
         if 0: # get table properties by sp
            rs=aado.SQL2RS('exec sp_help %s'%aparam)
            try:
               rs,status=rs.NextRecordset()
               file.write('<table>')
               file.write('<tr>')
               mf=rs.Fields.Count
               for i in range(mf):
                  file.write('<td>'+str(rs.Fields(i).Name)+'</td>')
               file.write('</tr>')
               while not rs.EOF and not rs.BOF:
                  file.write('<tr>')
                  for i in range(mf):
                     avalue=ADOLibInit.GetRSValueAsStr(rs,i)
                     file.write('<td>'+avalue+'</td>')
                  file.write('</tr>')
                  rs.MoveNext()
               file.write('</table>')
            finally:
               rs=aado.CloseRS(rs)
      elif atype=='sp':
         rs=aado.SQL2RS('exec sp_helptext %s'%aparam)
         try:
            file.write("<textarea id='Tresc' name='Tresc' wrap='Off' style='width:100%;height:600px;' >") #cols=32 rows=6
            avalue=''
            while not rs.EOF and not rs.BOF:
               avalue=avalue+ADOLibInit.GetRSValueAsStr(rs,0)
               rs.MoveNext()
            file.write(avalue)
            file.write('</textarea>')
         finally:
            rs=aado.CloseRS(rs)
      elif atype=='view':
         try:
            rs=aado.SQL2RS('exec sp_helptext %s'%aparam)
            avalue=''
            while not rs.EOF and not rs.BOF:
               avalue=avalue+ADOLibInit.GetRSValueAsStr(rs,0)
               rs.MoveNext()
         except:
            avalue=''
         try:
            file.write("<textarea id='Tresc' name='Tresc' wrap='Off' style='width:100%;height:600px;' >") #cols=32 rows=6
            file.write(avalue)
            file.write('</textarea>')
         finally:
            rs=aado.CloseRS(rs)
   finally:
      aado.Close()



