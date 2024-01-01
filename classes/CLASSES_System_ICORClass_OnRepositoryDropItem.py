# -*- coding: windows-1250 -*-
# saved: 2021/06/09 11:02:03

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
import CLASSES_Library_NetBase_WWW_Server_ServerUtil as ServerUtil
from icorlib.wwwmenu.menuutil import ICORWWWMenuItem
import string

def Dialog_MenuDrop_CopyOrMove():
   aaction=-1
   dclass=aICORDBEngine.Classes['CLASSES_System_Dialog_MenuDrop_CopyOrMove']
   doid=dclass.FirstObject()
   if doid<0:
      doid=dclass.AddObject()
   if not dclass.EditObject(doid):
      return
   dobj=dclass[doid]
   aobj1=dobj.MenuDropAction
   if aobj1:
      aaction=aobj1.Class.ActionID.ValuesAsInt(aobj1.OID)
   return aaction

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   DragItemType,DragItemName,DragItemValue,DragItemCID,DragItemOID,DropItemType,DropItemName,DropItemOID=tuple(string.split(Value,chr(255)))
   DragItemCID,DragItemOID,DropItemOID=int(DragItemCID),int(DragItemOID),int(DropItemOID)
   if 1==0:
      print 'CID:',CID
      print 'DragItemType:',aICORDBEngine.Variables._DragItemType,DragItemType
      print 'DragItemName:',aICORDBEngine.Variables._DragItemName,DragItemName
      print 'DragItemCID:',aICORDBEngine.Variables._DragItemCID,DragItemCID
      print 'DragItemOID:',aICORDBEngine.Variables._DragItemOID,DragItemOID
      print 'DragItemValue:',aICORDBEngine.Variables._DragItemValue,DragItemValue
      print 'DropItemType:',aICORDBEngine.Variables._DropItemType,DropItemType
      print 'DropItemName:',aICORDBEngine.Variables._DropItemName,DropItemName
      print 'DropItemOID:',aICORDBEngine.Variables._DropItemOID,DropItemOID
