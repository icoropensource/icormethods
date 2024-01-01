# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def num2strPL(num):
   word= {'0':'','1':'jeden ','2':'dwa ','3':'trzy ','4':'cztery ','5':'pi�� ','6':'sze�� ','7':'siedem ','8':'osiem ','9':'dziewi�� ',
      '10':'dziesi�� ','11':'jedena�cie ','12':'dwana�cie ','13':'trzyna�cie ','14':'czterna�cie ','15':'pi�tna�cie ','16':'szesna�cie ','17':'siedemna�cie ','18':'osiemna�cie ','19':'dziewi�tna�cie ',
      '20':'dwadzie�cia ','30':'trzydzie�ci ','40':'czterdzie�ci ','50':'pi��dziesi�t ','60':'sze��dziesi�t ','70':'siedemdziesi�t ','80':'osiemdziesi�t ','90':'dziewi��dziesi�t ',
      '100':'sto ','200':'dwie�cie ','300':'trzysta ','400':'czterysta ','500':'pi��set ','600':'sze��set ','700':'siedemset ','800':'osiemset ','900':'dziewi��set '
   }
   tys=(('','',''),('tysi�c ','tysi�ce ','tysi�cy '),('milion ','miliony ','milion�w '),('miliard ','miliardy ','miliard�w '))
   wynik,ind1='',0
   while num<>0:
      s=num%1000
      sto=s/100
      dzi=(s-sto*100)/10
      jed=s-sto*100-dzi*10
      if jed==1 and dzi==0 and sto==0:
         ind2=0
      elif jed>1 and jed<5 and dzi==0 and sto==0:
         ind2=1
      else:
         ind2=2
      wynik=tys[ind1][ind2]+wynik
      if dzi==1:
         wynik=word[str(sto*100)]+word[str(dzi*10+jed)]+wynik
      else:
         wynik=word[str(sto*100)]+word[str(dzi*10)]+word[str(jed)]+wynik
      num=(num-s)/1000
      ind1=ind1+1
   return wynik

def KwotaSlownie(akwota):
   ret=''
   KwSl='.'.split(str(akwota))
   if  KwSl[0]=="0":
       ret="zero";
   else:
       self.KwotaSlownie = num2str (int(KwSl[0])).rstrip();
   if ( len ( KwSl[0] ) == 1 ):
       if ( KwSl[0] == "1" ):
           self.KwotaSlownie += " z�oty "
       elif ( KwSl[0] in ("2", "3", "4") ):
           self.KwotaSlownie += " z�ote "
       else:
           self.KwotaSlownie += " z�otych "
   else:
       przedost = KwSl[0][len(KwSl[0])-2]
       ost = KwSl[0][len(KwSl[0])-1]
       if ( przedost != "1" ):
           if ( ost in ("2", "3", "4") ):
               self.KwotaSlownie += " z�ote "
           else:
               self.KwotaSlownie += " z�otych "
       else:
           self.KwotaSlownie += " z�otych "               
   self.KwotaSlownie += KwSl[1] + "/100"
   self.Slownie_V.SetValue (self.KwotaSlownie)
   self.Faktura.Dol.Slownie = self.KwotaSlownie

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   return


