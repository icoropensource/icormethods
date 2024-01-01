# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
from CLASSES_Library_NetBase_WWW_HTML_Tree_SimpleLinks_Main import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import CLASSES_Library_ICORBase_Interface_ICORSecurity as ICORSecurity
import string
import time

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('WybranyRozdzial',atype=mt_String,ahidden=1,adefaultcheck=1)
   awwweditor.RegisterField('KopiujRozdzial',adisplayed='Kopiuj rozdział (jeszcze nieaktywne!)',atype=mt_Boolean)
   awwweditor.RegisterField('WstawPrzedWybranaPozycje',adisplayed='Wstaw przed wybraną pozycję',atype=mt_Boolean)
   return awwweditor

def OnBeforeWWWAction(aobj,amenu,file):
   w=1
   if 0:
      w=w and ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelView',amenu.uid)
   if 0:
      w=w and ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelEdit',amenu.uid)
   if 0:
      w=w and ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelDelete',amenu.uid)
   return w

def DodajRozdzialy(anode,robj,auid,asrcoid):
   while robj:
#      bnode=anode.AddNode(robj.Naglowek,)
      if robj.OID!=asrcoid and ICORSecurity.CheckRecursiveAccessLevelForUser(robj,'AccessLevelView',auid):
         stext=string.replace(robj.Naglowek,'"','')
         stext=string.replace(stext,"'",'')
         bnode=anode.AddNode(robj.Naglowek,aonclick="javascript:jQuery('#WybranyRozdzial').val('%d');document.getElementById('ChapterName').innerHTML='%s';"%(robj.OID,XMLUtil.GetAsXMLStringNoPL(stext)))
         sobj=robj.PodRozdzialy
         if sobj:
            DodajRozdzialy(bnode,sobj,auid,asrcoid)
      robj.Next()

def OnWWWAction(aobj,amenu,file):
   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   if amenu.Action=='ObjectApplyMethods':
      file.write('<div><b>Wybrany rozdział:</b>&nbsp;<span name=ChapterName id=ChapterName>...</span></div><br>')
      asrcoid=aobj.OID
      print 'asrcoid:',asrcoid
      atree=SimpleLinksHTMLTree('Wybierz rozdział docelowy:')
      while 1:
         pobj=aobj.Struktura
         if pobj:
            break
         aobj=aobj.NadRozdzial
      robj=pobj.Rozdzialy
      DodajRozdzialy(atree.RootNode,robj,amenu.uid,asrcoid)
      atree.Write(file)
      awwweditor.Write(acaption='Przenieś')
   return 0 # show back reference to main object (1-link, 2-button)

def UpdateSGTabID(dobj):
   atabid=10
   while dobj:
      dobj.SGTabID=atabid
      atabid=atabid+10
      dobj.Next()

