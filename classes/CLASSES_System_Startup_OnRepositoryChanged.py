# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   print 'OnRepositoryChanged'
   return
   if CACHE_DISABLE:
      return
#   aclass=aICORDBEngine.Classes[CID]
   l=Value.split(':')
   acategory=l[0]
   amode=l[1]
   if acategory=='FIELD':
      foid=int(FieldName)
#     fclass=aICORDBEngine.Classes['CLASSES_System_ICORField']
#     ffieldcid=fclass.FieldsByName('aFieldOwnerClassID')
#     bcid=ffieldcid.ValuesAsInt(foid)
#     ffieldname=fclass.FieldsByName('aFieldName')
#     bname=ffieldname[foid]
#     bclass=aICORDBEngine.Classes[bcid]
#     if bclass is None:
#         bpath='{'+str(bcid)+'}'
#     else:
#        bpath=bclass.ClassPath
      if amode=='UPDATE':
         #print 'FIELD UPDATE: '+bpath+' '+bname+' ['+str(OID)+'] '
         aICORDBEngine.SysBase.SetLastFieldValueModificationID(foid,OID)
      elif amode=='DELETE':
         #print 'FIELD DELETE: '+bpath+' '+bname+' ['+str(OID)+'] '
         aICORDBEngine.SysBase.SetLastFieldValueModificationID(foid,OID)
      else:
         print 'unknown FIELD RepositoryChanged mode: %s'%amode
   elif acategory=='CLASS':
      bcid=int(FieldName)
#      bclass=aICORDBEngine.Classes[bcid]
#      if bclass is None:
#         bpath='{'+str(bcid)+'}'
#      else:
#         bpath=bclass.ClassPath
      if amode=='UPDATE':
#         print 'CLASS UPDATE: '+bpath+' ['+str(OID)+'] '
         aICORDBEngine.SysBase.SetLastClassModificationID(bcid)
      elif amode=='DELETE':
#         print 'CLASS DELETE: '+bpath+' ['+str(OID)+'] '
         aICORDBEngine.SysBase.SetLastClassModificationID(bcid)
      else:                      
         print 'unknown CLASS RepositoryChanged mode: %s'%amode
   return
