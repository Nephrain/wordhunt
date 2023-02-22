import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt6 import QtCore
import random


class WordSearch(QWidget):
    def __init__(self):
        super().__init__()

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

        self.grid = [
            [
                random.choice([k for k in letters for x in range(letters[k])])
                for _ in range(4)
            ]
            for _ in range(4)
        ]
        self.words = self.load_words()
        self.word_set = set(self.words)

        self.label_grid = QLabel()
        self.label_grid.setMinimumSize(
            100, 100
        )  # Set a minimum size to ensure the label is visible
        self.label_grid.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )  # Center the text in the label

        self.label_results = QLabel()
        self.label_results.setMinimumSize(
            100, 100
        )  # Set a minimum size to ensure the label is visible
        self.label_results.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )  # Center the text in the label

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Word Search"))
        self.layout.addWidget(self.label_grid)
        self.layout.addWidget(QLabel("Results"))
        self.layout.addWidget(self.label_results)

        self.setLayout(self.layout)

    def load_words(self):
        with open("Collins Scrabble Words (2019).txt") as f:
            words = f.read().splitlines()
        print(f"Loaded {len(words)} words from file")
        return words

    def get_grid_hash(self):
        return hash(str(self.grid))

    def get_words(self):
        words = set()

        def dfs(row, col, visited, word):
            if len(word) > 2 and word in self.word_set:
                words.add(word)

            for r, c in [
                (row + 1, col),
                (row - 1, col),
                (row, col + 1),
                (row, col - 1),
                (row + 1, col + 1),
                (row + 1, col - 1),
                (row - 1, col + 1),
                (row - 1, col - 1),
            ]:
                if r >= 0 and r < 4 and c >= 0 and c < 4 and (r, c) not in visited:
                    dfs(r, c, visited | {(r, c)}, word + self.grid[r][c])

        for row in range(4):
            for col in range(4):
                dfs(row, col, {(row, col)}, self.grid[row][col])

        print(f"Found {len(words)} words: {words}")
        return words

    def search(self):
        grid_hash = self.get_grid_hash()
        if not hasattr(self, "last_grid_hash") or self.last_grid_hash != grid_hash:
            found_words = sorted(self.get_words())
            self.found_words = found_words
            self.last_grid_hash = grid_hash
        else:
            found_words = self.found_words

        grid_text = "\n".join([" ".join(row) for row in self.grid])
        results_text = "\n".join(found_words)

        self.label_grid.setText(grid_text)
        self.label_results.setText(results_text)

    def showEvent(self, event):
        super().showEvent(event)
        self.search()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    word_search = WordSearch()
    word_search.show()
    sys.exit(app.exec())
