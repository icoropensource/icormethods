# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import md5

MODE=2 #0 - gen, 1 - check, 2 - merge

def GenList(aclasspath):
   aclass=aICORDBEngine.Classes[aclasspath]
   ltclass=aclass.GetInheritedClassesList()
   l=[]
   for tcid in ltclass:
      tclass=aICORDBEngine.Classes[tcid]
      eclass=aICORDBEngine.Classes[tclass.ClassPath+'/EventValue']
      epath=eclass.ClassPath
      eobj=eclass.GetFirstObject()
      while eobj:
         etext=eobj.EventSource
         etext=etext.replace(chr(13),'')
         etext=etext.replace(chr(10),' ')
         etext=etext.strip()
         edigest=md5.md5(etext).hexdigest()
         l.append([epath,str(eobj.OID),edigest])
         eobj.Next()
   l.sort()
   return l

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   l=GenList('CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_SourceEvents')
   if MODE==0:
      fout=open(FilePathAsSystemPath('%ICOR%/tmp/g/edigest.txt'),'w')
      for epath,eoid,edigest in l:
         fout.write('%s %s %s\n'%(epath,eoid,edigest))
      fout.close()
   if MODE==1:
      fin=open(FilePathAsSystemPath('%ICOR%/tmp/g/edigest.txt'),'r')
      atext=fin.read()
      fin.close()
      l2=[x.split() for x in atext.split('\n') if x]
      d1={}
      for epath,eoid,edigest in l2:
         d1[epath,eoid]=edigest
      fout=open(FilePathAsSystemPath('%ICOR%/tmp/g/edigest_2.txt'),'w')
      for epath,eoid,edigest in l:
         akey=epath,eoid
         if d1.get(akey,edigest)!=edigest:
            fout.write('%s %s %s\n'%(epath,eoid,edigest))
            eclass=aICORDBEngine.Classes[epath]
            atext=eclass.EventSource[int(eoid)]
            atext=atext.replace(chr(13),'')
            fout2=open(FilePathAsSystemPath('%%ICOR%%/tmp/g/%s - %s.py'%(epath.replace('\\','_'),eoid)),'w')
            fout2.write(atext)
            fout2.close()
      fout.close()
   if MODE==2:
      fin=open(FilePathAsSystemPath('%ICOR%/tmp/g/edigest_2.txt'),'r')
      atext=fin.read()
      fin.close()
      l=[x.split() for x in atext.split('\n') if x]
      for epath,eoid,edigest in l:
         eclass=aICORDBEngine.Classes[epath]
         atext=eclass.EventSource[int(eoid)]
         atext=atext.replace(chr(13),'')
         fout2=open(FilePathAsSystemPath('%%ICOR%%/tmp/g/%s - %s - orig.py'%(epath.replace('\\','_'),eoid)),'w')
         fout2.write(atext)
         fout2.close()
   return

