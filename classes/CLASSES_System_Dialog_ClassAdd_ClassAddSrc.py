# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

<HTML><HEAD>
<TITLE>Dodaj now&#261; klas&#281;</TITLE>
<META http-equiv="Content-Type" content="text/html; charset=windows-1250">
<META name="GENERATOR" content="ICOR">
</HEAD>

<BODY scroll="no">
Nazwa klasy: <input type=edit id=classedit size=32>
<br>
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
 <BUTTON onclick=DialogExitFunc(2) style="LEFT: 294px; POSITION: absolute; TOP: 63px; WIDTH: 100px; Z-INDEX: 100">Cancel</BUTTON>
 <BUTTON onclick=DialogExitFunc(1) style        ="LEFT: 186px; POSITION: absolute; TOP: 64px; WIDTH: 100px; Z-INDEX: 101">OK</BUTTON>
</BODY></HTML>

