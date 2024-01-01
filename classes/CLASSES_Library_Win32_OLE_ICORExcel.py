# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

try:
   import ICORDelphi
   icorapi=ICORDelphi
except:
   import icorapi

import string

EXCEL_COL_DICT = {
'A' : 1,'B' : 2,'C' : 3,'D' : 4,'E' : 5,'F' : 6,'G' : 7,'H' : 8,'I' : 9,
'J' : 10,'K' : 11,'L' : 12,'M' : 13,'N' : 14,'O' : 15,'P' : 16,'Q' : 17,
'R' : 18,'S' : 19,'T' : 20,'U' : 21,'V' : 22,'W' : 23,'X' : 24,'Y' : 25,
'Z' : 26,'AA' : 27,'AB' : 28,'AC' : 29,'AD' : 30,'AE' : 31,'AF' : 32,
'AG' : 33,'AH' : 34,'AI' : 35,'AJ' : 36,'AK' : 37,'AL' : 38,'AM' : 39,
'AN' : 40,'AO' : 41,'AP' : 42,'AQ' : 43,'AR' : 44,'AS' : 45,'AT' : 46,
'AU' : 47,'AV' : 48,'AW' : 49,'AX' : 50,'AY' : 51,'AZ' : 52,'BA' : 53,
'BB' : 54,'BC' : 55,'BD' : 56,'BE' : 57,'BF' : 58,'BG' : 59,'BH' : 60,
'BI' : 61,'BJ' : 62,'BK' : 63,'BL' : 64,'BM' : 65,'BN' : 66,'BO' : 67,
'BP' : 68,'BQ' : 69,'BR' : 70,'BS' : 71,'BT' : 72,'BU' : 73,'BV' : 74,
'BW' : 75,'BX' : 76,'BY' : 77,'BZ' : 78,'CA' : 79,'CB' : 80,'CC' : 81,
'CD' : 82,'CE' : 83,'CF' : 84,'CG' : 85,'CH' : 86,'CI' : 87,'CJ' : 88,
'CK' : 89,'CL' : 90,'CM' : 91,'CN' : 92,'CO' : 93,'CP' : 94,'CQ' : 95,
'CR' : 96,'CS' : 97,'CT' : 98,'CU' : 99,
'CV' : 100,'CW' : 101,'CX' : 102,'CY' : 103,'CZ' : 104,'DA' : 105,
'DB' : 106,'DC' : 107,'DD' : 108,'DE' : 109,'DF' : 110,'DG' : 111,
'DH' : 112,'DI' : 113,'DJ' : 114,'DK' : 115,'DL' : 116,'DM' : 117,
'DN' : 118,'DO' : 119,'DP' : 120,'DQ' : 121,'DR' : 122,'DS' : 123,
'DT' : 124,'DU' : 125,'DV' : 126,'DW' : 127,'DX' : 128,'DY' : 129,
'DZ' : 130,'EA' : 131,'EB' : 132,'EC' : 133,'ED' : 134,'EE' : 135,
'EF' : 136,'EG' : 137,'EH' : 138,'EI' : 139,'EJ' : 140,'EK' : 141,
'EL' : 142,'EM' : 143,'EN' : 144,'EO' : 145,'EP' : 146,'EQ' : 147,
'ER' : 148,'ES' : 149,'ET' : 150,'EU' : 151,'EV' : 152,'EW' : 153,
'EX' : 154,'EY' : 155,'EZ' : 156,'FA' : 157,'FB' : 158,'FC' : 159,
'FD' : 160,'FE' : 161,'FF' : 162,'FG' : 163,'FH' : 164,'FI' : 165,
'FJ' : 166,'FK' : 167,'FL' : 168,'FM' : 169,'FN' : 170,'FO' : 171,
'FP' : 172,'FQ' : 173,'FR' : 174,'FS' : 175,'FT' : 176,'FU' : 177,
'FV' : 178,'FW' : 179,'FX' : 180,'FY' : 181,'FZ' : 182,'GA' : 183,
'GB' : 184,'GC' : 185,'GD' : 186,'GE' : 187,'GF' : 188,'GG' : 189,
'GH' : 190,'GI' : 191,'GJ' : 192,'GK' : 193,'GL' : 194,'GM' : 195,
'GN' : 196,'GO' : 197,'GP' : 198,'GQ' : 199,'GR' : 200,'GS' : 201,
'GT' : 202,'GU' : 203,'GV' : 204,'GW' : 205,'GX' : 206,'GY' : 207,
'GZ' : 208,'HA' : 209,'HB' : 210,'HC' : 211,'HD' : 212,'HE' : 213,
'HF' : 214,'HG' : 215,'HH' : 216,'HI' : 217,'HJ' : 218,'HK' : 219,
'HL' : 220,'HM' : 221,'HN' : 222,'HO' : 223,'HP' : 224,'HQ' : 225,
'HR' : 226,'HS' : 227,'HT' : 228,'HU' : 229,'HV' : 230,'HW' : 231,
'HX' : 232,'HY' : 233,'HZ' : 234,'IA' : 235,'IB' : 236,'IC' : 237,
'ID' : 238,'IE' : 239,'IF' : 240,'IG' : 241,'IH' : 242,'II' : 243,
'IJ' : 244,'IK' : 245,'IL' : 246,'IM' : 247,'IN' : 248,'IO' : 249,
'IP' : 250,'IQ' : 251,'IR' : 252,'IS' : 253,'IT' : 254,'IU' : 255,
'IV' : 256,
}

