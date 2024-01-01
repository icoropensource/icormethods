# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_Services_DNS_SimpleCache_SimpleDNSCache import HostByAddressCache

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if FieldName=='RemoteAddrDNS':
      addr=aclass.RemoteAddr[OID]
      acache=HostByAddressCache()
      return acache[addr]
   return ''



