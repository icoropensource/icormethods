# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import string

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   """
IsMFSManager
"""
   if OID<0:
      return
   aclass=aICORDBEngine.Classes[CID]
   aobj=aclass[OID]
   startupclass=aICORDBEngine.Classes['CLASSES_System_Startup']
   profileclass=startupclass.ProfileGroup.ClassOfType
   usergroupsclass=profileclass.UserGroups.ClassOfType
   itemgroupsclass=profileclass.ItemGroups.ClassOfType
   groupclass=itemgroupsclass.Groups.ClassOfType
   userclass=usergroupsclass.Users.ClassOfType
   robj=aobj.OIDRange
   if not robj:
      print 'brak zdefiniowanego zakresu OID'
      return
   aminoid=robj['IDMin']
   uobj=aobj.UIDRange
   if not uobj:
      print 'brak zdefiniowanego zakresu UID'
      return
   aminuid=uobj['IDMin']

   poid=profileclass.Name.Identifiers(aobj.ProfileName)
   if poid>=0 and poid!=aminoid:
      print 'Nazwa profilu juz istnieje i OID jest poza zakresem'
      return
   if poid<0:
      profileclass.CreateObjectByID(aminoid)
      poid=aminoid
      profileclass.Name[aminoid]=aobj.ProfileName
      startupclass.ProfileGroup.AddRefs(startupclass.FirstObject(),[poid,profileclass.CID],asortedreffield=profileclass.Name,dosort=1,aremoveexisting=1)
   profileclass.OIDRange[poid]=aobj.OIDRange
   profileclass.UIDRange[poid]=aobj.UIDRange

   userclass.CreateObjectByID(aminuid)
   userclass.UserName[aminuid]=aobj.AdminName
   userclass.Password[aminuid]=aobj.AdminName
   userclass.VCFFirstName[aminuid]=aobj.AdminFirstName
   userclass.VCFLastName[aminuid]=aobj.AdminLastName
   sl=string.split(aobj.UserSecurityGroups,'\n')
   arefs=[]
   for aline in sl:
      l=string.split(aline,',')
      if len(l)==3:
         alevel=string.strip(l[0])
         aitemname=string.strip(l[1])
         agroup=string.strip(l[2])
         goid=groupclass.Name.Identifiers(agroup)
         if goid<0:
            goid=groupclass.AddObject()
            groupclass.Name[goid]=agroup
         ugoid=usergroupsclass.Name.Identifiers(aitemname)
         if ugoid<0:
            ugoid=usergroupsclass.AddObject()
         usergroupsclass.Name[ugoid]=aitemname
         usergroupsclass.AccessLevel[ugoid]=alevel
         usergroupsclass.Groups[ugoid]=[goid,groupclass.CID]
         arefs.append([ugoid,usergroupsclass.CID])
   userclass.Groups[aminuid]=arefs
   profileclass.UserGroups.AddRefs(poid,arefs,asortedreffield=usergroupsclass.Name,dosort=1,aremoveexisting=1)

   sl=string.split(aobj.ItemSecurityGroups,'\n')
   arefs=[]
   for aline in sl:
      l=string.split(aline,',')
      if len(l)==3:
         alevel=string.strip(l[0])
         aitemname=string.strip(l[1])
         agroup=string.strip(l[2])
         goid=groupclass.Name.Identifiers(agroup)
         if goid<0:
            goid=groupclass.AddObject()
            groupclass.Name[goid]=agroup
         ugoid=itemgroupsclass.Name.Identifiers(aitemname)
         if ugoid<0:
            ugoid=itemgroupsclass.AddObject()
         itemgroupsclass.Name[ugoid]=aitemname
         itemgroupsclass.AccessLevel[ugoid]=alevel
         itemgroupsclass.Groups[ugoid]=[goid,groupclass.CID]
         arefs.append([ugoid,itemgroupsclass.CID])
   profileclass.ItemGroups.AddRefs(poid,arefs,asortedreffield=itemgroupsclass.Name,dosort=1,aremoveexisting=1)

   if aobj.WorkflowProjectName:
      workflowpclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Projekt']
      woid=workflowpclass.Nazwa.Identifiers(aobj.WorkflowProjectName)
      if woid>=0 and woid!=aminoid:
         print 'Nazwa WorkflowProjectName juz istnieje i OID jest poza zakresem'
         return
      if woid<0:
         workflowpclass.CreateObjectByID(aminoid)
         woid=aminoid
         workflowpclass.Nazwa[woid]=aobj.WorkflowProjectName
      workflowpclass.AppPath[woid]=aobj.WorkflowAppPath
      workflowpclass.BaseNameModifier[woid]=aobj.WorkflowBaseNameModifier
      workflowpclass.DBAccess[woid]=aobj.WorkflowDBAccess
      workflowpclass.HTTPServerParameters[woid]=aobj.WorkflowHTTPServerParameters
      workflowpclass.WWWDataPath[woid]=aobj.WWWDataPath
      workflowpclass.WWWDataPathUserFiles[woid]=aobj.WWWDataPathUserFiles
      workflowpclass.WWWDataPathUserImages[woid]=aobj.WWWDataPathUserImages

   if aobj.WWWStructName:
      wwwstructpclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Struktura']
      soid=wwwstructpclass.Nazwa.Identifiers(aobj.WWWStructName)
      if soid>=0 and soid!=aminoid:
         print 'Nazwa WWWStructName juz istnieje i OID jest poza zakresem'
         return
      if soid<0:
         wwwstructpclass.CreateObjectByID(aminoid)
         soid=aminoid
         wwwstructpclass.Nazwa[soid]=aobj.WWWStructName
      wwwstructpclass.AppPaths[soid]=aobj.WWWStructAppPaths
      wwwstructpclass.DBAccess[soid]=aobj.WWWStructDBAccess
      wwwstructpclass.PageTemplate[soid]=aobj.WWWStructPageTemplate
      if aobj.WorkflowProjectName:
         workflowpclass.WWWMenuStruct[woid]=[soid,wwwstructpclass.CID]

   if aobj.MDQueryName:
      mdqueryclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_Query_MultiDimension_XML_Preprocessor']
      moid=mdqueryclass.Name.Identifiers(aobj.MDQueryName)
      if moid>=0 and moid!=aminoid:
         print 'Nazwa MDQueryName juz istnieje i OID jest poza zakresem'
         return
      if moid<0:
         mdqueryclass.CreateObjectByID(aminoid)
         moid=aminoid
         mdqueryclass.Name[moid]=aobj.MDQueryName
      mdqueryclass.SourceData[moid]=aobj.MDQueryXMLStruct

   return

