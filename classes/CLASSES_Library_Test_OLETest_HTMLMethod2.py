# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

<HTML><HEAD>
<TITLE>Dialog testowy opisujący różne takie wartości</TITLE>
<META http-equiv="Content-Type" content="text/html; charset=windows-1250">
<META name="GENERATOR" content="ICOR">
</HEAD>

<BODY scroll="no">
<%
aclass=aICORDBEngine.Classes['CLASSES_DataBase_Miasto_JednostkaOrganizacyjna']
aobj=aclass.GetFirstObject()
Response.write('<table>')
x=0
while aobj and x<10:
   s='<tr><td>%s</td><td>%s</td></tr>\n'%(aobj.Nazwa,aobj.Adres.Ulica)
   Response.write(s)
   aobj.Next()
   x=x+1
Response.write('</table>')
%>
<p>
<%
for i in range(10):
   Response.write('xx')
Response.write('<br>')
%>
Test

</p>

<script language="VBScript">
function DialogExitFunc(aresult)
   Dim aix,adialog
   Set aix=CreateObject("ICORAXInterface.Main")
   set adialog=aix.aICORDBEngine.Dialogs.GetDialogByHandle("<%=DHandle%>")
   adialog.ModalResult=aresult
   Set adialog=Nothing
   Set aix=Nothing
end function
</script>
<hr><button onclick="DialogExitFunc(1)">OK</button>
</BODY></HTML>


