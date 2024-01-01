# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

option explicit
sub showError(where)
   if Err.Number<>0 then
      aICORDBEngine.StdOutPrint "Error at " &where &" code=" & CStr(Err.Number) & " info=" & Err.Description
      err.Clear
   end if
end sub

function GetICOR()
   aICORDBEngine.StdOutPrint "GetICOR"
   Set GetICOR=aICORDBEngine
end function

function ICORMain(CID,FieldName,OID,Value,UID)
   on error resume next
   dim prefix,file
   dim dlg,factory
   dim i
   prefix="c:\tmp\mak\"
   file="demo.htm"

   set dlg = CreateObject("M32browser.M32Dialog.1")
   showError 1
   set factory = CreateObject("ScriptX.Factory")
   showError 2
   dlg.Build
   showError 3
   
   dlg.externalHandler = me
   showError 4
   dlg.Browser.Navigate2 prefix+file
   showError 5
   dlg.ctxMenus = false
   showError 6
   
   if 1 = 0 then
      dlg.MessageLoop
      showError 7
   else
      for i=1 to 1000
         dlg.MessageStep
         showError 8
      next
      dlg.externalHandler = Nothing
      showError 9
      dlg.Stop
      showError 10
   end if
   set dlg = Nothing
   showError 11
end function


