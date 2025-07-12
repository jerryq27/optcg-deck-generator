from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import (
    QIcon,
    QPalette,
    QPixmap,
)

"""
Widgets:
    CardFrame - Basic QFrame that displays a card and no interactive signals
    CardDropDown - Drop Down to select a card (Leader, DON, CardBack)
    CardGridArea - Scroll area with a grid layout for a list of cards
    CardGridButton - Card button component to use in a grid layout
    Test - Basic frame with border
"""

# Scaled sizes to maintain aspect ratio
IMAGE_BUTTON_WIDTH = 69
IMAGE_BUTTON_HEIGHT = 97
IMAGE_BUTTON_PADDING = 16


class CardFrame(QFrame):

    def __init__(self, image_path):
        super().__init__()

        self.layout = QVBoxLayout(self)
        image = QLabel()
        image_pixmap = QPixmap(str(image_path))
        if image_pixmap.isNull():
            image.setText("Error loading image.")
            print(f"Error loading the image: {image_path}, {image_path.exists()}")

        image_pixmap = image_pixmap.scaled(
            IMAGE_BUTTON_WIDTH,
            IMAGE_BUTTON_HEIGHT,
            aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio
        )
        image.setPixmap(image_pixmap)
        # image.setScaledContents(True)

        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(1)
        self.layout.addWidget(image)


class CardDropDown(QPushButton):

    def __init__(self, label, image_path):
        super().__init__(f"\n{label}")

        image_pixmap = QPixmap(str(image_path))
        if image_pixmap.isNull():
            print(f"Error loading the image: {image_path}, {image_path.exists()}")

        scaled_image_pixmap = image_pixmap.scaled(
            IMAGE_BUTTON_WIDTH,
            IMAGE_BUTTON_HEIGHT,
            aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio
        )
        icon_image = QIcon(scaled_image_pixmap)

        self.setIcon(icon_image)
        self.setIconSize(scaled_image_pixmap.size())


class CardGridArea(QScrollArea):

    def __init__(self, cards=[]):
        super().__init__()
        self.cards = cards
        self.card_buttons = []
        self.card_grid = QWidget()
        self.card_grid_layout = QGridLayout()

        self.card_grid.setLayout(self.card_grid_layout)

        for card in self.cards:
            card_button = CardGridButton(card)
            self.card_grid_layout.addWidget(card_button, card.row, card.col)
            self.card_buttons.append(card_button)

        self.setWidgetResizable(True)
        self.setWidget(self.card_grid)


class CardGridButton(QPushButton):

    def __init__(self, card):
        super().__init__()
        self.card = card
        self.row, self.col = card.coords

        image_pixmap = QPixmap(str(card.path))
        if image_pixmap.isNull():
            print(f"Error loading the image: {image_path}, {image_path.exists()}")

        scaled_image_pixmap = image_pixmap.scaled(
            IMAGE_BUTTON_WIDTH,
            IMAGE_BUTTON_HEIGHT,
            aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio
        )
        icon_image = QIcon(scaled_image_pixmap)

        self.setIcon(icon_image)
        self.setIconSize(scaled_image_pixmap.size())
        self.setFixedSize(
            IMAGE_BUTTON_WIDTH + IMAGE_BUTTON_PADDING,
            IMAGE_BUTTON_HEIGHT + IMAGE_BUTTON_PADDING
        )
        self.setCheckable(True)
        self.clicked.connect(self.action_click)

    def action_click(self):
        if self.isChecked():
            self.setStyleSheet(
                "QPushButton {"
                "  background-color: lightblue;"
                "}"
            )
            print(f"Selected card at ({self.row}, {self.col})")
        else:
            self.setStyleSheet(
                "QPushButton {"
                "  background-color: none;"
                "}"
            )
            print(f"Deselected card at ({self.row}, {self.col})")


class TestBox(QFrame):

    def __init__(self):
        super().__init__()

        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(1)

