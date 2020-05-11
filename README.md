# Aruba Central CaaS Python Script

These python scripts use the [Selenium](https://www.selenium.dev/) to grab the Aruba Central cookie. You can bypass the need for Selenium if you use your favorite browser and save the cookie yourself.

The [Selenium WebDriver](https://github.com/SeleniumHQ/selenium/tree/master/py) is required to use these scripts. If you choose not to use the Selenium, you will need to download and save the cookies necessary for the ```caas.py``` script. If you have issues using Selenium, please refer to thier [github repository](https://github.com/SeleniumHQ/selenium/tree/master/py). 

This script will install the Selenium webdriver for Python. However, you will need to install the necessary driver for yoru OS and browser. For example, Firefox uses the geckodrive. For details on which browser driver you install for your OS and browser, please refer to the [selenium github](https://github.com/SeleniumHQ/selenium/tree/master/py#Drivers) on drivers.

To install the script, 
```

```

Once the script has been downloaded, it is recommended to run the script within a virtual enviroment. This script is already configured for pipenv. To enable the virtual shell, execute the following:

```
pipenv shell
``
 
This will install all the necessary packages and start the virtual shell.

Copy the ```central_config.py.example``` to central_config.py``` and edit as necessary for your environment and Aruba Central account.

Store your CaaS JSON file in a file. Please see example1.py, example2.json and example3.json for examples. 

###The CaaS script take two arguments. 
- The configuration you want to upload to Central (in JSON) format. 
- The group_name and, if necessary, device that this config should apply to.

```
python3 caas.py your_json_file.json group_name
```
