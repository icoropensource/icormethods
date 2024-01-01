# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
import string
import md5

DD={
}

LClasses=[
'CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_SourceEvents_AddInTemplate_EventValue',
'CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_SourceEvents_EffectSkin_EventValue',
'CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_SourceEvents_Field_EventValue',
'CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_SourceEvents_PluginExtension_EventValue',
'CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_SourceEvents_PluginSkin_EventValue',
'CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_SourceEvents_WidgetTemplate_EventValue',
'CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_SourceEvents_Table_EventValue',
'CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_SourceEvents_Template_EventValue',
]

def GetCleanText(atext):
   atext=atext.replace(chr(13),'')
   l=atext.split(chr(10))
   l2=[]
   for s in l:
      s=s.strip()
      if s:
         l2.append(s)
   return ''.join(l2)

def TraverseClasses():
   class CIterator(ICORRepositoryIterator):
      def __init__(self):
         ICORRepositoryIterator.__init__(self)
      def OnPreField(self,aclass,afield):
         bfield=aclass.FieldsByName(afield)
         if not bfield.IsMemo:
            return
         aobj=aclass.GetFirstObject()
         while aobj:
            atext=bfield[aobj.OID]
            atext=GetCleanText(atext)
            ahash=md5.new(atext).hexdigest()
            akey="%s_%s %d"%(string.replace(aclass.ClassPath,'\\','_'),afield,aobj.OID)
            if DD:
               if DD.has_key(akey):
                  if DD[akey]!=ahash:
                     print akey
            else:
               print "'%s':'%s',"%(akey,ahash)
            aobj.Next()
   aiterator=CIterator()
   for aclasspath in LClasses:
      aclass=aICORDBEngine.Classes[aclasspath]
      aiterator.ForEachClass(aclass)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   ClearStdOut()
   TraverseClasses()
   return

