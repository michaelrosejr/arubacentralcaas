#!/usr/bin/env python3

import requests, json, pickle, logging, sys
from pprint import pprint
import central_config as cfg

logging.basicConfig(level=logging.DEBUG)

# group_name = "greendots/20:4c:03:12:33:20"
group_name = sys.argv[1]

# Open file and grab the cookie Selenium created
with open(cfg.cookie_file, "rb") as f:
    cookies_data = pickle.load(f)

logging.debug("COOKIE %s:", cookies_data)

# Convert the cookie into a format Python requests can use.
c = {c["name"]: c["value"] for c in cookies_data}

# config_path for AOS10, group_name for all others. May be interchangable.
# params = {"config_path": "/md/XXV-SEATTLE"}
params = {"cid": cfg.customer_id, "group_name": group_name}

headers = {
    "Content-Type": "application/json",
}

commited = requests.get(cfg.network_url + "/caas/v1/showcommand/object/committed?group_name=" + group_name, headers=headers, cookies=c)
pprint(commited.json())
# print(commited.text)