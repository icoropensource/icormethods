# -*- coding: windows-1250 -*-
# saved: 2021/06/09 11:03:44

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
import CLASSES_Library_NetBase_WWW_Server_ServerUtil as ServerUtil
import CLASSES_System_RepositoryManager_Utils_PGGenerator as PGGenerator
import string
import re
import os

def SearchText(atext,anewtext='',are=1):
   aclass=aICORDBEngine.Classes['CLASSES_System_ICORMethod']
   aobj=aclass.GetFirstObject()
   if are==1:
      atext=strLowerPL(atext)
      p1=re.compile(atext,re.I)
      lret=[]
      while aobj:                                            
         mtext=aobj.aMethodText
         if p1.search(mtext):
            sl=string.split(mtext,'\n')
            i=1
            for s in sl:
               if p1.search(s):
                  break
               i=i+1
            sl=string.split(aobj.aIDClassMethod,'_')
            bclass=aICORDBEngine.Classes[int(sl[0])]
            lret.append('  File "%s\\%s", line %d, in method'%(bclass.ClassPath,aobj.aMethodName,i))
            if anewtext:
               mtext=p1.sub(anewtext,mtext)
               aobj.aMethodText=mtext
         aobj.Next()
   else:
      btext=atext
      atext=strLowerPL(atext)
      lret=[]
      while aobj:
         mtext=strLowerPL(aobj.aMethodText)
         apos=string.find(mtext,atext)
         if apos>=0:
            sl=string.split(mtext,'\n')
            i=1
            for s in sl:
               if string.find(s,atext)>=0:
                  break
               i=i+1
            sl=string.split(aobj.aIDClassMethod,'_')
            bclass=aICORDBEngine.Classes[int(sl[0])]
            lret.append('  File "%s\\%s", line %d, in method'%(bclass.ClassPath,aobj.aMethodName,i))
            if anewtext:
               mtext=string.replace(aobj.aMethodText,btext,anewtext)
               aobj.aMethodText=mtext
         aobj.Next()
   lret.sort()
   for s in lret:
      print s
   return

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   InfoStatus('')
   aclass=aICORDBEngine.Classes[CID]
   if FieldName=='Class':
      if Value=='Klasa pochodna':
         s=InputString('Nowa klasa','Nazwa:','')
         if s=='':
            return
         aICORDBEngine.Classes.AddClass(OID,s)
      elif Value=='Wszystkie obiekty':
         bclass=aICORDBEngine.Classes[OID]
         bclass.SelectObjects(acaption=bclass.NameOfClass,adisabletoolbar=0,adisableediting=0)
      elif Value=='Pokaż strukturę':
         bclass=aICORDBEngine.Classes[OID]
         bclass.SelectInStructure()
      elif Value=='Zestawienia':
         bclass=aICORDBEngine.Classes[OID]
         bclass.SelectSummaries()
      elif Value=='Szukaj':
         bclass=aICORDBEngine.Classes[OID]
         bclass.SelectSearchInClass()
      elif Value=='Przejdź do klasy':
         s=InputString('Wybierz klasę:','ID','')
         if not s:
            return
         try:
            acid=int(s)
            aclass=aICORDBEngine.Classes[acid]
         except:
            aclass=aICORDBEngine.Classes[s]
         if aclass is None:
            return
         aclass.SelectInRepository()
      elif Value=='Właściwości pól':
         bclass=aICORDBEngine.Classes[OID]
         bclass.SelectClassFieldProperties()
      elif Value=='Pole':
         fclass=aICORDBEngine.Classes['CLASSES/System/Dialog/FieldAdd']
         fclass.DoFieldAdd(FieldName,OID,Value)
      elif Value=='Metoda':
         mclass=aICORDBEngine.Classes['CLASSES/System/Dialog/MethodAdd']
         mclass.DoMethodAdd(FieldName,OID,Value)
      elif Value=='Obiekt':
         bclass=aICORDBEngine.Classes[OID]
         s=InputString('Dodaj obiekt','OID:','')
         try:
            boid=int(s)
         except:
            boid=-1
         if boid>=0:
            if not bclass.ObjectExists(boid):
               bclass.CreateObjectByID(boid)
            bclass.EditObject(boid,atoolbar=1)
      elif Value=='Skasuj klasę':
         bclass=aICORDBEngine.Classes[OID]
         if MessageDialog('Czy jestes pewien, że chcesz skasować klasę '+bclass.NameOfClass+'?',mtConfirmation,mbYesNoCancel)!=mrYes:
            return
         aICORDBEngine.Classes.DeleteClass(OID)
      elif Value=='Replikuj dane':
         aclass=aICORDBEngine.Classes['CLASSES_System_Dialog_Replikacja_Send']
         aclass.DoSendReplication(FieldName,OID,Value)
      elif Value=='Pobierz replikację':
         aclass=aICORDBEngine.Classes['CLASSES_System_Dialog_Replikacja_Receive']
         aclass.DoReceiveReplication(FieldName,OID,Value)
      elif Value=='Sprawdź referencje':
         from CLASSES_Library_ICORBase_Replication_RevRefs_CheckReferences import ReferencesChecker
         bclass=aICORDBEngine.Classes[OID]
         acrefs=ReferencesChecker()
         acrefs.ForEachClass(bclass)
         acrefs.Dump()
      elif Value=='Sprawdź obiekty w klasie słownikowej':
         aclass=aICORDBEngine.Classes['CLASSES_System_Dialog_ClassRemoveNonReferencedObjects']
         aclass.DoRemoveNonRefObjects('',OID,'')
      elif Value=='Drukuj strukturę repozytorium':
         aclass=aICORDBEngine.Classes['CLASSES_System_Dialog_RepositoryUtil_CheckFields']
         aclass.DoCheckFields(FieldName,OID,Value)
      elif Value=='Ustaw kardynalność pól':
         bclass=aICORDBEngine.Classes[OID]
         afields=bclass.GetFieldsList()
         for afname in afields:
            afi=bclass.FieldsByName(afname)
            if afi.ClassOfType is None:
               continue
            w=1
            aoid=bclass.FirstObject()
            while aoid>=0:
               arefs=afi.GetRefList(aoid)
               if len(arefs)>1:
                  w=0
                  break
               aoid=bclass.NextObject(aoid)
            if w:
               afi.FieldEditor='ObjectsList'
               print 'zmiana atrybutu FieldEditor dla pola:',afi.Name
      elif Value=='Dodaj menu WWW dla edycji obiektów':
         bclass=aICORDBEngine.Classes[OID]
         mclass=aICORDBEngine.Classes.MetaClass.aWWWMenu.ClassOfType
         moid=mclass.AddObject()
         mclass.Name[moid]='Edycja'
         mclass.Caption[moid]='Edycja'
         mclass.Action[moid]='12:677:'
         mclass.ParamItem[moid]=bclass.ClassPath
         if not mclass.EditObject(moid):
            mclass.DeleteObject(moid)
            return
         aICORDBEngine.Classes.MetaClass.aWWWMenu.AddRefs(bclass.CID,[moid,mclass.CID])
      elif Value=='Dodaj menu WWW dla kasowania obiektów':
         bclass=aICORDBEngine.Classes[OID]
         mclass=aICORDBEngine.Classes.MetaClass.aWWWMenu.ClassOfType
         moid=mclass.AddObject()
         mclass.Name[moid]='Usuń pozycję'
         mclass.Caption[moid]='Usuń pozycję'
         mclass.ConfirmHRef[moid]='1'
         mclass.Action[moid]='13:677:'
         mclass.ParamItem[moid]=bclass.ClassPath
         if not mclass.EditObject(moid):
            mclass.DeleteObject(moid)
            return
         aICORDBEngine.Classes.MetaClass.aWWWMenu.AddRefs(bclass.CID,[moid,mclass.CID])
      elif Value=='Dodaj menu WWW dla uruchamiania metod':
         bclass=aICORDBEngine.Classes[OID]
         mclass=aICORDBEngine.Classes.MetaClass.aWWWMenu.ClassOfType
         moid=mclass.AddObject()
         mclass.Name[moid]='Metody'
         mclass.Caption[moid]='Metody'
         mclass.Action[moid]='14:677:'
         mclass.ParamItem[moid]=bclass.ClassPath
         if not mclass.EditObject(moid):
            mclass.DeleteObject(moid)
            return
         aICORDBEngine.Classes.MetaClass.aWWWMenu.AddRefs(bclass.CID,[moid,mclass.CID])
      elif Value=='Wyświetl skrypt PG - create':
         bclass=aICORDBEngine.Classes[OID]
         agenerator=PGGenerator.PGGenerator(bclass)
         agenerator.GenerateCreate()
      elif Value=='Wyświetl skrypt PG - select':
         bclass=aICORDBEngine.Classes[OID]
         agenerator=PGGenerator.PGGenerator(bclass)
         agenerator.GenerateSelect()
      elif Value=='Wyświetl skrypt PG - select JSONB':
         bclass=aICORDBEngine.Classes[OID]
         agenerator=PGGenerator.PGGenerator(bclass)
         agenerator.GenerateSelectJSONB(aoidinclude=1,aprint=1)
      elif Value=='Skasuj wszystkie obiekty':
         bclass=aICORDBEngine.Classes[OID]
         if MessageDialog('Czy jestes pewien, że chcesz skasować wszystkie obiekty w klasie '+bclass.NameOfClass+'?',mtConfirmation,mbYesNoCancel)!=mrYes:
            return
         class CIterator(ICORRepositoryIterator):
            def __init__(self):
               ICORRepositoryIterator.__init__(self)
            def OnPreClass(self,aclass):
               aclass.ClearAllObjects()
            def OnPostField(self,aclass,afieldname):
               afield=aclass.FieldsByName(afieldname)
               afield.ClearAllValues()
         CIterator().ForEachClass(bclass)
      elif Value=='Tekst w metodach':
         aclass=aICORDBEngine.Classes['CLASSES_System_Dialog_RepositoryUtil_TextSearch']
         aclass.DoTextSearch(FieldName,OID,Value)
         return
         xtext=InputString('Znajdź tekst w metodach','Ciąg znaków:','')
         if xtext:
            SearchText(xtext,'',are=0)
