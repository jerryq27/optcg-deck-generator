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
from .Widgets import (
    CardButton,
    TestBox,
)
from pathlib import Path


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("OPTCG Deck Builder")
        self.setFixedSize(QSize(1080, 720))

        main_layout = QHBoxLayout()
        main_layout.addLayout(self.create_left_side_layout())
        main_layout.addLayout(self.create_right_side_layout())

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)


    def create_left_side_layout(self):
        left_side_layout = QVBoxLayout()

        card_set_label = QLabel("Card Set")
        card_set_scroll_area = QScrollArea()

        deck_label = QLabel("Deck")
        deck_scroll_area = QScrollArea()

        left_side_layout.addWidget(card_set_label)
        left_side_layout.addWidget(card_set_scroll_area)
        left_side_layout.addWidget(deck_label)
        left_side_layout.addWidget(deck_scroll_area)

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

        base_path = Path().parent
        leader_path = base_path / "[ST-01]" / "ST01-001.png"
        don_path = base_path / "res" / "don-cards" / "1.png"
        card_back_path = base_path / "[ST-01]" / "ST01-003.png"

        cbtn_leader = CardButton("Select Leader", leader_path)
        cbtn_don = CardButton("Select DON", don_path)
        cbtn_card_back = CardButton("Select Card Back", card_back_path)

        card_buttons_layout.addWidget(cbtn_leader)
        card_buttons_layout.addWidget(cbtn_don)
        card_buttons_layout.addWidget(cbtn_card_back)

        btn_clear_deck = QPushButton("Clear Deck")
        btn_gen_deck_img = QPushButton("Generate Deck Image")
        button_layout.addWidget(btn_clear_deck)
        button_layout.addWidget(btn_gen_deck_img)

        right_side_layout.addWidget(cb_card_set, 0,0)
        right_side_layout.addLayout(card_buttons_layout, 1,0)
        right_side_layout.addWidget(TestBox(), 2,0)
        right_side_layout.addLayout(button_layout, 3,0)
        return right_side_layout

