# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import ICORRepositoryIterator

class ReferencesChecker(ICORRepositoryIterator):
   def __init__(self):
      ICORRepositoryIterator.__init__(self)
      self.ClassesDict={}
      self.EmptyClassesDict={}
      self.BadClassesDict={}
      self.DuplicateObjects={}
   def OnPreClass(self,aclass):
      afields=aclass.GetFieldsList()
      dfields_dup={}
      lfields=[]
      for afield in afields:
         afi=aclass.FieldsByName(afield)
         if not afi.ClassOfType is None:
            lfields.append(afi)
            if afi.WWWUpdateRefs:
               bfields=afi.ClassOfType.BackRefFields
               for bfield in bfields:
                  if bfield.ClassOfType.CID==afi.CID:
                     dfields_dup[afi.FOID]=1
      if not lfields:
         return
      droids={}
      aoid=aclass.FirstObject()
      while aoid>=0:
         for afi in lfields:
            arefs=afi.GetRefList(aoid)
            while arefs:
               if arefs.Class is None:
                  x=self.EmptyClassesDict.get((aclass.CID,afi.Name),0)
                  self.EmptyClassesDict[(aclass.CID,afi.Name)]=x+1
               else:
                  if not arefs.Class.ObjectExists(arefs.OID):
                     ood,fdict=self.ClassesDict.get(arefs.Class.CID,({},{}))
                     ood[arefs.OID]=1
                     fod=fdict.get((aclass.CID,afi.Name),{})
                     fod[aoid]=1
                     fdict[(aclass.CID,afi.Name)]=fod
                     self.ClassesDict[arefs.Class.CID]=(ood,fdict)
                  if arefs.CID!=afi.ClassOfType.CID:
                     x=self.BadClassesDict.get((aclass.CID,afi.Name),0)
                     self.BadClassesDict[(aclass.CID,afi.Name)]=x+1
                  if dfields_dup.has_key(afi.FOID):
                     d=droids.get((afi.Name,arefs.OID),{})
                     d[aoid]=1
                     droids[(afi.Name,arefs.OID)]=d
#                     if 0 and droids.has_key((afi.Name,arefs.OID)):
#                        l=self.DuplicateObjects.get((aclass.CID,afi.Name,aoid),{})
#                        if not l:
#                           l1=self.DuplicateObjects.get((aclass.CID,afi.Name,droids[(afi.Name,arefs.OID)]),{})
#                           l1[arefs.OID]=1
#                           self.DuplicateObjects[(aclass.CID,afi.Name,droids[(afi.Name,arefs.OID)])]=l1
#                        l[arefs.OID]=1
#                        self.DuplicateObjects[(aclass.CID,afi.Name,aoid)]=l
#                     else:
#                        droids[(afi.Name,arefs.OID)]=aoid
               arefs.Next()
         aoid=aclass.NextObject(aoid)
      for k,d in droids.items():
         if len(d.keys())>1:
            afiname,arefsoid=k
            self.DuplicateObjects[(aclass.CID,afiname,arefsoid)]=d.keys()
   def Dump(self,file=None):
      w1,w2,w3,w4=0,0,0,0
      if len(self.EmptyClassesDict.keys())>0:
         w1=1
         if file:
            file.write('<h1>Lista p�l z referencjami do nieistniej�cych klas</h1><br>\n')
         else:
            print '   *** Lista p�l z referencjami do nieistniej�cych klas ***'
         ckeys=self.EmptyClassesDict.keys()
         ckeys.sort()
         for acid,afname in ckeys:
            aclass=aICORDBEngine.Classes[acid]
            afield=aclass.FieldsByName(afname)
            if file:
               file.write('      %s %s %d<br>\n'%(aclass.ClassPath,afname,self.EmptyClassesDict[(acid,afname)]))
            else:
               print '     ',aclass.ClassPath,afname,self.EmptyClassesDict[(acid,afname)]
         if file:
            file.write('<hr>\n')
         else:
            print
      if len(self.BadClassesDict.keys())>0:
         w2=1
         if file:
            file.write('<h1>Lista p�l z referencjami do klas, nie b�d�cych w�a�ciwymi dla typu pola</h1><br>\n')
         else:
            print '   *** Lista p�l z referencjami do klas, nie b�d�cych w�a�ciwymi dla typu pola ***'
         ckeys=self.BadClassesDict.keys()
         ckeys.sort()
         for acid,afname in ckeys:
            aclass=aICORDBEngine.Classes[acid]
            afield=aclass.FieldsByName(afname)
            if file:
               file.write('      %s %s %d<br>\n'%(aclass.ClassPath,afname,self.BadClassesDict[(acid,afname)]))
            else:
               print '     ',aclass.ClassPath,afname,self.BadClassesDict[(acid,afname)]
         if file:
            file.write('<hr>\n')
         else:
            print
      if len(self.ClassesDict.keys())>0:
         w3=1
         if file:
            file.write('<h1>Lista klas z brakuj�cymi obiektami</h1><br>\n')
         else:
            print '   *** Lista klas z brakuj�cymi obiektami ***'
         for acid in self.ClassesDict.keys():
            aclass=aICORDBEngine.Classes[acid]
            ood,fdict=self.ClassesDict[acid]
            if file:
               file.write('   <b>%s %d</b></br>\n'%(aclass.ClassPath,len(ood.keys())))
            else:
               ls1=ood.keys()[:100]
               ls1.sort()
               print aclass.ClassPath,len(ood.keys()),ls1
            ackeys=fdict.keys()
            ackeys.sort()
            for acid,afname in ackeys:
               aclass=aICORDBEngine.Classes[acid]
               afield=aclass.FieldsByName(afname)
               if file:
                  file.write('      %s %s %d<br>\n'%(aclass.ClassPath,afname,len(fdict[(acid,afname)].keys())))
               else:
                  ls1=fdict[(acid,afname)].keys()[:50]
                  ls1.sort()
                  print '     ',aclass.ClassPath,afname,len(fdict[(acid,afname)].keys()),ls1
      if len(self.DuplicateObjects.keys())>0:
         w4=1
         if file:
            file.write('<h1>Lista p�l z powt�rzonymi obiektami</h1><br>\n')
         else:
            print '   *** Lista p�l z powt�rzonymi obiektami ***'
         lkeys=self.DuplicateObjects.keys()
         lkeys.sort()
         for acid,afname,aoid in lkeys:
            l=self.DuplicateObjects[acid,afname,aoid]
            l.sort()
            aclass=aICORDBEngine.Classes[acid]
            afield=aclass.FieldsByName(afname)
            aproperoid=''
            for bfield in afield.ClassOfType.BackRefFields:
               if bfield.FieldTID==aclass.CID:
                  brefs=bfield.GetRefList(aoid)
                  aproperoid=' (ok=%d)'%(brefs.OID,)
            if file:
               file.write('  %s %s[%d]%s %d<br>\n'%(aclass.ClassPath,afname,aoid,aproperoid,len(l)))
            else:
               print '  %s %s[%d]%s%s'%(aclass.ClassPath,afname,aoid,aproperoid,str(l))
      if not (w1 or w2 or w3):
         if file:
            file.write('<h1>Wszystko jest OK!</h1><br>\n')
         else:
            print '   *** Wszystko jest OK! ***'