#      elif Value=='Tekst RE w metodach':
#         aclass=aICORDBEngine.Classes['CLASSES_System_Dialog_RepositoryUtil_TextSearch']
#         aclass.DoTextSearch(FieldName,OID,Value)
#         return
#         xtext=InputString('Znajdź tekst w metodach','Wyrażenie regularne:','')
#         if xtext:
#            SearchText(xtext,'')
      elif Value=='Formatuj':
         aclass=aICORDBEngine.Classes['CLASSES/System/Dialog/ClassParameters']
         aclass.DoClassParameters(FieldName,OID,Value)

   elif FieldName=='Field':
      bclass=aICORDBEngine.Classes[OID]
      afieldname,amenu=tuple(string.split(Value,chr(255)))
      if amenu=='Skasuj pole':
         if MessageDialog('Czy jestes pewien, że chcesz skasować pole '+afieldname+'?',mtConfirmation,mbYesNoCancel)!=mrYes:
            return
         bclass.DeleteField(afieldname)
      elif amenu=='Referencja zwrotna do tej klasy':
         bfield=bclass.FieldsByName(afieldname)
         fclass=aICORDBEngine.Classes['CLASSES/System/Dialog/FieldAdd']
         ret=fclass.DoFieldAdd('',bfield.ClassOfType.CID,string.join([bclass.NameOfClass,'','','Class',bclass.ClassPath],ServerUtil.SPLIT_CHAR_PARAM))
         if ret=='1':
            print '#method OnObjectDelete:'
            print '   aclass.%s.DeleteReferencedObjects(OID)'%bfield.Name
            print '#method OnFieldChange:'
            print "   if FieldName in ['%s',]:"%bfield.Name
            print "      afield=aclass.FieldsByName(FieldName)"
            print "      afield.UpdateReferencedObjects(OID)"
      elif amenu=='Pokaż wartości':
         bfield=bclass.FieldsByName(afieldname)
         bfield.SelectValues()
      elif amenu=='Typ pola':
         bfield=bclass.FieldsByName(afieldname)
         bfield.ClassOfType.SelectInRepository()
      elif amenu=='Szukaj':
         bclass.SelectSearchInClass()
      elif amenu=='Formatuj':
         aclass=aICORDBEngine.Classes['CLASSES/System/Dialog/FieldParameters']
         aclass.DoFieldParameters(FieldName,OID,afieldname)
      elif amenu=='Zamień wartości pola':
         aclass=aICORDBEngine.Classes['CLASSES/System/Dialog/FieldReplaceValues']
         aclass.DoReplaceFieldValues(FieldName,OID,afieldname)
      elif amenu=='Skasuj puste referencje':
         aclass=aICORDBEngine.Classes['CLASSES_System_Dialog_FieldRemoveEmptyReferences']
         aclass.DoRemoveEmptyReferences(FieldName,OID,afieldname)
      elif amenu=='Uzupełnij pola UpdateRefs klasie słownikowej o BackRef':
         bfield=bclass.FieldsByName(afieldname)
         sfield=bclass.FieldsByName('SGTabID')
         dfield=bclass.FieldsByName('SGIsDeleted')
         rclass=bfield.ClassOfType
         if rclass is None:
            return
         rfields=rclass.GetFieldsList()
         rfield=None
         for arfieldname in rfields:
            rfield1=rclass.FieldsByName(arfieldname)
            if not rfield1.ClassOfType is None and rfield1.ClassOfType.CID==bclass.CID and rfield1.WWWUpdateRefs:
               rfield=rfield1
               break
         if rfield is None:
            return
         print 'znaleziono pole:',rfield.Name
         bobj=bclass.GetFirstObject()
         while bobj:
            brefs=bfield.GetRefList(bobj.OID)
            if not dfield is None and dfield.ValuesAsInt(bobj.OID):
               bobj.Next()
               continue
            while brefs:
               if rclass.ObjectExists(brefs.OID):
                  rrefs=rfield.GetRefList(brefs.OID)
                  if not rrefs.RefExists(bobj.OID):
                     print 'O1:',bobj.OID,'O2:',brefs.OID
                     rfield.AddRefs(brefs.OID,[bobj.OID,bobj.CID],asortedreffield=sfield,ainsertifnotexists=1)
               else:
                  print 'D1:',bobj.OID,'D2:',brefs.OID
               brefs.Next()
            bobj.Next()
         print 'koniec'
      elif amenu=='Zapisz wartości archiwalne':
         adir=InputDirectory()
         if not adir:
            return
         adir=FilePathAsSystemPath(adir)
         bfield=bclass.FieldsByName(afieldname)
         aoff=bfield.GetFirstDeletedOffset()
         i=0
         while aoff>=0:
            avalue=bfield.GetRecValueAsString(aoff)
            aoid=bfield.GetRecOID(aoff)
            if aoid>=0 and avalue and avalue!='Error!':
               adt=bfield.GetRecLastModification(aoff)
               alm=tdate2fmtstr(adt,delimiter='',longfmt=1)+'_'+ttime2fmtstr(adt,longfmt=1,delimiter='')
               fout=open(adir+'/%06d_%s_%06d_%s.py'%(bfield.CID,bfield.Name,aoid,alm),'w')
               fout.write(avalue)
               fout.close()
               i=i+1
            aoff=bfield.GetNextDeletedOffset(aoff)
         MessageDialog('Zgrano %d wartości archiwalnych'%i)
      elif amenu=='Zapisz wszystkie wartości':
         adir=InputDirectory()
         if not adir:
            return
         adir=FilePathAsSystemPath(adir)
         bfield=bclass.FieldsByName(afieldname)
         aoid=bclass.FirstObject()
         i=0
         while aoid>=0:
            avalue=bfield[aoid]
            if avalue and avalue!='Error!':
               fout=open(adir+'/%d.py'%(aoid,),'w')
               fout.write(avalue)
               fout.close()
               i=i+1
            aoid=bclass.NextObject(aoid)
         MessageDialog('Zgrano %d wartości'%i)
      elif amenu=='Importuj wartości z katalogu':
         adir=InputDirectory()
         if not adir:
            return
         adir=FilePathAsSystemPath(adir)
         bfield=bclass.FieldsByName(afieldname)
         l=os.listdir(adir)
         i=0
         for afilename in l:
            if not afilename:
               continue
            afilepath=adir+'/'+afilename
            print 'import:',afilepath
            fout=open(afilepath,'r')
            avalue=fout.read()
            fout.close()          
            aoid,aext=os.path.splitext(afilename)
            bfield[int(aoid)]=avalue
            i=i+1
         MessageDialog('Wgrano %d wartości'%i)
   elif FieldName=='Method':
      bclass=aICORDBEngine.Classes[OID]
      amethodname,amenu=tuple(string.split(Value,chr(255)))
      if amenu=='Skasuj metodę':
         if MessageDialog('Czy jestes pewien, że chcesz skasować metodę '+amethodname+'?',mtConfirmation,mbYesNoCancel)!=mrYes:
            return
         bclass.DeleteMethod(amethodname)
      elif amenu=='Uruchomienie metody':
         mclass=aICORDBEngine.Classes['CLASSES/System/Dialog/MethodExecute']
         mclass.DoMethodExecute(amethodname,OID,'')
      elif amenu=='Edycja metody':
         amethod=bclass.MethodsByName(amethodname)
         amethod.SelectInEditor()
      elif amenu=='Szukaj':
         bclass.SelectSearchInClass()
      elif amenu=='Zapisz wartości archiwalne':
         adir=InputDirectory()
         if not adir:
            return
         adir=FilePathAsSystemPath(adir)
         amethod=bclass.MethodsByName(amethodname)
         bfield=aICORDBEngine.Classes.MetaMethod.aMethodText
         aoff=bfield.GetFirstDeletedOffset()
         i=0
         while aoff>=0:
            avalue=bfield.GetRecValueAsString(aoff)
            aoid=bfield.GetRecOID(aoff)
            if aoid==amethod.MOID and avalue:
               adt=bfield.GetRecLastModification(aoff)
               alm=tdate2fmtstr(adt,delimiter='',longfmt=1)+'_'+ttime2fmtstr(adt,longfmt=1,delimiter='')
               fout=open(adir+'/%06d_%s_%06d_%s.py'%(bclass.CID,amethodname,aoid,alm),'w')
               avalue=string.replace(avalue,chr(13),'')
               fout.write(avalue)
               fout.close()
               i=i+1
            aoff=bfield.GetNextDeletedOffset(aoff)
         MessageDialog('Zgrano %d wartości archiwalnych'%i)
      elif amenu=='Formatuj':
         aclass=aICORDBEngine.Classes['CLASSES/System/Dialog/MethodParameters']
         aclass.DoMethodParameters(FieldName,OID,amethodname)

   elif FieldName=='StructureField':
      bclass=aICORDBEngine.Classes[OID]
      afieldpath,amenu=tuple(string.split(Value,chr(255)))
