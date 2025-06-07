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


# Scaled sizes to maintain aspect ratio
IMAGE_BUTTON_WIDTH = 69
IMAGE_BUTTON_HEIGHT = 97

class CardButton(QPushButton):

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


class Card(QFrame):

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


class CardGridArea(QScrollArea):

    def __init__(self, cards):
        super().__init__()
        card_set = QWidget()
        card_set_layout = QGridLayout()
        card_set.setLayout(card_set_layout)

        COLUMN_LIMIT = 5
        grid_row = 0
        grid_col = 0
        for i in range(len(cards)):
            card_set_layout.addWidget(cards[i], grid_row, grid_col)
            grid_col += 1
            if grid_col == COLUMN_LIMIT:
                grid_row += 1
                grid_col = 0

        self.setWidget(card_set)


class TestBox(QFrame):

    def __init__(self):
        super().__init__()

        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(1)

