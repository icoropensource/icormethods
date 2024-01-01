# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

class BrokerIsapi:
   proccmd = 'GETISAPIPIPE'
   procmin = 4
   procmax = 4
   procmem = 10*1024*1024
   procapp = 'c:\\icor\\bin\\icorisapir.exe CLASSES_Library_ICORBase_External_Broker_Handler_ISAPI_Dav'
#   procapp = 'c:\\icor\\bin\\icorisapirc.exe CLASSES_Library_ICORBase_External_Broker_Handler_ISAPI_Dav'
   procpip = 'ICORISAPIPIPE_%d'

class BrokerIsapiFilter:
   proccmd = 'GETISAPIFILTERPIPE'
   procmin = 1
   procmax = 1
   procmem = 10*1024*1024
   procapp = 'c:\\icor\\bin\\icorisapir.exe CLASSES_Library_ICORBase_External_Broker_Handler_ISAPI_Filter'
#   procapp = 'python.exe D:\\pymodules\\m32icor\\icorisapi\\wrap.py CLASSES_Library_ICORBase_External_Broker_Handler_ISAPI_Filter'
   procpip = 'ICORISAPIFILTERPIPE_%d'

class BrokerMethod:
   proccmd = 'GETMETHODPIPE'
   procmin = 4
   procmax = 4
   procmem = 10*1024*1024
   procapp = 'python.exe broker-method.py'
   procpip = 'ICORMETHODPIPE_%d'

brokers={
   BrokerIsapi.proccmd:      BrokerIsapi(),
   BrokerIsapiFilter.proccmd:   BrokerIsapiFilter(),
#   BrokerMethod.proccmd:      BrokerMethod(),
}




