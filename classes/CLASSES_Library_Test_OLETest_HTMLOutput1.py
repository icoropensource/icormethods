# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

option explicit

class Class1
   sub Dump(avalue)
      aICORDBEngine.StdOutPrint avalue
   end sub
end class

function ICORMain(CID,FieldName,OID,Value,UID)
   dim c1
   set c1=new Class1
   c1.Dump "aaaaaa"
end function



