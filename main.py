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
    QTableWidget,
    QTableWidgetItem,
    QTableView,
    QListWidget,
    QListWidgetItem,
)
from PyQt6.QtCore import QSize, Qt, QPoint, QMargins, QEvent, QAbstractTableModel
from PyQt6.QtGui import QFont, QCursor, QPainter

"""
TO-DO LIST
1. Fix found word list to prevent duplicates
    - make it so words actually show up
2. Make it so you can't skip around letters
    - Probably make an attribute for most recent letter and each new letter check all surrounding letters for it
3. Add points and a total point counter
4. Decrease hitboxes for letters for seamless diagonal navigation
5. Draw lines showing path
6. Calculate point totals of maps (and maybe veto bad ones)


"""


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

        self.sanitizeDict()
        self.createBoard()
        self.createSidebar()

        self.show()

    def eventFilter(self, object, event):
        widget = app.widgetAt(QCursor.pos())
        if (
            (
                event.type() == QEvent.Type.MouseMove
                or event.type() == QEvent.Type.MouseButtonPress
            )
            and isinstance(widget, QLabel)
            and not widget.property("visited")
            and widget.property("letter")
        ):
            local = widget.mapFromGlobal(QCursor.pos())
            if event.type() == QEvent.Type.MouseButtonPress or (
                abs(widget.rect().center().x() - local.x()) < 40
                and abs(widget.rect().center().y() - local.y()) < 40
            ):
                self.select(widget)
        elif event.type() == QEvent.Type.MouseButtonRelease:
            self.deselect()
        return False

    def select(self, widget):
        self.header.setText(self.header.text() + widget.text())
        widget.setProperty("visited", True)
        widget.setStyleSheet(
            widget.styleSheet() + "QLabel { background-color : lightgreen; }"
        )

    def deselect(self):
        word = self.header.text().strip().upper()
        if word in self.lines:
            self.table.setItem(self.table.rowCount() - 1, 0, QTableWidgetItem(word))
            item = QTableWidgetItem()
            item.setData(Qt.ItemDataRole.DisplayRole, (len(word) - 2) * 400)
            self.table.setItem(
                self.table.rowCount() - 1,
                1,
                item,
            )
            self.table.insertRow(self.table.rowCount())
        self.table.sortItems(1, Qt.SortOrder.DescendingOrder)

        self.header.setText("")
        for widget in self.words.children():
            if isinstance(widget, QLabel):
                widget.setProperty("visited", False)
                widget.setStyleSheet(
                    widget.styleSheet() + "QLabel { background-color : white; }"
                )

    def sanitizeDict(self):
        with open("Collins Scrabble Words (2019).txt") as f:
            self.lines = []
            for word in f.readlines():
                if len(word) > 3 and len(word) < 16:
                    self.lines.append(word.strip().upper())

    def createSidebar(self):
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setRowCount(2)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setItem(0, 0, QTableWidgetItem("Words"))
        self.table.setItem(0, 1, QTableWidgetItem("Points"))
        self.layout.addWidget(self.table)
        self.layout.addStretch()

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
