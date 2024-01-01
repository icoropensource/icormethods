# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import os

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
#   if not aclass.AllowDelete(OID):
#      return
#   print 'CLASS: OnObjectDelete:',aclass.aCID[OID],'[',OID,']'
#   print '   d:',aclass.aDerivedClasses[OID],'x'
   aclass.aEditorSheets.DeleteReferencedObjects(OID)
   aclass.aDerivedClasses.DeleteReferencedObjects(OID)
   aclass.aFields.DeleteReferencedObjects(OID)
   aclass.aMethods.DeleteReferencedObjects(OID)
   aclass.aSummaries.DeleteReferencedObjects(OID)
   aclass.aWWWMenu.DeleteReferencedObjects(OID)
   fname=aICORDBEngine.Variables['_ICOR_REPOSITORY_DIR']+'/MIID/'+str(OID)+'.moi'
   try:
      if os.path.exists(fname):
         os.unlink(fname)
   except:
      pass
#   aclass.AllowReadGroups.DeleteReferencedObjects(OID)
#   aclass.AllowWriteGroups.DeleteReferencedObjects(OID)
#   return aclass.AllowDelete(OID)
