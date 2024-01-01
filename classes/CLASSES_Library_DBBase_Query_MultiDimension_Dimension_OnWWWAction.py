# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
from CLASSES_Library_NetBase_WWW_Server_DoObjectEdit import ProcessObjectEdit
import string

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Name',aoid=aoid)
   awwweditor.RegisterField('TotalName',aoid=aoid)
   awwweditor.RegisterField('TitleCenteredFramed',aoid=aoid)
   awwweditor.RegisterField('FrameBegin',aoid=aoid)
   awwweditor.RegisterField('FrameEnd',aoid=aoid)
   awwweditor.RegisterField('FramedTotal',aoid=aoid)
   awwweditor.RegisterField('EmptyRowBefore',aoid=aoid)
   awwweditor.RegisterField('EmptyRowBeforeTotal',aoid=aoid)
   awwweditor.RegisterField('DisableTitle',aoid=aoid)
   awwweditor.RegisterField('DisableTotal',aoid=aoid)
   awwweditor.RegisterField('ShowSubDimensions',aoid=aoid)
   awwweditor.RegisterField('IsTotalBold',aoid=aoid)
   awwweditor.RegisterField('IsBold',aoid=aoid)
   awwweditor.RegisterField('IsItalic',aoid=aoid)
   awwweditor.RegisterField('IsTotalBiggerFont',aoid=aoid)
   awwweditor.RegisterField('IsTotalDoubleFrameAfter',aoid=aoid)
   awwweditor.RegisterField('FrameSize',aoid=aoid)
#   awwweditor.RegisterField('ShowSubDimensions',aoid=aoid)
   awwweditor.RegisterField('DisplayValueModifier',aoid=aoid,aempty='0.0')
   awwweditor.RegisterField('FormulaName',aoid=aoid)
   awwweditor.RegisterField('FormulaText',aoid=aoid)
   return awwweditor

def OnWWWAction(aclass,amenu,file):
   if amenu.Action=='ObjectEdit':
      pcid,poid,pfieldname=amenu.WWWParam
      awwweditor=RegisterFields(aclass,amenu,file,poid,None)
      awwweditor.Write(arefCID=pcid,arefOID=poid,arefField=pfieldname)

def OnWWWActionSubmit(aclass,amenu,areport,file):
   if amenu.Action in ['ObjectEdit']:
      awwweditor=RegisterFields(aclass,amenu,file,-1,areport)
      aoid=awwweditor['refOID']
      w=1
      w=w and awwweditor.CheckField('Name',file)
      w=w and awwweditor.CheckField('DisplayValueModifier',file)
      if not w:
         file.write('<font color="red"><h2><u>Popraw dane i spróbuj jeszcze raz.</u></h2><hr></font>\n')
         file.write('<a class=reflistoutnavy href="icormain.asp?jobtype=objectedit&CID=%d&OID=%d">Ostatnio edytowany obiekt</a><hr>'%(aclass.CID,aoid))
      else:
         aobj=aclass[aoid]
         aobj.Name=awwweditor['Name']
         aobj.TotalName=awwweditor['TotalName']
         aobj.TitleCenteredFramed=awwweditor['TitleCenteredFramed']
         aobj.FrameBegin=awwweditor['FrameBegin']
         aobj.FrameEnd=awwweditor['FrameEnd']
         aobj.EmptyRowBefore=awwweditor['EmptyRowBefore']
         aobj.EmptyRowBeforeTotal=awwweditor['EmptyRowBeforeTotal']
         aobj.DisableTitle=awwweditor['DisableTitle']
         aobj.DisableTotal=awwweditor['DisableTotal']
         aobj.IsTotalBold=awwweditor['IsTotalBold']
         aobj.IsItalic=awwweditor['IsItalic']
         aobj.IsTotalBiggerFont=awwweditor['IsTotalBiggerFont']
         aobj.FramedTotal=awwweditor['FramedTotal']
         aobj.ShowSubDimensions=awwweditor['ShowSubDimensions']
         aobj.IsBold=awwweditor['IsBold']
         aobj.IsTotalDoubleFrameAfter=awwweditor['IsTotalDoubleFrameAfter']
         aobj.FrameSize=awwweditor['FrameSize']
#         aobj.ShowSubDimensions=awwweditor['ShowSubDimensions']
         aobj.DisplayValueModifier=awwweditor['DisplayValueModifier']
         aobj.FormulaName=awwweditor['FormulaName']
         aobj.FormulaText=awwweditor['FormulaText']
         ProcessObjectEdit(file,aclass,aoid,amenu.uid)












