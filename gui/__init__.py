from PyQt6.QtCore import QSize
from PyQt6.QtGui import (
    QColor,
    QPalette,
)
from PyQt6.QtWidgets import (
    QMainWindow,
    QComboBox,
    QLabel,
    QGridLayout,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QWidget,
)
from .Objects import Card
from .Widgets import (
    CardDropDown,
    CardFrame,
    CardGridArea,
    CardGridButton,
    TestBox,
)
from pathlib import Path

GRID_COLUMN_LIMIT = 5

# Main should handle all signal and slots between widgets!
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("OPTCG Deck Builder")
        self.setFixedSize(QSize(1080, 720))

        """ State """
        base_path = Path().parent
        self.leader = Card(base_path / "[ST-01]" / "ST01-001.png")
        self.don = Card(base_path / "res" / "don-cards" / "1.png")
        self.card_back = Card(base_path / "[ST-01]" / "ST01-003.png")

        self.card_set_cards = self.get_test_cards(54)
        self.deck_cards = self.get_test_cards(12)


        """ Widgets """
        self.card_set_scroll_area = CardGridArea(self.card_set_cards)
        for card_button in self.card_set_scroll_area.card_buttons:
            card_button.clicked.connect(lambda r: self.sig_add_card_to_deck(r, card_button.card))
        self.deck_scroll_area = CardGridArea(self.deck_cards)

        """ Layouts """
        main_layout = QHBoxLayout()
        left_layout = self.create_left_side_layout()
        right_layout = self.create_right_side_layout()

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        widget = QWidget()
        widget.setLayout(main_layout)

        self.setCentralWidget(widget)


    def create_left_side_layout(self):
        left_side_layout = QVBoxLayout()

        card_set_label = QLabel("Card Set")
        left_side_layout.addWidget(card_set_label)
        left_side_layout.addWidget(self.card_set_scroll_area)

        deck_label = QLabel("Deck")
        left_side_layout.addWidget(deck_label)
        left_side_layout.addWidget(self.deck_scroll_area)

        return left_side_layout


    def create_right_side_layout(self):
        right_side_layout = QGridLayout()
        button_layout = QVBoxLayout()
        card_buttons_layout = QHBoxLayout()

        cb_card_set = QComboBox()
        cb_card_set.addItems([
            "ST-1",
            "ST-2",
            "ST-3",
        ])

        cbtn_leader = CardDropDown("Select Leader", self.leader.path)
        cbtn_don = CardDropDown("Select DON", self.don.path)
        cbtn_card_back = CardDropDown("Select Card Back", self.card_back.path)

        test_card = CardFrame(self.leader.path)

        card_buttons_layout.addWidget(cbtn_leader)
        card_buttons_layout.addWidget(cbtn_don)
        card_buttons_layout.addWidget(cbtn_card_back)
        # card_buttons_layout.addWidget(test_card)

        btn_clear_deck = QPushButton("Clear Deck")
        btn_clear_deck.clicked.connect(self.sig_clear_area)
        btn_gen_deck_img = QPushButton("Generate Deck Image")
        button_layout.addWidget(btn_clear_deck)
        button_layout.addWidget(btn_gen_deck_img)

        right_side_layout.addWidget(cb_card_set, 0,0)
        right_side_layout.addLayout(card_buttons_layout, 1,0)
        right_side_layout.addWidget(TestBox(), 2,0)
        right_side_layout.addLayout(button_layout, 3,0)
        return right_side_layout


    def sig_add_card_to_deck(self, result, card):
        print(f"Adding card {card.coords}: {result}")
        """
            1. Get last card coords
            2. Create new Card with last card coords
            3. Check if a new row needs to be added
            4. Add card to list
            5. Add new CardButton to layout
        """
        row, col = self.deck_cards[-1].coords
        if col == GRID_COLUMN_LIMIT:
            row += 1
            col = 0
        else:
            col += 1

        deck_card = Card(card.path, row, col)
        self.deck_cards.append(deck_card)
        deck_card_button = CardGridButton(deck_card)
        deck_card_button.clicked.connect(lambda r: self.sig_remove_card_from_deck(r, card))
        self.deck_scroll_area.card_grid_layout.addWidget(deck_card_button)

    def sig_remove_card_from_deck(self, result, card):
        print(f"Removing card {card.coords}: {result}")

    def sig_clear_area(self, result):
        deck_grid = self.deck_scroll_area.card_grid_layout
        while deck_grid.count():
            card = deck_grid.takeAt(0)
            card_widget = card.widget() if card and card.widget() else None
            if card_widget:
                deck_grid.removeWidget(card_widget)
                card_widget.deleteLater()

    def get_test_cards(self, number_of_cards):
        cards = []

        grid_row = 0
        grid_col = 0
        for i in range(number_of_cards):
            card = Card(self.don.path, grid_row, grid_col)
            cards.append(card)
            grid_col += 1
            if grid_col == GRID_COLUMN_LIMIT:
                grid_row += 1
                grid_col = 0

        return cards

