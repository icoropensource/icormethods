# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import string
from CLASSES_Library_ICORBase_Interface_ICORTextFile import TextFile

output_dir='c:/icor/tmp/'

ufields = [
#   ['CLASSES_Library_Dictionary_Named_ReplicationClassPath','IsClassRecursive',mt_Boolean],
#   ['CLASSES_Library_Dictionary_Named_ReplicationClassPath','IsFieldRecursive',mt_Boolean]
]

umethods = [
   ['CLASSES_DataBase_ASA_Import_Base','ImportUmowa']
]

def FileExists(afpath):
   try:
      f=open(afpath,'rb')
   except:
      return 0
   f.close()
   return 1

def UpdateMethodText(acpath,amname,fname,atext=''):
   fpath=FilePathAsSystemPath(output_dir+fname)
   aclass=aICORDBEngine.Classes[acpath]
   mclass=aICORDBEngine.Classes['CLASSES_System_ICORMethod']
   if aclass is None or mclass is None:
      print 'B��D! Klasa ',acpath,' nie istnieje!'
      return
   moid=mclass.aIDClassMethod.Identifiers(str(aclass.CID)+'_'+amname)
   if moid<0:
      print 'B��D! Metoda ',amname,' nie istnieje!'
      return
   amethod=aclass.MethodsByName(amname)
   if amethod is None:
      print 'B��D! Metoda ',amname,' nie istnieje!'
      return
   if atext=='':
      if not FileExists(fpath):
         print 'B��D! Plik ',fpath,' nie istnieje!'
         return
      try:
         file=TextFile(fpath,'r')
      except RuntimeError,e:
         if e.args[0]=='Not a gzipped file':
            file=open(fpath,'rt')
      try:
         atext=''
         aline=file.readline()
         while aline:
            atext=atext+aline
            aline=file.readline()
      finally:
         file.close()
   mclass.aMethodText[moid]=atext
   mclass.aLastModified.SetValuesAsDateTime(moid,ICORUtil.tdatetime())

def ExportMethods():
   for acname,amname in umethods:
      print 'metoda:',amname
      aclass=aICORDBEngine.Classes[acname]
      if aclass is None:
         print 'B��D! Klasa ',acname,' nie istnieje!'
         continue
      m1=aclass.MethodsByName(amname)
      if m1 is None:
         print 'B��D! Metoda ',amname,' nie istnieje!'
         continue
      afile=FilePathAsSystemPath(output_dir+acname+'_'+amname)
      atext=m1.MethodText
      file=TextFile(afile+'.gz','w')
      try:
         file.write(atext)
      finally:
         file.close()

def SaveRep():
   ExportMethods()
   return


def LoadRep():
# aktualizacja pol
   for acname,afname,aftype in ufields:
      print 'pole:',afname
      aclass=aICORDBEngine.Classes[acname]
      f1=aclass.FieldsByName(afname)
      if f1 is None:
         fdef1=ICORFieldDefinition(afname,aftype)
         aclass.AddField(fdef1)

# aktualizacja metod
   for acname,amname in umethods:
      print 'metoda:',amname
      aclass=aICORDBEngine.Classes[acname]
      if aclass is None:
         print 'B��D! Klasa ',acname,' nie istnieje!'
         continue
      m1=aclass.MethodsByName(amname)
      if m1 is None:
         mdef1=ICORMethodDefinition(amname)
         print 'dodaje metode',amname
         aclass.AddMethod(mdef1)
      UpdateMethodText(acname,amname,acname+'_'+amname+'.gz')
   return

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   ClearStdOut()
#   SaveRep()
   LoadRep()
   MessageDialog('Koniec pobierania aktualizacji. Zamknij program i uruchom ponownie aby zako�czy� proces aktualizacji.',mtInformation,mbOK)
   return



