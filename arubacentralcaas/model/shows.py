import sys
from pathlib import Path

sys.path.append(str(Path(".").absolute().parent))
from ..config.settings import get_config, get_ttl_hash  # noqa: E402
from ..views.displays import check_output  # noqa: E402


def show_device_committed(group_name, account):
    central = get_config(account, ttl_hash=get_ttl_hash())
    apiPath = "/caasapi/v1/showcommand/object/committed"
    apiMethod = "GET"
    apiParams = {"limit": 0, "offset": 0, "group_name": group_name}
    query = central.command(apiMethod=apiMethod, apiPath=apiPath, apiParams=apiParams)
    return query


def show_device_effective(group_name, account):
    central = get_config(account, ttl_hash=get_ttl_hash())
    apiPath = "/caasapi/v1/showcommand/object/effective"
    apiMethod = "GET"
    apiParams = {"limit": 0, "offset": 0, "group_name": group_name}
    query = central.command(apiMethod=apiMethod, apiPath=apiPath, apiParams=apiParams)

    return query


def get_gateways(account):
    central = get_config(account, ttl_hash=get_ttl_hash())
    apiPath = "/monitoring/v1/mobility_controllers"
    apiMethod = "GET"
    apiParams = {"sku_type": "GATEWAY"}
    query = central.command(apiMethod=apiMethod, apiPath=apiPath, apiParams=apiParams)
    response = check_output(query)
    return response


def get_routes(serial, account):
    central = get_config(account, ttl_hash=get_ttl_hash())
    apiPath = "/api/routing/v1/route"
    apiMethod = "GET"
    apiParams = {"device": serial}
    query = central.command(apiMethod=apiMethod, apiPath=apiPath, apiParams=apiParams)
    response = check_output(query)
    return response