def OnWWWActionSubmit(aobj,amenu,areport,file):
   if not areport['refMode']:
      awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
      if awwweditor['WybranyRozdzial']:
         robj=aobj.Class[int(awwweditor['WybranyRozdzial'])]
         if robj.OID!=aobj.OID:
            file.write('<h2>Rozdział przenoszony : %s</h2>'%aobj.Naglowek)
            file.write('<h2>Rozdział docelowy : %s</h2>'%robj.Naglowek)
            rclass=aobj.Class
            soid=aobj.OID
            doid=robj.OID
            wib=ICORUtil.str2bool(awwweditor['WstawPrzedWybranaPozycje'])
            wcopy=ICORUtil.str2bool(awwweditor['KopiujRozdzial'])
            if wib:
               aobj.SGTabID=robj.Class.SGTabID.ValuesAsInt(robj.OID)-1
               if aobj.NadRozdzial:
                  noid=aobj.NadRozdzial.OID
                  rclass.PodRozdzialy.DeleteRefs(noid,[soid,rclass.CID])
               else:
                  toid=aobj.Struktura.OID
                  sclass=aobj.Struktura.Class
                  sclass.Rozdzialy.DeleteRefs(toid,[soid,rclass.CID])
               if robj.NadRozdzial:
                  noid=robj.NadRozdzial.OID
                  rclass.PodRozdzialy.AddRefs(noid,[soid,rclass.CID],ainsertbefore=[doid,rclass.CID])
                  rclass.Struktura[soid]=''
                  dobj=rclass[noid].PodRozdzialy
               else:
                  toid=robj.Struktura.OID
                  sclass=robj.Struktura.Class
                  rclass.NadRozdzial[soid]=''
                  sclass.Rozdzialy.AddRefs(toid,[soid,rclass.CID],ainsertbefore=[doid,rclass.CID])
                  dobj=sclass[toid].Rozdzialy
               UpdateSGTabID(dobj)
            else:
               aobj.SGTabID=99999
               if aobj.NadRozdzial:
                  noid=aobj.NadRozdzial.OID
                  rclass.PodRozdzialy.DeleteRefs(noid,[soid,rclass.CID])
                  rclass.PodRozdzialy.AddRefs(doid,[soid,rclass.CID],asortedreffield=rclass.SGTabID,aremoveexisting=1)
                  rclass.Struktura[soid]=''
               else:
                  toid=aobj.Struktura.OID
                  sclass=aobj.Struktura.Class
                  rclass.Struktura[soid]=''
                  sclass.Rozdzialy.DeleteRefs(toid,[soid,rclass.CID])
                  rclass.PodRozdzialy.AddRefs(doid,[soid,rclass.CID],asortedreffield=rclass.SGTabID,aremoveexisting=1)
               dobj=rclass[doid].PodRozdzialy
               UpdateSGTabID(dobj)
            file.write('<h1><font color="green">Rozdział został przeniesiony. Sprawdź czy atrybut TabID jest poprawnie ustawiony w nowej strukturze i pamiętaj o odświeżeniu drzewa rozdziałów w menu.</font></h1>')
         else:
            file.write('<h1><font color="red">Rozdział docelowy i żródłowy są tymi samymi rozdziałami.</font></h1>')
      else:
         file.write('<h1><font color="red">Proszę wybrać rozdział docelowy.</font></h1>')
      awwweditor.WriteObjectView(aobj,asbutton=1)

def PrepareResultXMLFile(file,aaction,atext):
   xmlfile=XMLUtil.MXMLFile(file)
   xmlfile.Header()
   xmlfile.TagOpen('result')
   d={}
   d['action']=aaction
   d['text']=atext
   xmlfile.TagOpen('item',d,aclosetag=1)
   xmlfile.TagClose('result')
   xmlfile.close()