EXCEL_COL_LIST=['A',
'B', 'C', 'D', 'E', 'F',
'G', 'H', 'I', 'J', 'K',
'L', 'M', 'N', 'O', 'P',
'Q', 'R', 'S', 'T', 'U',
'V', 'W', 'X', 'Y', 'Z',
'AA', 'AB', 'AC', 'AD', 'AE',
'AF', 'AG', 'AH', 'AI', 'AJ',
'AK', 'AL', 'AM', 'AN', 'AO',
'AP', 'AQ', 'AR', 'AS', 'AT',
'AU', 'AV', 'AW', 'AX', 'AY',
'AZ', 'BA', 'BB', 'BC', 'BD',
'BE', 'BF', 'BG', 'BH', 'BI',
'BJ', 'BK', 'BL', 'BM', 'BN',
'BO', 'BP', 'BQ', 'BR', 'BS',
'BT', 'BU', 'BV', 'BW', 'BX',
'BY', 'BZ', 'CA', 'CB', 'CC',
'CD', 'CE', 'CF', 'CG', 'CH',
'CI', 'CJ', 'CK', 'CL', 'CM',
'CN', 'CO', 'CP', 'CQ', 'CR',
'CS', 'CT', 'CU', 'CV', 'CW',
'CX', 'CY', 'CZ', 'DA', 'DB',
'DC', 'DD', 'DE', 'DF', 'DG',
'DH', 'DI', 'DJ', 'DK', 'DL',
'DM', 'DN', 'DO', 'DP', 'DQ',
'DR', 'DS', 'DT', 'DU', 'DV',
'DW', 'DX', 'DY', 'DZ', 'EA',
'EB', 'EC', 'ED', 'EE', 'EF',
'EG', 'EH', 'EI', 'EJ', 'EK',
'EL', 'EM', 'EN', 'EO', 'EP',
'EQ', 'ER', 'ES', 'ET', 'EU',
'EV', 'EW', 'EX', 'EY', 'EZ',
'FA', 'FB', 'FC', 'FD', 'FE',
'FF', 'FG', 'FH', 'FI', 'FJ',
'FK', 'FL', 'FM', 'FN', 'FO',
'FP', 'FQ', 'FR', 'FS', 'FT',
'FU', 'FV', 'FW', 'FX', 'FY',
'FZ', 'GA', 'GB', 'GC', 'GD',
'GE', 'GF', 'GG', 'GH', 'GI',
'GJ', 'GK', 'GL', 'GM', 'GN',
'GO', 'GP', 'GQ', 'GR', 'GS',
'GT', 'GU', 'GV', 'GW', 'GX',
'GY', 'GZ', 'HA', 'HB', 'HC',
'HD', 'HE', 'HF', 'HG', 'HH',
'HI', 'HJ', 'HK', 'HL', 'HM',
'HN', 'HO', 'HP', 'HQ', 'HR',
'HS', 'HT', 'HU', 'HV', 'HW',
'HX', 'HY', 'HZ', 'IA', 'IB',
'IC', 'ID', 'IE', 'IF', 'IG',
'IH', 'II', 'IJ', 'IK', 'IL',
'IM', 'IN', 'IO', 'IP', 'IQ',
'IR', 'IS', 'IT', 'IU', 'IV',]

def GetCellAddressAsExcelCellAddress(acol,arow=0):
   if arow:
      return EXCEL_COL_LIST[acol-1]+str(arow)
   else:
      return EXCEL_COL_LIST[acol-1]+str(arow)

def GetExcelCellAddressAsCellAddress(s):
   if s[1]>'9':
      return [int(EXCEL_COL_DICT[s[:2].upper()]),int(s[2:])]
   return [int(EXCEL_COL_DICT[s[0].upper()]),int(s[1:])]

class ICORExcel:
   def __init__(self,anew=0):
      icorapi.ExcelOpen(anew)
   def __del__(self):
      icorapi.ExcelClose()
   def __getitem__(self,key):
      acol,arow=key
      return icorapi.ExcelGetCellValue(acol,arow)
   def __setitem__(self,key,value):
      acol,arow=key
      return icorapi.ExcelSetCellValue(acol,arow,value)
   def Execute(self,awhat,avalue=''):
      return icorapi.ExcelExecute(awhat,avalue)
   def AddSheet(self,aname):
      self.Execute('AddSheet',aname)
   def SelectSheet(self,aname):
      self.Execute('SelectSheet',aname)
   def SetSheetName(self,aname):
      self.Execute('SetSheetName',aname)
   def GetSheetName(self):
      return self.Execute('GetSheetName')
   def GetSheetID(self):
      return self.Execute('GetSheetID')
   def ClearSheet(self):
      self.Execute('ClearSheet')
   def AutoFit(self):
      self.Execute('AutoFit')
   def EnableUpdating(self):
      self.Execute('ScreenUpdating','1')
   def DisableUpdating(self):
      self.Execute('ScreenUpdating','0')
   def Show(self):
      self.Execute('Visible','1')


