# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import string
import bisect
import types

class SimpleLinksHTMLTreeNode:
   def __init__(self,acaption=None,aref='',atreeid='0',aexpanded=0,aparent=None,aonclick=''):
      if acaption is None:
         acaption=''
      else:
         if not acaption:
            acaption='--'
      self.Caption=string.replace(acaption,'"','')
      self.Caption=string.replace(self.Caption,"'",'')
      self.Ref=aref
      self.OnClick=aonclick
      self.Parent=aparent
      self.TreeID=atreeid
      self.SubNodes=[]
      self.Expanded=aexpanded
   def __cmp__(self,other):
      return ICORUtil.ICORCompareText(string.strip(self.Caption),string.strip(other.Caption))
   def AddNode(self,acaption,aref='',aexpanded=0,asorted=0,aonclick=''):
      anode=SimpleLinksHTMLTreeNode(acaption,aref,self.TreeID,aexpanded,self,aonclick)
      if asorted:
         bisect.insort_left(self.SubNodes,anode)
      else:
         self.SubNodes.append(anode)
      return anode
   def Write(self,file,aindent=0,acnt=0,alast=0,aindentstr=''):
      sdn,sd,sh='','',''
      file.write('<span style="WHITE-SPACE:nowrap;">')
      if aindent:
         file.write(aindentstr)
         sdf='folder_%s_%s'%(self.TreeID,str(acnt))
         if self.SubNodes!=[]:
            if alast:
               f1='/icormanager/images/tree/menu_corner_plus.png'
               f2='/icormanager/images/tree/menu_corner_minus.png'
            else:
               f1='/icormanager/images/tree/menu_tee_plus.png'
               f2='/icormanager/images/tree/menu_tee_minus.png'
            sdn='div_%s_%s'%(self.TreeID,str(acnt))
            sd=' onclick="treeNodeClick%s();" mDIVID="%s" mFOLDERID="%s"'%(self.TreeID,sdn,sdf)
            f3='/icormanager/images/tree/menu_folder_closed.png'
            f4='/icormanager/images/tree/menu_folder_open.png'
            scur='cursor:pointer;'
         else:
            if alast:
               f1='/icormanager/images/tree/menu_corner.png'
            else:
               f1='/icormanager/images/tree/menu_tee.png'
            f2=f1
            f3='/icormanager/images/tree/menu_link_txt.png'
            f4=f3
            scur=''

         if self.Ref:
            sh=' href="%s"'%(self.Ref,)
         if self.OnClick:
            sh=sh+' onclick="%s"'%(self.OnClick,)
            if not self.Ref:
               sh=sh+' style="cursor:pointer;"'
         if self.Expanded:
            fexp=f2
            fexp2=f4
         else:
            fexp=f1
            fexp2=f3

         s1='<img border=0 align=absmiddle style="%svspace:0;hspace:0;align:absmiddle;" SRC="%s" mImage1="%s" mImage2="%s"%s>'%(scur,fexp,f1,f2,sd)
         file.write(s1)

         s1='<img border=0 id="%s" align=absmiddle style="vspace:0;hspace:0;align:absmiddle;" SRC="%s" mImage1="%s" mImage2="%s">'%(sdf,fexp2,f3,f4)
         file.write(s1)

         s2='&nbsp;<a%s class=reflistoutnavy style="vspace:0;hspace:0;align:absmiddle;">%s</a>'%(sh,XMLUtil.GetAsXMLStringNoPL(self.Caption))
         file.write(s2+'<br>\n')

         if sdn:
            if self.Expanded:
               se=''
            else:
               se=' style="display:none;"'
            file.write('<span id="%s"%s>\n'%(sdn,se))
      else:
         if self.Ref:
            sh=' href="%s"'%(self.Ref,)
         if self.OnClick:
            sh=sh+' onclick="%s"'%(self.OnClick,)
            if not self.Ref:
               sh=sh+' style="cursor:pointer;"'
         if sh:
            s2='<b>&nbsp;&nbsp;<a%s class=reflistoutnavy style="vspace:0;hspace:0;align:absmiddle;">%s</a></b><br>\n'%(sh,XMLUtil.GetAsXMLStringNoPL(self.Caption))
            file.write(s2)
         else:
            file.write('<img class=tree align=absmiddle src="/icormanager/images/tree/menu_root.png"><b>&nbsp;&nbsp;%s</b><br>\n'%XMLUtil.GetAsXMLStringNoPL(self.Caption))
      for i in range(len(self.SubNodes)):
         anode=self.SubNodes[i]
         blast=i==len(self.SubNodes)-1
         if alast:
            si=aindentstr+'<img src="/icormanager/images/tree/empty.png" align=absmiddle style="vspace:0;hspace:0;align:absmiddle;">'
         else:
            if aindent:
               si=aindentstr+'<img src="/icormanager/images/tree/menu_bar.png" align=absmiddle style="vspace:0;hspace:0;align:absmiddle;">'
            else:
               si=''
         acnt=anode.Write(file,aindent+1,acnt+1,alast=blast,aindentstr=si)
      if sdn:
         file.write('</span>\n')
      file.write('</span>\n')
      return acnt+1

