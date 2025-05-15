from PyQt6.QtWidgets import QFrame, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import (
    QIcon,
    QPalette,
    QPixmap,
)


class CardButton(QPushButton):

    # Scaled sizes to maintain aspect ratio
    IMAGE_BUTTON_WIDTH = 69
    IMAGE_BUTTON_HEIGHT = 97

    def __init__(self, label, image_path):
        super().__init__(f"\n{label}")

        image_pixmap = QPixmap(str(image_path))
        if image_pixmap.isNull():
            print(f"Error loading the image: {image_path}, {image_path.exists()}")

        scaled_image_pixmap = image_pixmap.scaled(
            CardButton.IMAGE_BUTTON_WIDTH,
            CardButton.IMAGE_BUTTON_HEIGHT,
            aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio
        )
        icon_image = QIcon(scaled_image_pixmap)

        self.setIcon(icon_image)
        self.setIconSize(scaled_image_pixmap.size())


class Card(QFrame):

    def __init__(self):
        super().__init__()


class TestBox(QFrame):

    def __init__(self):
        super().__init__()

        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(1)

