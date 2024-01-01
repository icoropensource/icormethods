# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

<HTML><HEAD>
<TITLE></TITLE>
<META http-equiv="Content-Type" content="text/html; charset=windows-1250">
<META name="GENERATOR" content="ICOR">
</HEAD>

<BODY>
<font color="saddlebrown" size="+3">
<p>
Jestem tutaj!
</p>
</font>

aobj=aclass.GetFirstObject()
while aobj.Exists():
   
   aobj.Next()

<script language="VBScript">
sub TestMethodInfo(apath,amname)
   Dim aix,aclass,amethod
   Set aix=CreateObject("ICORAXInterface.Main")
   Set aclass=aix.aICORDBEngine.Classes.GetClassByName(apath)
   Set amethod=aclass.Methods(amname)
'   document.all.divinfo.insertAdjacentText "BeforeEnd",amethod.MethodText
   document.all.divinfo.innerText = amethod.MethodText
   Set amethod=Nothing
   Set aclass=Nothing
   Set aix=Nothing
end sub

function VBFunc
   call TestMethodInfo(document.all.classedit.value,document.all.methodedit.value)
end function

function TestFunc
   msgbox "aaaa"
end function
</script>

<input type=edit id=classedit size=50 value="CLASSES\Library\Test\OLETest">
<input type=edit id=methodedit value="DialogTest">
<button onclick="VBFunc()"> Click!</button>
<hr>
<font name="courier new" size=1 color="navy">
<p id=divinfo></p>
<font>
<hr>


<script language="VBScript">
function DialogExitFunc(aresult)
   Dim aix,adialog
   Set aix=CreateObject("ICORAXInterface.Main")
   set adialog=aix.aICORDBEngine.Dialogs.GetDialog("","CLASSES\Library\Test\OLETest\HTMLMethod1") 'current method path
   adialog.ModalResult=aresult
   Set adialog=Nothing
   Set aix=Nothing
end function
</script>
<button onclick="DialogExitFunc(1)">OK</button>
<button onclick="DialogExitFunc(2)">Cancel</button>
<button onclick="DialogExitFunc(3)">Abort</button>
<button onclick="DialogExitFunc(4)">Retry</button>
<button onclick="DialogExitFunc(5)">Ignore</button>
<button onclick="DialogExitFunc(6)">Yes</button>
<button onclick="DialogExitFunc(7)">No</button>
<hr>
<button onclick="TestFunc()" style="HEIGHT: 30px; WIDTH: 346px">Metoda przykladowa</button></font></font>

</BODY></HTML>