class SimpleLinksHTMLTree:
   def __init__(self,acaption=None,aref='',atreeid='0',aexpanded=1,aonclick=''):
      self.TreeID=atreeid
      self.RootNode=SimpleLinksHTMLTreeNode(acaption,aref,atreeid,aexpanded,None,aonclick=aonclick)
   def Write(self,file):
      aconnection=ICORUtil.GetCONNECTION()
      fopened=isinstance(file,types.StringTypes)
      if len(self.RootNode.SubNodes)==1:
         self.RootNode.SubNodes[0].Expanded=1
      if fopened:
         file=open(file,'w')
         file.write("""
<html>
<head>
<link rel=STYLESHEET type="text/css" href="icor.css" title="SOI">
<meta http-equiv="Content-Language" content="pl">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta name="GENERATOR" content="ICOR">
<title>%s</title>
</head>                         
<body>
"""%(XMLUtil.GetAsXMLStringNoPL(self.RootNode.Caption),))
      file.write("""
<SCRIPT LANGUAGE=JavaScript DEFER>
function treeNodeClick%s() {
   var aelement=window.event.srcElement;
   var sdiv=aelement.getAttribute("mDIVID");
   var adiv=document.getElementById(sdiv);
   var simg=aelement.getAttribute("mFOLDERID");
   var aimg=document.getElementById(simg);
   if (adiv.style.display=='none') {
      adiv.style.display='';
      aelement.src=aelement.getAttribute("mImage2");
      aimg.src=aimg.getAttribute("mImage2");
   } else {
      adiv.style.display='none'; 
      aelement.src=aelement.getAttribute("mImage1");
      aimg.src=aimg.getAttribute("mImage1");
   }
}
</SCRIPT>
"""%(self.TreeID,))
      file.write('<br><div style="font-size:12px">\n')
      self.RootNode.Write(file)
      file.write('</div>\n')
      if fopened:
         file.write('</body></html>')
         file.close()

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
#   atree=SimpleLinksHTMLTree('Lista przykładowa')
   atree=SimpleLinksHTMLTree()
   anode=atree.RootNode.AddNode('pozycja1','www.icor.pl',aexpanded=1)
   bnode=anode.AddNode('pozycja 1-1','www.icor.pl')
   bnode=anode.AddNode('pozycja 1-2','www.icor.pl')
   anode=atree.RootNode.AddNode('pozycja2','www.icor.pl')
   bnode=anode.AddNode('pozycja 2-1','www.icor.pl')
   cnode=bnode.AddNode('pozycja 2-1-1','www.icor.pl')
   cnode=bnode.AddNode('pozycja 2-1-2','www.icor.pl')
   cnode=bnode.AddNode('pozycja 2-1-3','www.icor.pl')
   bnode=anode.AddNode('pozycja 2-2','www.icor.pl')
   anode=atree.RootNode.AddNode('pozycja2','www.icor.pl')
   bnode=anode.AddNode('pozycja 2-1','www.icor.pl')
   cnode=bnode.AddNode('pozycja 2-1-1','www.icor.pl')
   cnode=bnode.AddNode('pozycja 2-1-2','www.icor.pl')
   cnode=bnode.AddNode('pozycja 2-1-3','www.icor.pl')
   bnode=anode.AddNode('pozycja 2-2','www.icor.pl',aexpanded=1)
   anode=bnode.AddNode('pozycja2','www.icor.pl',aexpanded=1)
   bnode=anode.AddNode('pozycja 2-1','www.icor.pl',aexpanded=1)
   cnode=bnode.AddNode('pozycja 2-1-1','www.icor.pl')
   cnode=bnode.AddNode('pozycja 2-1-2','www.icor.pl')
   cnode=bnode.AddNode('pozycja 2-1-3','www.icor.pl')
   bnode=anode.AddNode('pozycja 2-2','www.icor.pl',aexpanded=1)

   fname='c:/icor/html/output/output.html'
   atree.Write(fname)
   ExecuteShellCommand(fname)
   return



