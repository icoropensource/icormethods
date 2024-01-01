# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

<%
#
# Strona do zarzadzania wpisami przez moderatora
#
aTable_KsiegaGosci=this.CRM.BaseNameModifier+'BZR_'+Plugin.PluginVars['aTableOID_KsiegaGosci']

dd={'PluginOID':str(Plugin.OID),'aTable_KsiegaGosci':aTable_KsiegaGosci,'ASPBegin':ASPBegin,'ASPEnd':ASPEnd}
atext="""
%(ASPEnd)s
<script language=javascript>
function potwierdz_submit(json) {
   $("#wi_"+json.oid+"/*").remove();
   $("#wi_"+json.oid).append("<font color=navy size=+2>"+json.info+"&nbsp;&nbsp;&nbsp;</font>");
}

function potwierdz(amode,aoid) {
   $.getJSON("plugin_%(PluginOID)s_submit.asp?mode="+amode+"&oid="+aoid+"&rv="+Math.random(),potwierdz_submit);
}
</script>
%(ASPBegin)s
rs.Open "select top 500 _OID,DataWpisu,Tytul,Autor,Email,Tresc,IdRozdzialu,Status from %(aTable_KsiegaGosci)s WHERE Status in ('M','G') ORDER BY DataWpisu ASC", cn
if rs.EOF or rs.BOF then
   Response.Write("<h1>Brak wpisów do moderacji</h1>")
else
   Response.Write("<span class='objectsviewcaption'>Księga gości</span>")
   Do While Not rs.EOF
      aoid=rs("_OID")

      Response.write "<div style='background:#c1dcbe;border:solid 2px #CBD79D;margin:10px;padding:5px;'>"
      Response.write "<b><i>"+rs("Tytul")
      Response.write "</i></b><br>wysłany przez: <b>"+rs("Autor")
      Response.write "</b>, dnia: <b>"+CStr(rs("DataWpisu"))+"</b>, Status: <b>"+rs("Status")+"</b>, EMail: <b>"+rs("EMail")+"</b>"
      Response.write "<hr style='border: dashed 2px green;'>"
      Response.write rs("Tresc")
      Response.write "<hr style='border: dashed 2px green;'>"
%(ASPEnd)s
<span id=wi_%(ASPVarBegin)saoid%(ASPEnd)s></span>
<span id=wa_%(ASPVarBegin)saoid%(ASPEnd)s>
<button onclick='javascript:potwierdz("1","%(ASPVarBegin)saoid%(ASPEnd)s")'><font color=green>Potwierdź wpis</font></button>&nbsp;&nbsp;&nbsp;
<button onclick='javascript:potwierdz("0","%(ASPVarBegin)saoid%(ASPEnd)s")'><font color=red>Anuluj wpis</font></button>&nbsp;&nbsp;&nbsp;
</span>
%(ASPBegin)s
      Response.write "</div>"
      rs.MoveNext
   Loop
end if
"""%dd

aitem=this.CRM.GetNewCRMItem()
afname='%splugin_%d_manage.asp'%(this.CRM.BaseDirectory,Plugin.OID)
aitem.WriteASP(afname,atext)
%>

