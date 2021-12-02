import meraki
import re
from pprint import pp

# Organization ID
ORG_ID = ""

# Network ID
NETWORK_ID = ""

# Conf File
CONF_FILE = "/etc/dnsmasq.d/meraki"


def listHelper():
    """List all networks and organizations for API key"""
    dashboard = meraki.DashboardAPI(output_log=False, print_console=False)
    organizations = dashboard.organizations.getOrganizations()

    for org in organizations:
        pp(org)
        if not org["api"]["enabled"]:
            continue
        pp(dashboard.organizations.getOrganizationNetworks(org['id']))


def is_valid_hostname(hostname):
    """
    https://stackoverflow.com/questions/2532053/validate-a-hostname-string
    """
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        # strip exactly one dot from the right, if present
        hostname = hostname[:-1]
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))


def main():
    # Must have MERAKI_DASHBOARD_API_KEY environment variable set
    dashboard = meraki.DashboardAPI(output_log=False, print_console=False)
    clients = dashboard.networks.getNetworkClients(NETWORK_ID, -1)

    for client in clients:
        dns_name = client["description"]
        prefix = ""

        if not dns_name:
            continue

        dns_name = dns_name.lower()
        dns_name = dns_name.replace(" ", "-")
        dns_name = dns_name.replace("_", "-")

        if not is_valid_hostname(dns_name):
            prefix = "#"

        print(f'')
        print(f'# Device: {client["description"]}, MAC: {client["mac"]}')
        print(
            f'# SSID: {client["ssid"]}, OS: {client["os"]}, Vendor: {client["manufacturer"]}')
        print(f'{prefix}address=/{dns_name}/{client["ip"]}')
        print(f'{prefix}address=/{dns_name}.internal/{client["ip"]}')


if __name__ == '__main__':
    main()
