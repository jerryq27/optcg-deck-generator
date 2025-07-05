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

# Main should handle all signal and slots between widgets!
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("OPTCG Deck Builder")
        self.setFixedSize(QSize(1080, 720))

        """ Objects"""
        base_path = Path().parent
        self.leader = Card(base_path / "[ST-01]" / "ST01-001.png")
        self.don = Card(base_path / "res" / "don-cards" / "1.png")
        self.card_back = Card(base_path / "[ST-01]" / "ST01-003.png")

        """ Widgets """
        card_set_cards = self.get_test_cards(54, method="add")
        self.card_set_scroll_area = CardGridArea(card_set_cards)

        deck_cards = self.get_test_cards(12, method="remove")
        self.deck_scroll_area = CardGridArea(deck_cards)

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
        deck_label = QLabel("Deck")

        left_side_layout.addWidget(card_set_label)
        left_side_layout.addWidget(self.card_set_scroll_area)
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


    def sig_add_card_to_deck(self, card):
        print(f"Adding card {card.coords}")

    def sig_remove_card_from_deck(self, card):
        print(f"Removing card {card.coords}")

    def sig_clear_area(self):
        deck_grid = self.deck_scroll_area.card_grid_layout
        while deck_grid.count():
            card = deck_grid.takeAt(0)
            card_widget = card.widget() if card and card.widget() else None
            if card_widget:
                deck_grid.removeWidget(card_widget)
                card_widget.deleteLater()

    def get_test_cards(self, number_of_cards, method):
        cards = []

        COLUMN_LIMIT = 5
        grid_row = 0
        grid_col = 0
        for i in range(number_of_cards):
            card = Card(self.don.path, grid_row, grid_col)
            card_button = CardGridButton(card)
            if method == "add":
                card_button.clicked.connect(self.sig_add_card_to_deck)
            else:
                card_button.clicked.connect(self.sig_remove_card_from_deck)
            cards.append(card_button)
            grid_col += 1
            if grid_col == COLUMN_LIMIT:
                grid_row += 1
                grid_col = 0

        return cards

