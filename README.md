# MERAKI DNS

This scripts generates a dnsmasq compatible set of address from a list of clients in dashboard. This works per network. The goal is to replicate a feature that most basic routers have - DNS entries for local devices with fixed DHCP assignments.

## Configuration

### Enable the API
Follow the official [instructions]() for creating an API key for your organization. Once you have your api key, export an environment variable e.g.

`export MERAKI_DASHBOARD_API_KEY=023709870987fa897db987b2bdf210fb9ad99`

This variable must be present for whatever terminal will be consuming the API.

### Configure