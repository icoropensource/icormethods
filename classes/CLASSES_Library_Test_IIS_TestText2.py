# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

<%
#
# Strona sluzaca do potwierdzania wpisow - zwraca wynik w JSON
#
aTable_KsiegaGosci=this.CRM.BaseNameModifier+'BZR_'+Plugin.PluginVars['aTableOID_KsiegaGosci']

afname='%splugin_%d_submit.asp'%(this.CRM.BaseDirectory,Plugin.OID)
fout=open(afname,'w')
try:
   dd={'PluginOID':str(Plugin.OID),'aTable_KsiegaGosci':aTable_KsiegaGosci,'ASPBegin':ASPBegin,'ASPEnd':ASPEnd}
   atext="""<!-- #include file="../../../inc/adovbs.inc" -->
<!-- #include file="../inc/_page_begin.asp" -->
%(ASPBegin)s
Response.Charset = "windows-1250"
'   Response.CodePage = 1250
Response.CacheControl = "Private"
Response.ExpiresAbsolute = #1/1/1999 1:10:00 AM#

aoid=Request.QueryString("oid")
amode=Request.QueryString("mode")

ainfo="???"

Set cn = Server.CreateObject("ADODB.Connection")
cn.CursorLocation=2 'adUseServer
cn.CommandTimeout=15
cn.ConnectionTimeout=15
cn.Open CONNECTION_STRING
Set rs = Server.CreateObject("ADODB.Recordset")
rs.ActiveConnection = cn
rs.CursorType = 1 'adOpenKeyset
rs.LockType = 3 'adLockOptimistic

rs.Open "select _OID,Tytul,Autor,EMail,Tresc,IDRozdzialu,Status from %(aTable_KsiegaGosci)s WHERE _OID='"+aoid+"'",cn
if rs.EOF or rs.BOF then
   ainfo="nieprawidłowy OID"
else
   ainfo="nieprawidłowy tryb zapisu"
   if amode="1" then
      rs("Status")="Z"
      ainfo="Wpis potwierdzony"
   end if
   if amode="0" then
      rs("Status")="X"
      ainfo="Wpis anulowany"
   end if
   rs.Update
end if
if rs.State<>0 then
   rs.Close
end if

cn.Close
set rs=Nothing
set cn=Nothing

Response.write "{'oid':'"+aoid+"','info':'"+ainfo+"'}"
%(ASPEnd)s
"""%dd
   fout.write(atext)
finally:
   fout.close()
%>

