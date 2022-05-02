#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Optional

import typer
from rich import print
from rich.console import Console

from .config.settings import settings
from .model.push_config import caas_push_config
from .model.shows import get_gateways, get_routes, show_device_committed, show_device_effective
from .views.displays import display_account, display_gateways, display_output, display_routes

console = Console()
app = typer.Typer()


storedaccount = settings.ACCOUNT
print(
    f"\nUsing acccount: [#ff8300]{storedaccount}[/#ff8300]. \nTo change use --account or"
    " set the ACCOUNT environment variable: [yellow]export ACCOUNT='myprofile'[/yellow].\n"
)


@app.command()
def show_accounts(account: str = typer.Option(storedaccount, help="show accounts")):
    """
    show a list of accounts configured in the config.yaml file

    """
    display_account(account)


@app.command()
def show_routes(
    serial: str = typer.Argument(..., help="show route table for device"),
    account: str = typer.Option(storedaccount, help="show gateways"),
):
    """
    show route table for device

    SERIAL required for this command
    """
    with console.status("Getting Routes...", spinner="point", spinner_style="bold green"):
        routes = get_routes(serial, account)
    display_routes(serial, routes)


@app.command()
def show_gateways(account: str = typer.Option(storedaccount, help="show gateways")):
    """
    show list of gateways in Central account

    """
    with console.status("Getting gateways...", spinner="point", spinner_style="bold green"):
        gateways = get_gateways(account)
    display_gateways(gateways)


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
    with console.status("Getting show committed...", spinner="point", spinner_style="bold green"):
        query = show_device_committed(group, account)
        display_output(query, save)


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
    with console.status("Getting show effective...", spinner="point", spinner_style="bold green"):
        query = show_device_effective(group, account)
        display_output(query, save)


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
