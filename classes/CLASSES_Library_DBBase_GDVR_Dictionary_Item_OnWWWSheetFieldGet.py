# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORChart import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import aICORWWWServerInterface
from CLASSES_Library_NetBase_WWW_HTML_Tree_SimpleLinks_Main import SimpleLinksHTMLTree
import random

def OnBeforeSheetOutput(aclass,aoid,asheetid,file):
   pass

def OnBeforeFieldOutput(aclass,afield,aoid,asheetid,file,afields):
   if afield.Name=='ValueFields':
      file.write('</table><br>')
      atree=SimpleLinksHTMLTree('Pola i wartości')
      aobj=aclass[aoid]
      aobj2=aobj.ValueFields
      while aobj2:
         sh='icormain.asp?jobtype=objectedit&CID=%d&OID=%d'%(aobj2.Class.CID,aobj2.OID)
         ss=aobj2.Description
         if ss:
            ss=', '+ss
         dnode=atree.RootNode.AddNode(aobj2.Caption+ss,sh)
         plist=[]
         aobj3=aobj2.DateValues
         while aobj3:             
            sn=aobj3.ValueDT+'<font color="brown">, '+aobj3.ValueF+'</font>'
            sh='icormain.asp?jobtype=objectedit&CID=%d&OID=%d'%(aobj3.Class.CID,aobj3.OID)
            plist.append([sn,sh])
            aobj3.Next()
         plist.sort()
         for sn,sh in plist:
            pnode=dnode.AddNode(sn,sh)
         aobj2.Next()
      atree.Write(file)
      file.write('<table><br>')
      return 0

def OnAfterFieldOutput(aclass,afield,aoid,asheetid,file,afields):
   pass

def OnAfterSheetOutput(aclass,aoid,asheetid,file,afields):
   if 'ValueFields' in afields: #enter value here
      achart=ICORHTMLChartMSControl20(aclass,1000+asheetid)
      achart.Title=aclass.ItemName[aoid] #enter value here
      achart.ChartType=VtChChartType3dBar
      achart.Stacked=0
      achart.Chart3D=1

      ddict={}
      clist=[]
      aobj=aclass[aoid]
      aobj2=aobj.ValueFields
      while aobj2:
         ss=aobj2.Description
         if ss:
            ss=aobj2.Caption+', '+ss
         else:
            ss=aobj2.Caption
         clist.append(ss)
         aobj3=aobj2.DateValues
         while aobj3:
            adt=aobj3.ValueDT
            vdict=ddict.get(adt,{})
            vdict[ss]=aobj3.ValueF
            ddict[adt]=vdict
            aobj3.Next()
         aobj2.Next()
      clist.sort()
      for acolumn in clist:
         achart.AddColumn(acolumn)
      dlist=ddict.keys()
      dlist.sort()

      arow=1
      for adate in dlist:
         achart.AddRow(adate)
         for i in range(len(clist)):
            try:
               achart[arow,i+1]=ddict[adate][clist[i]]
            except:
               achart[arow,i+1]=0
         arow=arow+1
      if arow>1:
         achart.WriteToFile(file)
      return
                                            


