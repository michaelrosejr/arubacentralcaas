#!/usr/bin/env python3

import requests, json, logging, sys
from pprint import pprint
import central_config as cfg

logging.basicConfig(level=logging.WARN)

# group_name = "greendots/20:4c:03:12:33:20"
group_name = sys.argv[1]

# Open file and grab the token
with open(cfg.token_file, "rb") as f:
    token_data = json.load(f)

logging.debug("tokens %s:", token_data)



# config_path for AOS10, group_name for all others. May be interchangable.
# params = {"config_path": "/md/XXV-SEATTLE"}
# params = {"group_name": group_name }

headers = {
    "Content-Type": "application/json",
}

data = {
    "access_token": token_data["access_token"]
}

commited = requests.get(cfg.api_url + "/caasapi/v1/showcommand/object/committed?group_name=" + group_name, headers=headers, data=json.dumps(data))
# pprint(commited.json())
print(json.dumps(commited.json(), indent=1))