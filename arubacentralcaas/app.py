#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inspect
import ipaddress
import json
import logging
import time
from functools import lru_cache
from pathlib import Path
from threading import local
from turtle import up
from typing import Optional

import typer
import yaml
from pycentral.base import ArubaCentralBase
from rich import box, print
from rich.console import Console
from rich.table import Table

from config.settings import configfile, settings

console = Console()
app = typer.Typer()


logger = logging.getLogger(__name__)

test_dir = "tests/resources/"
save_output_dir = "temp/"
storedaccount = settings.ACCOUNT
print(
    f"\nUsing acccount: [#ff8300]{storedaccount}[/#ff8300]. \nTo change use --account or set the ACCOUNT environment variable: [yellow]export ACCOUNT='myprofile'[/yellow].\n"
)


class central_test:
    def __init__(self, function_called):
        self.function_called = function_called

    def command(self, **kwargs):
        test_file_name = f"test_{self.function_called}.json"
        print(f"\nUsing test file: [yellow]{test_file_name}[/yellow]")
        with open(f"{test_dir}{test_file_name}", "r") as file:
            test_json = json.load(file)
        return test_json


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


def display_output(output, save=None):
    if output["code"] != 200:
        print(f"\n\n[red]Error Status Code: {output['code']} : {output['msg']}[/red]")
        exit(1)
    else:
        command_called = inspect.stack()[2][3]
        if save:
            with open(f"{save_output_dir}/{command_called}.json", "w+") as file:
                json.dump(output["msg"], file, indent=4)
        from rich import print_json

        print_json(json.dumps(output["msg"]))


def check_output(output):
    # Dump output for building tests
    # with open("temp/output.json", "w+") as file:
    #     json.dump(output, file, indent=4)
    if output["code"] != 200:
        print(f"\n\n[red]Error Status Code: {output['code']} : {output['msg']}[/red]")
        exit(1)
    else:
        return output["msg"]


def show_device_committed(group_name, account, save=None):
    central = get_config(account, ttl_hash=get_ttl_hash())
    apiPath = "/caasapi/v1/showcommand/object/committed"
    apiMethod = "GET"
    apiParams = {"limit": 0, "offset": 0, "group_name": group_name}
    query = central.command(apiMethod=apiMethod, apiPath=apiPath, apiParams=apiParams)
    display_output(query, save)


def show_device_effective(group_name, account, save=None):
    central = get_config(account, ttl_hash=get_ttl_hash())
    apiPath = "/caasapi/v1/showcommand/object/effective"
    apiMethod = "GET"
    apiParams = {"limit": 0, "offset": 0, "group_name": group_name}
    query = central.command(apiMethod=apiMethod, apiPath=apiPath, apiParams=apiParams)
    display_output(query, save)
    # return query


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


def caas_push_config(config_file, groupdev_name, account):
    central = get_config(account, ttl_hash=get_ttl_hash())
    with open(config_file, "rb") as jfile:
        payload = json.load(jfile)
    if "cli_cmds" not in payload.keys():
        print(
            "[red]\nError: The config file does not contain any CLI commands. Please check the config file to ensure 'cli_cmds' is present."
        )
        exit(1)
    else:
        apiPath = "/caasapi/v1/exec/cmd"
        apiMethod = "POST"
        apiParams = {
            "cid": configfile[account]["customer_id"],
            "group_name": groupdev_name,
        }
        apiHeaders = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {central.getToken()['access_token']}",  # type: ignore
        }
        print(
            f"[bold]You are about to push changes to the account[/bold] [#ff8300]{account}[/#ff8300]!"
        )
        confirm = console.input(
            f"Type`[bold red]confirm[/bold red]` to [red]push[/red] changes in file '[cyan]{config_file}[/cyan]' to [yellow]{groupdev_name}[/yellow]: "
        )

        if confirm == "confirm":
            print(f"\nConfirmation recieved!")
            print(
                f"Pushing configuration in [blue]{config_file}[/blue] to [green]{groupdev_name}[/green]...\n"
            )
            query = central.command(
                apiMethod=apiMethod,
                headers=apiHeaders,
                apiPath=apiPath,
                apiParams=apiParams,
                apiData=payload,
            )

            if query["code"] != 200:
                response = (
                    f"[red]Error Status Code: {query['code']} : {query['msg']}[/red]"
                )
            else:
                response = query["msg"]
        else:
            print("Aborting changes...")
            response = ""
            exit(1)
    return response


@app.command()
def show_accounts(account: str = typer.Option(storedaccount, help="show accounts")):
    '''
        show a list of accounts configured in the config.yaml file

    '''
    print(f"Account Name: [#ff8300]{settings.ACCOUNT}[/#ff8300]")
    print("\nOther accounts in config file:")
    for profiles in configfile.keys():
        print(f"\t[cyan]{profiles}[/cyan]")


