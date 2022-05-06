# Aruba Central CaaS CLI

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/) [![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)

Tested Aruba Central 2.5.5

This CLI is tool to view, manage and push devices changes via JSON updates to Aruba Central API for gateways/controllers (SD-WAN or AOS10). The CaaS API is useful if the Web GUI or RESTful API does not exist for specific feature or option in the config, that is not available in the Web GUI.

If you're looking for the previous script, it has been moved to /deprecated folder.

Commands available:

```bash
❯ caas --help

Using acccount: central_info. 
To change use --account or set the ACCOUNT environment variable: export ACCOUNT='myprofile'.

Usage: caas [OPTIONS] COMMAND [ARGS]...

Options:
  --save								 Save out to temp/ as JSON file
  --help                          Show this message and exit.

Commands:
  push-config     Push json config to group/device.
  show-accounts   show a list of accounts configured in the config.yaml file
  show-committed  'show configuration committed' for group/device
  show-effective  'show configuration effective' for group/device
  show-gateways   show list of gateways in Central account
  show-routes     show route table for device

```
## Installation

Requires python 3.9+ and pip

### PIP
```
pip install arubacentralcaas
```


### Using Poetry
```
git clone https://github.com/michaelrosejr/arubacentralcaas.git
poetry install
poetry shell
```

### Using venv
```
git clone https://github.com/michaelrosejr/arubacentralcaas.git
python3 -m venv venv
source venv/bin/activate
cd arubacentralcaas/
pip install -r requirements.txt

```

##Create a config file
Then create the `config.yaml` file in the `$HOME/config` or `$HOME/.config/central/` directory. There's a [`config.yaml.sample`](https://github.com/michaelrosejr/arubacentralcaas/blob/master/arubacentralcaas/config/config.yaml.sample) file to use as a template. The script will default to 'central_info' as the account name if one is not set.

```bash
central_info:
    client_id: "<Your Aruba Central API Client ID>"
    client_secret: "<Client Secret for the specified Client ID>"
    customer_id: "<Aruba Central Customer ID>"
    username: "<Aruba Central Username>"
    password: "<aruba-central-account-password>"
    base_url: "https://central-apigw.central.arubanetworks.com"  # The base of the Aruba Central API GW *for the Cluster you belong to* Starts with https://, ends with arubanetworks.com
```



You can pass the account name using the `--account [account_name]` option. You can also set the environment variable as well: `export ACCOUNT=[account_name]`

Once the config.yaml file has been created, you can then execute the script.

```
caas --help
```

### show accounts
To show the accuonts you setup in `config.yaml`:

```
caas show-accounts
``` 

### show gateways
To show the gateways configured in Aruba Central:

```
caas show-gateways
```

### show commited or effective changes
To show committed or effective changes on the gateway:

```
caas show-committed GROUP_NAME
caas show-committed GROUP_NAME/DEVICE_MAC_ADDRESS

caas show-effective GROUP_NAME
caas show-effective GROUP_NAME/DEVICE_MAC_ADDRESS
```

### Push a config
Finally to push changes to a Central group or device:
Create a JSON file in the format of:
`example2.json`

```
{
    "cli_cmds": [
        "netdestination test-api-alias",
        "host 1.2.3.4",
        "!",
        "ip access-list session test-api-acl",
        "alias test-api-alias any any permit",
        "!"
    ]
}
```

Then load push the configuration to Aruba Central via this caas CLI:

```
caas push-config sample/example2.json GROUP/00:11:22:33:44:55
```

### Save your output (--save)
The `show-committed` and `show-effective` commands have an option called `--save`, that will save the output into JSON format for you to edit and upload later. This file is located in the `./temp` directory.

## Configuration
There are additioanl configuration located in the `config/settings.py` file as well.

