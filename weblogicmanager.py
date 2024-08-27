import asyncio
import aiohttp
from aiohttp import BasicAuth
import logging
import yaml
import click

class WebLogicManager:
    def __init__(self, admin_url, username, password, request_timeout=3):
        self.admin_url = admin_url
        self.username = username
        self.password = password
        self.request_timeout = request_timeout
        self.session = None        
        self.targets_url = f"{self.admin_url}/management/weblogic/latest/domainConfig/JDBCSystemResources/wamDataSrc?links=none&fields=targets"
        self.clusters_url = f"{self.admin_url}/management/weblogic/latest/domainConfig/clusters?links=none&fields=servers,name"
        self.servers_url = f"{self.admin_url}/management/weblogic/latest/domainConfig/servers?links=none&fields=listenAddress,listenPort,name"
        
        # Configure logging to log to a file
        logging.basicConfig(
            filename='weblogicmanager.log',  # Log file name
            level=logging.INFO,  # Log level
            format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
        )
        self.logger = logging.getLogger(__name__)

    async def fetch_data(self, url):
        """Fetch data from a URL with basic authentication and check for non-JSON response."""
        auth = BasicAuth(self.username, self.password)
        try:
            async with self.session.get(url, auth=auth, timeout=self.request_timeout) as response:
                status = response.status
                content_type = response.headers.get('Content-Type', '')
                
                if 'application/json' in content_type:
                    content = await response.json()
                    self.logger.info(f"Fetched {url} - Status: {status} - JSON Response: {content}")
                else:
                    content = await response.text()
                    self.logger.info(f"Fetched {url} - Status: {status} - Non-JSON Response: {content}")
                
                return content
        except asyncio.TimeoutError:
            self.logger.error(f"Request to {url} timed out.")
            return None

    async def invoke_url(self, url):
        """Invoke a URL asynchronously and check for non-JSON response."""
        auth = BasicAuth(self.username, self.password)
        try:
            async with self.session.get(url, auth=auth, timeout=self.request_timeout) as response:
                status = response.status
                content_type = response.headers.get('Content-Type', '')
                
                if 'application/json' in content_type:
                    content = await response.json()
                    self.logger.info(f"Invoked {url} - Status: {status} - JSON Response: {content}")
                else:
                    content = await response.text()
                    self.logger.info(f"Invoked {url} - Status: {status} - Non-JSON Response: {content}")
                
                return content
        except asyncio.TimeoutError:
            self.logger.error(f"Request to {url} timed out.")
            return None

    def get_server_url(self, server_name, servers_list):
        """Get the URL for server management based on server details."""
        for server in servers_list:
            if server['name'].lower() == server_name.lower():
                return f"http://{server['listenAddress']}:{server['listenPort']}/management/weblogic"
        return None

    async def process_targets(self):
        """Main method to fetch targets, clusters, and servers, and invoke the management URLs."""
        async with aiohttp.ClientSession() as self.session:
            # Asynchronously fetching data with basic authentication
            targets, clusters, servers = await asyncio.gather(
                self.fetch_data(self.targets_url),
                self.fetch_data(self.clusters_url),
                self.fetch_data(self.servers_url)
            )

            # Check if any of the responses are None (indicating a timeout or other error)
            if targets is None or clusters is None or servers is None:
                self.logger.error("One or more requests failed. Exiting.")
                return

            # Process the targets
            result = []
            server_list = servers['items']

            for target in targets['targets']:
                target_type, target_name = target['identity']

                if target_type == "servers":
                    # Direct server target
                    server_url = self.get_server_url(target_name, server_list)
                    if server_url:
                        result.append(server_url)

                elif target_type == "clusters":
                    # Cluster target - find servers in the cluster
                    for cluster in clusters['items']:
                        if cluster['name'].lower() == target_name.lower():
                            for cluster_server in cluster['servers']:
                                server_name = cluster_server['identity'][1]
                                server_url = self.get_server_url(server_name, server_list)
                                if server_url:
                                    result.append(server_url)

            # Log the list of listenAddress:listenPort/management/weblogic/start for each target
            self.logger.info(f"Resulting URLs: {result}")

            # Asynchronously invoke the URLs in result
            invoke_tasks = [self.invoke_url(url) for url in result]
            await asyncio.gather(*invoke_tasks)

@click.command()
@click.option('--config', required=True, type=click.Path(exists=True), help='Path to the configuration YAML file.')
def main(config):
    """Main function to start WebLogicManager with configuration from YAML file."""
    # Read admin hosts and ports from a YAML configuration file
    with open(config, 'r') as file:
        config_data = yaml.safe_load(file)

    admin_hosts = config_data['admin_hosts']
    admin_ports = config_data['admin_ports']

    for admin_host, admin_port in zip(admin_hosts, admin_ports):
        manager = WebLogicManager(admin_url=f"http://{admin_host}:{admin_port}", username="weblogic", password="welcome1")    
        asyncio.run(manager.process_targets())

if __name__ == "__main__":
    main()
