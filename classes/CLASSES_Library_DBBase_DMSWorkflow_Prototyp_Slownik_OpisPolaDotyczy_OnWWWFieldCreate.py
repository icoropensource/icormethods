# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:14:52

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import icorlib.projekt.msqllib as msqllib
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import icordbmain.adoutil as ADOLibInit
import string
import icordbmain.dbaccess as dbaccess

def GetTableInfo(file,atablename,adbobj):
   try:
      aado=ADOLibInit.ADOUtil(acnt=1,acominitialize=1,dbaccessobj=adbobj)
   except Exception,v:
      print 'Exception:',v
      ADOLibInit.handle_com_error(v)
      import traceback
      traceback.print_exc()
      return
   try:
      rs=aado.GetRS("select ordinal_position,column_name,data_type,column_default,character_maximum_length,numeric_precision,numeric_precision_radix,numeric_scale,datetime_precision,is_nullable,character_set_name,collation_name from information_schema.columns where table_name='%s' order by ORDINAL_POSITION"%atablename)
      try:
         aado.GetRSAsTable(rs,file,atablename)
      finally:
         rs=aado.CloseRS(rs)
   finally:
      aado.Close()

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('W0',adisplayed='Usunięcie wartości domyślnej',atype=mt_Boolean,avalue='0')
   awwweditor.RegisterField('W1',adisplayed='Usunięcie indeksów',atype=mt_Boolean,avalue='0')
   awwweditor.RegisterField('W2',adisplayed='Usunięcie pola',atype=mt_Boolean,avalue='0')
   awwweditor.RegisterField('W3',adisplayed='Dodanie pola',atype=mt_Boolean,avalue='0')
   awwweditor.RegisterField('W4',adisplayed='Dodanie wartości domyślnej',atype=mt_Boolean,avalue='0')
   awwweditor.RegisterField('W5',adisplayed='Dodanie indeksów',atype=mt_Boolean,avalue='0')
   awwweditor.RegisterField('W6',adisplayed='Zmiana nazwy kolumny',atype=mt_Boolean,avalue='0')
   return awwweditor

def RegisterFieldsStep1(aclass,amenu,file,aoid=-1,areport=None,avalue=''):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('SQL',atype=mt_Memo,avalue=avalue)
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
      tobj=aobj.Dotyczy
      pobj=tobj.Projekt
      atablename='%sBZR_%d'%(pobj.BaseNameModifier,aobj.Dotyczy.OID)
      GetTableInfo(file,atablename,pobj.DBAccess)
      aisversioncontrol=tobj['IsVersionControl',mt_Integer]
      atablenamev=''
      if aisversioncontrol:
         atablenamev='%sBZR_V_%d'%(tobj.Projekt.BaseNameModifier,aobj.Dotyczy.OID)
         GetTableInfo(file,atablenamev,pobj.DBAccess)
   return 0 # show back reference to main object (1-link, 2-button)

