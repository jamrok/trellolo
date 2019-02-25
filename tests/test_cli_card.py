import re

from click.testing import CliRunner

import pytest
from tests.test_cli__main import helper_check_cli
from tests.test_cli_board import BoardOps
from trellolo.commands import commands


def test_card_invalid_api_key():
    """Test that invalid API key gives a meaningful error response"""
    helper_check_cli(
        args=[
            "-k api -t token card show"
        ],
        expected_content=[
            "Error: 401: invalid key"
        ],
        exit_code=1,
        strict=True
    )


def test_card_invalid_id():
    helper_check_cli(
        args=[
            "card show -i bad_card_id"
        ],
        expected_content=[
            "Error: 400: invalid id"
        ],
        exit_code=1,
        strict=True
    )


def test_card_valid_id_but_missing_resource():
    helper_check_cli(
        args=[
            "card show -i 123456789123456789123456"
        ],
        expected_content=[
            "Error: 404: The requested resource was not found."
        ],
        exit_code=1,
        strict=True
    )


def test_card_show_help():
    helper_check_cli(
        args=[
            "card show",
            "card show -h",
            "card show --help"
        ],
        expected_content=[
            "Usage:",
            "Show all cards.",
            "-a, --all",
            "-i, --id TEXT",
        ],
        exit_code=0
    )


class CardOps:
    boardops = None
    list = None
    card_title = ""
    card_id = ""
    comment_id = ""

    def __init__(self):
        self.boardops = BoardOps()
        self.card_title = "trellolo:pytest test card add"

    def refresh(self):
        self.boardops.refresh()
        board = [
            b for b in self.boardops.boards
            if self.boardops.board_title == b.name
        ].pop()
        try:
            _list = self.boardops.boardapi.get_lists_by_board_id(
                board.id
            ).pop()
        except IndexError:
            _list = None
        CardOps.list = _list

    def add_card(self):
        _args = (
            f"card add -t '{self.card_title}'"
            " -d 'test desc' -c blue -c green"
            f" -l {self.list.id}"
        )
        self.result_add_card = CliRunner().invoke(commands, args=_args)
        CardOps.card_id = re.sub(
            r".*Card ID: (\w+).*", "\\1",
            self.result_add_card.output.split("\n")[0]
        )
        return self.result_add_card

    def add_card_comment(self):
        assert len(self.card_id) == 24
        _args = (
            f"card add_comment -c '{self.card_title}'"
            f" -i {self.card_id}"
        )
        self.result_add_card_comment = CliRunner().invoke(commands, args=_args)
        CardOps.comment_id = re.sub(
            r".*Comment ID: (\w+) .*", "\\1",
            self.result_add_card_comment.output.split("\n")[2]
        )
        return self.result_add_card_comment

    def delete_card_comment(self):
        assert len(self.card_id) == 24
        assert len(self.comment_id) == 24
        assert self.card_id != self.comment_id

        _args = (
            f"card delete_comment -c {self.comment_id} -i {self.card_id}"
        )
        return CliRunner().invoke(commands, args=_args)

    def delete_card(self):
        self.refresh()
        card_ids = [
            c.id for c in self.list.cards
            if self.card_title == c.name
        ]
        assert len(card_ids) > 0
        for card_id in card_ids:
            _args = (f"card delete -i {card_id}")
            result1 = CliRunner().invoke(commands, args=_args)
            for content in [f"Card {card_id} deleted"]:
                assert content in result1.output
            assert result1.exit_code == 0


@pytest.fixture(scope="session")
def card_operations():
    return CardOps()


def get_card_instance(card_operations):
    return card_operations


def test_card_list_exists_to_add_card_to(card_operations):
    card_operations.refresh()
    assert card_operations.list is not None


@pytest.mark.dependency()
def test_card_add(card_operations):
    result = card_operations.add_card()
    for content in ["Card Added:", "blue", "green", "Label"]:
        assert content in result.output
    assert result.exit_code == 0


@pytest.mark.dependency(depends=["test_card_add"])
def test_card_add_comment(card_operations):
    result = card_operations.add_card_comment()
    for content in ["Comment Added:", "blue", "green", "Label"]:
        assert content in result.output
    assert result.exit_code == 0


@pytest.mark.dependency(depends=["test_card_add_comment"])
def test_card_show_by_id(card_operations):
    """Test that the card command shows whether cards are present or not"""
    helper_check_cli(
        args=[
            f"card show --id {card_operations.card_id}",
            f"card show -i {card_operations.card_id}"
        ],
        expected_content=[
            "Board ID:",
            "List ID:",
            "Card ID:",
            "Label(s)",
            "Comment ID:",
        ],
        exit_code=0
    )


@pytest.mark.dependency(depends=["test_card_add_comment"])
def test_card_show_all():
    """Test that the card command shows whether cards are present or not"""
    helper_check_cli(
        args=[
            "card show -a",
            "card show --all"
        ],
        expected_content=[
            "Board ID:",
            "List ID:",
            "Card ID:",
            "Label(s)",
            "Comment ID:",
        ],
        exit_code=0
    )
