from trellolo.trello import Board, Card, Comment, Label, List
from trellolo.trelloapi import TrelloAPI


class BoardAPI:

    _initialized = False

    def __init__(self, key="", token=""):
        self.auth(key, token)

    def auth(self, key="", token=""):
        TrelloAPI(key, token)
        self.initialized = TrelloAPI.initialized

    @property
    def initialized(self):
        return self._initialized

    @initialized.setter
    def initialized(self, val):
        self._initialized = val

    def add_board(self, name):
        url = "/1/boards/"
        query_string = {"name": name}
        resp = TrelloAPI.send_request(
            method="POST", url=url, params=query_string
        )
        if resp:
            print("Board Added:")
            board = self.get_board_by_id(resp["id"])
            print(board)
            return board
        else:
            raise Exception("Unable to create board")

    def delete_board(self, id):
        url = f"/1/boards/{id}"
        board = self.get_board_by_id(id)
        if not board.id:
            raise Exception(f"Unable to find board with ID: {id}")

        resp = TrelloAPI.send_request(method="DELETE", url=url)
        if resp:
            print(f"Board {id} deleted")
        else:
            raise Exception("Unable to delete board")

    def get_board_ids(self, title=""):
        url = "/1/members/me/boards"
        query_string = {"filter": "all", "fields": ""}
        resp = TrelloAPI.send_request(url, params=query_string)
        boards = []
        if resp:
            boards = [b["id"] for b in resp if b.get("id")]
        return boards

    def get_board_labels(self, id=""):
        url = f"/1/boards/{id}/labels"
        query_string = {"fields": "all"}
        resp = TrelloAPI.send_request(url, params=query_string)
        labels = []
        if resp:
            for l in resp:
                label = Label(l)
                labels.append(label)
        return labels

    def get_list_by_id(self, id=""):
        url = f"/1/lists/{id}"
        query_string = {"fields": "all"}
        resp = TrelloAPI.send_request(url, params=query_string)
        _list = List()
        if resp:
            _list = List(resp)
            _list.cards = self.get_cards_by_list_id(id)
        return _list

    def get_cards_by_list_id(self, id=""):
        url = f"/1/lists/{id}/cards"
        resp = TrelloAPI.send_request(url)
        cards = []
        if resp:
            cards = [Card(c) for c in resp]
        return cards

    def get_board_by_id(self, id=""):
        url = f"/1/boards/{id}"
        query_string = {"actions": "all", "cards": "all", "lists": "all"}
        resp = TrelloAPI.send_request(url, params=query_string)
        board = Board()
        if resp:
            board = Board(resp)
        return board

    def get_lists_by_board_id(self, id=""):
        url = f"/1/boards/{id}/lists"
        query_string = {"cards": "all", "card_fields": "all"}
        resp = TrelloAPI.send_request(url, params=query_string)
        lists = []
        if resp:
            for l in resp:
                _list = List(l)
                lists.append(_list)
        return lists

    def get_card_comments_by_id(self, id=""):
        url = f"/1/cards/{id}/actions"
        query_string = {"filter": "commentCard"}
        resp = TrelloAPI.send_request(url, params=query_string)
        comments = []
        if resp:
            comments = [Comment(c) for c in resp]
        return comments

    def add_card(self, list_id, name="", description="", label_colour=[]):
        url = "/1/cards"
        _list = self.get_list_by_id(list_id)
        labels = []
        if _list.id:
            labels = [
                l.id
                for l in self.get_board_labels(_list.board_id)
                if l.colour in label_colour
            ]

        if not labels:
            raise Exception(f"Unable to find label: {label_colour}")

        query_string = {
            "idList": list_id,
            "name": name,
            "pos": "bottom",
            "idLabels": ",".join(labels),
            "desc": description,
        }
        resp = TrelloAPI.send_request(
            method="POST", url=url, params=query_string
        )
        if resp:
            card = self.get_card_by_id(resp['id'])
            print(f"Card Added: {card}")
            return card
        else:
            raise Exception("Unable to add card")

    def add_card_comment(self, id, comment):
        url = f"/1/cards/{id}/actions/comments"
        card = self.get_card_by_id(id)
        if not card.id:
            raise Exception(f"Unable to find card with ID: {id}")

        query_string = {"text": comment}
        resp = TrelloAPI.send_request(
            method="POST", url=url, params=query_string
        )
        if resp:
            card = self.get_card_by_id(id)
            card.show_details = True
            card.comments = self.get_card_comments_by_id(id)
            print(f"Comment Added: {card}")
        else:
            raise Exception("Unable to add comment")

    def delete_card_comment(self, id, comment_id):
        url = f"/1/cards/{id}/actions/{comment_id}/comments"
        card = self.get_card_by_id(id)
        if not card.id:
            raise Exception(f"Unable to find card with ID: {id}")

        resp = TrelloAPI.send_request(method="DELETE", url=url)
        if resp:
            print("Comment Deleted")
        else:
            raise Exception("Unable to delete comment")

    def get_card_by_id(self, id=""):
        url = f"/1/cards/{id}"
        query_string = {"fields": "all", "card_fields": "all"}
        resp = TrelloAPI.send_request(url, params=query_string)
        card = Card()
        if resp:
            card = Card(resp)
            if card.has_comments:
                card.comments = self.get_card_comments_by_id(id)
        return card

    def delete_card_by_id(self, id=""):
        url = f"/1/cards/{id}"
        resp = TrelloAPI.send_request(method="DELETE", url=url)
        if resp:
            print(f"Card {id} deleted")

    def get_all_boards(self):
        boards = []
        for id in self.get_board_ids():
            board = self.get_board_by_id(id)
            boards.append(board)
        return boards

    def show_all_by_type(self, lists=False, cards=False):
        allboards = self.get_all_boards()

        if len(allboards) == 0:
            print("No boards available!")  # pragma: no cover
        else:
            for board in allboards:
                if lists or cards:
                    board.show_details = True
                    board.lists = self.get_lists_by_board_id(board.id)
                    if cards:
                        self.update_boardlist_with_card_info(
                            board, show_details=True
                        )
                print(board)

    def get_all_board_details(self, board_id, card="", list=""):
        board = self.get_board_by_id(board_id)
        board.show_details = True
        if list:
            board.lists = [list]
        elif card:
            board.lists = [self.get_list_by_id(card.list_id)]
        else:
            board.lists = self.get_lists_by_board_id(board.id)

        board = self.update_boardlist_with_card_info(
            board, show_details=True, card=card, list=list
        )
        return board

    def show_by_id(self, id, type):
        if type == "list":
            _list = self.get_list_by_id(id)
            board = self.get_all_board_details(
                _list.board_id, list=_list
            )
        elif type == "card":
            card = self.get_card_by_id(id)
            board = self.get_all_board_details(
                card.board_id, card=card
            )
        elif type == "board":
            board = self.get_all_board_details(id)
        else:
            raise Exception("Unknown type for show_by_id()")
        print(board)

    def update_boardlist_with_card_info(
        self, board: Board, show_details=False, card="", list=""
    ):
        """Get detailed board list with card information"""
        for _list in [
            l for l in board.lists if not list or l.id == list.id
        ]:
            _list.show_details = show_details
            cards = []
            for _card in [
                c for c in _list.cards if not card or c.id == card.id
            ]:
                if _card.has_comments:
                    _card.comments = self.get_card_comments_by_id(_card.id)
                cards.append(_card)
            _list.cards = cards
        return board