def OnWWWActionSubmit(aobj,amenu,areport,file):
   if not areport['refMode']:
      awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
      tobj=aobj.Dotyczy
      atablename='%sBZR_%d'%(tobj.Projekt.BaseNameModifier,aobj.Dotyczy.OID)
      aisversioncontrol=tobj['IsVersionControl',mt_Integer]
      atablenamev=''
      if aisversioncontrol:
         atablenamev='%sBZR_V_%d'%(tobj.Projekt.BaseNameModifier,aobj.Dotyczy.OID)
      afieldname=aobj.NazwaID
      yobj=aobj.TypPolaDotyczy

      aProjectVars=ICORUtil.ParseVars(tobj.Projekt.ProjectVars,{'aCgiScriptPath':'','aExternalDictMaxItemsCount':'300','aMSSQLVersion':'2008','aSQLScriptsCreate':'0'})
      aSQLVersion=int(aProjectVars.get('aMSSQLVersion','2008'))

      aftype,afdefault=msqllib.GetFieldCreateParms(yobj.Nazwa,yobj.Opis,yobj.Rozmiar,aobj.DomyslnaWartosc,aIsVersionControl=0,adblquote=1,asqlversion=aSQLVersion)
      aftypev,afdefaultv='',''
      if aisversioncontrol:
         aftypev,afdefaultv=msqllib.GetFieldCreateParms(yobj.Nazwa,yobj.Opis,yobj.Rozmiar,aobj.DomyslnaWartosc,aIsVersionControl=1,adblquote=1,asqlversion=aSQLVersion)
      atext="""
BEGIN TRANSACTION
DECLARE @sconstraint nvarchar(400)
DECLARE @SQL nvarchar(2000)
DECLARE @TableName nVarchar(200)
DECLARE @ColName nVarchar(200)
DECLARE @ColNameNew nVarChar(200)
DECLARE @ColTypeNew nVarChar(200)
DECLARE @ColDefaultNew nVarChar(200)
"""
      if aisversioncontrol:
         atext=atext+"""DECLARE @TableNameV nVarchar(200)
DECLARE @ColTypeNewV nVarChar(200)
DECLARE @ColDefaultNewV nVarChar(200)
"""

      atext=atext+"""
SELECT @TableName='%s'
SELECT @ColName='%s'
SELECT @ColNameNew='%s'     
SELECT @ColTypeNew='%s'
SELECT @ColDefaultNew='%s'
"""%(atablename,afieldname,afieldname,aftype,afdefault)
      if aisversioncontrol:
         atext=atext+"""SELECT @TableNameV='%s'
SELECT @ColTypeNewV='%s'
SELECT @ColDefaultNewV='%s'
"""%(atablenamev,aftypev,afdefaultv)

      if ICORUtil.str2bool(awwweditor['W0']):
         atext=atext+"""
-- usuniecie wartosci domyslnej z kolumny
SELECT @sconstraint=d.name FROM sys.default_constraints as d
   JOIN sys.objects as o
   ON o.object_id = d.parent_object_id
   JOIN sys.columns as c
   ON c.object_id = o.object_id AND c.column_id = d.parent_column_id
   JOIN sys.schemas as s
   ON s.schema_id = o.schema_id
   WHERE o.name=@TableName AND c.name = @ColName
IF @sconstraint<>'' BEGIN
   select @sql = 'Alter Table ' + @TableName + ' Drop Constraint ' + @sconstraint
   EXEC(@sql)
END
"""
         if aisversioncontrol:
            atext=atext+"""
-- usuniecie wartosci domyslnej z kolumny w tabeli wersyjnej
SELECT @sconstraint=d.name FROM sys.default_constraints as d
   JOIN sys.objects as o
   ON o.object_id = d.parent_object_id
   JOIN sys.columns as c
   ON c.object_id = o.object_id AND c.column_id = d.parent_column_id
   JOIN sys.schemas as s
   ON s.schema_id = o.schema_id
   WHERE o.name=@TableNameV AND c.name = @ColName
IF @sconstraint<>'' BEGIN
   select @sql = 'Alter Table ' + @TableNameV + ' Drop Constraint ' + @sconstraint
   EXEC(@sql)
END
"""
      if ICORUtil.str2bool(awwweditor['W1']):
         atext=atext+"""
-- usuniecie indeksu w kolumnie
IF EXISTS (SELECT name FROM sysindexes WHERE name = 'id_'+@TableName+'_'+@ColName) BEGIN
   SELECT @SQL = 'DROP INDEX ' + @TableName + '.id_'+@TableName+'_'+@ColName
   EXEC(@SQL)
END
"""
         if aisversioncontrol:
            atext=atext+"""
-- usuniecie indeksu w kolumnie z tabeli wersyjnej
IF EXISTS (SELECT name FROM sysindexes WHERE name = 'id_'+@TableNameV+'_'+@ColName) BEGIN
   SELECT @SQL = 'DROP INDEX ' + @TableNameV + '.id_'+@TableNameV+'_'+@ColName
   EXEC(@SQL)
END
"""
      if ICORUtil.str2bool(awwweditor['W2']):
         atext=atext+"""
-- usuniecie kolumny
IF EXISTS (SELECT COLUMN_NAME FROM information_schema.columns WHERE TABLE_NAME = @TableName AND COLUMN_NAME=@ColName) BEGIN
   SELECT @SQL = 'Alter table ' + @TableName + ' Drop Column ' + @ColName
   EXEC(@SQL)
END
"""
         if aisversioncontrol:
            atext=atext+"""
-- usuniecie kolumny z tabeli wersyjnej
IF EXISTS (SELECT COLUMN_NAME FROM information_schema.columns WHERE TABLE_NAME = @TableNameV AND COLUMN_NAME=@ColName) BEGIN
   SELECT @SQL = 'Alter table ' + @TableNameV + ' Drop Column ' + @ColName
   EXEC(@SQL)
END
"""
      if ICORUtil.str2bool(awwweditor['W3']):
         atext=atext+"""
-- utworzenie kolumny
IF @ColNameNew<>'' BEGIN
   IF @ColDefaultNew<>'' BEGIN
      SELECT @SQL = 'Alter table ' + @TableName + ' ADD ' + @ColNameNew + ' '+ @ColTypeNew + + ' NOT NULL CONSTRAINT df_'+@TableName+'_'+@ColNameNew+' DEFAULT ' + @ColDefaultNew
   END ELSE BEGIN
      SELECT @SQL = 'Alter table ' + @TableName + ' ADD ' + @ColNameNew + ' '+ @ColTypeNew + + ' NOT NULL'
   END
   EXEC(@SQL)
END
"""
         if aisversioncontrol:
            atext=atext+"""
-- utworzenie kolumny w tabeli wersyjnej
IF @ColNameNew<>'' BEGIN
   IF @ColDefaultNewV<>'' BEGIN
      SELECT @SQL = 'Alter table ' + @TableNameV + ' ADD ' + @ColNameNew + ' '+ @ColTypeNewV + + ' NOT NULL CONSTRAINT df_'+@TableNameV+'_'+@ColNameNew+' DEFAULT ' + @ColDefaultNewV
   END ELSE BEGIN
      SELECT @SQL = 'Alter table ' + @TableNameV + ' ADD ' + @ColNameNew + ' '+ @ColTypeNewV + + ' NOT NULL'
   END
   EXEC(@SQL)
END
"""
      if ICORUtil.str2bool(awwweditor['W4']) and not ICORUtil.str2bool(awwweditor['W3']):
         atext=atext+"""
-- przypisanie wartosci domyslnej do kolumny
IF @ColNameNew<>'' AND @ColDefaultNew<>'' BEGIN
   SELECT @SQL = 'Alter table ' + @TableName + ' ADD CONSTRAINT df_'+@TableName+'_'+@ColNameNew+' DEFAULT ' + @ColDefaultNew + ' FOR '+@ColNameNew
   EXEC(@SQL)
END
"""
         if aisversioncontrol:
            atext=atext+"""
-- przypisanie wartosci domyslnej do kolumny w tabeli wersyjnej
IF @ColNameNew<>'' AND @ColDefaultNewV<>'' BEGIN
   SELECT @SQL = 'Alter table ' + @TableNameV + ' ADD CONSTRAINT df_'+@TableNameV+'_'+@ColNameNew+' DEFAULT ' + @ColDefaultNewV + ' FOR '+@ColNameNew
   EXEC(@SQL)
END
"""
      if ICORUtil.str2bool(awwweditor['W5']):
         atext=atext+"""
-- utworzenie nowego indeku dla kolumny
IF EXISTS (SELECT name FROM sysindexes WHERE name = 'id_'+@TableName+'_'+@ColNameNew) BEGIN
   SELECT @SQL = 'DROP INDEX ' + @TableName + '.id_'+@TableName+'_'+@ColNameNew
   EXEC(@SQL)
END
SELECT @SQL = 'CREATE INDEX id_'+@TableName+'_'+@ColNameNew+' ON '+@TableName+' ('+@ColNameNew+')'
EXEC(@SQL)
"""
         if aisversioncontrol:
            atext=atext+"""
-- utworzenie nowego indeku dla kolumny w tabeli wersyjnej
IF EXISTS (SELECT name FROM sysindexes WHERE name = 'id_'+@TableNameV+'_'+@ColNameNew) BEGIN
   SELECT @SQL = 'DROP INDEX ' + @TableNameV + '.id_'+@TableNameV+'_'+@ColNameNew
   EXEC(@SQL)
END
SELECT @SQL = 'CREATE INDEX id_'+@TableNameV+'_'+@ColNameNew+' ON '+@TableNameV+' ('+@ColNameNew+')'
EXEC(@SQL)
"""

      if ICORUtil.str2bool(awwweditor['W6']):
         atext=atext+"""
-- zmiana nazwy kolumny
IF @ColName<>@ColNameNew BEGIN
   SELECT @sconstraint=@TableName + '.' + @ColName
   EXECUTE sp_rename @sconstraint, @ColNameNew, 'COLUMN'
END
"""
         if aisversioncontrol:
            atext=atext+"""
-- zmiana nazwy kolumny w tabeli wersyjnej
IF @ColName<>@ColNameNew BEGIN
   SELECT @sconstraint=@TableNameV + '.' + @ColName
   EXECUTE sp_rename @sconstraint, @ColNameNew, 'COLUMN'
END
"""

      atext=atext+"""
COMMIT
"""
#      file.write('<h1>Step 0</h1>')
      bwwweditor=RegisterFieldsStep1(aobj.Class,amenu,file,aobj.OID,None,avalue=atext)
      bwwweditor.Write(arefMode='step1')

      tobj=aobj.Dotyczy
      pobj=tobj.Projekt
      atablename='%sBZR_%d'%(pobj.BaseNameModifier,aobj.Dotyczy.OID)
      GetTableInfo(file,atablename,pobj.DBAccess)
      aisversioncontrol=tobj['IsVersionControl',mt_Integer]
      atablenamev=''
      if aisversioncontrol:
         atablenamev='%sBZR_V_%d'%(tobj.Projekt.BaseNameModifier,aobj.Dotyczy.OID)
         GetTableInfo(file,atablenamev,pobj.DBAccess)
   elif areport['refMode']=='step1':
      tobj=aobj.Dotyczy
      pobj=tobj.Projekt
      awwweditor=RegisterFieldsStep1(aobj.Class,amenu,file,aobj.OID,areport)
      try:
         aado=ADOLibInit.ADOUtil(acnt=1,acominitialize=1,dbaccessobj=pobj.DBAccess)
      except Exception,v:
         print 'Exception:',v
         ADOLibInit.handle_com_error(v)
         import traceback
         traceback.print_exc()
         return
      try:
         w=0
         rs=None
         try:
            rs=aado.SQL2RS(awwweditor['SQL'])
            w=1
         except Exception,v:
            file.write('<font color=red><pre>')
            hresult_code, hresult_name, additional_info, parameter_in_error = v
            exception_string = ["%s - %s" % (hex (hresult_code), hresult_name)]
            if additional_info:
               wcode, source_of_error, error_description, whlp_file, whlp_context, scode = additional_info
               exception_string.append ("  Error in: %s" % source_of_error)
               exception_string.append ("  %s - %s" % (hex (scode), error_description.strip ()))
            for s in exception_string:
               file.write(s+'\n')
            if 0:
               sl=ICORUtil.GetLastExceptionInfo()
               for s in sl:
                  file.write(s+'\n')
            file.write('</pre></font>')
         try:
            if w:
               aado.GetRSAsTable(rs,file,'Wynik')
         finally:
            rs=aado.CloseRS(rs)
      finally:
         aado.Close()
      if w:
         file.write('<h1>Kod SQL uruchomiony i wykonany.</h1>')

