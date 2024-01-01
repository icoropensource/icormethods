# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

option explicit

function ICORMain(CID,FieldName,OID,Value,UID)
   dim adialog,aclass,amethod
   Set aclass=aICORDBEngine.Classes.GetClassByID(OID)
   Set amethod=aclass.Methods(Value)
   set adialog=aICORDBEngine.Dialogs.GetDialog("",amethod.MethodPath)
'   adialog.StayOnTop=True
   adialog.Editor.ActivateApplets=True
   adialog.Editor.ActivateActiveXControls=True
   adialog.Editor.ActivateDTCs=True
   adialog.Editor.BrowseMode=True
   adialog.Editor.SourceCodePreservation=True
   adialog.Editor.DocumentHTML=amethod.MethodText
   adialog.Caption=amethod.MethodPath
   ICORMain=adialog.ShowModal()
   call adialog.Release
   set adialog=Nothing
   Set amethod=Nothing
   Set aclass=Nothing
end function

