# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

ChartTypes=[
   [0,'Clustered Column'],
   [1,'Stacked Column'],
   [2,'100% Stacked Column'],
   [3,'Clustered Bar'],
   [4,'Stacked Bar'],
   [5,'100% Stacked Bar'],
   [6,'Line'],
   [8,'Stacked Line'],
   [10,'100% Stacked Line'],
   [7,'Line with Markers'],
   [9,'Stacked Line with Markers'],
   [11,'100% Stacked Line with Markers'],
   [12,'Smooth Line'],
   [14,'Stacked Smooth Line'],
   [16,'100% Stacked Smooth Line'],
   [13,'Smooth Line with Markers'],
   [15,'Stacked Smooth Line with Markers'],
   [17,'100% Stacked Smooth Line with Markers'],
   [18,'Pie'],
   [19,'Pie Exploded'],
   [20,'Stacked Pie'],
   [21,'Scatter'],
   [25,'Scatter with Lines'],
   [24,'Scatter with Markers and Lines'],
   [26,'Filled Scatter'],
   [23,'Scatter with Smooth Lines'],
   [22,'Scatter with Markers and Smooth Lines'],
   [27,'Bubble'],
   [28,'Bubble with Lines'],
   [29,'Area'],
   [30,'Stacked Area'],
   [31,'100% Stacked Area'],
   [32,'Doughnut'],
   [33,'Exploded Doughnut'],
   [34,'Radar with Lines'],
   [35,'Radar with Lines and Markers'],
   [36,'Filled Radar'],
   [37,'Radar with Smooth Lines'],
   [38,'Radar with Smooth Lines and Markers'],
   [39,'High-Low-Close'],
   [40,'Open-High-Low-Close'],
   [41,'Polar'],
   [42,'Polar with Lines'],
   [43,'Polar with Lines and Markers'],
   [44,'Polar with Smooth Lines'],
   [45,'Polar with Smooth Lines and Markers'],
]

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   for aid,aname in DATA1:
      aoid=aclass.AddObject()
      aclass.ChartID[aoid]=str(aid)
      aclass.Name[aoid]=aname
   return



