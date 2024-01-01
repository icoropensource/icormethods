# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

option explicit

function ICORMain(CID,FieldName,OID,Value,UID)
   dim adialog
   set adialog=aICORDBEngine.Dialogs.GetDialog()
   adialog.Editor.DocumentHTML="<HTML><head><title>Caption bla bla</title></head><body>" & _
      "<P>Hello world!!!</P>" & _
      "</BODY></HTML>"
   adialog.StayOnTop=False
   adialog.Caption="Dialog testowy #3"
   adialog.Show
'   call adialog.Release
'   msgbox adialog.Editor.DOM.all.classedit.value & " : " & adialog.Editor.DOM.all.methodedit.value
   set adialog=Nothing
end function



