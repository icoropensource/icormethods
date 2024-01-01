# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('NowaNazwa',adisplayed='Nowa nazwa',atype=mt_String)
   return awwweditor

def RegisterFieldsStep1(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Field1',adisplayed='Pole S',atype=mt_String,avalue='ABC')
   awwweditor.RegisterField('Field2',adisplayed='Pole I',atype=mt_Integer,avalue='123')
   awwweditor.RegisterField('Field3',adisplayed='Pole DT',atype=mt_DateTime,avalue='2002/02/02')
   return awwweditor
                  
def OnBeforeWWWAction(aobj,amenu,file):
   return 1

def OnWWWAction(aobj,amenu,file):
   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   if amenu.Action=='ObjectApplyMethods':
      awwweditor.Write()
   return 1 # show back reference to main object

def OnWWWActionSubmit(aobj,amenu,areport,file):
   if not areport['refMode']:
      awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
      boid=aobj.Class.Nazwa.Identifiers(awwweditor['NowaNazwa'])
      if boid>=0:
         file.write('<h1><font color="red">Tabela o nazwie %s już istnieje!</font></h1>'%awwweditor['NowaNazwa'])
      else:
         boid=aobj.AddObject()
         bobj=aobj.Class[boid]
         bobj.Nazwa=awwweditor['NowaNazwa']
         bobj.NazwaTabeli=awwweditor['NowaNazwa']
         bobj.AccessLevelDelete=aobj.Class.AccessLevelDelete[aobj.OID]
         bobj.AccessLevelEdit=aobj.Class.AccessLevelEdit[aobj.OID]
         bobj.Dotyczy=aobj.Class.Dotyczy[aobj.OID]
         bobj.Grupa=aobj.Grupa
         bobj.NazwaObiektu=aobj.NazwaObiektu

         lrefs=[]
         cobj=aobj.PolaczeniaDoTabel
         while cobj:
            doid=cobj.AddObject()
            dobj=cobj.Class[doid]
            dobj.DestinationTable=cobj.Class.DestinationTable[cobj.OID]
            dobj.SourceTable=cobj.Class.SourceTable[cobj.OID]
            dobj.DestinationField=cobj.DestinationField
            dobj.LinkConstraint=cobj.LinkConstraint
            dobj.LinkTabID=cobj.LinkTabID
            dobj.SourceField=cobj.SourceField
            dobj.WWWDisabledTable=cobj.WWWDisabledTable
            dobj.CMSDisabledTable=cobj.CMSDisabledTable
            lrefs.extend([doid,dobj.CID])
            cobj.Next()
         bobj.PolaczeniaDoTabel=lrefs

         lrefs=[]
         cobj=aobj.Zakladki
         while cobj:
            doid=cobj.AddObject()
            dobj=cobj.Class[doid]
            dobj.Nazwa=cobj.Nazwa
            dobj.ZakladkaID=cobj.ZakladkaID
            dobj.BazaZrodlowa=cobj.Class.BazaZrodlowa[cobj.OID]
            lrefs.extend([doid,dobj.CID])
            cobj.Next()
         bobj.Zakladki=lrefs

         lrefs=[]
         cobj=aobj.Pola
         while cobj:
            doid=cobj.AddObject()
            dobj=cobj.Class[doid]
            dobj.Nazwa=cobj.Nazwa
            dobj.NazwaWidoczna=cobj.NazwaWidoczna
            dobj.Opis=cobj.Opis
            dobj.SGIsAliased=cobj.SGIsAliased
            dobj.SGIsIndexed=cobj.SGIsIndexed
            dobj.SGIsInteractive=cobj.SGIsInteractive
            dobj.SGIsObligatory=cobj.SGIsObligatory
            dobj.SGIsSearch=cobj.SGIsSearch
            dobj.SGIsSorted=cobj.SGIsSorted
            dobj.SGSortStyle=cobj.SGSortStyle
            dobj.SGIsUnique=cobj.SGIsUnique
            dobj.SGMaxValue=cobj.SGMaxValue
            dobj.SGMinValue=cobj.SGMinValue
            dobj.SGTabIndex=cobj.SGTabIndex
            dobj.TextCols=cobj.TextCols
            dobj.TextRows=cobj.TextRows
            dobj.TextNoWrap=cobj.TextNoWrap
            dobj.ExtDictConstraint=cobj.ExtDictConstraint
            dobj.Dotyczy=cobj.Class.Dotyczy[cobj.OID]
            dobj.TypPolaDotyczy=cobj.Class.TypPolaDotyczy[cobj.OID]
            dobj.WartosciSlownika=cobj.Class.WartosciSlownika[cobj.OID]
            dobj.ZrodloDanychSlownika=cobj.Class.ZrodloDanychSlownika[cobj.OID]
            lrefs.extend([doid,dobj.CID])
            cobj.Next()
         bobj.Pola=lrefs

         pobj=aobj.Projekt
         pobj.Class.BazyZrodlowe.AddRefs(pobj.OID,[bobj.OID,bobj.CID],asortedreffield=bobj.Class.Nazwa,dosort=1)

      awwweditor.WriteObjectView(bobj,asbutton=1)
#      file.write('<h2>Field : %s</h2>'%awwweditor['Nazwa'])
#      bwwweditor=RegisterFieldsStep1(aobj.Class,amenu,file,aobj.OID,None)
#      bwwweditor.Write(arefMode='step1')
   elif areport['refMode']=='step1':
      awwweditor=RegisterFieldsStep1(aobj.Class,amenu,file,aobj.OID,areport)
      file.write('<h1>Step 1</h1>')
      file.write('<h2>Field 1: %s</h2>'%awwweditor['Field1'])
      file.write('<h2>Field 2: %s</h2>'%awwweditor['Field2'])
      file.write('<h2>Field 3: %s</h2>'%awwweditor['Field3'])


