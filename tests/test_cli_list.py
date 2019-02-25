from tests.test_cli__main import helper_check_cli
from tests.test_cli_card import CardOps


def test_list_invalid_api_key():
    """Test that invalid API key gives a meaningful error response"""
    helper_check_cli(
        args=[
            "-k api -t token list show"
        ],
        expected_content=[
            "Error: 401: invalid key"
        ],
        exit_code=1,
        strict=True
    )


def test_list_show_all():
    """Test that the list command shows whether lists are present or not"""
    helper_check_cli(
        args=[
            "list show -a",
            "list show --all"
        ],
        expected_content=[
            "Board ID:",
            "List ID:",
        ],
        exit_code=0
    )


def test_list_invalid_id():
    helper_check_cli(
        args=[
            "list show -i bad_list_id"
        ],
        expected_content=[
            "Error: 400: invalid id"
        ],
        exit_code=1,
        strict=True
    )


def test_list_valid_id_but_missing_resource():
    helper_check_cli(
        args=[
            "list show -i 123456789123456789123456"
        ],
        expected_content=[
            "Error: 404: model not found"
        ],
        exit_code=1,
        strict=True
    )


def test_list_show_by_id():
    """Test that the card command shows whether cards are present or not"""
    helper_check_cli(
        args=[
            f"list show --id {CardOps.list.id}",
            f"list show -i {CardOps.list.id}"
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


def test_list_show_help():
    helper_check_cli(
        args=[
            "list show",
            "list show -h",
            "list show --help"
        ],
        expected_content=[
            "Usage:",
            "Show all lists.",
            "-a, --all",
            "-i, --id TEXT",
        ],
        exit_code=0
    )
