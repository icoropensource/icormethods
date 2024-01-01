# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

option explicit
    
function ICORMain(CID,FieldName,OID,Value,UID)
   dim aobj
   Dim objXL
   Dim objXLchart
   Dim intRotate

   aICORDBEngine.StdOutPrint "Class: " & CID & " " & "AXTest2"
   Set objXL = CreateObject("Excel.Application")
   objXL.Workbooks.Add
   objXL.Cells(1,1).Value = 5
   objXL.Cells(1,2).Value = 10
   objXL.Cells(1,3).Value = 15
   objXL.Range("A1:C1").Select
   
   Set objXLchart = objXL.Charts.Add()
   objXL.Visible = True
   objXLchart.Type = -4100     
   
   For intRotate = 5 To 180 Step 5
       objXLchart.Rotation = intRotate
   Next
   
   For intRotate = 175 To 0 Step -5
       objXLchart.Rotation = intRotate
   Next
   objXL.Quit
   ICORMain="AXTest2"
end function