#      return

   if DropItemType=='Class':
      aclass=aICORDBEngine.Classes[DropItemOID]
      if DragItemType=='Field':
         if MessageDialog('Czy chcesz przeniesc '+DragItemName+' do '+DropItemName+'?',mtConfirmation,mbYesNoCancel)!=mrYes:
            return
         acopy=0
         ret=MessageDialog('Czy chcesz przenieść także wartości pola?',mtConfirmation,mbYesNoCancel)
         if ret==mrCancel:
            return
         if ret==mrYes:
            acopy=1
         bclass=aICORDBEngine.Classes[DragItemCID]
         afield=bclass.FieldsByName(DragItemName)
         aftype=-1
         if afield.FieldTID>MAX_ICOR_SYSTEM_TYPE:
            ret=MessageDialog('Czy chcesz uaktualnić typ pola?',mtConfirmation,mbYesNoCancel)
            if ret==mrCancel:
               return
            if ret==mrYes:
               adialog=InputElementDialog('Wybierz typ dla pola '+DragItemName)
               if not adialog.Show():
                  return
               tclass=aICORDBEngine.Classes[adialog.ClassPath]
               if tclass is None:
                  print 'Klasa nie istnieje',adialog.ClassPath
                  return
               aftype=tclass.CID
         aclass.CopyField(DragItemCID,DragItemName,copyvalues=acopy,afieldtype=aftype)
         return
      if DragItemType=='Method':
         if MessageDialog('Czy chcesz przeniesc '+DragItemName+' do '+DropItemName+'?',mtConfirmation,mbYesNoCancel)!=mrYes:
            return
         aclass.CopyMethod(DragItemCID,DragItemName)
      if DragItemType=='Class':
         dclass=aICORDBEngine.Classes['CLASSES_System_Dialog_RepositoryDrop_ClassItemOnClassItem']
         doid=dclass.FirstObject()
         if doid<0:
            doid=dclass.AddObject()
         if not dclass.EditObject(doid):
            return
         dobj=dclass[doid]
         aobj1=dobj.ClassDropAction
         aaction=-1
         if aobj1:
            aaction=aobj1.Class.ActionID.ValuesAsInt(aobj1.OID)
         if aaction==1: # przenieś
            aICORDBEngine.Classes.MoveClass(CID,DragItemCID)
         elif aaction==2: # zrób pole w/g typu
            bclass=aICORDBEngine.Classes[DragItemCID]
            fclass=aICORDBEngine.Classes['CLASSES/System/Dialog/FieldAdd']
            ret=fclass.DoFieldAdd.Execute('',aclass.CID,string.join([bclass.NameOfClass,'','','Class',bclass.ClassPath],ServerUtil.SPLIT_CHAR_PARAM))
            if ret=='1':
               pass
   elif DropItemType=='Field':
      if DragItemType=='Field':
         aclass=aICORDBEngine.Classes[DragItemCID]
         bclass=aICORDBEngine.Classes[DropItemOID]
         afield=aclass.FieldsByName(DragItemName)
         bfield=bclass.FieldsByName(DropItemName)
         ret=MessageDialog('Czy chcesz przenieść wartości pola %s do pola %s?'%(DragItemName,DropItemName),mtConfirmation,mbYesNoCancel)
         if ret==mrCancel:
            return
         if ret==mrYes:
            aoid=afield.GetFirstValueID()
            while aoid>=0:
               bfield[aoid]=afield[aoid]
               aoid=afield.GetNextValueID(aoid)
   elif DropItemType=='WWWMenuItem':
      amenu=ICORWWWMenuItem(UID,DropItemOID)
      if DragItemType=='WWWMenuItem':
         dclass=aICORDBEngine.Classes['CLASSES_System_Dialog_MenuDrop_MenuItemOnMenuItem']
         doid=dclass.FirstObject()
         if doid<0:
            doid=dclass.AddObject()
         if not dclass.EditObject(doid):
            return
         dobj=dclass[doid]
         aobj1=dobj.MenuDropAction
         aaction=-1
         if aobj1:
            aaction=aobj1.Class.ActionID.ValuesAsInt(aobj1.OID)
         bmenu=ICORWWWMenuItem(UID,DragItemOID)
         if aaction==1: # wstaw przed
            amenu.InsertMenuBefore(bmenu)
         elif aaction==2: # dodaj jako podpozycje
            amenu.AddChildMenu(bmenu)
         elif aaction==3: # skopiuj tylko jedna
            pass
         elif aaction==4: # skopiuj cale drzewko
            pass
      elif DragItemType=='SummaryItem':
         amenu.AddSummary(DragItemOID)
      elif DragItemType=='WWWSummaryItem':
         aaction=Dialog_MenuDrop_CopyOrMove()
         if aaction==1: # kopiuj
            amenu.AddSummary(DragItemOID,asumminfo=1,adeletesummoidfromownermenu=0)
         elif aaction==2: # przenieś
            amenu.AddSummary(DragItemOID,asumminfo=1,adeletesummoidfromownermenu=1)
   elif DropItemType=='WWWSummaryItem':
      if DragItemType=='WWWSummaryItem':
         siclass=aICORDBEngine.Classes['CLASSES_Library_NetBase_WWW_Dictionary_Report_SummaryInfo']
         siobj=siclass[DropItemOID]
         amenu=ICORWWWMenuItem(UID,siobj.ParentMenu.OID)
         aaction=Dialog_MenuDrop_CopyOrMove()
         if aaction==1: # kopiuj
            amenu.AddSummary(DragItemOID,asumminfo=1,ainsertbefore=[DropItemOID,siclass.CID],adeletesummoidfromownermenu=0)
         elif aaction==2: # przenieś
            amenu.AddSummary(DragItemOID,asumminfo=1,ainsertbefore=[DropItemOID,siclass.CID],adeletesummoidfromownermenu=1)
      elif DragItemType=='SummaryItem':
         siclass=aICORDBEngine.Classes['CLASSES_Library_NetBase_WWW_Dictionary_Report_SummaryInfo']
         siobj=siclass[DropItemOID]
         amenu=ICORWWWMenuItem(UID,siobj.ParentMenu.OID)
         amenu.AddSummary(DragItemOID,ainsertbefore=[DropItemOID,siclass.CID])
   else:
         ret=MessageDialog('Operacje przeniesienia '+DragItemType+':'+DragItemName+' do '+DropItemType+':'+DropItemName+' jest niedostępna.',mtInformation,mbOK)
   return