@app.command()
def show_routes(
    serial: str = typer.Argument(..., help="show route table for device"),
    account: str = typer.Option(storedaccount, help="show gateways"),
):
    """
    show route table for device

    SERIAL required for this command
    """
    with console.status(
        "Getting Routes...", spinner="point", spinner_style="bold green"
    ):
        routes = get_routes(serial, account)
    # print(routes["summary"])
    # print(routes["routes"])
    print("")
    route_summary = Table(title="Route Summary", show_header=False, box=box.SIMPLE)
    route_summary.add_row("Total Routes", str(routes["summary"]["total"]))
    route_summary.add_row("Default Routes", str(routes["summary"]["default"]))
    route_summary.add_row("Static Routes", str(routes["summary"]["static"]))
    route_summary.add_row("Connected Routes", str(routes["summary"]["connected"]))
    route_summary.add_row("Overlay Routes", str(routes["summary"]["overlay"]))

    console.print(route_summary)

    route_table = Table(title=f"Route Table: {serial}", box=box.SIMPLE)
    route_table.add_column(
        "",
    )
    route_table.add_column("Destination")
    route_table.add_column("D/M")
    route_table.add_column("Nexthop")
    for route in routes["routes"]:
        if route["nexthop"][0]["protocol"] != "Connected":
            if route["nexthop"][0]["protocol"] == "Static":
                rowstyle = "cyan"
            else:
                rowstyle = "#d78700"
            try:
                nexthopip = ipaddress.ip_address(route["nexthop"][0]["address"])
                route_table.add_row(
                    route["nexthop"][0]["protocol"],
                    route["prefix"] + "/" + str(route["length"]),
                    "["
                    + str(route["nexthop"][0]["admin_distance"])
                    + "/"
                    + str(route["nexthop"][0]["metric"])
                    + "]",
                    "via " + route["nexthop"][0]["address"],
                    style=rowstyle,
                )
            except ValueError:
                # nexthopip = route["nexthop"][0]["address"]
                nexthopip = 0
            if nexthopip == 0:
                if len(route["nexthop"]) > 1:
                    nexthopaddress = ""
                    for nh in route["nexthop"]:
                        nexthopaddress += "ipsec map " + nh["address"] + "\n"
                else:
                    nexthopaddress = "ipsec map " + route["nexthop"][0]["address"]
                route_table.add_row(
                    route["nexthop"][0]["protocol"],
                    route["prefix"] + "/" + str(route["length"]),
                    "["
                    + str(route["nexthop"][0]["admin_distance"])
                    + "/"
                    + str(route["nexthop"][0]["metric"])
                    + "]",
                    nexthopaddress,
                    style=rowstyle,
                )
    console.print(route_table)


@app.command()
def show_gateways(account: str = typer.Option(storedaccount, help="show gateways")):
    """
    show list of gateways in Central account

    """
    with console.status(
        "Getting gateways...", spinner="point", spinner_style="bold green"
    ):
        gateways = get_gateways(account)
    gateway_table = Table(title="Gateways", box=box.SIMPLE)
    gateway_table.add_column("Name")
    gateway_table.add_column("SN")
    gateway_table.add_column("IP")
    gateway_table.add_column("MAC")
    gateway_table.add_column("Group")
    gateway_table.add_column("Status")
    gateway_table.add_column("GROUP/MAC")

    for eachgw in gateways["mcs"]:
        gateway_table.add_row(
            eachgw["name"],
            eachgw["serial"],
            eachgw["ip_address"],
            eachgw["macaddr"],
            eachgw["group_name"],
            eachgw["status"],
            f'[bold cyan]{eachgw["group_name"]}/{eachgw["macaddr"]}[/bold cyan]',
        )

    console.print(gateway_table)


@app.command()
def show_committed(
    group: str = typer.Argument(
        ...,
        help="show configuration committed for group or group/mac_addr. Ex: Seattle or Seattle/c2:46:65:dc:f8:16",
    ),
    account: str = typer.Option(storedaccount, help="show gateways"),
    save: Optional[bool] = False,
):
    """
    'show configuration committed' for group/device
    """
    with console.status(
        "Getting show committed...", spinner="point", spinner_style="bold green"
    ):
        query = show_device_committed(group, account, save)


@app.command()
def show_effective(
    group: str = typer.Argument(
        ...,
        help="show configuration effective for group or group/mac_addr. Ex: Seattle or Seattle/c2:46:65:dc:f8:16",
    ),
    account: str = typer.Option(storedaccount, help="show gateways"),
    save: Optional[bool] = False,
):
    """
    'show configuration effective' for group/device
    """
    with console.status(
        "Getting show effective...", spinner="point", spinner_style="bold green"
    ):
        query = show_device_effective(group, account, save)


@app.command()
def push_config(
    config_file: str = typer.Argument(..., help="json config file to push"),
    groupdev_name: str = typer.Argument(
        ...,
        help="group/device name of group/device. Ex: Seattle or Seattle/c2:46:65:dc:f8:16",
    ),
    account: str = typer.Option(storedaccount, help="show gateways"),
):
    """

    Push json config to group/device.

    Ex: ./caas push-config newroute.json Seattle/c2:46:65:dc:f8:16

    """

    query = caas_push_config(config_file, groupdev_name, account)
    print(query)


if __name__ == "__main__":
    app()