def DoMenuWorkflowChapterMove(file,coid1,coid2,aparam,UID):
   bclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Struktura']
   rclass=bclass.Rozdzialy.ClassOfType

   if not rclass.ObjectExists(coid1):
      PrepareResultXMLFile(file,'BAD','Błędny OID rozdziału źródłowego')
      return
   if not rclass.ObjectExists(coid2):
      PrepareResultXMLFile(file,'BAD','Błędny OID rozdziału docelowego')
      return
   if not aparam in ['0','1']:
      PrepareResultXMLFile(file,'BAD','Błędny parametr docelowy')
      return
   aobj=rclass[coid1]
   robj=rclass[coid2]
   sobj=robj.AsObject()
   while sobj:
      if aobj.OID==sobj.OID:
         PrepareResultXMLFile(file,'BAD','Rozdział docelowy jest podrozdziałem rozdziału źródłowego')
         return
      sobj=sobj.NadRozdzial

   if not ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelEdit'):
      PrepareResultXMLFile(file,'BAD','Brak uprawnień do rozdziału źródłowego')
      return
   if aparam=='0':
      if not ICORSecurity.CheckRecursiveAccessLevelForUser(robj,'AccessLevelEdit'):
         PrepareResultXMLFile(file,'BAD','Brak uprawnień do rozdziału docelowego')
         return
   elif aparam=='1':
      if robj.NadRozdzial:
         if not ICORSecurity.CheckRecursiveAccessLevelForUser(robj.NadRozdzial,'AccessLevelEdit'):
            PrepareResultXMLFile(file,'BAD','Brak uprawnień do rozdziału nadrzędnego')
            return
      else:
         if not ICORSecurity.CheckRecursiveAccessLevelForUser(robj.Struktura,'AccessLevelEdit'):
            PrepareResultXMLFile(file,'BAD','Brak uprawnień do struktury rozdziałów')
            return

   soid=aobj.OID
   doid=robj.OID
   wib=0
   if aparam=='1':
      wib=1
   if wib:
      aobj.SGTabID=robj.Class.SGTabID.ValuesAsInt(robj.OID)-1
      if aobj.NadRozdzial:
         noid=aobj.NadRozdzial.OID
         rclass.PodRozdzialy.DeleteRefs(noid,[soid,rclass.CID])
      else:
         toid=aobj.Struktura.OID
         sclass=aobj.Struktura.Class
         sclass.Rozdzialy.DeleteRefs(toid,[soid,rclass.CID])
      if robj.NadRozdzial:
         noid=robj.NadRozdzial.OID
         rclass.PodRozdzialy.AddRefs(noid,[soid,rclass.CID],ainsertbefore=[doid,rclass.CID])
         rclass.Struktura[soid]=''
         dobj=rclass[noid].PodRozdzialy
      else:
         toid=robj.Struktura.OID
         sclass=robj.Struktura.Class
         rclass.NadRozdzial[soid]=''
         sclass.Rozdzialy.AddRefs(toid,[soid,rclass.CID],ainsertbefore=[doid,rclass.CID])
         dobj=sclass[toid].Rozdzialy
      UpdateSGTabID(dobj)
   else:
      aobj.SGTabID=99999
      if aobj.NadRozdzial:
         noid=aobj.NadRozdzial.OID
         rclass.PodRozdzialy.DeleteRefs(noid,[soid,rclass.CID])
         rclass.PodRozdzialy.AddRefs(doid,[soid,rclass.CID],asortedreffield=rclass.SGTabID,aremoveexisting=1)
         rclass.Struktura[soid]=''
      else:
         toid=aobj.Struktura.OID
         sclass=aobj.Struktura.Class
         rclass.Struktura[soid]=''
         sclass.Rozdzialy.DeleteRefs(toid,[soid,rclass.CID])
         rclass.PodRozdzialy.AddRefs(doid,[soid,rclass.CID],asortedreffield=rclass.SGTabID,aremoveexisting=1)
      dobj=rclass[doid].PodRozdzialy
      UpdateSGTabID(dobj)

   PrepareResultXMLFile(file,'OK','Rozdział przeniesiony')

def PrepareResultJSONFile(file,aaction,atext):
   file.write('{status:"%s",info:"%s"}'%(aaction,atext))

