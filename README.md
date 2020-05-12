# Aruba Central CaaS Python Script

These python scripts use the [Selenium](https://www.selenium.dev/) to grab the Aruba Central cookie. You can bypass the need for Selenium if you use your favorite browser and save the cookie yourself.

The [Selenium WebDriver](https://github.com/SeleniumHQ/selenium/tree/master/py) is required to use these scripts. If you choose not to use the Selenium, you will need to download and save the cookies necessary for the ```caas.py``` script. If you have issues using Selenium, please refer to thier [github repository](https://github.com/SeleniumHQ/selenium/tree/master/py). 

This script will install the Selenium webdriver for Python. However, you will need to install the necessary driver for yoru OS and browser. For example, Firefox uses the geckodrive. For details on which browser driver you install for your OS and browser, please refer to the [selenium github](https://github.com/SeleniumHQ/selenium/tree/master/py#Drivers) on drivers.

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

Store your CaaS JSON file in a file. Please see ```example1.py```, ```example2.json``` and ```example3.json``` for examples. 

### Get the cookies
Execute the following script to start Selenium to login using your browser to save the cookies.

This script must run from your terminal/shell and not inside your IDE.

```
python3 ac_cookie.py
```

**NOTE**: Once the script completes, the script will create a file called ```cookie.pkl```. This is the cookies downloaded from your webbrowser and saved in [pickle](https://docs.python.org/3/library/pickle.html) object as Selenium stores the the cookies in a seriealized object. This file will be used in the next section.

### The CaaS script take two arguments. 
- The configuration you want to upload to Central (in JSON) format. 
- The group_name and, if necessary, device that this config should apply to.

```
python3 caas.py your_json_file.json group_name
```
