# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import string
import os

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]

   return

   if 0:
      awidth,aheight=16,16
      adir=ICORUtil.InputDirectory()

      awidth,aheight=16,16
      adir='%ICOR%/WWWRoot/images/icons/twotone/blue'
      aprefix='twotone_'

      awidth,aheight=12,12
      adir='%ICOR%/WWWRoot/images/icons/sweetie2/png'
      aprefix='sweetie2_'

   awidth,aheight=16,16
   adir='%ICOR%/WWWRoot/images/icons/silk/icons'
   aprefix='silk_'

   if not adir:
      return
   print 'adir:',adir
   adir=FilePathAsSystemPath(adir)
   i=string.find(adir,'WWWRoot')
   bdir=adir
   if i>=0:
      bdir='/icormanager'+string.replace(adir[i+7:],'\\','/')
   print '>%s<'%adir
   l=os.listdir(adir)
   acnt=1
   for afname in l:
      if afname[-4:].lower() in ['.jpg','.png','.gif']:
         aname=aprefix+afname[:-4]
         aoid=aclass.Name.Identifiers(aname)
         if aoid<0:
            print acnt,bdir+'/'+afname
            aoid=aclass.AddObject()
            aclass.Location[aoid]=bdir+'/'+afname
            aclass.Name[aoid]=aname
            aclass.Width[aoid]=awidth
            aclass.Height[aoid]=aheight
            acnt=acnt+1
   print 'total:',acnt
   return



