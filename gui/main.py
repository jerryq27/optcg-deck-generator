import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("OPTCG Deck Builder")
        button = QPushButton("Press me!")

        self.setCentralWidget(button)

