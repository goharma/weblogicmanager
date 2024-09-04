from weblogic.management.security.authentication import UserReaderMBean
from weblogic.management.security.authentication import GroupReaderMBean
from weblogic.management.security.authentication import MemberGroupListerMBean
from weblogic.security.providers.authentication import DefaultAuthenticatorMBean
from weblogic.management.security.authentication import AuthenticationProviderMBean
from weblogic.management.security.authentication import GroupEditorMBean
from weblogic.management.utils import NameListerMBean
from weblogic.management.security.authorization import RoleMapperMBean
from weblogic.security.providers.xacml.authorization import XACMLAuthorizerMBean
from weblogic.management.utils import PropertiesListerMBean
from weblogic.management.security.authorization import RoleReaderMBean
from weblogic.security.providers.xacml.authorization import XACMLRoleMapperMBean
from weblogic.security.providers.xacml.authorization import XACMLAuthorizerMBean

connect("weblogic","weblogic","t3://adminIP:6500")
realm1=cmo.getSecurityConfiguration().getDefaultRealm()
atns = realm1.getAuthorizers()
realm=cmo.getSecurityConfiguration().getDefaultRealm().lookupAuthorizer('XACMLAuthorizer')
## if you are using any custom Authorizer us the custome authorizer name ####
#realm=cmo.getSecurityConfiguration().getDefaultRealm().lookupAuthorizer('DefaultAuthorizer')
print realm
print realm1
print atns
for i in atns:
     print "______________________"
     print i
     if isinstance(i,XACMLAuthorizerMBean):
         userReader = i
         print "here"
         cursor = i.listAllPolicies(1000)
         #listpolicy= i.listPoliciesByResourceType('type=<jndi>',0)
         print 'policies are: '
         print cursor
         #print listpolicy
         while userReader.haveCurrent(cursor):
             print userReader.getCurrentProperties(cursor)
             userReader.advance(cursor)
         userReader.close
