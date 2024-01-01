# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORSecurity as ICORSecurity
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_WWW_Server_ServerUtil as ServerUtil
import icordbmain.adoutil as ADOLibInit
import subprocess
import time
import string
import os
import icordbmain.dbaccess as dbaccess

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   ret='OK'
   l=string.split(FieldName,ServerUtil.SPLIT_CHAR_PARAM)
   if len(l)!=8:
      return 'Nieprawidłowa ilość parametrów.'
   araportoid=l[0]
   aitemoid=l[1]
   atoid=l[2]
   atitle=l[3]
   adescription=l[4]
   adepartment=l[5]
   aauthor=l[6]
   amode=l[7]
   aretoid=0
   if amode[-4:]=='_oid':
      amode=amode[:-4]
      aretoid=1
      ret=''
   apluginoid=OID
   if apluginoid>=0:
      lclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Component_Plugin']
      aobj=lclass[apluginoid]
      avars=ICORUtil.ParseVars(aobj.PluginVars)
      if amode=='pdf_htmldoc':
         aPath_HTMLDOC=avars.get('aPath_HTMLDOC','')
         if not aPath_HTMLDOC:
            if aretoid:
               return ''
            else:
               return 'Obsługa raportów PDF nie jest zainstalowana'
         if string.find(aPath_HTMLDOC,' ')>=0:
            if aPath_HTMLDOC[:1]!='"' and aPath_HTMLDOC[-1:]!='"':
               aPath_HTMLDOC='"'+aPath_HTMLDOC+'"'
         aPaths_Images=avars.get('aPaths_Images','')
         aparmimages=''
         if aPaths_Images:
            if aPaths_Images[-1:]!=';':
               aPaths_Images=aPaths_Images+';'
            aparmimages=' --path "%s"'%aPaths_Images

   tclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Dotyczy']
   tobj=tclass[int(atoid)]
   abasenamemodifier=tobj.Projekt.BaseNameModifier

   adatapath=FilePathAsSystemPath(tobj.Projekt.WWWDataPath,aslash='/')
   if adatapath[-1:]!='/':
      adatapath=adatapath+'/'
   adatapath=adatapath+'sqlfiles/'
   try:
      aado=ADOLibInit.ADOUtil(aconnectionstring,acnt=1,acominitialize=1,dbaccessobj=tobj.Projekt.DBAccess)
   except Exception,v:
      print 'Exception:',v
      ADOLibInit.handle_com_error(v)
      import traceback
      traceback.print_exc()
      if aretoid:
         return ''
      else:
         return 'Wystąpił problem z dostępem do danych'
   try:
      w=0
      try:                            
         rs=aado.GetRS("select _OID, Name, Path, FileSize, LastModification, Description, InformacjaPodmiotUdostepniajacy, InformacjaOsobaOdpowiedzialna, InformacjaDataWytworzenia, RefTable, RefOID, _datetime, _UID, _UserName from %sFILEUPLOADS_0 WHERE _OID='-1'"%(abasenamemodifier,))
         w=1
      except:
         import traceback
         traceback.print_exc()
         if aretoid:
            return ''
         else:
            return 'Wystąpił problem z dostępem do listy plików'
      foid=''
      try:                            
         if w and rs.State!=aado.adoconst.adStateClosed:
            if rs.EOF or rs.BOF:
               rs.AddNew()
            if amode=='pdf':
               afiletitle=ICORUtil.GetStringAsSafeFileName(atitle+' - '+ICORUtil.tdatetime2fmtstr(adelimiter='',atimedelimiter='',apartdelimiter='-')+'.pdf')
            elif amode=='doc':
               afiletitle=ICORUtil.GetStringAsSafeFileName(atitle+' - '+ICORUtil.tdatetime2fmtstr(adelimiter='',atimedelimiter='',apartdelimiter='-')+'.docx')
            rs.Fields.Item("Name").Value=afiletitle
            rs.Fields.Item("Path").Value=afiletitle
   #         rs("FileSize")=CLng(mitems(i))
   #         rs("LastModification")=mitems(i)
            rs.Fields.Item("Description").Value=adescription
            rs.Fields.Item("InformacjaPodmiotUdostepniajacy").Value=adepartment
            rs.Fields.Item("InformacjaOsobaOdpowiedzialna").Value=aauthor
   #         rs("InformacjaDataWytworzenia")=getStrAsDateTime(mitems(i),0,0,0)
            rs.Fields.Item("RefTable").Value=abasenamemodifier+'BZR_'+atoid
            rs.Fields.Item("RefOID").Value=aitemoid
            rs.Fields.Item("_UID").Value=str(UID)
            auser=ICORSecurity.ICORSecurityUser(UID)
            rs.Fields.Item("_UserName").Value=auser.UserName
   #         rs("_datetime")=Now
            aado.UpdateRS(rs)
            foid=ADOLibInit.GetRSValueAsStr(rs,'_OID')
            if aretoid:
               ret=foid
   #         print 'FOID:',foid
            rs=aado.CloseRS(rs)
      except:
         import traceback
         traceback.print_exc()
         if aretoid:
            return ''
         else:
            return 'Wystąpił problem z zapisem sygnatury pliku'
      try:
         if foid:
#            fout=open('d:/icor/output.htm','wb')
#            fout.write(Value)
#            fout.close()
            apdf=''
            alen=0
            if amode=='pdf':
               aparamspath=FilePathAsSystemPath('%ICOR%/bin/webutils/wkhtmltopdf/wkhtmltopdf.exe')
               aparams=aparamspath+' --encoding windows-1250 -q --print-media-type - %s%s.dat'%(adatapath,foid)
               p=subprocess.Popen(aparams,shell=False,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
               p.stdin.write(Value)
               p.stdin.close()
               p.stdout.close()
               acnt=12
               while acnt:
                  try:
                     alen=os.path.getsize('%s%s.dat'%(adatapath,foid))
                     break
                  except:
                     acnt=acnt-1
                     if acnt:
                        time.sleep(0.2)
            elif amode=='doc':
               apdf=Value
               alen=len(apdf)
            elif amode=='pdf_htmldoc':
               aparams='%s -t pdf14 --webpage --no-title --linkstyle plain --size A4 --left 1.00in --right 0.50in --top 0.50in --bottom 0.50in --header ... --footer ..1 --nup 1 --tocheader .t. --tocfooter ..i --portrait --color --no-pscommands --no-xrxcomments --compression=9 --jpeg=98 --fontsize 7.0 --fontspacing 1.1 --headingfont Helvetica --bodyfont Helvetica --headfootsize 10.0 --headfootfont Helvetica --charset cp-1250 --links --embedfonts --pagemode document --pagelayout single --firstpage p1 --pageeffect none --pageduration 10 --effectduration 1.0 --no-encryption --permissions all  --owner-password ""  --user-password "" --browserwidth 800%s --quiet -'%(aPath_HTMLDOC,aparmimages)
               p=subprocess.Popen(aparams,shell=False,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
               p.stdin.write(Value)
               p.stdin.close()
               apdf=p.stdout.read()
               p.stdout.close()
            if apdf:
               alen=len(apdf)
               fout=open(adatapath+foid+'.dat','wb')
               fout.write(apdf)
               fout.close()
            aado.Execute("UPDATE %sFILEUPLOADS_0 SET FileSize=%d WHERE _OID='%s'"%(abasenamemodifier,alen,foid))
      except:
         import traceback
         traceback.print_exc()
         if aretoid:
            return ''
         else:
            return 'Wystąpił problem z konwersją pliku.'
   finally:
      aado.Close()
   return ret


