#!/usr/bin/env python3

import requests, json, logging, sys
import yaml
import os
from pprint import pprint
from pycentral.base import ArubaCentralBase
from lib import getapi


logging.basicConfig(
    format="%(asctime)s - %(name)s — %(levelname)s - %(message)s", level=logging.WARNING
)
logging.getLogger("ARUBA_BASE").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def main():
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
    if len(sys.argv) > 1:
        group_name = sys.argv[1]
    else:
        print("Group name is not set. \n show_committed.py GROUP_NAME|GROUP_NAME/MAC.\nSee README.md")
        sys.exit(1)

    # Open file and grab the token
    with open(r"config/config.yaml") as file:
        configfile = yaml.load(file, Loader=yaml.FullLoader)

    central_info = configfile[account]
    region_url = configfile["regions"][region]

    central = ArubaCentralBase(central_info=central_info, ssl_verify=True)

    logger.debug(f"token {central.getToken()['access_token']}:")

    # config_path for AOS10, group_name for all others. May be interchangable.
    # params = {"config_path": "/md/XXV-SEATTLE"}
    # params = {"group_name": group_name }


    token = central.loadToken()
    apiPath = "/caasapi/v1/showcommand/object/committed"

    response = getapi.APICall(central = central, token = token, url = region_url, apiPath = apiPath, reqtype="get", group_name = group_name)
    pprint(response.getData(), indent=2)


if __name__ == "__main__":
   main()
