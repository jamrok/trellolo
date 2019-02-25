from pathlib import PurePath
from sys import argv

import click

from trellolo.board import BoardAPI
from trellolo.config import Config

# Add "-h" support
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

# Instantiate object that will later be used to interact with boards
trello = BoardAPI()


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-k", "--api-key", help="Your Trello API key", envvar="TRELLO_KEY"
)
@click.option("-t", "--token", help="Your Trello token", envvar="TRELLO_TOKEN")
def commands(api_key, token):
    """CLI for interacting with the Trello API"""
    try:
        if api_key and token:
            trello.auth(key=api_key, token=token)
    except Exception as e:
        raise click.ClickException(e)


################################
# CONFIG COMMAND
################################
@commands.command()
@click.option("-k", "--api-key", help="Enter your Trello API key")
@click.option("-t", "--token", help="Enter your Trello token")
def config(api_key, token):
    """Save Trello API key to the trellolo config file.\n
    Prompts for an API key if no options are specified.\n
    Credentials can also be read from the TRELLO_KEY and TRELLO_TOKEN
    environment variables
    """

    if api_key is None:
        api_key = click.prompt("Enter API key", hide_input=True)
    if token is None:
        token = click.prompt("Enter Token", hide_input=True)
    try:
        if api_key and token:
            Config.save(api_key, token)
            click.echo(f"Saved API key to {Config.config_file}")
    except Exception as e:
        raise click.ClickException(f"Unable to write to file:\n  {e}")


def load_config():
    """Load the config and instantiate an API client"""
    if trello.initialized or (
        # TODO: Find a  better way to determine the CliRunner invoked args
        # This is caused the help tests to fail when no config file or api
        # vars were present because get_os_args is diff from the invoked args
        set(["-h", "--help"]) & set(click.get_os_args())
    ):
        return
    try:
        data = Config.load()
        if not data:
            raise Exception(
                "No api key or token found. \n"
                f"  Run: [ {PurePath(argv[0]).name} config --help ]"
                f" for more information."
            )
        trello.auth(**data)
    except TypeError as e:
        raise click.ClickException(
            "Unable to load config." f"\n  Check {Config.config_file}:\n  {e}"
        )
    except Exception as e:
        raise click.ClickException(
            f"Unable to load config information:\n  {e}"
        )


################################
# CARD COMMANDS
################################


@commands.group()
def card():
    """Interact with cards"""
    load_config()  # load api and token from config


@card.command("add")
@click.option("-t", "--title", required=True)
@click.option("-d", "--description", "--desc")
@click.option("-l", "--list_id", required=True)
@click.option(
    "-c",
    "--labels",
    default="null",
    multiple=True,
    type=click.Choice(
        [
            "yellow",
            "purple",
            "blue",
            "red",
            "green",
            "orange",
            "black",
            "sky",
            "pink",
            "lime",
            "null",
        ]
    ),
)
# @click.option('-clbl', '--custom-labels'
#    , multiple=True
#    , type=(str, str) # name and colour
# )
def card_add(title, description, list_id, labels):
    """Adds a card to a specified list on a given board."""
    try:
        return trello.add_card(
            list_id, name=title, description=description, label_colour=labels
        )
    except Exception as e:
        raise click.ClickException(e)


@card.command("add_comment")
@click.option("-i", "--id", required=True, help="Card ID")
@click.option("-c", "--comment", required=True, help="Comment Text")
def card_add_comment(id="", comment=""):
    """Add a comment to a card"""
    try:
        trello.add_card_comment(id, comment)
    except Exception as e:
        raise click.ClickException(e)


@card.command("delete_comment")
@click.option("-i", "--id", required=True, help="Card ID")
@click.option("-c", "--comment_id", required=True, help="Comment ID")
def card_del_comment(id="", comment_id=""):
    """Delete a comment from a card"""
    try:
        trello.delete_card_comment(id, comment_id)
    except Exception as e:
        raise click.ClickException(e)


@card.command("show")
@click.option("-i", "--id", help="Show card details by id")
@click.option(
    "-a", "--all", is_flag=True,
    help="Show all cards on all lists on all boards"
)
# @click.option("-t", "--title")
# @click.option("-b", "--board")
# @click.option("-l", "--list")
# def card_show(id, title, board, list):
def card_show(id, all):
    """Show all cards. Can be filtered by specifying a board and list."""
    try:
        if id:
            trello.show_by_id(id, "card")
        elif all:
            trello.show_all_by_type(cards=True)
        else:
            click.echo(click.get_current_context().get_help())
    except Exception as e:
        raise click.ClickException(f"{e}")


@card.command("delete")
@click.option("-i", "--id", required=True, help="Delete card by id")
def card_delete(id):
    """Deleted a card using the ID."""
    try:
        trello.delete_card_by_id(id)
    except Exception as e:
        raise click.ClickException(e)


################################
# BOARD COMMANDS
################################


@commands.group()
def board():
    """Interact with boards"""
    load_config()  # load api and token from config


@board.command("show")
@click.option("-a", "--all", is_flag=True, help="Show all boards")
@click.option("-i", "--id", help="Show board by id")
def board_show(id, all):
    """Show all boards. Can be filtered by specifying a board id."""
    try:
        if id:
            trello.show_by_id(id, "board")
        elif all:
            trello.show_all_by_type()
        else:
            click.echo(click.get_current_context().get_help())
    except Exception as e:
        raise click.ClickException(e)


@board.command("add")
@click.option("-n", "--name")
def board_add(name):
    """Create a new board."""
    try:
        if name:
            trello.add_board(name)
        else:
            click.echo(click.get_current_context().get_help())
    except Exception as e:
        raise click.ClickException(e)


@board.command("delete")
@click.option("-i", "--id", required=True, help="Delete board by id")
def board_delete(id):
    """Delete a board."""
    try:
        trello.delete_board(id)
    except Exception as e:
        raise click.ClickException(e)


################################
# LIST COMMANDS
################################


@commands.group()
def list():
    """Interact with lists"""
    load_config()  # load api and token from config


@list.command("show")
@click.option("-i", "--id", help="Show list details by id")
@click.option("-a", "--all", is_flag=True, help="Show all lists on all boards")
# @click.option("-t", "--title")
# @click.option("-b", "--board")
# def list_show(title, board):
def list_show(id, all):
    """Show all lists. Can be filtered by specifying a board."""
    try:
        if id:
            trello.show_by_id(id, "list")
        elif all:
            trello.show_all_by_type(lists=True)
        else:
            click.echo(click.get_current_context().get_help())
    except Exception as e:
        raise click.ClickException(e)
