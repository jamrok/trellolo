from tests.test_cli__main import helper_check_cli
from tests.test_cli_board import BoardOps
from tests.test_cli_card import CardOps


def test_board_show_by_id():
    """Test that the card command shows whether cards are present or not"""
    helper_check_cli(
        args=[
            f"board show --id {CardOps.list.board_id}",
            f"board show -i {CardOps.list.board_id}"
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


class TestCleanup:
    """Cleanup board and card at end"""

    def test_card_delete_comment(self):
        result = CardOps().delete_card_comment()
        for content in ["Comment Deleted"]:
            assert content in result.output
        assert result.exit_code == 0

    def test_card_delete(self):
        CardOps().delete_card()

    def test_board_delete(self):
        BoardOps().delete_board()
