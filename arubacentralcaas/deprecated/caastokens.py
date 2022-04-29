#!/usr/bin/env python3

import requests, json, logging, sys
import yaml
import os
from pprint import pprint
from pycentral.base import ArubaCentralBase
from lib import getapi


def main():
    logging.basicConfig(
        format="%(asctime)s - %(name)s — %(levelname)s - %(message)s",
        level=logging.WARNING,
    )
    logging.getLogger("ARUBA_BASE").setLevel(logging.WARNING)
    logger = logging.getLogger(__name__)

    if "CENTRAL_ACCOUNT" in os.environ:
        account = os.environ["CENTRAL_ACCOUNT"]
    else:
        logger.error(
            "CENTRAL_ACCOUNT environment variables is not set. Please set with the account profile used in the config (config.yaml) file. Please see README.md file."
        )
        sys.exit(1)

    if "CENTRAL_REGION" in os.environ:
        region = os.environ["CENTRAL_REGION"]
    else:
        logger.error(
            "CENTRAL_REGION environment variables is not set. Please set with the account profile used in the config (config.yaml) file. Please see README.md file."
        )
        sys.exit(1)

    logger.info(f"ACCOUNT: {account} REGION:{region}")

    # group_name = "greendots/20:4c:03:12:33:20"
    group_name = sys.argv[2]

    with open(sys.argv[1], "rb") as pf:
        payload = json.load(pf)

    # Open file and grab the token
    with open(r"config/config.yaml") as file:
        configfile = yaml.load(file, Loader=yaml.FullLoader)

    central_info = configfile[account]
    region_url = configfile["regions"][region]

    central = ArubaCentralBase(central_info=central_info, ssl_verify=True)
    logger.debug(f"token {central.getToken()['access_token']}:")

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

    # config_path for AOS10, group_name for all others. May be interchangable.
    # params = {"config_path": "/md/XXV-SEATTLE"}

    token = central.loadToken()
    apiPath = "/caasapi/v1/exec/cmd"


    response = getapi.APICall(central = central, token = token, url = region_url, apiPath = apiPath, reqtype="post", group_name = group_name, payload = payload)
    # pprint(response.getData(), indent=2)
    print(response.getData()['_global_result']['status_str'])




if __name__ == "__main__":
    main()
