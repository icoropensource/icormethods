# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORSecurity as ICORSecurity
import CLASSES_Library_ICORBase_Replication_Security_DoLoad as SecurityDoLoad
import CLASSES_Library_ICORBase_Replication_Send_GenerateReplication as GenerateReplication
import time

PCLASSES=[
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Projekt',
]

LCLASSES=[
   'CLASSES\Library\DBBase\DMSWorkflow\Meta\FileItem',
   'CLASSES\Library\DBBase\DMSWorkflow\Meta\Profile',
   'CLASSES\Library\DBBase\DMSWorkflow\Meta\Slownik',
   'CLASSES\Library\DBBase\DMSWorkflow\Meta\Slownik\SQLTemplate',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Dokument',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Dokumentacja',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Dokumentacja\Publikacja',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Dokumentacja\Rozdzial',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Dotyczy',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\ExternalTable',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\JednostkaOrganizacyjna',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Kreatory',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Kreatory\Etap',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Kreatory\Main',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Kreatory\Pole',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\OpisPola',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\PMServer',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\PMServer\AplikacjaZrodlowa',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\PMServer\Main',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\PMServer\Narzedzia',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\PMServer\Narzedzia\Mapowe',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\PMServer\Narzedzia\OptymalizacjaGoncow',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\PMServer\SOKMain',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Procedura',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Projekt',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\AddIns',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\AddIns\AddIn',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\AddedHTML',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\Alerty',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\CDNServerParameters',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\CDNSyncFolders',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\Czynnosc',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\DBAccess',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\DaneRodzajowe\Zakladka',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\EffectSkin',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\ExternalDBAccess',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\HTTPServerParameters',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\ListyWysylkowe\ElementListy',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\ListyWysylkowe\Kategoria',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\ListyWysylkowe\ListaWysylkowa',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\Maps',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\Maps\Server',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\Maps\Service',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\OpisPolaDotyczy',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\PageHTML\DocumentPageHTML',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\PageHTML\ProjectPageHTML',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\RozdzialyUsuniete',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\SMTPServerParameters',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\SearchAction',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\Security',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\Security\SecurityMap',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\SheetMethods',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\SourceEventSection\APIMethod',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\SourceEventSection\AddIn',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\SourceEventSection\Chapter',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\SourceEventSection\EffectSkin',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\SourceEventSection\Field',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\SourceEventSection\Plugin',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\SourceEventSection\Table',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\SourceEventSection\Widget',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\SourceEventSection\XMLData',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\SourceEvents\APIMethod\EventValue',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\SourceEvents\AddIn\EventValue',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\SourceEvents\Chapter\EventValue',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\SourceEvents\EffectSkin\EventValue',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\SourceEvents\Field\EventValue',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\SourceEvents\Plugin\EventValue',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\SourceEvents\Table\EventValue',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\SourceEvents\Widget\EventValue',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\SourceEvents\XMLData\EventValue',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\SzablonGenerowania',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\TableLink',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\UserCode',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\UserTSQL',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\UserXML',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\UserXSD',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\UserXSL',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\WWWStructAppPaths',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\XMLData\DocumentXMLData',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\Slownik\XMLData\TableXMLData',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\XMLRozdzialy',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\XMLRozdzialy\API',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\XMLRozdzialy\API\Library',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\XMLRozdzialy\API\Method',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\XMLRozdzialy\API\Namespace',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\XMLRozdzialy\API\Parameter',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\XMLRozdzialy\API\ReturnStruct',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\XMLRozdzialy\API\ReturnStructParameter',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\XMLRozdzialy\Component\Effects',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\XMLRozdzialy\Component\Plugin',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\XMLRozdzialy\Component\Widget',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\XMLRozdzialy\DataModel\Model',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\XMLRozdzialy\GalleryInfo',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\XMLRozdzialy\GrupaRozdzialow',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\XMLRozdzialy\MetaTemplate',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\XMLRozdzialy\PageCSS',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\XMLRozdzialy\PageFileItem',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\XMLRozdzialy\PageTemplate',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\XMLRozdzialy\Presentation\ChapterView',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\XMLRozdzialy\Presentation\JSLibManager',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\XMLRozdzialy\RSSInfo',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\XMLRozdzialy\Rozdzial',
   'CLASSES\Library\DBBase\DMSWorkflow\Prototyp\XMLRozdzialy\Struktura',
]

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   if CID<0:
      CID='CLASSES_Library_ICORBase_Replication_Update'
   aclass=aICORDBEngine.Classes[CID]
   # zaktualizowac metode CLASSES_Library_ICORBase_Interface_ICORSecurity
   # dodac metode CLASSES_System_SystemDictionary_ProfileGroup_OnObjectExport
   # zmienic metode CLASSES_System_User_OnObjectExport
   # dodac metode CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_EffectSkin_OnObjectExport
   # dodac metode CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_SourceEvents_EffectSkin_EventValue_OnObjectExport
   # dodac metode CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_SourceEventSection_EffectSkin_OnObjectExport
   # dodac metode CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Component_Effects_OnObjectExport
   # zmienic metode CLASSES_Library_ICORBase_Replication_Send_GenerateReplication
   # dodac ta metode i uruchomic sekcja po sekcji - ewentualnie zmienic pozostale wymagane metody
   # do klasy CLASSES_System_User dodac pole VCFPhone i ustawic jego opcje

   # przed generowanie plikow: nacisnac 'p' w icorstart a po wykonaniu operacji ponownie p (aby sie ewentualnie pliki zapisaly)

   if 0 or Value=='SecProfileSave':
      # zgrac security
      # wyedytowac plik i usunac niepotrzebne profile
      asecprofile=ICORSecurity.ICORSecurityProfile()
      asecprofile.SetByAll()
      asecprofile.DumpXML('%ICOR%/upgradeicor_security.xml',auidranges=1,ausers=1,aoidranges=1)

   if 0 or Value=='CreateReplicationObjects':
      # utworzyc obiekty replikacyjne
      # wejsc ewentualnie do edycji utworzonych obiektow i ustawic wymagane OIDRanges a dla User - wlasciwe UIDRanges
      sclass=aICORDBEngine.Classes['CLASSES_Library_ICORBase_Replication_Send']
      rclass=aICORDBEngine.Classes['CLASSES_Library_Dictionary_Named_ReplicationClassPath']
      soid=sclass.Name.Identifiers('ICORUpgrade')
      if soid<0:
         soid=sclass.AddObject()
      sobj=sclass[soid]
      sobj.Name='ICORUpgrade'
      sobj.Description='Upgrade do ICOR 2'
      sobj.OutputFile='%ICOR%/upgradeicor_objects.gz'
      sobj.AllowSystem=1
      sobj.DisableClassMethods=1
      sobj.DisableObjectMethods=1
      arefs=sclass.BaseClasses.GetRefList(soid)
      for eclass in LCLASSES:
         apos,afind=arefs.FindRefByValue('Name',eclass)
         if not afind:
            roid=rclass.AddObject()
            rclass.Name[roid]=eclass
            rclass.IsClassRecursive[roid]=0
            rclass.IsFieldRecursive[roid]=0
            arefs.AddRef(roid,rclass.CID)
      arefs.Store()

   if 0 or Value=='CreateReplicationObjectsRecursive':
      # utworzyc obiekty replikacyjne - wedlug pol
      sclass=aICORDBEngine.Classes['CLASSES_Library_ICORBase_Replication_Send']
      rclass=aICORDBEngine.Classes['CLASSES_Library_Dictionary_Named_ReplicationClassPath']
      soid=sclass.Name.Identifiers('ICORUpgradeRecursive')
      if soid<0:
         soid=sclass.AddObject()
      sobj=sclass[soid]
      sobj.Name='ICORUpgradeRecursive'
      sobj.Description='Upgrade do ICOR 3'
      sobj.OutputFile='%ICOR%/upgradeicor_objects_recursive.gz'
      sobj.AllowSystem=1
      sobj.DisableClassMethods=1
      sobj.DisableObjectMethods=1
      arefs=sclass.BaseClasses.GetRefList(soid)
      for eclass in PCLASSES:
         apos,afind=arefs.FindRefByValue('Name',eclass)
         if not afind:
            roid=rclass.AddObject()
            rclass.Name[roid]=eclass
            rclass.IsClassRecursive[roid]=0
            rclass.IsFieldRecursive[roid]=1
            arefs.AddRef(roid,rclass.CID)
      arefs.Store()

   if 0 or Value=='GenerateReplication':
      # nacisnac 'p' w icorstart
      # zgrac obiekty
      sclass=aICORDBEngine.Classes['CLASSES_Library_ICORBase_Replication_Send']
      soid=sclass.Name.Identifiers('ICORUpgrade')
      citerator=GenerateReplication.ICORReplicationIterator(soid,adisablestructdefinitions=1)
      citerator.Generate()
      # przeniesc pliki do katalogu ICOR

   if 0 or Value=='GenerateReplicationRecursive':
      # nacisnac 'p' w icorstart
      # zgrac obiekty
      sclass=aICORDBEngine.Classes['CLASSES_Library_ICORBase_Replication_Send']
      soid=sclass.Name.Identifiers('ICORUpgradeRecursive')
      citerator=GenerateReplication.ICORReplicationIterator(soid,adisablestructdefinitions=1)
      citerator.Generate()
      # przeniesc pliki do katalogu ICOR

   if 0 or Value=='SecurityLoad':
      # nacisnac 'p' w icorstart
      # mozna wylaczyc synchronizacje z PostgreSQL, ale potem koniecznie import do PG
      # sprawdzic w ustawieniach systemu czy nie jest wlaczone antimalware protection z online sprawdzaniem i powylaczac to
      # zaimportowac security
      # sprawdzic przypisane grupy do profilow etc.
      # uruchomic ewentualnie: CLASSES_System_User_UpdateObiektow
      SecurityDoLoad.SecurityLoad('%ICOR%/upgradeicor_security.xml')

   if 0 or Value=='ReceiveReplication':
      # nacisnac 'p' w icorstart
      # zaimportoowac obiekty
      rclass=aICORDBEngine.Classes['CLASSES_Library_ICORBase_Replication_Receive']
      roid=rclass.Name.Identifiers('ICORUpgradeReceive')
      rclass.InputFile[roid]='%ICOR%/upgradeicor_objects.gz'
      rclass.ReceiveReplication('',roid)
      # zerknac do logow icor.exe aby sprawdzic zapis do PG

   if 0 or Value=='Finish':
      # uruchomic sprawdzenie referencji dla system i library i naprawic co trzeba
      # sprawdzic, czy nie trzeba uruchomic metody upgrade z: CLASSES_Library_ICORBase_Replication_Update_UpgradeICOR
      # dodac do CLASSES_Library_NetBase_WWW_Server odpowiedni wpis z dostepem do wwwmenustruct dla aplikacji
      # przypisac do usera typu Boss odpowiednie nowe uprawnienia
      # przerestartowac v i o w icorstart
      # zalogowac sie do panelu
      # uzupelnic dane projektu: dbaccess, addins
      # uzupelnic dane wwwmenustruct: dodac/poprawic plugins, dbaccesspublic, kodowanie w serwisie, apppaths na %icor%
      # przegenerowac szablon glowny
      # zmienic w kodzie Session na Dession
      # sprawdzic w MS SQL czy format daty jest ustawiony prawidlowo - ustawic w registry przez HKU_DefaultLocale.reg oraz dla uzytkownika Administrator
      # w migrowanych projektach sprawdzic, czy sa dodane nowe kolumny do tabeli Multimedia
      pass

   return

