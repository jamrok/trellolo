class TrelloObject:
    """Base Trello object"""

    show_details = False

    def __init__(self, info: dict = {}):
        self.name = info.get("name")
        self.id = info.get("id")

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, _id):
        self._id = _id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val

    def __repr__(self):
        return str(vars(self))

    def __str__(self):
        return f"{self.__class__.__name__} ID: {self.id} | Name: {self.name}"


class Board(TrelloObject):
    """Trello Board object"""

    def __init__(self, info: dict = {}):
        super().__init__(info)
        self.lists = info.get("lists", [])

    @property
    def lists(self):
        return self._lists

    @lists.setter
    def lists(self, lists):
        self._lists = lists
        if lists and isinstance(lists[0], dict):
            self._lists = [List(l) for l in lists]

    def __str__(self):
        data = [f"{super().__str__()}"]
        if self.show_details:
            if self.lists:
                data.extend([str(l) for l in self.lists])
            else:
                data.append(
                    "  🗋 No lists are on this board.\n"
                )  # pragma: no cover
        return "\n".join(data)


class List(TrelloObject):
    """Trello List object"""

    def __init__(self, info: dict = {}):
        super().__init__(info)
        self.cards = info.get("cards", [])
        self.board_id = info.get("idBoard")

    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, val=[]):
        self._cards = val
        if val and isinstance(val[0], dict):
            self._cards = [Card(c) for c in val]

    @property
    def board_id(self):
        return self._board_id

    @board_id.setter
    def board_id(self, board_id: str):
        self._board_id = board_id

    def __str__(self):
        data = [f"  📄 {super().__str__()}"]
        if self.show_details:
            if self.cards:
                data.extend([str(c) for c in self.cards])
            else:
                data.append("    🃠 No cards are on this list.")
        data.append("")
        return "\n".join(data)


class Card(TrelloObject):
    """Trello Card object"""

    def __init__(self, info: dict = {}, has_comments=False):
        super().__init__(info)
        self.board_id = info.get("idBoard")
        self.list_id = info.get("idList")
        self.comments = info.get("comments", [])
        self.labels = info.get("labels", [])
        if isinstance(info, dict) and info.get("badges"):
            self.has_comments = bool(info.get("badges").get("comments", 0))
        else:
            self.has_comments = 0

    @property
    def board_id(self):
        return self._board_id

    @board_id.setter
    def board_id(self, board_id: str):
        self._board_id = board_id

    @property
    def list_id(self):
        return self._list_id

    @list_id.setter
    def list_id(self, list_id: str):
        self._list_id = list_id

    @property
    def comments(self):
        return self._comments

    @comments.setter
    def comments(self, comments=[]):
        self._comments = comments

    @property
    def has_comments(self):
        return self._has_comments

    @has_comments.setter
    def has_comments(self, info: bool = False):
        self._has_comments = info

    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, labels=[]):
        self._labels = [Label(l) for l in labels]

    def __str__(self):
        data = [f"    🃪 {super().__str__()}"]
        if self.labels:
            data.append(
                f"{' '*5} 🏷  Label(s): "
                f"{[ l.colour for l in self.labels ]}"
            )
        if self.comments:
            data.extend([str(c).rstrip() for c in self.comments])
        # else:
        #     data.append(f"{' '*8}💭  No comments on card")
        return "\n".join(data)


class Comment(TrelloObject):
    """Trello Comment object"""

    def __init__(self, info={}):
        super().__init__({
            "name": info.get("memberCreator").get("fullName"),
            "id": info.get("id")
        })
        self.date = info.get("date")
        self.text = info.get("data").get("text")

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date=""):
        self._date = date

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, info=""):
        self._text = info

    def __str__(self):
        return str(
            f"{' '*8}💭  " +
            super().__str__() +
            f" | Date: {self.date}"
            f" | Text: {self.text}"
        )


class Label(TrelloObject):
    """Trello Label object"""

    _id_board = ""

    def __init__(self, info: dict = {}):
        super().__init__(info)
        self.colour = info.get("color")
        if not self.id_board:
            self.id_board = info.get("idBoard")

    @property
    def colour(self):
        return self._colour

    @colour.setter
    def colour(self, colour: str):
        self._colour = colour

    @property
    def id_board(self):
        return self._id_board

    @id_board.setter
    def id_board(self, id_board=""):
        self._id_board = id_board
