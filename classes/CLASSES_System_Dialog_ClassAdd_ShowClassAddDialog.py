# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

option explicit

function ICORMain(CID,FieldName,OID,Value,UID)
   dim adialog
   set adialog=aICORDBEngine.Dialogs.GetDialog()
   adialog.Editor.DocumentHTML="<HTML><head><title>Dodaj klase</title></head><body>" & _
      "" & _
      "</BODY></HTML>"
   adialog.StayOnTop=False
   adialog.Caption="Dialog testowy #3"
   adialog.ShowModal
   call adialog.Release
   msgbox adialog.Editor.DOM.all.classedit.value
   set adialog=Nothing
end function
