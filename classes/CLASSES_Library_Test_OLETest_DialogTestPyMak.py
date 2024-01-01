# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from m32.ole import dispatch

def MethodText(aPath,aMethodName):
#   aclass=aICORDBEngine.Classes.GetClassByName(aPath)
   aclass=aICORDBEngine.Classes[aPath]
   return aclass.MethodsByName(aMethodName).MethodText

def main():
   aix = dispatch.DispatchObject("ICORAXInterface.Main")
   try:
      adialog=aix.aICORDBEngine.Dialogs.GetDialog()
#      dispatch.BrowseObject(adialog.Editor)
      try:
         aPath='CLASSES/Library/Test/OLETest'
         aMethodName='HTMLMethod1'
         data=MethodText(aPath,aMethodName)
         adialog.Editor.DocumentHTML=data
         adialog.Caption = 'DialogTest'
         adialog.ShowModal()
#         dispatch.BrowseObject(adialog.Editor.DOM.all)
         print adialog.Editor.DOM.all.classedit.value,
         print ' : ',
         print adialog.Editor.DOM.all['methodedit'].value
      except:
         from m32.m32printtb import print_tb,why
         why(withwhy=1)
         print 'error 1'
      adialog.Release()
      del adialog
   except:
      print 'error 2'
   del aix

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   ole=dispatch.ole32()
   try:
      main()
   except:
      print 'wow - error'
   del ole



