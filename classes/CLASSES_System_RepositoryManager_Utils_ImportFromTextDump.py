# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil

import os
import string

def GetAsOneLineString(data):
   data=string.replace(data,"&","&amp;")
   data=string.replace(data,"\\","&bslash;")
   data=string.replace(data,"\"","&quot;") #"
   data=string.replace(data,chr(9),"&#9;")
   data=string.replace(data,chr(10),"&#10;")
   data=string.replace(data,chr(13),"&#13;")
   return data

def GetOneLineStringAsString(data):
   def dorepl(amatch):
      s=amatch.group(amatch.lastindex)
      if s=='amp':
         return '&'
      elif s=='quot':
         return '"'
      elif s=='bslash':
         return '\\'
      i=int(s)
      if i in [9,10,13]:
         return chr(i)
      return '&#'+s+';'
   data=re.sub('\&\#(\d+)\;|\&(amp)\;|\&(bslash)\;|\&(quot)\;',dorepl,data)
   return data

def GetFieldByFID(afid):
   fclass=aICORDBEngine.Classes['CLASSES_System_ICORField']
   aidclass=fclass.FieldsByName('aIDClassField')[afid]
   l=aidclass.split('_')
   bclass=aICORDBEngine.Classes[int(l[0])]
   afield=bclass.FieldsByName(l[1])
   return afield

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]

   adir='f:/icor/python/repair/modbfs_20160126_1153'
   fout=open('f:/icor/tmp/g/x/ilog.txt','w')
   l=os.listdir(adir)
   for afname in l:
      if not afname[-4:]=='.txt':
         continue
      afid=int(afname[:-8])
      fin=open(os.path.join(adir,afname),'r')
      atext=fin.read()
      fin.close()
      d={}
      try:
         exec atext in d,d
      except:
         print '$$ afname: %s'%(afname,)
         import traceback
         traceback.print_exc()
         continue
      afield=GetFieldByFID(afid)
      InfoStatus('%d - %d'%(afid,len(d['DATA'])))
      icnt=0
      for akeyid,aownerid,cadt,aisdeleted,avalue in d['DATA']:
         wupdate=0
         cvalue=None
         if not afield.ClassItem.ObjectExists(akeyid):
            wupdate=1
            fout.write('   %d [%d] - "%s"\n'%(akeyid,wupdate,avalue[:50].replace('\n','')))
         else:
            cdt=ICORUtil.getStrAsDateTime(cadt)
            odt=afield.GetValueLastModified(akeyid)
            if (cdt>odt) and not ((cdt[0]==1970) and (odt[0]==1899)):
               wupdate=2                             
               fout.write('   %d [%d] - %s - %s\n'%(akeyid,wupdate,str(cdt),str(odt)))
            else:
               ovalue=afield[akeyid]
               if not ovalue:
                  if avalue:
                     wupdate=3
                     fout.write('   %d [%d] - "%s"\n'%(akeyid,wupdate,avalue[:50].replace('\n','')))
               else:
                  cvalue=GetOneLineStringAsString(avalue)
                  if (len(cvalue)>=len(ovalue)) and (cvalue!=ovalue):
                     if afield.FieldTID!=mt_DateTime:
                        afname='f:/icor/tmp/g/x/ilog-%d-%s-%d-%s-%d.txt'%(afield.CID,afield.ClassItem.ClassPath.replace('\\','_'),afid,afield.Name,akeyid)
                        if os.path.exists(afname):
                           wupdate=4
                           fout.write('   %d [%d] - "%s"\n'%(akeyid,wupdate,cvalue[:50].replace('\n','')))
                        if 0:
                           fout2=open(afname,'w')
                           fout2.write(cvalue)
                           fout2.write('\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n')
                           fout2.write(ovalue)
                           fout2.close()
         if wupdate>0:
            icnt=icnt+1
            #if cvalue is None:
              #cvalue=GetOneLineStringAsString(avalue)
            #afield[akeyid]=cvalue
            #afield.SetFieldModification(akeyid,cadt)
      if icnt:
         fout.write('FID: %d {%d}-%d-%s-%s (%d)\n\n'%(afid,len(d['DATA']),afield.CID,afield.ClassItem.ClassPath.replace('\\','_'),afield.Name,icnt))
   fout.close()
   return

