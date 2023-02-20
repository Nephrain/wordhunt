import sys, string, random
from os.path import exists
from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QMainWindow,
    QApplication,
)
from PyQt6.QtCore import QSize, Qt, QPoint, QMargins, QEvent
from PyQt6.QtGui import QFont, QCursor, QPainter


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):

        self.setWindowTitle("Word Hunt")
        self.setMinimumSize(0, 0)

        self.window = QWidget()
        self.layout = QHBoxLayout()
        self.setCentralWidget(self.window)
        self.window.setLayout(self.layout)

        self.createBoard()
        self.createSidebar()

        self.show()

    def eventFilter(self, object, event):
        widget = app.widgetAt(QCursor.pos())
        if (
            event.type() == QEvent.Type.MouseMove
            and isinstance(widget, QLabel)
            and not widget.property("visited")
            and widget.property("letter")
        ):
            self.header.setText(self.header.text() + widget.text())
            widget.setProperty("visited", True)
            widget.setStyleSheet(
                widget.styleSheet() + "QLabel { background-color : lightgreen; }"
            )
        elif event.type() == QEvent.Type.MouseButtonRelease:
            self.header.setText("")
            for widget in self.words.children():
                if isinstance(widget, QLabel):
                    widget.setProperty("visited", False)
                    widget.setStyleSheet(
                        widget.styleSheet() + "QLabel { background-color : white; }"
                    )
        return True

    def createSidebar(self):
        a = QLabel()
        a.setText("sidebar")
        a.setMinimumSize(QSize(150, 10))
        a.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("QLabel { background-color : gray; }")
        self.layout.addWidget(a)

    def createBoard(self):
        letters = {
            "A": 43,
            "B": 11,
            "C": 23,
            "D": 17,
            "E": 57,
            "F": 9,
            "G": 13,
            "H": 15,
            "I": 38,
            "J": 1,
            "K": 6,
            "L": 28,
            "M": 15,
            "N": 34,
            "O": 37,
            "P": 16,
            "Q": 1,
            "R": 39,
            "S": 29,
            "T": 36,
            "U": 19,
            "V": 5,
            "W": 7,
            "X": 1,
            "Y": 9,
            "Z": 1,
        }

        self.words = QWidget()
        self.grid = QGridLayout()
        self.grid.setContentsMargins(QMargins(30, 30, 30, 30))
        self.grid.setHorizontalSpacing(4)
        self.grid.setVerticalSpacing(4)

        for row in range(4):
            for col in range(4):
                label = QLabel(
                    random.choice([k for k in letters for x in range(letters[k])]), self
                )
                label.setMinimumSize(QSize(120, 120))
                label.setMaximumSize(QSize(120, 120))
                label.setScaledContents(True)
                label.setProperty("visited", False)
                label.setProperty("letter", True)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.installEventFilter(self)

                self.grid.addWidget(label, row, col)

        self.word = ""

        main = QWidget()
        self.words.setStyleSheet(
            """QLabel { 
                        background-color : white; 
                        color : black; 
                        border-radius: 20px; 
                        font-size: 40px;
                        margin: 5px 5px 5px 5px
                        }"""
        )
        self.words.setLayout(self.grid)
        vbox = QVBoxLayout()

        self.header = QLabel()
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("QLabel { background-color : gray; }")
        vbox.addWidget(self.header)
        vbox.addWidget(self.words)

        main.setLayout(vbox)

        self.layout.addWidget(main)


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    app.exec()
