# Python Starter

Quickly get started with [Python](https://www.python.org/) using this starter! 

- If you want to upgrade Python, you can change the image in the [Dockerfile](./.devcontainer/Dockerfile).


# Import necessary modules
from weblogic.management.security.authorization import RoleMapperMBean

# Connect to the Admin Server
connect('weblogic_username', 'weblogic_password', 't3://admin_server_host:admin_server_port')

# Start an edit session
edit()
startEdit()

# Navigate to the DataSource
cd('/JDBCSystemResources/YourDataSourceName/JdbcResource/YourDataSourceName')

# Navigate to the security policies for the DataSource
cd('JDBCDataSourceParams/YourDataSourceName')

# Create a new security policy
try:
    # Replace 'YourDataSourceName' with the actual name of your datasource
    policyName = 'YourDataSourceNamePolicy'
    realmName = 'myrealm'
    resourceId = 'type=jdbc,application=YourDataSourceName'
    
    # Create a new RoleMapper for the specific DataSource
    cd('/SecurityConfiguration/mydomain/Realms/' + realmName + '/RoleMappers/XACMLRoleMapper')
    
    # Add a security policy for a specific user
    cmo.createRoleMapping(policyName, resourceId, None, ['web-admin'])
    
    # Add a security policy for a specific role
    cmo.createRoleMapping(policyName, resourceId, 'SPNGO', None)

    # Save and activate the changes
    save()
    activate(block='true')
    
    print("Security policy created successfully for DataSource: YourDataSourceName")
except Exception as e:
    print("Error occurred while creating security policy: ", e)
    undo('true', 'y')
    cancelEdit('y')

# Disconnect from Admin Server
disconnect()
