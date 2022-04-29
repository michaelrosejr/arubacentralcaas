# Aruba Central CaaS Python Script

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/) [![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)

This script push devices changes via JSON updates to Aruba Central API for gateways/controllers (SD-WAN or AOS10). The CaaS API is useful if the Web GUI or RESTful API does not exist for specific feature or option in the config, that is not available in the Web GUI.

As of Aruba Central 2.5.1 (Tested on 2.5.5), the CaaS API is now available using access tokens. If you're looking for the previous script, it has been moved to /deprecated folder.

Commands available:

show-gateways 
show-accounts
show-committed [GROUP or GROUP/DEVICE_MAC]
show-effective [GROUP or GROUP/DEVICE_MAC]
show-routes [GROUP/DEVICE_MAC]
push-config [filename.json]  [GROUP/DEVICE_MAC]

To get started, first create the config.yaml file in the /config directory. There's a config.yaml.sample file to use as a template. The script will default to '''central_info''' as the account name if one is not set.

You can pass the account name using the --account [account_name] option. You can also set the environment variable as well: export ACCOUNT=[account_name]

Once the config.yaml file has been created, you can then 

