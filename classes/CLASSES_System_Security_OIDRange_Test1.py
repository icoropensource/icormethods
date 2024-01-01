# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import time

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   for aoid in [2 ,
3 ,
4 ,
5 ,
6 ,
7 ,
8 ,
9 ,
10,
11,
12,
13,
14,
15,
16,
17,
18,
19,
20,
21,
22,
24,
25,
26,
27,
28,
29,
30,
31,
32,
33,
34,
36,
37,
38,
39,
40,
41,
42,
43,
44,
45,
46,
47,
48,
49,
50,
51,
52,
53,
54,
55,
56,
57,
58,
59,
60,
61,
62,
63,
64,
65,
66,
67,
68,
69,
70,
71,
72,
73,
74,
75,
76,
77,
78,
79,
80,
81,
82,
83,
84,
85,
86,
87,
88,
89,
90,
91,
92,
93,
94,
95,
96,
97,
98,
99,
100,
101,
102,
103,
104,
105,
106,
107,
108,
109,
110,
111,
112,
113,
114,
115,
116]:
      aclass.Name[aoid]=''

   return
   adt1=time.clock()
   icnt,gcnt=0,0
   for boid in range(500,100000,500):
      #boid=arangeobject.OID
      aclass=aICORDBEngine.User.OIDRange.ClassOfType
      aobj=aclass.GetFirstObject()
      aidmin,aidmax=-1,-1
      while aobj:
         amin,amax=aobj['IDMin'],aobj['IDMax']
         if boid>=amin and boid<=amax:
            aidmin,aidmax=amin,amax
            break
         aobj.Next()
      if aidmin>=0:
         gcnt=gcnt+1
      icnt=icnt+1
   adt2=time.clock()
   print adt2-adt1,icnt,gcnt

   return
