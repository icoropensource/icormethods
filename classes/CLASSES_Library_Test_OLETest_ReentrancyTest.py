# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

option explicit

dim g1

function ICORMain(CID,FieldName,OID,Value,UID)
   dim l1,aclass,amethod
   aICORDBEngine.StdOutPrint "in:" & aICORDBEngine.Variables("reentry")
   if aICORDBEngine.Variables("reentry")="2" then exit function
   if aICORDBEngine.Variables("reentry")="1" then aICORDBEngine.Variables("reentry")="2"
   if aICORDBEngine.Variables("reentry")="" then aICORDBEngine.Variables("reentry")="1"
   g1="g1"
   l1="l1"
   set aclass=aICORDBEngine.Classes(CID)
   set amethod=aclass.Methods("ReentrancyTest")
   amethod.Execute
   aICORDBEngine.StdOutPrint "RE: " & g1 & " : " & l1
   g1="g2"
   l1="l2"
end function



