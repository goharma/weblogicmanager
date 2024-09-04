# Python Starter

Quickly get started with [Python](https://www.python.org/) using this starter! 

- If you want to upgrade Python, you can change the image in the [Dockerfile](./.devcontainer/Dockerfile).


curl -u admin:adminpassword -X POST -H "Content-Type: application/json" -d '{
  "expression": "(weblogic.entitlement.rules.RolePredicate[AdminRole])",
  "name": "DataSourceAdminPolicy"
}' \
"http://hostname:port/management/weblogic/latest/domainConfig/JDBCSystemResources/yourDataSourceName/JdbcResource/yourDataSourceName/Security/Policies"
