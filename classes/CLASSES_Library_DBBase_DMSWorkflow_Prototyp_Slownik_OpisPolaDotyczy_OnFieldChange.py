# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:14:37

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import icorlib.projekt.msqllib as MSQLLib
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import string
import os

def GraphCreate(aobj):
   aMaxDictValueLen,aDictValues,aDictValuesParents=MSQLLib.GetCSVDictValues(aobj.WartosciSlownika)
   import pydot
   agraph=0
   if len(aDictValuesParents.keys())>0:
      agraph=1
   if agraph:
      g=pydot.Dot(charset='latin1',root='START')
   else:
      g=pydot.Dot(charset='latin1',root='START',K='1')
   tn=pydot.Node('START',color='#67849C',fillcolor='#A6C0D6',style='filled',fontname='Helvetica')
   g.add_node(tn)
   for akey,avalue in aDictValues:
      if akey!=avalue:
         alabel=akey+'\\n'+avalue
      else:
         alabel=akey
#      print 'alabel:',ICORUtil.str2ASCII(alabel)
      tn=pydot.Node(ICORUtil.strPL2ASCII(akey),label=ICORUtil.strPL2ASCII(alabel),color='#67849C',fillcolor='#A6C0D6',style='filled',fontname='Helvetica')
      g.add_node(tn)
      if not aDictValuesParents.has_key(akey):
#         print 'akey:',ICORUtil.str2ASCII(akey)
         e=pydot.Edge('START',ICORUtil.strPL2ASCII(akey),color='#67849C')
         g.add_edge(e)
   for akey,lvalue in aDictValuesParents.items():
      for bkey in lvalue:
         if not bkey:
            bkey='START'
#         print ' bkey:',ICORUtil.str2ASCII(bkey)
#         print ' akey:',ICORUtil.str2ASCII(akey)
         e=pydot.Edge(ICORUtil.strPL2ASCII(bkey),ICORUtil.strPL2ASCII(akey),color='#67849C')
         g.add_edge(e)
   tobj=aobj.Dotyczy
   pobj=tobj.Projekt
   aAppPath=pobj.AppPath
   if aAppPath[-1:]!='/':
      aAppPath=aAppPath+'/'
   adir=FilePathAsSystemPath(aICORWWWServerInterface.AppPath)+aAppPath+'dictgraphs'
   if not os.path.exists(adir):
      os.makedirs(adir)
   try:
      afname=adir+'/%d_%d_%s.png'%(aobj.CID,aobj.OID,aobj.NazwaID)
      if agraph: #['circo','dot','fdp','neato','twopi']:
         g.write_png(afname,prog='dot')
      else:
         g.write_png(afname,prog='fdp')
   except:
      print 'Graphviz DICT ERROR:',aobj.OID,aobj.NazwaID
      raise

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if FieldName=='Nazwa':
      s=aclass.Nazwa[OID]
      if s in ['_ChapterID','_OIDDictRef','Informacja data wytworzenia','Informacja opis czynności','Informacja osoba odpowiedzialna','Informacja podmiot udostępniający']:
         aclass.Grupa[OID]='Sygnatura'
      if s[:1]!='_':
         s=ICORUtil.str2ProperID(s)
      aclass.NazwaID[OID]=s
   if FieldName in ['FieldEvents',]:
      afield=aclass.FieldsByName(FieldName)
      afield.UpdateReferencedObjects(OID)
   if FieldName=='WartosciSlownika_xxx':
      try:
         aobj=aclass[OID]
         tobj=aobj.TypPolaDotyczy
         if tobj.Opis in ['Słownik użytkownika','Słownik użytkownika - liczba całkowita']:
            GraphCreate(aobj)
      except:
         print 'Error in Graphviz interface:'
         import traceback
         traceback.print_exc()
   return

