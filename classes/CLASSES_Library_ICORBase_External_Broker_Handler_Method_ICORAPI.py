# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

import sys
import string
import MPipes
import os

def Log(s):
   amode='a+'
   fname='d:/icor/log/mpipe.log'
   try:
      f=open(fname,amode)
      if s[-1:]!='\n':
         s=s+'\n'
      f.write('['+str(os.getpid())+'] '+s)
      f.close()
   except:
      pass

aICORPipesCollection=MPipes.MPipesCollection(sys.__dict__.get('ICOR_SERVER','.'),'ICORPipe0')
aICORPipesCollection.Add(4)

def AddObject(fparamI1,fparamI2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiii','',0,8,fparamI1,fparamI2)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def CheckObjectBySummary(fparamI1,fparamI2,fparamI3,fparamI4,fparamI5):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiiii','',1,20,fparamI1,fparamI2,fparamI3,fparamI4,fparamI5)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def ClassExists(fparamI1,fparamI2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiii','',2,8,fparamI1,fparamI2)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def ClearAllObjects(fparamI1,fparamI2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiii','',3,8,fparamI1,fparamI2)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def ClearAllValues(fparamI1,fparamI2,fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii',fparamS1,4,12+len(fparamS1),fparamI1,fparamI2,len(fparamS1))
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def ClearStdErr():
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('ii','',5,0)
   finally:
      aICORPipesCollection.Release(apipe)

def ClearStdOut():
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('ii','',6,0)
   finally:
      aICORPipesCollection.Release(apipe)

def CompareOIDValue(fparamI1,fparamI2,fparamS1,fparamI3,fparamS2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiiii',string.join([fparamS1,fparamS2],''),7,20+len(fparamS1)+len(fparamS2),fparamI1,fparamI2,len(fparamS1),fparamI3,len(fparamS2))
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def CompareOIDs(fparamI1,fparamI2,fparamS1,fparamI3,fparamI4):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiiii',fparamS1,8,20+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3,fparamI4)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def CreateObjectByID(fparamI1,fparamI2,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii','',9,12,fparamI1,fparamI2,fparamI3)
   finally:
      aICORPipesCollection.Release(apipe)

def DeleteObject(fparamI1,fparamI2,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii','',10,12,fparamI1,fparamI2,fparamI3)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def DeleteVariable(fparamI1,fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiii',fparamS1,11,8+len(fparamS1),fparamI1,len(fparamS1))
   finally:
      aICORPipesCollection.Release(apipe)

def DialogInput(fparamI1,fparamS1,fparamS2,fparamS3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',string.join([fparamS1,fparamS2,fparamS3],''),12,16+len(fparamS1)+len(fparamS2)+len(fparamS3),fparamI1,len(fparamS1),len(fparamS2),len(fparamS3))
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def DoEvents():
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('ii','',13,0)
   finally:
      aICORPipesCollection.Release(apipe)

def EditObject(fparamI1,fparamI2,fparamI3,fparamS1,fparamI4):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiiii',fparamS1,14,20+len(fparamS1),fparamI1,fparamI2,fparamI3,len(fparamS1),fparamI4)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def ExcelClose():
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('ii','',15,0)
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def ExcelExecute(fparamS1,fparamS2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiii',string.join([fparamS1,fparamS2],''),16,8+len(fparamS1)+len(fparamS2),len(fparamS1),len(fparamS2))
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def ExcelGetCellValue(fparamI1,fparamI2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiii','',17,8,fparamI1,fparamI2)
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def ExcelOpen(fparamI1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iii','',18,4,fparamI1)
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def ExcelSetCellValue(fparamI1,fparamI2,fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii',fparamS1,19,12+len(fparamS1),fparamI1,fparamI2,len(fparamS1))
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def ExecuteMethod(fparamI1,fparamI2,fparamS1,fparamS2,fparamI3,fparamS3,fparamI4):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiiiiii',string.join([fparamS1,fparamS2,fparamS3],''),20,28+len(fparamS1)+len(fparamS2)+len(fparamS3),fparamI1,fparamI2,len(fparamS1),len(fparamS2),fparamI3,len(fparamS3),fparamI4)
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def ExportModuleAsString(fparamI1,fparamS1,fparamS2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii',string.join([fparamS1,fparamS2],''),21,12+len(fparamS1)+len(fparamS2),fparamI1,len(fparamS1),len(fparamS2))
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def FindValue(fparamI1,fparamI2,fparamS1,fparamS2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',string.join([fparamS1,fparamS2],''),22,16+len(fparamS1)+len(fparamS2),fparamI1,fparamI2,len(fparamS1),len(fparamS2))
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def FindValueBoolean(fparamI1,fparamI2,fparamS1,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',fparamS1,23,16+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def FindValueDateTime(fparamI1,fparamI2,fparamS1,fparamI3,fparamI4,fparamI5,fparamI6,fparamI7,fparamI8,fparamI9):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiiiiiiiii',fparamS1,24,40+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3,fparamI4,fparamI5,fparamI6,fparamI7,fparamI8,fparamI9)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def FindValueFloat(fparamI1,fparamI2,fparamS1,fparamD1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiid',fparamS1,25,20+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamD1)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def FindValueInteger(fparamI1,fparamI2,fparamS1,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',fparamS1,26,16+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def FormatFNum(fparamS1,fparamD1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiid',fparamS1,27,12+len(fparamS1),len(fparamS1),fparamD1)
      ret=apipe.ReadString()
   finally:                    
      aICORPipesCollection.Release(apipe)
   return ret

def GetClassID(fparamI1,fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiii',fparamS1,28,8+len(fparamS1),fparamI1,len(fparamS1))
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetClassLastModification(fparamI1,fparamI2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiii','',29,8,fparamI1,fparamI2)
      ret=apipe.ReadInts(7)
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetClassProperty(fparamI1,fparamI2,fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii',fparamS1,30,12+len(fparamS1),fparamI1,fparamI2,len(fparamS1))
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetDeletedObjectsList(fparamI1,fparamI2,fparamI3,fparamI4,fparamI5,fparamI6,fparamI7,fparamI8,fparamI9):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiiiiiiii','',32,36,fparamI1,fparamI2,fparamI3,fparamI4,fparamI5,fparamI6,fparamI7,fparamI8,fparamI9)
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetFieldLastModification(fparamI1,fparamI2,fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii',fparamS1,33,12+len(fparamS1),fparamI1,fparamI2,len(fparamS1))
      ret=apipe.ReadInts(7)
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetFieldModification(fparamI1,fparamI2,fparamS1,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',fparamS1,34,16+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3)
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetFieldObjectsCount(fparamI1,fparamI2,fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii',fparamS1,35,12+len(fparamS1),fparamI1,fparamI2,len(fparamS1))
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetFieldProperty(fparamI1,fparamI2,fparamS1,fparamS2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',string.join([fparamS1,fparamS2],''),36,16+len(fparamS1)+len(fparamS2),fparamI1,fparamI2,len(fparamS1),len(fparamS2))
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetFieldValue(fparamI1,fparamI2,fparamS1,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',fparamS1,37,16+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3)
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetFieldValueByPosition(fparamI1,fparamI2,fparamS1,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',fparamS1,38,16+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3)
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetFieldValueDate(fparamI1,fparamI2,fparamS1,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',fparamS1,39,16+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3)
      ret=apipe.ReadInts(3)
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetFieldValueDateTime(fparamI1,fparamI2,fparamS1,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',fparamS1,40,16+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3)
      ret=apipe.ReadInts(7)
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetFieldValueFloat(fparamI1,fparamI2,fparamS1,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',fparamS1,41,16+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3)
      ret=apipe.ReadFloat()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetFieldValueFmt(fparamI1,fparamI2,fparamS1,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',fparamS1,42,16+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3)
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetFieldValueInt(fparamI1,fparamI2,fparamS1,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',fparamS1,43,16+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetFieldValueLastModification(fparamI1,fparamI2,fparamS1,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',fparamS1,44,16+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3)
      ret=apipe.ReadInts(7)
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetFieldValuePyTime(fparamI1,fparamI2,fparamS1,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',fparamS1,45,16+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3)
      ret=apipe.ReadInts(9)
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetFieldValueTime(fparamI1,fparamI2,fparamS1,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',fparamS1,46,16+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3)
      ret=apipe.ReadInts(4)
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetFieldsList(fparamI1,fparamI2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiii','',47,8,fparamI1,fparamI2)
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetFirstClass(fparamI1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iii','',48,4,fparamI1)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetFirstDeletedOffset(fparamI1,fparamI2,fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii',fparamS1,49,12+len(fparamS1),fparamI1,fparamI2,len(fparamS1))
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetFirstFieldValueID(fparamI1,fparamI2,fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii',fparamS1,50,12+len(fparamS1),fparamI1,fparamI2,len(fparamS1))
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetFirstObjectID(fparamI1,fparamI2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiii','',51,8,fparamI1,fparamI2)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetHashFile(fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iii',fparamS1,52,4+len(fparamS1),len(fparamS1))
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetHashString(fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iii',fparamS1,53,4+len(fparamS1),len(fparamS1))
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetICORHandle():
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('ii','',54,0)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetLastFieldValueID(fparamI1,fparamI2,fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii',fparamS1,55,12+len(fparamS1),fparamI1,fparamI2,len(fparamS1))
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetLastObjectID(fparamI1,fparamI2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiii','',56,8,fparamI1,fparamI2)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetMethodLastModification(fparamI1,fparamI2,fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii',fparamS1,57,12+len(fparamS1),fparamI1,fparamI2,len(fparamS1))
      ret=apipe.ReadInts(7)
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetMethodProperty(fparamI1,fparamI2,fparamS1,fparamS2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',string.join([fparamS1,fparamS2],''),58,16+len(fparamS1)+len(fparamS2),fparamI1,fparamI2,len(fparamS1),len(fparamS2))
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetMethodsList(fparamI1,fparamI2,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii','',59,12,fparamI1,fparamI2,fparamI3)
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetNextClass(fparamI1,fparamI2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiii','',60,8,fparamI1,fparamI2)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetNextDeletedOffset(fparamI1,fparamI2,fparamS1,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',fparamS1,61,16+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetNextFieldValueID(fparamI1,fparamI2,fparamS1,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',fparamS1,62,16+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetNextFreeObjectID(fparamI1,fparamI2,fparamI3,fparamI4):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii','',130,16,fparamI1,fparamI2,fparamI3,fparamI4)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetNextObjectID(fparamI1,fparamI2,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii','',63,12,fparamI1,fparamI2,fparamI3)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetObjectCount(fparamI1,fparamI2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiii','',64,8,fparamI1,fparamI2)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetObjectIDByPosition(fparamI1,fparamI2,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii','',65,12,fparamI1,fparamI2,fparamI3)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetObjectModification(fparamI1,fparamI2,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii','',66,12,fparamI1,fparamI2,fparamI3)
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetPrevFieldValueID(fparamI1,fparamI2,fparamS1,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',fparamS1,67,16+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetPrevObjectID(fparamI1,fparamI2,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii','',68,12,fparamI1,fparamI2,fparamI3)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetRecLastModification(fparamI1,fparamI2,fparamS1,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',fparamS1,69,16+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3)
      ret=apipe.ReadInts(7)
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetRecOID(fparamI1,fparamI2,fparamS1,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',fparamS1,70,16+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetRecOwnerID(fparamI1,fparamI2,fparamS1,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',fparamS1,71,16+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetRecValueAsString(fparamI1,fparamI2,fparamS1,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',fparamS1,72,16+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3)
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetStdDialogValue(fparamI1,fparamS1,fparamS2,fparamS3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',string.join([fparamS1,fparamS2,fparamS3],''),73,16+len(fparamS1)+len(fparamS2)+len(fparamS3),fparamI1,len(fparamS1),len(fparamS2),len(fparamS3))
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetStringAsSafeScriptString(fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iii',fparamS1,74,4+len(fparamS1),len(fparamS1))
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetSystemID(fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iii',fparamS1,75,4+len(fparamS1),len(fparamS1))
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetValueIDByPosition(fparamI1,fparamI2,fparamS1,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',fparamS1,76,16+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def GetVariable(fparamI1,fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiii',fparamS1,77,8+len(fparamS1),fparamI1,len(fparamS1))
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def ICORCompareText(fparamS1,fparamS2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiii',string.join([fparamS1,fparamS2],''),78,8+len(fparamS1)+len(fparamS2),len(fparamS1),len(fparamS2))
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def ICORLowerCase(fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iii',fparamS1,79,4+len(fparamS1),len(fparamS1))
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def ICORSetClipboard(fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iii',fparamS1,80,4+len(fparamS1),len(fparamS1))
   finally:
      aICORPipesCollection.Release(apipe)

def ICORUpperCase(fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iii',fparamS1,81,4+len(fparamS1),len(fparamS1))
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def ImportModuleAsString(fparamI1,fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiii',fparamS1,82,8+len(fparamS1),fparamI1,len(fparamS1))
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def IsFieldInClass(fparamI1,fparamI2,fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii',fparamS1,83,12+len(fparamS1),fparamI1,fparamI2,len(fparamS1))
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def IsMethodInClass(fparamI1,fparamI2,fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii',fparamS1,84,12+len(fparamS1),fparamI1,fparamI2,len(fparamS1))
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def IsMethodInThisClass(fparamI1,fparamI2,fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii',fparamS1,85,12+len(fparamS1),fparamI1,fparamI2,len(fparamS1))
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def IsObjectDeleted(fparamI1,fparamI2,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii','',86,12,fparamI1,fparamI2,fparamI3)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def MessageShow(fparamI1,fparamS1,fparamI2,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',fparamS1,87,16+len(fparamS1),fparamI1,len(fparamS1),fparamI2,fparamI3)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def ObjectExists(fparamI1,fparamI2,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii','',88,12,fparamI1,fparamI2,fparamI3)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def OnStdErrPrint(fparamI1,fparamS1,fparamI2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii',fparamS1,89,12+len(fparamS1),fparamI1,len(fparamS1),fparamI2)
   finally:
      aICORPipesCollection.Release(apipe)

def OnStdOutPrint(fparamI1,fparamS1,fparamI2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii',fparamS1,90,12+len(fparamS1),fparamI1,len(fparamS1),fparamI2)
   finally:
      aICORPipesCollection.Release(apipe)

def RepositoryChange(fparamI1,fparamS1,fparamI2,fparamI3,fparamS2,fparamS3,fparamS4):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiiiiii',string.join([fparamS1,fparamS2,fparamS3,fparamS4],''),91,28+len(fparamS1)+len(fparamS2)+len(fparamS3)+len(fparamS4),fparamI1,len(fparamS1),fparamI2,fparamI3,len(fparamS2),len(fparamS3),len(fparamS4))
   finally:
      aICORPipesCollection.Release(apipe)

def SelectClassFieldProperties(fparamI1,fparamI2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiii','',92,8,fparamI1,fparamI2)
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def SelectElementDialog(fparamI1,fparamS1,fparamI2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii',fparamS1,93,12+len(fparamS1),fparamI1,len(fparamS1),fparamI2)
      ret=apipe.ReadStrings()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def SelectFieldValues(fparamI1,fparamI2,fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii',fparamS1,94,12+len(fparamS1),fparamI1,fparamI2,len(fparamS1))
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def SelectInEditor(fparamI1,fparamI2,fparamS1,fparamS2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',string.join([fparamS1,fparamS2],''),95,16+len(fparamS1)+len(fparamS2),fparamI1,fparamI2,len(fparamS1),len(fparamS2))
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def SelectObjects(fparamI1,fparamI2,fparamS1,fparamI3,fparamI4):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiiii',fparamS1,96,20+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3,fparamI4)
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def SelectObjectsFromDictionary(fparamI1,fparamI2,fparamS1,fparamS2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',string.join([fparamS1,fparamS2],''),97,16+len(fparamS1)+len(fparamS2),fparamI1,fparamI2,len(fparamS1),len(fparamS2))
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def SelectSearchInClass(fparamI1,fparamI2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiii','',98,8,fparamI1,fparamI2)
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def SelectSummaries(fparamI1,fparamI2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiii','',99,8,fparamI1,fparamI2)
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def SetClassLastModification(fparamI1,fparamI2,fparamI3,fparamI4,fparamI5,fparamI6,fparamI7,fparamI8,fparamI9):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiiiiiiii','',100,36,fparamI1,fparamI2,fparamI3,fparamI4,fparamI5,fparamI6,fparamI7,fparamI8,fparamI9)
   finally:
      aICORPipesCollection.Release(apipe)

def SetClassProperty(fparamI1,fparamI2,fparamS1,fparamS2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',string.join([fparamS1,fparamS2],''),101,16+len(fparamS1)+len(fparamS2),fparamI1,fparamI2,len(fparamS1),len(fparamS2))
   finally:
      aICORPipesCollection.Release(apipe)

def SetFieldLastModification(fparamI1,fparamI2,fparamS1,fparamI3,fparamI4,fparamI5,fparamI6,fparamI7,fparamI8,fparamI9):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiiiiiiiii',fparamS1,103,40+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3,fparamI4,fparamI5,fparamI6,fparamI7,fparamI8,fparamI9)
   finally:
      aICORPipesCollection.Release(apipe)

def SetFieldModification(fparamI1,fparamI2,fparamS1,fparamI3,fparamS2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiiii',string.join([fparamS1,fparamS2],''),104,20+len(fparamS1)+len(fparamS2),fparamI1,fparamI2,len(fparamS1),fparamI3,len(fparamS2))
   finally:
      aICORPipesCollection.Release(apipe)

def SetFieldProperty(fparamI1,fparamI2,fparamS1,fparamS2,fparamS3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiiii',string.join([fparamS1,fparamS2,fparamS3],''),105,20+len(fparamS1)+len(fparamS2)+len(fparamS3),fparamI1,fparamI2,len(fparamS1),len(fparamS2),len(fparamS3))
   finally:
      aICORPipesCollection.Release(apipe)

def SetFieldValue(fparamI1,fparamI2,fparamS1,fparamI3,fparamS2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiiii',string.join([fparamS1,fparamS2],''),106,20+len(fparamS1)+len(fparamS2),fparamI1,fparamI2,len(fparamS1),fparamI3,len(fparamS2))
   finally:
      aICORPipesCollection.Release(apipe)

def SetFieldValueDate(fparamI1,fparamI2,fparamS1,fparamI3,fparamI4,fparamI5,fparamI6):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiiiiii',fparamS1,107,28+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3,fparamI4,fparamI5,fparamI6)
   finally:
      aICORPipesCollection.Release(apipe)

def SetFieldValueDateTime(fparamI1,fparamI2,fparamS1,fparamI3,fparamI4,fparamI5,fparamI6,fparamI7,fparamI8,fparamI9,fparamI10):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiiiiiiiiii',fparamS1,108,44+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3,fparamI4,fparamI5,fparamI6,fparamI7,fparamI8,fparamI9,fparamI10)
   finally:
      aICORPipesCollection.Release(apipe)

def SetFieldValueLastModification(fparamI1,fparamI2,fparamS1,fparamI3,fparamI4,fparamI5,fparamI6,fparamI7,fparamI8,fparamI9,fparamI10):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiiiiiiiiii',fparamS1,109,44+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3,fparamI4,fparamI5,fparamI6,fparamI7,fparamI8,fparamI9,fparamI10)
   finally:
      aICORPipesCollection.Release(apipe)

def SetFieldValueTime(fparamI1,fparamI2,fparamS1,fparamI3,fparamI4,fparamI5,fparamI6,fparamI7):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiiiiiii',fparamS1,110,32+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3,fparamI4,fparamI5,fparamI6,fparamI7)
   finally:
      aICORPipesCollection.Release(apipe)

def SetMethodLastModification(fparamI1,fparamI2,fparamS1,fparamI3,fparamI4,fparamI5,fparamI6,fparamI7,fparamI8,fparamI9):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiiiiiiiii',fparamS1,111,40+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3,fparamI4,fparamI5,fparamI6,fparamI7,fparamI8,fparamI9)
   finally:
      aICORPipesCollection.Release(apipe)

def SetMethodProperty(fparamI1,fparamI2,fparamS1,fparamS2,fparamS3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiiii',string.join([fparamS1,fparamS2,fparamS3],''),112,20+len(fparamS1)+len(fparamS2)+len(fparamS3),fparamI1,fparamI2,len(fparamS1),len(fparamS2),len(fparamS3))
   finally:
      aICORPipesCollection.Release(apipe)

def SetObjectModification(fparamI1,fparamI2,fparamI3,fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',fparamS1,113,16+len(fparamS1),fparamI1,fparamI2,fparamI3,len(fparamS1))
   finally:
      aICORPipesCollection.Release(apipe)

def SetObjectModified(fparamI1,fparamI2,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii','',114,12,fparamI1,fparamI2,fparamI3)
   finally:
      aICORPipesCollection.Release(apipe)

def SetProgress(fparamI1,fparamI2,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii','',115,12,fparamI1,fparamI2,fparamI3)
   finally:
      aICORPipesCollection.Release(apipe)

def SetTestDecFieldValue(fparamI1,fparamI2,fparamS1,fparamI3,fparamI4,fparamS2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiiiii',string.join([fparamS1,fparamS2],''),129,24+len(fparamS1)+len(fparamS2),fparamI1,fparamI2,len(fparamS1),fparamI3,fparamI4,len(fparamS2))
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def SetTestFieldValue(fparamI1,fparamI2,fparamS1,fparamI3,fparamI4,fparamS2,fparamS3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiiiiii',string.join([fparamS1,fparamS2,fparamS3],''),127,28+len(fparamS1)+len(fparamS2)+len(fparamS3),fparamI1,fparamI2,len(fparamS1),fparamI3,fparamI4,len(fparamS2),len(fparamS3))
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def SetTestIncFieldValue(fparamI1,fparamI2,fparamS1,fparamI3,fparamI4,fparamS2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiiiii',string.join([fparamS1,fparamS2],''),128,24+len(fparamS1)+len(fparamS2),fparamI1,fparamI2,len(fparamS1),fparamI3,fparamI4,len(fparamS2))
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def SetVariable(fparamI1,fparamS1,fparamS2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiii',string.join([fparamS1,fparamS2],''),116,12+len(fparamS1)+len(fparamS2),fparamI1,len(fparamS1),len(fparamS2))
   finally:
      aICORPipesCollection.Release(apipe)

def ShellExecute(fparamI1,fparamS1,fparamS2,fparamS3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',string.join([fparamS1,fparamS2,fparamS3],''),117,16+len(fparamS1)+len(fparamS2)+len(fparamS3),fparamI1,len(fparamS1),len(fparamS2),len(fparamS3))
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def SortFile(fparamI1,fparamS1,fparamS2,fparamI2,fparamI3,fparamI4,fparamI5):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiiiiii',string.join([fparamS1,fparamS2],''),118,28+len(fparamS1)+len(fparamS2),fparamI1,len(fparamS1),len(fparamS2),fparamI2,fparamI3,fparamI4,fparamI5)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def StatusInfo(fparamI1,fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiii',fparamS1,119,8+len(fparamS1),fparamI1,len(fparamS1))
   finally:
      aICORPipesCollection.Release(apipe)

def Str2DateTime(fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iii',fparamS1,120,4+len(fparamS1),len(fparamS1))
      ret=apipe.ReadInts(7)
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def Str2HTMLStr(fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iii',fparamS1,121,4+len(fparamS1),len(fparamS1))
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def SummaryEdit(fparamI1,fparamI2):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiii','',122,8,fparamI1,fparamI2)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def URLString2NormalString(fparamS1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iii',fparamS1,123,4+len(fparamS1),len(fparamS1))
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def ValueExists(fparamI1,fparamI2,fparamS1,fparamI3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',fparamS1,124,16+len(fparamS1),fparamI1,fparamI2,len(fparamS1),fparamI3)
      ret=apipe.ReadInt()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def getcommand(fparamI1,fparamS1,fparamS2,fparamS3):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiiiii',string.join([fparamS1,fparamS2,fparamS3],''),125,16+len(fparamS1)+len(fparamS2)+len(fparamS3),fparamI1,len(fparamS1),len(fparamS2),len(fparamS3))
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret

def getline(fparamS1,fparamI1):
   apipe=aICORPipesCollection.Get()
   try:
      apipe.WriteMessage('iiii',fparamS1,126,8+len(fparamS1),len(fparamS1),fparamI1)
      ret=apipe.ReadString()
   finally:
      aICORPipesCollection.Release(apipe)
   return ret