#      print bclass.NameOfClass,afieldpath
      if afieldpath:
         bfields=[]
         sfl=string.split(afieldpath,'\\')
         lclass=bclass
         for afieldname in sfl:
            lfield=lclass.FieldsByName(afieldname)
            bfields.append([lclass,lfield])
            lclass=lfield.ClassOfType
      else:
         bfields=[[bclass,None],]
#      for lclass,lfield in bfields:
#         if lfield is None:
#            print lclass.NameOfClass,'None'
#         else:
#            print lclass.NameOfClass,lfield.Name
      if amenu=='Pokaż w strukturze klas':
         if bfields==[]:
            return
         lclass,lfield=bfields[len(bfields)-1]
         if lfield is None:
            lclass.SelectInRepository()
         else:
            lfield.SelectInRepository()
      elif amenu=='Pokaż wartości':
         lclass,lfield=bfields[len(bfields)-1]
         if lfield is None:
            lclass.SelectObjects(acaption=lclass.NameOfClass,adisabletoolbar=0,adisableediting=0)
         else:
            lfield.SelectValues()
      elif amenu=='Dostęp do wszystkich wartości pola':
         if bfields==[]:
            return
         lclass,lfield=bfields[0]
         aline="""aclass=aICORDBEngine.Classes['%s']
aobj0=aclass.GetFirstObject()
while aobj0:"""%string.replace(lclass.ClassPath,'\\','_')
         lines=[aline,]
         if not lfield is None:
            level=1
            for lclass,lfield in bfields:
               if lfield.ClassOfType is None:
                  s='%sprint aobj%d.%s'%('   '*level,level-1,lfield.Name)
                  lines.append(s)
                  level=level-1
               else:
                  s='%saobj%d=aobj%d.%s'%('   '*level,level,level-1,lfield.Name)
                  lines.append(s)
                  s='%swhile aobj%d:'%('   '*level,level)
                  lines.append(s)
                  if level<len(bfields):
                     level=level+1
            for i in range(level,0,-1):
               s='%saobj%d.Next()'%('   '*(i+1),i)
               lines.append(s)
         lines.append('   aobj0.Next()\n')
         lines=string.join(lines,'\n')
         SetClipboard(lines)
         sl=string.split(lines,'\n')
         for aline in sl:
            print aline
      elif amenu=='Dostęp do jednej wartości pola':
         if bfields==[]:
            return
         lclass,lfield=bfields[0]
         aline1="aclass=aICORDBEngine.Classes['%s']"%string.replace(lclass.ClassPath,'\\','_')
         aline2="aobj0=aclass.GetFirstObject()"
         lines=[aline1,aline2]
         bline=[]
         if not lfield is None:
            for lclass,lfield in bfields:
               bline.append('.%s'%(lfield.Name))
         if lfield.ClassOfType is None:
            bline.insert(0,'avalue=aobj0')
         else:
            bline.insert(0,'aobj=aobj0')
         lines.append(string.join(bline,''))
         if lfield.ClassOfType is None:
            lines.append('if avalue is None:')
            lines.append("   print 'Empty!'")
            lines.append('else:')
            lines.append('   print avalue')
         else:
            lines.append('while aobj:')
            lines.append('   aobj.Next()')
         SetClipboard(string.join(lines,'\n'))
         for aline in lines:
            print aline

   elif FieldName=='WWWServer':
      ServerClass=aICORDBEngine.Classes['CLASSES_Library_NetBase_WWW_Server']
      ServerClass.EditObject(OID,acaption='Edycja parametrów serwera WWW',atoolbar=1)
   elif FieldName=='WWWIntroduction':
      ServerClass=aICORDBEngine.Classes['CLASSES_Library_NetBase_WWW_Server']
      ServerClass.EditObject(OID,acaption='Edycja parametrów serwera WWW',atoolbar=1)
   elif FieldName=='WWWMenu':
      ServerClass=aICORDBEngine.Classes['CLASSES_Library_NetBase_WWW_Server']
      ServerClass.EditObject(OID,acaption='Edycja parametrów serwera WWW',atoolbar=1)
   elif FieldName=='WWWMenuItem':
      from icorlib.wwwmenu.menuutil import ICORWWWMenuItem
      amenu=Value
      bmenu=ICORWWWMenuItem(UID,OID)
      if amenu=='Edycja':
         bmenu.MenuClass.EditObject(OID,acaption='Edycja WWW menu',atoolbar=1)
         bmenu.Refresh()
      elif amenu=='Podpozycja':
         coid=bmenu.MenuClass.AddObject()
         if bmenu.MenuClass.EditObject(coid,acaption='Edycja WWW menu',atoolbar=1):
            cmenu=ICORWWWMenuItem(UID,coid)
            bmenu.AddChildMenu(cmenu)
         else:
            bmenu.MenuClass.DeleteObject(coid)
      elif amenu=='Pozycja przed':
         coid=bmenu.MenuClass.AddObject()
         if bmenu.MenuClass.EditObject(coid,acaption='Edycja WWW menu',atoolbar=1):
            cmenu=ICORWWWMenuItem(UID,coid)
            bmenu.InsertMenuBefore(cmenu)
         else:
            bmenu.MenuClass.DeleteObject(coid)
      elif amenu=='Zestawienie':
         sclass=bmenu.MenuClass.Summaries.ClassOfType
         soid=sclass.AddObject()
         sclass.ParentMenu[soid]=[bmenu.oid,bmenu.MenuClass.CID]
         if sclass.EditObject(soid,acaption='Edycja parametrów zestawienia',atoolbar=1):
            bmenu.AddSummary(soid,asumminfo=1)
         else:
            sclass.DeleteObject(soid)
      elif amenu=='Raport':
         sclass=bmenu.MenuClass.Report.ClassOfType
         soid=sclass.AddObject()
         sclass.ParentMenu[soid]=[bmenu.oid,bmenu.MenuClass.CID]
         if sclass.EditObject(soid,acaption='Edycja parametrów raportu',atoolbar=1):
            bmenu.AddReport(soid)
         else:
            sclass.DeleteObject(soid)
      elif amenu=='Wyłącz pozycję':
         bmenu.StoreAccessLevel(adisabled=1)
      elif amenu=='Przywróc widoczność':
         bmenu.RestoreAccessLevel()
      elif amenu=='Odłącz możliwość edycji treści':
         bmenu.SetEditMode(adisable=1)
      elif amenu=='Skasuj':
         if MessageDialog('Czy jestes pewien, że chcesz skasować menu '+bmenu.Caption+'?',mtConfirmation,mbYesNoCancel)!=mrYes:
            return
         bmenu.RemoveMenuRefFromParentMenu(adelete=1)
      elif amenu=='Zapamiętaj':
         fname=InputFile(bmenu.Caption+'.html')
         if not fname:
            return
         fname=FilePathAsSystemPath(fname)
         lms=aICORDBEngine.Variables._LastWWWMenuItemPopupMenuSelected
         m1,m2='Opis HTML','Treść HTML'
         if lms==m1:
            atext=bmenu.PageHTMLInfo
         elif lms==m2:
            atext=bmenu.PageHTML
         fin=open(fname,'w')
         try:
            fin.write(atext)
         finally:
            fin.close()
      elif amenu=='Sprawdź treść':
         bmenu.SprawdzTresc()
         print 'Koniec'
      elif amenu=='Generuj projekt HTML Help':
         from CLASSES_Library_NetBase_WWW_HTML_HelpGenerator_Project_Generate import HTMLHelpGenerator
         agenerator=HTMLHelpGenerator(bmenu)
         agenerator.DoGenerate()
      elif amenu=='Otwórz':
         fname=InputFile(bmenu.Caption+'.html')
         if not fname:
            return
         fname=FilePathAsSystemPath(fname)
         lms=aICORDBEngine.Variables._LastWWWMenuItemPopupMenuSelected
         m1,m2='Opis HTML','Treść HTML'
         fin=open(fname,'r')
         try:
            atext=fin.read()
         finally:
            fin.close()
         if lms==m1:
            bmenu.PageHTMLInfo=atext
         elif lms==m2:
            bmenu.PageHTML=atext
      elif amenu=='Czyść':
         lms=aICORDBEngine.Variables._LastWWWMenuItemPopupMenuSelected
         m1,m2='Opis HTML','Treść HTML'
         if lms==m1:
            s1='opis HTML'
         elif lms==m2:
            s1='treść HTML'
         if MessageDialog('Czy jesteś pewien, że chcesz skasować '+s1+'?',mtConfirmation,mbYes+mbNo)!=mrYes:
            return
         if lms==m1:
            bmenu.PageHTMLInfo=''
         elif lms==m2:
            bmenu.PageHTML=''
      elif amenu=='Edycja HTML':
         lms=aICORDBEngine.Variables._LastWWWMenuItemPopupMenuSelected
         m1,m2='Opis HTML','Treść HTML'
         if lms==m1:
            s1='PageHTMLInfo'
         elif lms==m2:
            s1='PageHTML'
         aICORDBEngine.RepositoryChange('HTMLEdit',bmenu.MenuClass.CID,bmenu.oid,s1,bmenu.Caption[:16],bmenu.Caption)
      elif amenu=='Zaznacz zestawienia typu Worksheet':
         bmenu.SetWorksheetQueries()
      elif amenu=='Export XML podpozycji':
         fname=InputFile(bmenu.Caption)
         if not fname:
            return
         fname=FilePathAsSystemPath(fname)
         fout=open(fname,'w')
         try:
            bmenu.XMLExportSubItems(fout)
         finally:
            fout.close()
         MessageDialog('Koniec exportu')
      elif amenu=='Import XML podpozycji':
         fname=InputFile(bmenu.Caption)
         if not fname:
            return
         bmenu.XMLImportSubItems(fname)
         MessageDialog('Koniec importu')
      else:
         aICORDBEngine.Variables._LastWWWMenuItemPopupMenuSelected=amenu
   elif FieldName=='WWWReportItem':
      from icorlib.wwwmenu.menuutil import ICORWWWMenuItem
      amenu=Value
      ReportClass=aICORDBEngine.Classes['CLASSES_Library_NetBase_WWW_Dictionary_Report_Item']
      sobj=ReportClass[OID]
      bmenu=ICORWWWMenuItem(UID,sobj.ParentMenu.OID)
      if amenu=='Edycja':
         ReportClass.EditObject(OID,acaption='Edycja parametrów raportu',atoolbar=1)
         bmenu.RefreshReports()
      elif amenu=='Przejdź do metody':
         s=ReportClass.PageMethod[OID]
         s=string.replace(s,'\\','_')
         s=string.replace(s,'/','_')
         sl=string.split(s,'_')
         amname=sl[len(sl)-1]
         acpath=string.join(sl[:-1],'_')
         bclass=aICORDBEngine.Classes[acpath]
         if bclass is None:
            return
         amethod=bclass.MethodsByName(amname)
         if amethod is None:
            return
         aline=ReportClass.PageMethodEvent[OID]
         amethod.SelectInEditor(aline)
      elif amenu=='Skasuj':
         if MessageDialog('Czy jesteś pewien, że chcesz skasować ten raport?',mtConfirmation,mbYes+mbNo)!=mrYes:
            return
         bmenu.DeleteReport(OID,1)
   elif FieldName=='WWWSummaryItem':
      from icorlib.wwwmenu.menuutil import ICORWWWMenuItem
      amenu=Value
      SummaryClass=aICORDBEngine.Classes['CLASSES_Library_NetBase_WWW_Dictionary_Report_SummaryInfo']
      sobj=SummaryClass[OID]
      bmenu=ICORWWWMenuItem(UID,sobj.ParentMenu.OID)
      if amenu=='Edycja':
         SummaryClass.EditObject(OID,acaption='Edycja parametrów zestawienia',atoolbar=1)
         bmenu.RefreshSummaries()
      elif amenu=='Pokaż zestawienie':
         summoid=SummaryClass.Summary.ValuesAsInt(OID)
         if summoid>=0:
            SummaryEdit(summoid)
            bmenu.RefreshSummaries()
      elif amenu=='Przejdź do klasy bazowej zestawienia':
         summoid=SummaryClass.Summary.ValuesAsInt(OID)
         if summoid>=0:
            sclass=aICORDBEngine.Classes['CLASSES_System_SummaryItem']
            scid=sclass.OwnerCID.ValuesAsInt(summoid)
            tclass=aICORDBEngine.Classes[scid]
            if not tclass is None:
               tclass.SelectInRepository()
      elif amenu=='Duplikuj zestawienie':
         from CLASSES_Library_ICORBase_Interface_ICORSummary import DoSummaryLoad,DoSummarySave
         summoid=SummaryClass.Summary.ValuesAsInt(OID)
         if summoid>=0:
            sclass=aICORDBEngine.Classes['CLASSES_System_SummaryItem']
            s=DoSummarySave(summoid)
            soid=DoSummaryLoad(s,ownerClass=sclass.OwnerCID.ValuesAsInt(summoid))
            bmenu.AddSummary(soid)
      elif amenu=='Przejdź do metody':
         s=SummaryClass.CustomPageByMethod[OID]
         s=string.replace(s,'\\','_')
         s=string.replace(s,'/','_')
         sl=string.split(s,'_')
         amname=sl[len(sl)-1]
         acpath=string.join(sl[:-1],'_')
         bclass=aICORDBEngine.Classes[acpath]
         amethod=bclass.MethodsByName(amname)
         amethod.SelectInEditor('DoCustomPageByMethod')
      elif amenu=='Skasuj':
         if MessageDialog('Czy jesteś pewien, że chcesz skasować to zestawienie?',mtConfirmation,mbYes+mbNo)!=mrYes:
            return
         bmenu.DeleteSummary(OID,1)
   elif FieldName=='RFSServer':
      ServerClass=aICORDBEngine.Classes['CLASSES_Library_NetBase_WWW_Server']
      if Value=='Edycja':
         ServerClass.EditObject(OID,acaption='Edycja parametrów serwera WWW',atoolbar=1)
   elif FieldName=='RFSCollection':
      from CLASSES_Library_NetBase_RemoteFileSystem_Item_RFSInterface import ICORRFSItem
      arfsitem=ICORRFSItem(UID,OID)
      if Value=='Edycja':
         arfsitem.RFSClass.EditObject(OID,acaption='Edycja elementu RFS',atoolbar=1)
      elif Value=='Otwórz':
         ExecuteShellCommand(arfsitem.Location)
      elif Value=='Kasuj':
         if MessageDialog('Czy jestes pewien, że chcesz skasować kolekcję '+arfsitem.Name+'?',mtConfirmation,mbYesNoCancel)!=mrYes:
            return
         arfsitem.RemoveItem()
      elif Value=='Aktualizuj z dysku':
         arfsitem.UpdateFromDisk()
   elif FieldName=='RFSItem':
      from CLASSES_Library_NetBase_RemoteFileSystem_Item_RFSInterface import ICORRFSItem
      arfsitem=ICORRFSItem(UID,OID)
      if Value=='Edycja':
         arfsitem.RFSClass.EditObject(OID,acaption='Edycja elementu RFS',atoolbar=1)
      elif Value=='Uruchom':
         ExecuteShellCommand(arfsitem.Location)
      elif Value=='Kasuj':
         if MessageDialog('Czy jestes pewien, że chcesz skasować pozycję '+arfsitem.Name+'?',mtConfirmation,mbYesNoCancel)!=mrYes:
            return
         arfsitem.RemoveItem()
   elif FieldName=='SecurityUserUser':
      if Value=='Edycja':
         aICORDBEngine.User.EditObject(OID)
   elif FieldName=='SecurityGroupUser':
      if Value=='Edycja':
         aclass=aICORDBEngine.Classes['CLASSES_System_Group']
         aclass.EditObject(OID)
   elif FieldName=='SecurityAccessLevelUser':
      if Value=='Edycja':
         aclass=aICORDBEngine.Classes['CLASSES_System_GroupAccessLevel']
         aclass.EditObject(OID)
   elif FieldName=='SecurityProfileGroupUser':
      if Value=='Edycja':
         aclass=aICORDBEngine.Classes['CLASSES_System_SystemDictionary_ProfileGroup']
         aclass.EditObject(OID)
   elif FieldName=='EditorText':
      if Value=='XML Encode':
         from CLASSES_Library_NetBase_Utils_XMLUtil import GetAsXMLString
         s=GetCurrentEditorText()
         s=GetAsXMLString(s)
         s=string.replace(s,'&#10;','&#10;\n')
         SetCurrentEditorText(s)
      elif Value=='XML Decode':
         from xml.parsers import xmllib
         s=GetCurrentEditorText()
         s=string.replace(s,chr(10),'')
         s=string.replace(s,chr(13),'')
         aparser=xmllib.XMLParser()
         s=aparser.translate_references(s)
         SetCurrentEditorText(s)
      elif Value=='Otwórz plik i dokonaj konwersji tabulatorów':
         afname=InputFile()
         if not afname:
            return
         st=InputString('Jeden tabulator to ... ','spacje','8')
         try:
            t=int(st)
         except:
            t=-1
         if t<1:
            return
         f=open(afname,'r')
         s=f.read()
         f.close()
         s=string.expandtabs(s,t)
         SetCurrentEditorText(s)
      elif Value=='Py2HTML':
         from CLASSES_Library_NetBase_WWW_HTML_Util_Py2HTML import PrettyPyPrint
         s=GetCurrentEditorText()
         s=PrettyPyPrint(s)
         SetClipboard(s)
   elif FieldName=='HTMLEditorText':
      if Value=='XML Encode':
         from CLASSES_Library_NetBase_Utils_XMLUtil import GetAsXMLString
         s=GetCurrentHTMLEditorText()
         s=GetAsXMLString(s)
         s=string.replace(s,'&#10;','&#10;\n')
         SetCurrentHTMLEditorText(s)
      elif Value=='XML Decode':
         from xml.parsers import xmllib
         s=GetCurrentHTMLEditorText()
         s=string.replace(s,chr(10),'')
         s=string.replace(s,chr(13),'')
         aparser=xmllib.XMLParser()
         s=aparser.translate_references(s)
         SetCurrentHTMLEditorText(s)
      elif Value=='ISO2Win':
         from CLASSES_Library_NetBase_WWW_HTML_Util_ConversionsPL import Win2ISO,ISO2Win
         s=GetCurrentHTMLEditorText()
         s=ISO2Win(s)
         SetCurrentHTMLEditorText(s)
      elif Value=='Win2ISO':
         from CLASSES_Library_NetBase_WWW_HTML_Util_ConversionsPL import Win2ISO,ISO2Win
         s=GetCurrentHTMLEditorText()
         s=Win2ISO(s)
         SetCurrentHTMLEditorText(s)
   return


