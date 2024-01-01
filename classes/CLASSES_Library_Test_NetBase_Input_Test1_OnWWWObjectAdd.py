# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *

def RegisterFields(aclass,amenu,file,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('PoleS')
   awwweditor.RegisterField('PoleI')
   awwweditor.RegisterField('PoleF')
   awwweditor.RegisterField('PoleD')
   awwweditor.RegisterField('PoleB')
   awwweditor.RegisterField('PoleM')
   awwweditor.RegisterField('PoleC',asubfields=['PoleS'])
   awwweditor.RegisterField('PoleVS',atype=mt_String,avalue='bla bla',adescription='To jest opis tego pola\nCiekawe, czy bedzie widać\n podział na linie')
   awwweditor.RegisterField('PoleVI',atype=mt_Integer,avalue='123')
   awwweditor.RegisterField('PoleVF',atype=mt_Double,avalue='123.45')
   awwweditor.RegisterField('PoleVD',atype=mt_DateTime,avalue='1999/1/1')
   awwweditor.RegisterField('PoleVB1',atype=mt_Boolean,avalue='0')
   awwweditor.RegisterField('PoleVB2',atype=mt_Boolean,avalue='1')
   awwweditor.RegisterField('PoleVM',atype=mt_Memo,avalue=['bla bla','bla kla','kla bla'])
   return awwweditor

def OnWWWObjectAdd(aclass,amenu,file):
   awwweditor=RegisterFields(aclass,amenu,file)
   awwweditor.Write()

def OnWWWObjectAddSubmit(aclass,amenu,areport,file):
   awwweditor=RegisterFields(aclass,amenu,file,areport)
   awwweditor.Read()
   file.write('<h1>OK</h1>')
   file.write(str(areport.keys()))
   awwweditor.Write()





