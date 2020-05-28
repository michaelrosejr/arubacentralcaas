# Aruba Central CaaS Python Script

As of Aruba Central 2.5.1, the CaaS API is now available using access tokens. If you're looking for the previous script, it has been moved to cookie_version.

These python scripts use the CaaS API to push configurations to Aruba Central that the GUI does not support. This is particluarly useful if you have to make a signficant amount of changes, such as add a large number of netdestiations, ACLs, VLANs, etc.

To install the script, 
```
git clone git@github.com:michaelrosejr/arubacentralcaas.git
```
### Start the virtualized shell
Once the script has been downloaded, it is recommended to run the script within a virtual enviroment. This script is already configured for pipenv. To enable the virtual shell, execute the following:

```
pipenv shell
```
 
This will install all the necessary packages and start the virtual shell.

Copy the ```central_config.py.example``` to ```central_config.py``` and edit as necessary for your environment and Aruba Central account.

For confiugrations you want to push to Central, store your CaaS JSON in a file. Please see ```example1.py```, ```example2.json``` and ```example3.json``` for examples. 


### The CaaS script takes two arguments. 
- The configuration you want to upload to Central (in JSON) format. 
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