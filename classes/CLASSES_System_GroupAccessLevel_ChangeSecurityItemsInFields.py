# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORSearch import *

def PrintSecurity(aclass,aprofile=''):
   l=[]
   aobj=aclass.GetFirstObject()
   while aobj:
      s1=aobj.Name
      pobj=aobj.Profile
      if pobj:
         s2=pobj.Name
      else:
         s2=''
      if aprofile:
         if s2==aprofile:
            l.append([s2,s1])
      else:
         l.append([s2,s1])
      aobj.Next()
   l.sort()
   for s1,s2 in l:
      print '"%s",'%(s2,)

def ChangeSecurity(aclass,lsec):
   fsecname=aclass.Name
   i=0
   dsec={}
   while i<len(lsec):
      aoid1=fsecname.Identifiers(lsec[i])
      aoid2=fsecname.Identifiers(lsec[i+1])
      dsec[aoid1]=aoid2
      print aoid1,aoid2,lsec[i],lsec[i+1]
      i=i+2
   fclass=aICORDBEngine.Classes['CLASSES_System_ICORField']
   ffieldtypeid=fclass.FieldsByName('aFieldTypeID')
   ffieldname=fclass.FieldsByName('aFieldName')
   ffieldownerclassid=fclass.FieldsByName('aFieldOwnerClassID')
   asearch=ICORRepositorySearch(ffieldtypeid)
   aposition=asearch.FirstEQ(aclass.CID)
   if aposition<0:
      print 'no items'
      return
   aoid=ffieldtypeid.GetValueIDByPosition(aposition)
   while aoid>=0:
      atypeid=int(ffieldtypeid[aoid])
      if atypeid!=aclass.CID:
         break
      bcid=ffieldownerclassid.ValuesAsComp(aoid)
      bclass=aICORDBEngine.Classes[bcid]
      if bclass is None:
         print 'empty class ID:',bcid
      else:
         bfieldname=ffieldname[aoid]
         bfield=bclass.FieldsByName(bfieldname)
         boid=bfield.GetFirstValueID()
         wcnt,wcnta=0,0
         while boid>=0:
            brefs=bfield.GetRefList(boid)
            w=0
            ldel,ladd=[],[]
            for i in range(brefs.len):
               toid=brefs.refs[i][0]
               if dsec.has_key(toid):
                  ldel.append(toid)
                  ladd.append(dsec[toid])
                  w=1
                  wcnt=wcnt+1
            if w:
               for toid in ldel:
                  brefs.DelRef(toid)
               for toid in ladd:
                  if not brefs.RefExists(toid):
                     brefs.AddRef(toid,aclass.CID)
                     wcnta=wcnta+1
#               brefs.Store()
            boid=bfield.GetNextValueID(boid)
         print bcid,bclass.NameOfClass,bfieldname,wcnta,wcnt
      aoid=ffieldtypeid.GetNextValueID(aoid)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   #PrintSecurity(aclass,'')
   #l=[]
   #   ChangeSecurity(aclass,l)
   return



