#!/usr/bin/env python3

import ipaddress
import json
import logging

import typer
import yaml
from pycentral.base import ArubaCentralBase
from rich import box, print
from rich.console import Console
from rich.table import Table

console = Console()
app = typer.Typer()

with open(r"config/config.yaml") as file:
    configfile = yaml.load(file, Loader=yaml.FullLoader)

account = "central_info"
central_info = configfile[account]
logger = logging.getLogger(__name__)
central = ArubaCentralBase(central_info=central_info, ssl_verify=True, logger=logger)


def show_commited(group_name):
    apiPath = "/caasapi/v1/showcommand/object/committed"
    apiMethod = "GET"
    apiParams = {"limit": 0, "offset": 0, "group_name": group_name}
    query = central.command(apiMethod=apiMethod, apiPath=apiPath, apiParams=apiParams)
    return query


def get_gateways():
    apiPath = "/monitoring/v1/mobility_controllers"
    apiMethod = "GET"
    apiParams = {"sku_type": "GATEWAY"}
    query = central.command(apiMethod=apiMethod, apiPath=apiPath, apiParams=apiParams)
    return query


def get_routes(serial):
    apiPath = "/api/routing/v1/route"
    apiMethod = "GET"
    apiParams = {"device": serial}
    query = central.command(apiMethod=apiMethod, apiPath=apiPath, apiParams=apiParams)
    return query["msg"]


def caas_push_config(config_file, groupdev_name):
    with open("config_file", "rb") as jfile:
        payload = json.load(jfile)
    apiPath = "/caas/v1/exec/cmd"
    apiMethod = "POST"
    apiParams = {"cid": central_info.customer_id, "group_name": groupdev_name}
    apiData = json.dumps(payload)
    query = central.command(
        apiMethod=apiMethod, apiPath=apiPath, apiParams=apiParams, apiData=apiData
    )
    return query


@app.command()
def show_routes(serial: str = typer.Argument(..., help="show route table for device")):
    """
    show route table for device

    SERIAL required for this command
    """
    with console.status(
        "Getting Routes...", spinner="point", spinner_style="bold green"
    ):
        routes = get_routes(serial)
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
def show_gateways():
    """
    show list of gateways in Central account

    """
    with console.status(
        "Getting gateways...", spinner="point", spinner_style="bold green"
    ):
        gateways = get_gateways()
    gateway_table = Table(title="Gateways", box=box.SIMPLE)
    gateway_table.add_column("Name")
    gateway_table.add_column("SN")
    gateway_table.add_column("IP")
    gateway_table.add_column("MAC")
    gateway_table.add_column("Group")
    gateway_table.add_column("Status")
    gateway_table.add_column("GROUP/MAC")

    for eachgw in gateways["msg"]["mcs"]:
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
def show(
    group: str = typer.Argument(
        ...,
        help="show configuration committed for group or group/mac_addr. Ex: Seattle or Seattle/c2:46:65:dc:f8:16",
    )
):
    """
    'show configuration committed' for group/device
    """
    query = show_commited(group)
    print(query["msg"])


@app.command()
def push_config(
    config_file: str = typer.Argument(..., help="json config file to push"),
    groupdev_name: str = typer.Argument(
        ...,
        help="group/device name of group/device. Ex: Seattle or Seattle/c2:46:65:dc:f8:16",
    ),
):
    """

    Push json config to group/device.

    Ex: ./caas push-config newroute.json Seattle/c2:46:65:dc:f8:16

    """
    with console.status(
        "Pushing Configuration...", spinner="point", spinner_style="bold green"
    ):
        query = caas_push_config(config_file, groupdev_name)
    print(query)


if __name__ == "__main__":
    app()
