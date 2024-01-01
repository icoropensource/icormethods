# -*- coding: windows-1250 -*-
# saved: 2021/06/08 16:36:02

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from icorlib.wwwmenu.menuutil import ICORWWWMenuItem
import string

def GetMenuPath(aobj,res):
   res.insert(0,aobj.Caption)
   bobj=aobj.ParentMenu
   if bobj:
      GetMenuPath(bobj,res)

def Update1(aclass):
   qclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_Query_WorkSheet_Main']
   aobj=aclass.GetFirstObject()
   while aobj.Exists():
      if aobj.WorkSheetQueriesIDs:
         res=[]
         GetMenuPath(aobj,res)
         apath=string.join(res,'/')
         sl=string.split(aobj.WorkSheetQueriesIDs,',')
         print 'MENU:',aobj.OID,apath
         for aqname in sl:
            qoid=qclass.TableID.Identifiers(aqname)
            if qoid<0:
               print '   zestawienie nie istnieje:',aqname
            else:
               print '   nowe zestawienie:',aqname
               amenu=ICORWWWMenuItem(0,aobj.OID)
               sclass=amenu.MenuClass.Summaries.ClassOfType
               soid=sclass.AddObject()
               sclass.WorksheetQueries[soid]=[qoid,qclass.CID]
               sclass.Name[soid]=qclass.TableTitle[qoid]
               amenu.MenuClass.Summaries.AddRefs(aobj.OID,[soid,sclass.CID])
      aobj.Next()

def Update2(aclass):
   fin=open('c:/icor/out.txt','r')
   l=fin.readline()
   while l:
      sl=string.split(l[:-1],chr(255))
      aoid=int(sl[0])
      aclass.ParamItem[aoid]=sl[1]
      aclass.ParamValue[aoid]=sl[2]
      aclass.ParamSubItem[aoid]=sl[3]
      l=fin.readline()
   fin.close()

def TestUpdate1(aclass):
   Update2(aclass)
   return
   Update1(aclass)
   return

   pclass=aclass.PageHTMLItems.ClassOfType
   aoid=aclass.FirstObject()
   c1,c2=0,0
   while aoid>=0:
      s=aclass.PageHTML[aoid]
      if s!='<P>&nbsp;</P>' and s!='':
         c1=c1+1
         if 1:
            lm=aclass.PageHTML.GetValueLastModified(aoid)
            w=0
            pobj=aclass[aoid].PageHTMLItems
            while pobj:
               if pobj.PageName.Name=='Text':
                  if pobj.TextValue!=s:
                     print aoid,lm,aclass.Caption[aoid]
                     w=1
                     break
               pobj.Next()
            if w:
               poid=pclass.AddObject()
               pclass.LastModification.SetValuesAsDateTime(poid,lm)
               pclass.ModifiedBy[poid]=[0,309] #administrator
               pclass.PageName[poid]=[2,1465] #text
               pclass.TextValue[poid]=s
               aclass.PageHTMLItems.AddRefs(aoid,[poid,pclass.CID],asortedreffield=pclass.LastModification,adescending=1)

#      s=aclass.PageHTMLInfo[aoid]
#      if s!='<P>&nbsp;</P>' and s!='':
#         c2=c2+1
#         if 0:
#            poid=pclass.AddObject()
#            lm=aclass.PageHTMLInfo.GetValueLastModified(aoid)
#            pclass.LastModification.SetValuesAsDateTime(poid,lm)
#            pclass.ModifiedBy[poid]=[0,309] #administrator
#            pclass.PageName[poid]=[1,1465] #info
#            pclass.TextValue[poid]=s
#            aclass.PageHTMLItems.AddRefs(aoid,[poid,pclass.CID],asortedreffield=pclass.LastModification,adescending=1)
      aoid=aclass.NextObject(aoid)
   print c1,c2
   return

def FFunc1(aclass,afield):
   print afield.Name,afield.WWWTreeRecur

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aclass.ForEachField(FFunc1)



