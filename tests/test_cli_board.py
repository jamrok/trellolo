from os import getenv

from click.testing import CliRunner

import pytest
from tests.test_cli__main import helper_check_cli
from trellolo.board import BoardAPI
from trellolo.commands import commands
from trellolo.config import Config


def test_board_invalid_api_key():
    """Test that invalid API key gives a meaningful error response"""
    helper_check_cli(
        args=[
            "-k api -t token board show"
        ],
        expected_content=[
            "Error: 401: invalid key"
        ],
        exit_code=1,
        strict=True
    )


def test_board_show_board_add_help():
    """Test that invalid API key gives a meaningful error response"""
    helper_check_cli(
        args=[
            "board add"
        ],
        expected_content=[
            "Create a new board.",
            "-n, --name TEXT"
        ],
        exit_code=0,
    )


def test_board_invalid_id():
    helper_check_cli(
        args=[
            "board show -i bad_board_id"
        ],
        expected_content=[
            "Error: 400: invalid id"
        ],
        exit_code=1,
        strict=True
    )


def test_board_valid_id_but_missing_resource():
    helper_check_cli(
        args=[
            "board show -i 123456789123456789123456"
        ],
        expected_content=[
            "Error: 404: The requested resource was not found."
        ],
        exit_code=1,
        strict=True
    )


def test_board_show_help():
    helper_check_cli(
        args=[
            "board show",
            "board show -h",
            "board show --help"
        ],
        expected_content=[
            "Usage:",
            "Show all boards.",
            "-a, --all",
            "-i, --id TEXT",
        ],
        exit_code=0
    )


class BoardOps:
    boards = []
    board_title = ""
    key = ""
    token = ""

    def __init__(self):
        self.board_title = "zTest Board by trellolo"
        """Finds the board ID"""
        key = getenv("TRELLO_KEY")
        token = getenv("TRELLO_TOKEN")
        if not key or not token:
            key = Config.api_key()
            token = Config.token()

        assert isinstance(key, str)
        assert isinstance(token, str)
        self.boardapi = BoardAPI(key, token)

    def refresh(self):
        try:
            boards = self.boardapi.get_all_boards()
        except Exception:
            boards = None
        self.boards = boards

    def add_board(self):
        _args = (
            f"board add -n '{self.board_title}'"
        )
        self.result_add_board = CliRunner().invoke(commands, args=_args)
        return self.result_add_board

    def delete_board(self):
        self.refresh()
        board_ids = [
            b.id for b in self.boards
            if f"{self.board_title}" == b.name
        ]
        assert len(board_ids) > 0
        for board_id in board_ids:
            _args = (f"board delete -i {board_id}")
            result1 = CliRunner().invoke(commands, args=_args)
            for content in [f"Board {board_id} deleted"]:
                assert content in result1.output
            assert result1.exit_code == 0


@pytest.fixture(scope="session")
def board_operations():
    return BoardOps()


def test_board_ensure_board_exists(board_operations):
    assert board_operations.boards is not None


@pytest.mark.dependency()
def test_board_add(board_operations):
    result = board_operations.add_board()
    for content in [
        "Board Added:", "Board ID:", f"Name: {BoardOps().board_title}"
    ]:
        assert content in result.output
    assert result.exit_code == 0


def test_board_show_all():
    """Test that the board command shows whether boards are present or not"""
    helper_check_cli(
        args=[
            "board show -a",
            "board show --all"
        ],
        expected_content=[
            "Board ID:",
        ],
        exit_code=0
    )
