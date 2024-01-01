# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

import random

phonedata = [
   ['+48-91-',4000000,741234,899897,'telefon domowy'],
   ['+48-91-',4000000,741234,899897,'telefon służbowy'],
   ['+48-91-',4000000,741234,899897,'telefon służbowy'],
   ['+48-91-',4000000,741234,899897,'telefon sekretariatu'],
   ['+48-91-',4000000,741234,899897,'telefon kontaktowy w godz. 18-22'],
   ['0-501-',100000,12311,98876,'telefon komórkowy'],
   ['0-601-',700000,12311,98876,'telefon komórkowy'],
   ['0-602-',700000,12311,98876,'telefon komórkowy'],
   ]

class NumeryTelefonow:
   def __init__(self):
      self.Data=phonedata
      self.Opis=''
   def __getattr__(self,name):
      if name=='Numer':
         pdata=self.Data[random.randint(0,len(self.Data)-1)]
         self.Opis=pdata[4]
         return pdata[0]+str(pdata[1]+random.randint(pdata[2],pdata[3]))