def DoMenuWorkflowChapterMoveDrag(file,coid1,coid2,atype,arel1,arel2,UID):
   sclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Struktura']
   gclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_GrupaRozdzialow']
   wclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Struktura']
   rclass=sclass.Rozdzialy.ClassOfType

   if 0:
      print 'DoMenuWorkflowChapterMoveDrag'
      print '  coid1',coid1,type(coid1)
      print '  coid2',coid2,type(coid2)
      print '  atype',atype,type(atype)
      print '  arel1',arel1,type(arel1)
      print '  arel2',arel2,type(arel2)
      print '  UID',UID,type(UID)

   if (arel1=='chapter') and not rclass.ObjectExists(coid1):
      PrepareResultJSONFile(file,'BAD','Błędny OID rozdziału źródłowego')
      return
   if (arel2=='chapter') and not rclass.ObjectExists(coid2):
      PrepareResultJSONFile(file,'BAD','Błędny OID rozdziału docelowego')
      return
   if (arel2=='chaptergroup') and not gclass.ObjectExists(coid2):
      PrepareResultJSONFile(file,'BAD','Błędny OID grupy docelowej')
      return
   if (arel2=='menustruct') and not wclass.ObjectExists(coid2):
      PrepareResultJSONFile(file,'BAD','Błędny OID grupy docelowej')
      return
   if not atype in ['before','after','inside']:
      PrepareResultJSONFile(file,'BAD','Błędny parametr docelowy')
      return
   if not arel1 in ['chapter',]:
      PrepareResultJSONFile(file,'BAD','Błędny obiekt źródłowy')
      return
   if not arel2 in ['chaptergroup','chapter','menustruct']:
      PrepareResultJSONFile(file,'BAD','Błędny obiekt docelowy')
      return

   if arel1=='chapter' and arel2=='chapter':
      aobj=rclass[coid1]
      robj=rclass[coid2]
      sobj=robj.AsObject()
      while sobj:
         if aobj.OID==sobj.OID:
            PrepareResultJSONFile(file,'BAD','Rozdział docelowy jest podrozdziałem rozdziału źródłowego')
            return
         sobj=sobj.NadRozdzial
      if not ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelEdit'):
         PrepareResultJSONFile(file,'BAD','Brak uprawnień do rozdziału źródłowego')
         return

      if atype in ['inside',]:
         if not ICORSecurity.CheckRecursiveAccessLevelForUser(robj,'AccessLevelEdit'):
            PrepareResultJSONFile(file,'BAD','Brak uprawnień do rozdziału docelowego')
            return
      elif atype in ['before','after']:
         if robj.NadRozdzial:
            if not ICORSecurity.CheckRecursiveAccessLevelForUser(robj.NadRozdzial,'AccessLevelEdit'):
               PrepareResultJSONFile(file,'BAD','Brak uprawnień do rozdziału nadrzędnego')
               return
         else:
            if not ICORSecurity.CheckRecursiveAccessLevelForUser(robj.Struktura,'AccessLevelEdit'):
               PrepareResultJSONFile(file,'BAD','Brak uprawnień do struktury rozdziałów')
               return

   if arel1=='chapter' and arel2=='menustruct':
      aobj=rclass[coid1]
      astructobj=sclass[coid2]
      if not ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelEdit'):
         PrepareResultJSONFile(file,'BAD','Brak uprawnień do rozdziału źródłowego')
         return
      if not ICORSecurity.CheckRecursiveAccessLevelForUser(astructobj,'AccessLevelEdit'):
         PrepareResultJSONFile(file,'BAD','Brak uprawnień do struktury rozdziałów')
         return

   if arel1=='chapter' and arel2=='chaptergroup':
      aobj=rclass[coid1]
      gobj=gclass[coid2]
      astructobj=gobj.Struktura
      if not ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelEdit'):
         PrepareResultJSONFile(file,'BAD','Brak uprawnień do rozdziału źródłowego')
         return
      if not ICORSecurity.CheckRecursiveAccessLevelForUser(gobj,'AccessLevelView'):
         PrepareResultJSONFile(file,'BAD','Brak uprawnień do grupy rozdziałów')
         return
      if not ICORSecurity.CheckRecursiveAccessLevelForUser(astructobj,'AccessLevelEdit'):
         PrepareResultJSONFile(file,'BAD','Brak uprawnień do struktury rozdziałów')
         return

   #usuniecie ze struktury i z grup rozdzialow
   if aobj.NadRozdzial:
      st_o=rclass.PodRozdzialy[aobj.NadRozdzial.OID]
      rclass.PodRozdzialy.DeleteRefs(aobj.NadRozdzial.OID,[aobj.OID,rclass.CID])
      acnt=5
      while acnt:
         st_n=rclass.PodRozdzialy[aobj.NadRozdzial.OID]
         #print 'REMOVE:',aobj.OID,aobj.NadRozdzial.OID
         #print '  ',st_o
         #print '  ',st_n
         if st_o==st_n:
            #print 'ROZDZIAL NIE USUNIETY Z LISTY PODROZDZIALOW:',acnt
            acnt=acnt-1
            time.sleep(1)
         else:
            acnt=0
   if aobj.Struktura:
      sclass.Rozdzialy.DeleteRefs(aobj.Struktura.OID,[aobj.OID,rclass.CID])
   if aobj.GrupaRozdzialow:
      aobj.GrupaRozdzialow=''

   if arel1=='chapter' and arel2=='chapter' and atype=='before':
      dobj=rclass[coid2]
      gobj=dobj.GrupaRozdzialow

      if gobj:
         destfield=gclass.Rozdzialy
         destoid=gobj.OID

         destfield.AddRefs(destoid,[coid1,rclass.CID],ainsertbefore=[coid2,rclass.CID])

         sobj=gobj.Struktura
         destfield2=sclass.Rozdzialy
         destoid2=sobj.OID
         destfield2.AddRefs(destoid2,[coid1,rclass.CID])

         aobj.Struktura=[sobj.OID,sclass.CID]
         aobj.GrupaRozdzialow=gobj
         aobj.NadRozdzial=''

         UpdateSGTabID(sobj.Rozdzialy)
      else:
         nobj=dobj.NadRozdzial
         if nobj:
            destfield=rclass.PodRozdzialy
            destoid=nobj.OID
         else:
            destfield=sclass.Rozdzialy
            destoid=dobj.Struktura.OID

         destfield.AddRefs(destoid,[coid1,rclass.CID],ainsertbefore=[coid2,rclass.CID])

         aobj.NadRozdzial=dobj.NadRozdzial
         aobj.Struktura=dobj.Struktura
         aobj.GrupaRozdzialow=''

         if nobj:
            UpdateSGTabID(dobj.NadRozdzial.PodRozdzialy)
         else:
            UpdateSGTabID(dobj.Struktura.Rozdzialy)

   if arel1=='chapter' and arel2=='chapter' and atype=='after':
      dobj=rclass[coid2]
      gobj=dobj.GrupaRozdzialow

      if gobj:
         destfield=gclass.Rozdzialy
         destoid=gobj.OID

         destfield.AddRefs(destoid,[coid1,rclass.CID],ainsertafter=[coid2,rclass.CID])

         sobj=gobj.Struktura
         destfield2=sclass.Rozdzialy
         destoid2=sobj.OID
         destfield2.AddRefs(destoid2,[coid1,rclass.CID])

         aobj.Struktura=[sobj.OID,sclass.CID]
         aobj.GrupaRozdzialow=gobj
         aobj.NadRozdzial=''

         UpdateSGTabID(sobj.Rozdzialy)
      else:
         nobj=dobj.NadRozdzial
         if nobj:
            destfield=rclass.PodRozdzialy
            destoid=nobj.OID
         else:
            destfield=sclass.Rozdzialy
            destoid=dobj.Struktura.OID

         destfield.AddRefs(destoid,[coid1,rclass.CID],ainsertafter=[coid2,rclass.CID])

         aobj.NadRozdzial=dobj.NadRozdzial
         aobj.Struktura=dobj.Struktura
         aobj.GrupaRozdzialow=''

         if nobj:
            UpdateSGTabID(dobj.NadRozdzial.PodRozdzialy)
         else:
            UpdateSGTabID(dobj.Struktura.Rozdzialy)

   if arel1=='chapter' and arel2=='chapter' and atype=='inside':
      dobj=rclass[coid2]
      destfield=rclass.PodRozdzialy
      destoid=coid2

      destfield.AddRefs(destoid,[coid1,rclass.CID])

      aobj.NadRozdzial=dobj
      aobj.Struktura=''
      aobj.GrupaRozdzialow=''

      UpdateSGTabID(dobj.PodRozdzialy)

   if arel1=='chapter' and arel2=='menustruct' and atype=='inside':
      destfield=sclass.Rozdzialy
      destoid=coid2

      destfield.AddRefs(destoid,[coid1,rclass.CID])

      aobj.NadRozdzial=''
      aobj.Struktura=[coid2,sclass.CID]
      aobj.GrupaRozdzialow=''

      UpdateSGTabID(astructobj.Rozdzialy)

   if arel1=='chapter' and arel2=='chaptergroup' and atype in ['before','after']:
      gobj=gclass[coid2]
      sobj=gobj.Struktura
      destfield=sclass.Rozdzialy
      destoid=sobj.OID
      srobj=sobj.Rozdzialy

      if srobj:
         destfield.AddRefs(destoid,[coid1,rclass.CID],ainsertbefore=[srobj.OID,rclass.CID])
      else:
         destfield.AddRefs(destoid,[coid1,rclass.CID])

      aobj.NadRozdzial=''
      aobj.Struktura=[sobj.OID,sclass.CID]
      aobj.GrupaRozdzialow=''

      UpdateSGTabID(sobj.Rozdzialy)

   if arel1=='chapter' and arel2=='chaptergroup' and atype=='inside':
      gobj=gclass[coid2]
      sobj=gobj.Struktura
      destfield=gclass.Rozdzialy
      destoid=coid2
      destfield2=sclass.Rozdzialy
      destoid2=sobj.OID

      destfield.AddRefs(destoid,[coid1,rclass.CID])
      destfield2.AddRefs(destoid2,[coid1,rclass.CID])

      aobj.NadRozdzial=''
      aobj.Struktura=[sobj.OID,sclass.CID]
      aobj.GrupaRozdzialow=gobj

      UpdateSGTabID(sobj.Rozdzialy)

   PrepareResultJSONFile(file,'OK','Rozdział przeniesiony')

