# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   aobj=aclass[aoid]
   arefs=aobj.TabeleZrodlowe.AsRefs()
   bobj=aobj.Projekt.BazyZrodlowe
   tlist=[]
   while bobj:
      if not arefs.RefExists(bobj.OID,bobj.CID):
         tlist.append(bobj.OID)
         awwweditor.RegisterField('tab_%d'%bobj.OID,adisplayed=bobj.Grupa+' / '+bobj.Nazwa+' ['+str(bobj.OID)+']',atype=mt_Bool)
      bobj.Next()
   return awwweditor,tlist

def RegisterFieldsStep1(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Field1',adisplayed='Pole S',atype=mt_String,avalue='ABC')
   awwweditor.RegisterField('Field2',adisplayed='Pole I',atype=mt_Integer,avalue='123')
   awwweditor.RegisterField('Field3',adisplayed='Pole DT',atype=mt_DateTime,avalue='2002/02/02')
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

def OnWWWAction(aobj,amenu,file):
   awwweditor,tlist=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   if amenu.Action=='ObjectApplyMethods':
      awwweditor.Write()
   return 0 # show back reference to main object (1-link, 2-button)

def AddField(attrs,rfields,tobj,aclass):
   afnameid=afname=attrs['name']
   if afname[:1]!='_':
      afnameid=ICORUtil.str2ProperID(afname)
   apos,afind=rfields.FindRefByValue('NazwaID',afnameid)
   if afind:
      return None
   aoid=aclass.AddObject(arefobject=tobj)
   aclass.Nazwa[aoid]=afname
   aclass.SGIsAliased[aoid]=int(attrs.get('isaliased','1'))
   if not attrs.get('type','') in ['Opis','HTML']:
      aclass.SGIsIndexed[aoid]=1
   aclass.SGIsInteractive[aoid]=1
   aclass.SGIsSearch[aoid]=int(attrs.get('issearch','1'))
   aclass.SGIsSingleViewHidden[aoid]=int(attrs.get('issingleviewhidden','0'))
   if attrs.get('type','')=='OID':
      aclass.SGIsDictViewHidden[aoid]=0
      aclass.SGIsSingleViewHidden[aoid]=1
   aclass.SGIsDictViewHidden[aoid]=int(attrs.get('isdictviewhidden','0'))
   aclass.SGIsObligatory[aoid]=int(attrs.get('isobligatory','0'))
   aclass.SGTabIndex[aoid]=10000
   tclass=aclass.TypPolaDotyczy.ClassOfType
   toid=tclass.Opis.Identifiers(attrs.get('type',''))
   if toid>=0:
      aclass.TypPolaDotyczy[aoid]=[toid,tclass.CID]
   return aoid

def OnWWWActionSubmit(aobj,amenu,areport,file):
   if not areport['refMode']:
      abasenamemodifier=aobj.Projekt.BaseNameModifier
      aprojectname=aobj.Projekt.Nazwa
      tclass=aobj.Class.TabeleZrodlowe.ClassOfType
      fclass=tclass.Pola.ClassOfType
      awwweditor,tlist=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
      trefs=[]
      for toid in tlist:
         if ICORUtil.str2bool(awwweditor['tab_%d'%toid]):
            trefs.append([toid,tclass.CID])
            tobj=tclass[toid]
            tobj.IsVersionControl=1
#            tobj.Grupa='WWW Menu Struct'
            file.write('<h3>call python2 UTIL_%sBZR_%d.py CREATE</h3>'%(abasenamemodifier,toid))
            file.write('<h3>call python2 UTIL_%sBZR_%d.py CREATESP</h3>'%(abasenamemodifier,toid))
            file.write('<h3>call python2 UTIL_%sBZR_V_%d.py CREATE</h3>'%(abasenamemodifier,toid))
            file.write('<h3>call python2 UTIL_%sBZR_V_%d.py CREATESP</h3>'%(abasenamemodifier,toid))
            lfields=[{
         'name':'Informacja podmiot udostępniający',
         'type':'Ciąg znaków - 1 linia',
         'issearch':'1',
         'isaliased':'1',
         'isdictviewhidden':'1',
         },
         {
         'name':'Informacja osoba odpowiedzialna',
         'type':'Ciąg znaków - 1 linia',
         'issearch':'1',
         'isaliased':'1',
         'isdictviewhidden':'1',
         },
         {
         'name':'Informacja data wytworzenia',
         'type':'Data',
         'issearch':'1',
         'isaliased':'1',
         'isdictviewhidden':'1',
         'isobligatory':'1',
         },
         {
         'name':'Informacja opis czynności',
         'type':'Ciąg znaków - 1 linia',
         'issearch':'1',
         'isaliased':'1',
         'isdictviewhidden':'1',
         'isobligatory':'1',
         },
         {
         'name':'_OIDDictRef',
         'type':'OID',
         'issearch':'0',
         'isaliased':'0',
         'issingleviewhidden':'1',
         },
         {
         'name':'_ChapterID',
         'type':'Liczba całkowita',
         'issearch':'0',
         'isaliased':'0',
         'isdictviewhidden':'1',
         'issingleviewhidden':'0',
         }]
            arefs=[]
            rfields=tclass.Pola.GetRefList(toid)
            for d in lfields:
               foid=AddField(d,rfields,tobj,fclass)
               if not foid is None:
                  arefs.append([foid,fclass.CID])
            tclass.Pola.AddRefs(toid,arefs,asortedreffield=tclass.Pola.ClassOfType.SGTabIndex,dosort=1)
            dobj=tclass[toid].Pola
            atabid=10
            while dobj:
               dobj.SGTabIndex=atabid
               atabid=atabid+10
               dobj.Next()
      aobj.Class.TabeleZrodlowe.AddRefs(aobj.OID,trefs,asortedreffield=aobj.Class.TabeleZrodlowe.ClassOfType.Nazwa,dosort=1)



