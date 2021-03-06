# Aruba Central CaaS Python Script

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/) [![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)

This script push devices changes via JSON updates to Aruba Central API for gateways/controllers (SD-WAN or AOS10). This is useful if the Web GUI or API does not exist for specific feature or option in the config, that's not available in the Web GUI.

As of Aruba Central 2.5.1, the CaaS API is now available using access tokens. If you're looking for the previous script, it has been moved to cookie_version.

I've also added a python script to do the equiviant to a `show committed` in the AOS CLI. The script is called `show_committed`. Please [see details below](#show-committed) on show_committed below.

These python scripts use the CaaS API to push configurations to Aruba Central that the GUI does not support. This is particluarly useful if you have to make a signficant amount of changes, such as add a large number of netdestiations, ACLs, VLANs, etc.


### Update
2020-12-11: This script now uses pycentral SDK. The biggest change is the config file has been moved to the config directory and now uses yaml. You can also add multiple Aruba Central accounts and change which account you're using setting the OS environment setting.

```
CENTRAL_ACCOUNT=hoolio
CENTRAL_REGION=us2
```

Mac/Linux: 
`export CENTRAL_ACCOUNT=hoolio`

Windows: 
`setx CENTRAL_ACCOUNT=hoolio`


The config.yaml file has a list of regions, which may be incomplete. Please refer to Aruba Central help guides for the URL for your region.

### Installation

To install the script, 
```
git clone https://github.com/michaelrosejr/arubacentralcaas.git
```
### Usage
Once the script has been downloaded, it is recommended to run the script within a virtual enviroment. This script is already configured for pipenv. To enable the virtual shell, execute the following:

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt 
```
 
This will install all the necessary packages and start the virtual shell.

In the config directory, copy the ```config.yaml.sample``` to ```config.yaml``` and edit as necessary for your environment and Aruba Central account.

For confiugrations you want to push to Central, store your CaaS JSON in a file. Please see ```example1.py```, ```example2.json``` and ```example3.json``` for examples. 


### The CaaS script takes two arguments. 
- The configuration you want to upload to Central (in JSON) format. Please see above on setting up the configuratio file.
- The group_name and, if necessary, device that this config should apply to.

`group_name/MAC:ADDRESS:OF:DEVICE`

```
python3 caastokens.py your_json_file.json group_name
```

Example of a device level change:

```
python3 caastokens.py example1.json SEATTLE/20:3b:03:b5:f9:15
```

OR for a group level change:

```
python3 caastokens.py example1.json SEATTLE
```

![](images/caastokens.png)



### <a id="show-committed">Show Committed</a>
The following script will show the configuration of a device or group in Central. The configuration for this script will be pulled from the `central_config.py` file. 
****NOTE: The show_committed script only uses the token_file and api_url


```python3 show_committed.py SEATTLE```

OR

```python3 show_committed.py SEATTLE/20:3b:03:b5:f9:15```

![](images/show_committed.png)

### License
 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### Contribute
If you're interested in contributing to add feature or fix bugs, please open an issue to discuss and Pull Requests to fix an identified bug. PR's are always welcome! Please be sure to have a detailed PR description that clearly describes the problem and solution. 
