import inspect
import ipaddress
import json

from rich import box, print
from rich.console import Console
from rich.table import Table

from ..config.settings import configfile  # noqa: E402
from ..config.settings import save_output_dir, settings

console = Console()


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


def display_account(account):
    print(f"Account Name: [#ff8300]{settings.ACCOUNT}[/#ff8300]")
    print("\nOther accounts in config file:")
    for profiles in configfile.keys():
        print(f"\t[cyan]{profiles}[/cyan]")


def display_gateways(gateways):
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


def display_routes(serial, routes):
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
                    "[" + str(route["nexthop"][0]["admin_distance"]) + "/" + str(route["nexthop"][0]["metric"]) + "]",
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
                    "[" + str(route["nexthop"][0]["admin_distance"]) + "/" + str(route["nexthop"][0]["metric"]) + "]",
                    nexthopaddress,
                    style=rowstyle,
                )
    console.print(route_table)
