# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

lqueries=[
   [r'''All user objects''',r'''(&(objectCategory=person)(objectClass=user))'''],
   [r'''All user objects (Note 1)''',r'''(sAMAccountType=805306368)'''],
   [r'''All computer objects''',r'''(objectCategory=computer)'''],
   [r'''All contact objects''',r'''(objectClass=contact)'''],
   [r'''All group objects''',r'''(objectCategory=group)'''],
   [r'''All organizational unit objects''',r'''(objectCategory=organizationalUnit)'''],
   [r'''All container objects''',r'''(objectCategory=container)'''],
   [r'''All builtin container objects''',r'''(objectCategory=builtinDomain)'''],
   [r'''All domain objects''',r'''(objectCategory=domain)'''],
   [r'''Computer objects with no description''',r'''(&(objectCategory=computer)(!(description=*)))'''],
   [r'''Group objects with a description''',r'''(&(objectCategory=group)(description=*))'''],
   [r'''Users with cn starting with "ICOR"''',r'''(&(objectCategory=person)(objectClass=user)(cn=ICOR*))'''],
   [r'''Object with description "ICOR"''',r'''(description=ICOR)'''],
   [r'''Phone numbers in form (xxx) xxx-xxx''',r'''(telephoneNumber=(*)*-*)'''],
   [r'''Groups with cn starting with "ICOR" or "Admin"''',r'''(&(objectCategory=group)(|(cn=ICOR*)(cn=Admin*)))'''],
   [r'''All users with both a first and last name.''',r'''(&(objectCategory=person)(objectClass=user)(givenName=*)(sn=*))'''],
   [r'''All users with direct reports but no manager''',r'''(&(objectCategory=person)(objectClass=user)(directReports=*)(!(manager=*)))'''],
   [r'''All users with specified email address''',r'''(&(objectCategory=person)(objectClass=user)(|(proxyAddresses=*:jsmith@company.com)(mail=jsmith@company.com)))'''],
   [r'''All users with Logon Script: field occupied''',r'''(&(objectCategory=person)(objectClass=user)(scriptPath=*))'''],
   [r'''Object with Common Name "Jim * Smith" (Notes 3, 19)''',r'''(cn=Jim \2A Smith)'''],
   [r'''Objects with sAMAccountName that begins with "x", "y", or "z"''',r'''(sAMAccountName>=x)'''],
   [r'''Objects with sAMAccountName that begins with "a" or any number or symbol except "$"''',r'''(&(sAMAccountName<=a)(!(sAMAccountName=$*)))'''],
   [r'''All users with "Password Never Expires" set (Note 4)''',r'''(&(objectCategory=person)(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=65536))'''],
   [r'''All disabled user objects (Note 4)''',r'''(&(objectCategory=person)(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=2))'''],
   [r'''All enabled user objects (Note 4)''',r'''(&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))'''],
   [r'''All users not required to have a password (Note 4)''',r'''(&(objectCategory=person)(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=32))'''],
   [r'''All users with "Do not require kerberos preauthentication" enabled''',r'''(&(objectCategory=person)(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=4194304))'''],
   [r'''Users with accounts that do not expire (Note 5)''',r'''(&(objectCategory=person)(objectClass=user)(|(accountExpires=0)(accountExpires=9223372036854775807)))'''],
   [r'''Users with accounts that do expire (Note 5)''',r'''(&(objectCategory=person)(objectClass=user)(accountExpires>=1)(accountExpires<=9223372036854775806))'''],
   [r'''Accounts trusted for delegation (unconstrained delegation)''',r'''(userAccountControl:1.2.840.113556.1.4.803:=524288)'''],
   [r'''Accounts that are sensitive and not trusted for delegation''',r'''(userAccountControl:1.2.840.113556.1.4.803:=1048576)'''],
   [r'''All distribution groups (Notes 4, 15)''',r'''(&(objectCategory=group)(!(groupType:1.2.840.113556.1.4.803:=2147483648)))'''],
   [r'''All security groups (Notes 4, 19)''',r'''(groupType:1.2.840.113556.1.4.803:=2147483648)'''],
   [r'''All built-in groups (Notes 4, 16, 19)''',r'''(groupType:1.2.840.113556.1.4.803:=1)'''],
   [r'''All global groups (Notes 4, 19)''',r'''(groupType:1.2.840.113556.1.4.803:=2)'''],
   [r'''All domain local groups (Notes 4, 19)''',r'''(groupType:1.2.840.113556.1.4.803:=4)'''],
   [r'''All universal groups (Notes 4, 19)''',r'''(groupType:1.2.840.113556.1.4.803:=8)'''],
   [r'''All global security groups (Notes 17, 19)''',r'''(groupType=-2147483646)'''],
   [r'''All universal security groups (Notes 17, 19)''',r'''(groupType=-2147483640)'''],
   [r'''All domain local security groups (Notes 17, 19)''',r'''(groupType=-2147483644)'''],
   [r'''All global distribution groups (Note 19)''',r'''(groupType=2)'''],
   [r'''All objects with service principal name''',r'''(servicePrincipalName=*)'''],
   [r'''Users with "Allow Access" on "Dial-in" tab of ADUC (Note 6)''',r'''(&(objectCategory=person)(objectClass=user)(msNPAllowDialin=TRUE))'''],
   [r'''Users with "Control access though NPS Network Policy" on "Dial-in" tab of ADUC''',r'''(&(objectCategory=person)(objectClass=user)(!(msNPAllowDialin=*)))'''],
   [r'''All groups created after January 1, 2018''',r'''(&(objectCategory=group)(whenCreated>=20180101000000.0Z))'''],
   [r'''All users where an administrator has set that they must change their password at next logon''',r'''(&(objectCategory=person)(objectClass=user)(pwdLastSet=0))'''],
   [r'''All users that changed their password since April 15, 2011 (CST) (Note 7)''',r'''(&(objectCategory=person)(objectClass=user)(pwdLastSet>=129473172000000000))'''],
   [r'''All users with "primary" group other than "Domain Users"''',r'''(&(objectCategory=person)(objectClass=user)(!(primaryGroupID=513)))'''],
   [r'''All computers with "primary" group "Domain Computers"''',r'''(&(objectCategory=computer)(primaryGroupID=515))'''],
   [r'''Object with GUID "90395F191AB51B4A9E9686C66CB18D11" (Note 8)''',r'''(objectGUID=\90\39\5F\19\1A\B5\1B\4A\9E\96\86\C6\6C\B1\8D\11)'''],
   [r'''Object beginning with GUID "90395F191AB51B4A" (Note 8)''',r'''(objectGUID=\90\39\5F\19\1A\B5\1B\4A*)'''],
   [r'''Object with SID "S-1-5-21-73586283-152049171-839522115-1111" (Note 9)''',r'''(objectSID=S-1-5-21-73586283-152049171-839522115-1111)'''],
   [r'''Object with SID "0105000000000005150000006BD662041316100943170A3257040000" (Note 9)''',r'''(objectSID=\01\05\00\00\00\00\00\05\15\00\00\00\6B\D6\62\04\13\16\10\09\43\17\0A\32\57\04\00\00)'''],
   [r'''All computers that are not Domain Controllers (Note 4)''',r'''(&(objectCategory=computer)(!(userAccountControl:1.2.840.113556.1.4.803:=8192)))'''],
   [r'''All Domain Controllers (Note 4)''',r'''(&(objectCategory=computer)(userAccountControl:1.2.840.113556.1.4.803:=8192))'''],
   [r'''All Domain Controllers (Notes 14, 19)''',r'''(primaryGroupID=516)'''],
   [r'''All servers''',r'''(&(objectCategory=computer)(operatingSystem=*server*))'''],
   [r'''All member servers (not DC's) (Note 4)''',r'''(&(objectCategory=computer)(operatingSystem=*server*)(!(userAccountControl:1.2.840.113556.1.4.803:=8192)))'''],
   [r'''All direct members of specified group "ICOR"''',r'''(memberOf=cn=ICOR,ou=East,dc=Domain,dc=com)'''],
   [r'''All users not direct members of a specified group "ICOR"''',r'''(&(objectCategory=person)(objectClass=user)(!(memberOf=cn=ICOR,ou=East,dc=Domain,dc=com)))'''],
   [r'''All groups with specified direct member (Note 19)''',r'''(member=cn=Jim Smith,ou=West,dc=Domain,dc=com)'''],
   [r'''All members of specified group, including due to group nesting (Note 10)''',r'''(memberOf:1.2.840.113556.1.4.1941:=cn=Test,ou=East,dc=Domain,dc=com)'''],
   [r'''All groups specified user belongs to, including due to group nesting (Notes 10, 19)''',r'''(member:1.2.840.113556.1.4.1941:=cn=Jim Smith,ou=West,dc=Domain,dc=com)'''],
   [r'''Objects with givenName "Jim*" and sn "Smith*", or with cn "Jim Smith*" (Note 11)''',r'''(anr=Jim Smith)'''],
   [r'''All attributes in the Schema container replicated to the GC (Notes 6, 12)''',r'''(&(objectCategory=attributeSchema)(isMemberOfPartialAttributeSet=TRUE))'''],
   [r'''All operational (constructed) attributes in the Schema container (Notes 4, 12)''',r'''(&(objectCategory=attributeSchema)(systemFlags:1.2.840.113556.1.4.803:=4))'''],
   [r'''All attributes in the Schema container not replicated to other Domain Controllers (Notes 4, 12)''',r'''(&(objectCategory=attributeSchema)(systemFlags:1.2.840.113556.1.4.803:=1))'''],
   [r'''All objects where deletion is not allowed (Notes 4)''',r'''(systemFlags:1.2.840.113556.1.4.803:=2147483648)'''],
   [r'''Attributes whose values are copied when the object is copied (Notes 4, 12)''',r'''(searchFlags:1.2.840.113556.1.4.803:=16)'''],
   [r'''Attributes preserved in tombstone object when object deleted (Notes 4, 12)''',r'''(searchFlags:1.2.840.113556.1.4.803:=8)'''],
   [r'''Attributes in the Ambiguous Name Resolution (ANR) set (Notes 4, 12)''',r'''(searchFlags:1.2.840.113556.1.4.803:=4)'''],
   [r'''Attributes in the Schema that are indexed (Notes 4, 12)''',r'''(searchFlags:1.2.840.113556.1.4.803:=1)'''],
   [r'''Attributes marked confidential in the schema (Notes 4, 12)''',r'''(searchFlags:1.2.840.113556.1.4.803:=128)'''],
   [r'''Attributes in the RODC filtered attribute set, or FAS (Notes 4, 12)''',r'''(searchFlags:1.2.840.113556.1.4.803:=512)'''],
   [r'''All inter-site connection objects in the Configuration container (Note 13)''',r'''(objectClass=siteLink)'''],
   [r'''All intra-site connection objects in the Configuration container (Note 13))''',r'''(objectClass=nTDSConnection)'''],
   [r'''The nTDSDSA objects associated with all Global Catalogs. This will identify all DC's that are GC's. (Note 4)''',r'''(&(objectCategory=nTDSDSA)(options:1.2.840.113556.1.4.803:=1))'''],
   [r'''The nTDSDSA object associated with the PDC Emulator. This will identify the DC with the PDC Emulator FSMO role (Note 18).''',r'''(&(objectClass=domainDNS)(fSMORoleOwner=*))'''],
   [r'''The nTDSDSA object associated with the RID Master. This will identify the DC with the RID Master FSMO role (Note 18).''',r'''(&(objectClass=rIDManager)(fSMORoleOwner=*))'''],
   [r'''The nTDSDSA object associated with the Infrastructure Master. This will identify the DC with this FSMO role (Note 18).''',r'''(&(objectClass=infrastructureUpdate)(fSMORoleOwner=*))'''],
   [r'''The nTDSDSA object associated with the Schema Master. This will identify the DC with the Schema Master FSMO role (Note 18).''',r'''(&(objectClass=dMD)(fSMORoleOwner=*))'''],
   [r'''The nTDSDSA object associated with the Domain Naming Master. This will identify the DC with this FSMO role (Note 18).''',r'''(&(objectClass=crossRefContainer)(fSMORoleOwner=*))'''],
   [r'''All Exchange servers in the Configuration container (Note 13)''',r'''(objectCategory=msExchExchangeServer)'''],
   [r'''All objects protected by AdminSDHolder''',r'''(adminCount=1)'''],
   [r'''All trusts established with a domain''',r'''(objectClass=trustedDomain)'''],
   [r'''All Group Policy objects''',r'''(objectCategory=groupPolicyContainer)'''],
   [r'''All service connection point objects''',r'''(objectClass=serviceConnectionPoint)'''],
   [r'''All Read-Only Domain Controllers (Notes 4, 19)''',r'''(userAccountControl:1.2.840.113556.1.4.803:=67108864)'''],
]

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aoid=100000001
   for acaption,aquery in lqueries:
      aclass.Nazwa[aoid]=acaption
      aclass.Query[aoid]=aquery
      aoid=aoid+1
   return

