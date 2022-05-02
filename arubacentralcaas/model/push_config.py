import json

from rich import print
from rich.console import Console

from ..config.settings import configfile, get_config, get_ttl_hash

console = Console()


def caas_push_config(config_file, groupdev_name, account):
    central = get_config(account, ttl_hash=get_ttl_hash())
    with open(config_file, "rb") as jfile:
        payload = json.load(jfile)
    if "cli_cmds" not in payload.keys():
        print(
            "[red]\nError: The config file does not contain any CLI commands. \
                Please check the config file to ensure 'cli_cmds' is present."
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
        print(f"[bold]You are about to push changes to the account[/bold] [#ff8300]{account}[/#ff8300]!")
        confirm = console.input(
            f"Type`[bold red]confirm[/bold red]` to [red]push[/red] changes in file \
                '[cyan]{config_file}[/cyan]' to [yellow]{groupdev_name}[/yellow]: "
        )

        if confirm == "confirm":
            print("\nConfirmation recieved!")
            print(f"Pushing configuration in [blue]{config_file}[/blue] to [green]{groupdev_name}[/green]...\n")
            query = central.command(
                apiMethod=apiMethod,
                headers=apiHeaders,
                apiPath=apiPath,
                apiParams=apiParams,
                apiData=payload,
            )

            if query["code"] != 200:
                response = f"[red]Error Status Code: {query['code']} : {query['msg']}[/red]"
            else:
                response = query["msg"]
        else:
            print("Aborting changes...")
            response = ""
            exit(1)
    return response
