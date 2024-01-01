# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORSecurity import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
from CLASSES_Library_NetBase_WWW_Server_ServerUtil import ICORReport
from CLASSES_Library_NetBase_RemoteFileSystem_Item_RFSInterface import ICORRFSItem
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import aICORWWWServerInterface
import string
import time

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
#   print 'value=',Value
   areport=ICORReport(Value)
   if areport.COMMAND=='IsDir':
      arfsitem=ICORRFSItem(UID,int(areport.RFS_ITEM_OID))
      areport.SetValue('STATUS',str(arfsitem.IsCollection()))
   elif areport.COMMAND=='GetStartupData':
      areport.SetValue('DNSIP',aICORWWWServerInterface.RFSNameServerIP)
      areport.SetValue('IP',aICORWWWServerInterface.RFSFTPServerIP)
      areport.SetValue('PORT',aICORWWWServerInterface.RFSFTPServerPort)
      return areport.AsString()
   elif areport.COMMAND=='GetOIDAsPath':
      arfsitem=ICORRFSItem(UID,int(areport.RFS_ITEM_OID))
      areport.SetValue('ITEM_PATH',arfsitem.AsPath())
      return areport.AsString()
   elif areport.COMMAND=='GetPathAsOID':
      rootitem=ICORRFSItem(UID,int(areport.ROOT_OID))
      apath=areport.PATH
      arfsitem=rootitem.GetRelativeItem(apath,rootitem)
      if arfsitem is None:
         areport.SetValue('STATUS','0')
      else:
         areport.SetValue('STATUS','1')
         areport.SetValue('RFS_ITEM_OID',str(arfsitem.oid))
      return areport.AsString()
   elif areport.COMMAND=='GetPathAsLocation':
      rootitem=ICORRFSItem(UID,int(areport.ROOT_OID))
      apath=areport.PATH
      arfsitem=rootitem.GetRelativeItem(apath,rootitem)
      if arfsitem is None:
         areport.SetValue('STATUS','0')
      else:
         areport.SetValue('STATUS','1')
         areport.SetValue('ITEM_LOCATION',arfsitem.Location)
         areport.SetValue('ITEM_IS_COLLECTION',str(arfsitem.IsCollection()))
         areport.SetValue('RFS_ITEM_OID',str(arfsitem.oid))
      return areport.AsString()
   elif areport.COMMAND=='GetSubItems':
      rootitem=ICORRFSItem(UID,int(areport.ROOT_OID))
      apath=areport.PATH
      along=int(areport.LONG)
      arfsitem=rootitem.GetRelativeItem(apath,rootitem)
      if arfsitem is None:
         areport.SetValue('STATUS','0')
      else:
         l=arfsitem.GetSubItems(along)
         l.append('')
         s=string.join(l,chr(252))
         areport.SetValue('STATUS','1')
         areport.SetValue('ITEM_LOCATION',arfsitem.Location)
         areport.SetValue('ITEM_IS_COLLECTION',str(arfsitem.IsCollection()))
         areport.SetValue('RFS_ITEM_OID',str(arfsitem.oid))
         areport.SetValue('SUB_ITEMS',s)
      return areport.AsString()
   elif areport.COMMAND=='MKDIR':
      arfsitem=ICORRFSItem(UID,int(areport.PARENT_OID))
      aname=areport.DIR_NAME
      arfsitem.AddCollection(aname)
      return areport.AsString()
   elif areport.COMMAND=='STOR':
      arfsitem=ICORRFSItem(UID,int(areport.PARENT_OID))
      aname=areport.ITEM_NAME
      arfsitem.AddItem(aname)
      return areport.AsString()
   elif areport.COMMAND=='UNLINK':
      arfsitem=ICORRFSItem(UID,int(areport.PARENT_OID))
      aname=areport.ITEM_NAME
      arfsitem.RemoveItem(aname)
      return areport.AsString()
   elif areport.COMMAND=='RENAME':
      arfsitem=ICORRFSItem(UID,int(areport.ITEM_OID))
      aname=areport.ITEM_NAME
      arfsitem.RenameItem(aname)
      return areport.AsString()
   else:
      return 'babol'
   return str(uid)



