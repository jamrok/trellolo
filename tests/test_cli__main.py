import sys
from os import environ
from pathlib import Path
from random import choices
from string import ascii_lowercase

from click.testing import CliRunner

import pytest
from trellolo import __main__
from trellolo.commands import commands, load_config, trello
from trellolo.config import Config


def helper_check_cli(
    click_cmd="",
    args: list = [],
    expected_content: list = [],
    any_content: list = [],
    exit_code: int = 1,
    strict=False,
    input=""
):
    if not click_cmd:
        click_cmd = commands
    # Inject args into sys.argv because I can't access the args via invoke
    # See: trellolo.commands.load_config()
    orig_argv = sys.argv
    results = []
    for arg in args:
        sys.argv = orig_argv + [arg]
        results.append(CliRunner().invoke(click_cmd, args=arg, input=input))

    for result in results:
        for content in expected_content:
            if strict:
                assert content == str(result.output).strip()
            else:
                assert content in result.output
        if any_content:
            if strict:
                assert [
                    c for c in any_content if c == str(result.output).strip()
                ]
            else:
                assert [c for c in any_content if c in result.output]
        assert result.exit_code == exit_code


def test_cli_main():
    """Test calling main"""
    with pytest.raises(SystemExit) as e:
        sys.argv = [""]
        __main__.main()
    assert e.value.code == 0


def test_cli_with_no_args():
    """Test that syntax usage is shown when no arguments supplied"""
    result = CliRunner().invoke(commands)
    assert result.output[0:7] == "Usage: "
    assert result.exit_code == 0


rand = "".join(choices(ascii_lowercase, k=7))
orig_file = Config.config_file
new_file = Path(str(orig_file) + "." + rand)


@pytest.fixture(scope="module")
def cfg_backup(request):
    """Rename old config file and test accessing it when it's missing"""
    if orig_file.exists():
        Config.config_file.rename(new_file)
    # Always restore the file regardless of success/failure
    request.addfinalizer(cfg_restore_or_delete)


def cfg_restore_or_delete():
    """Put back the original config file if any existed"""
    if new_file.exists():
        new_file.rename(orig_file)
    else:
        if orig_file.exists():
            orig_file.unlink()


def test_config_missing(cfg_backup):
    """Temporarily rename the config file if found and test"""
    result = Config.load()
    # verify that None is returned when the file is missing
    assert result is None


def test_config_prompt_for_credentials(cfg_backup):
    """Test that API key and token can be entered and saved to a file"""
    helper_check_cli(
        args=[
            "config"
        ],
        expected_content=[
            "Enter API key:",
            "Enter Token:",
            "Saved API key to",
        ],
        exit_code=0,
        input="key123\ntoken456\n"
    )


def test_config_load_directly(cfg_backup):
    """Test that we can load the contents of the file via function call"""
    result = Config.load()
    key = result.get("key")
    token = result.get("token")
    assert key == "key123" and token == "token456"
    orig_file.unlink()
    assert key and token


def test_config_api_key_loading_from_config_file():
    """Test that we can load the contents of the config file via script"""

    k, t = ["TRELLO_KEY", "TRELLO_TOKEN"]
    key = environ[k]
    token = environ[t]
    if k in environ:
        key = environ[k]
        del environ[k]
    if t in environ:
        token = environ[t]
        del environ[t]
    Config.save(key, token)
    trello.initialized = False
    load_config()
