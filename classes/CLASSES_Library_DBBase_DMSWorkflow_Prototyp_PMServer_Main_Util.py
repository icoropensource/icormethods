# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def num2strPL(num):
   word= {'0':'','1':'jeden ','2':'dwa ','3':'trzy ','4':'cztery ','5':'pięć ','6':'sześć ','7':'siedem ','8':'osiem ','9':'dziewięć ',
      '10':'dziesięć ','11':'jedenaście ','12':'dwanaście ','13':'trzynaście ','14':'czternaście ','15':'piętnaście ','16':'szesnaście ','17':'siedemnaście ','18':'osiemnaście ','19':'dziewiętnaście ',
      '20':'dwadzieścia ','30':'trzydzieści ','40':'czterdzieści ','50':'pięćdziesiąt ','60':'sześćdziesiąt ','70':'siedemdziesiąt ','80':'osiemdziesiąt ','90':'dziewięćdziesiąt ',
      '100':'sto ','200':'dwieście ','300':'trzysta ','400':'czterysta ','500':'pięćset ','600':'sześćset ','700':'siedemset ','800':'osiemset ','900':'dziewięćset '
   }
   tys=(('','',''),('tysiąc ','tysiące ','tysięcy '),('milion ','miliony ','milionów '),('miliard ','miliardy ','miliardów '))
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
           self.KwotaSlownie += " złoty "
       elif ( KwSl[0] in ("2", "3", "4") ):
           self.KwotaSlownie += " złote "
       else:
           self.KwotaSlownie += " złotych "
   else:
       przedost = KwSl[0][len(KwSl[0])-2]
       ost = KwSl[0][len(KwSl[0])-1]
       if ( przedost != "1" ):
           if ( ost in ("2", "3", "4") ):
               self.KwotaSlownie += " złote "
           else:
               self.KwotaSlownie += " złotych "
       else:
           self.KwotaSlownie += " złotych "               
   self.KwotaSlownie += KwSl[1] + "/100"
   self.Slownie_V.SetValue (self.KwotaSlownie)
   self.Faktura.Dol.Slownie = self.KwotaSlownie

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   return


