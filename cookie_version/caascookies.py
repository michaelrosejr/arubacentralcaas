#!/usr/bin/env python3

import requests, json, pickle, logging, sys
from pprint import pprint
import central_config as cfg

# Enable logging. If its too verbose, change DEBUG to ERROR or another level
logging.basicConfig(level=logging.DEBUG)

# group_name = "greendots/20:4c:03:12:33:20"
group_name = sys.argv[2]

with open(sys.argv[1], "rb") as pf:
    payload = json.load(pf)



# CLI command to send
# payload = (
#     '{"cli_cmds": ["vlan 879", "description \'This is API description\'", "!"]}'
# )

# Another example of a CLI command - multi-line
# payload =  {
#     "cli_cmds": [
#         "netdestination test-api-alias",
#         "host 1.2.3.4",
#         "!",
#         "ip access-list session test-api-acl",
#         "alias test-api-alias any any permit",
#         "!"
#         ]
# }

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
response = requests.post(cfg.network_url + "/caas/v1/exec/cmd", params=params, headers=headers, data=json.dumps(payload), cookies=c)

print("POST Status Code: ", response.status_code)
print("POST Response: ")
pprint(response.json())

# commited = requests.get(cfg.network_url + "/caas/v1/showcommand/object/committed?group_name=" + group_name, headers=headers, cookies=c)
# print("Commit Status Code: ", commited.status_code)
# pprint(commited.json())





