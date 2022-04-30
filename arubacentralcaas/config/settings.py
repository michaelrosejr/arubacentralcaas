import inspect
import sys
import time
from functools import lru_cache

import yaml
from loguru import logger
from model.tests import central_test
from pycentral.base import ArubaCentralBase
from pydantic import BaseSettings

test_dir = "tests/resources/"
save_output_dir = "temp/"

logger.add(
    sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO"
)


class Settings(BaseSettings):
    ACCOUNT: str = "central_info"


settings = Settings()  # type: ignore

with open(r"config/config.yaml") as file:
    configfile = yaml.load(file, Loader=yaml.FullLoader)


@lru_cache
def get_config(account, ttl_hash=None):
    del ttl_hash  # to emphasize we don't use it and to shut pylint up
    global storedaccount
    storedaccount = account
    # One day we will use this to cache the config
    # account_name = {
    #     "storedaccount": storedaccount,
    # }
    # cachefile = ".cache/caascache.json"
    # Path(".cache").mkdir(parents=True, exist_ok=True)
    # cachefile = Path(cachefile)
    # if cachefile.is_file():
    #     with open(cachefile, "r") as file:
    #         token = file.read()
    # else:
    #     cachefile.touch(exist_ok=True)
    #     with open(cachefile, "w+") as cache:
    #         json.dump(account_name, cache)
    central_info = configfile[storedaccount]
    # Grab the calling function so we can use it for testing
    calling_function = inspect.stack()[1][3]

    if account == "tests":
        # Send name of calling function to pull test json file
        central = central_test(calling_function)
    else:
        central = ArubaCentralBase(
            central_info=central_info, ssl_verify=True, logger=logger
        )

    return central


def get_ttl_hash(seconds=300):
    """Return the same value withing `seconds` time period"""
    return round(time.time() / seconds)
