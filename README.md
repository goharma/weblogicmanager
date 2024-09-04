# Python Starter

Quickly get started with [Python](https://www.python.org/) using this starter! 

- If you want to upgrade Python, you can change the image in the [Dockerfile](./.devcontainer/Dockerfile).


# Connect to the Admin Server
connect('weblogic_username', 'weblogic_password', 't3://admin_server_host:admin_server_port')

# Navigate to the security realm (usually 'myrealm')
realmName = 'myrealm'
roleMapperName = 'XACMLRoleMapper'  # Ensure this is the correct RoleMapper for your configuration

# Use Runtime MBean Server to get the Realm MBean
realmPath = '/SecurityConfiguration/mydomain/Realms/' + realmName
cd(realmPath + '/RoleMappers/' + roleMapperName)

# Define the security policy
resourcePath = 'type=weblogic,jdbc,resource=jdbc/MyDataSource'
policyExpression = 'Grp(SPNGO) | user(web-admin)'

# Set the security policy
try:
    # Check if RoleMapper is XACMLRoleMapper to use specific XACML functions
    cmo.createRoleExpression(resourcePath, policyExpression)
    print("Security policy created successfully for JDBC Datasource: MyDataSource")
except Exception as e:
    print("Error occurred while creating security policy: ", e)

# Disconnect from Admin Server
disconnect()

