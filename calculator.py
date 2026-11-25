import json
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QGridLayout,
    QLineEdit,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

HISTORY_FILE = "history.json"


def load_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []


def save_history(records):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


class HistoryWindow(QDialog):
    def __init__(self, records, parent=None):
        super().__init__(parent)
        self.records = records
        self.selected_value = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Історія обчислень")
        self.resize(260, 320)
        self.setStyleSheet("background-color: #2b2b2b; color: white;")

        v_layout = QVBoxLayout()

        self.history_list = QListWidget()
        self.history_list.setStyleSheet(
            "background-color: #1e1e1e; color: white; font-size: 14px; padding: 6px;"
        )

        for item in reversed(self.records):
            expr = item.get("expression", "")
            res = item.get("result", "")
            self.history_list.addItem(f"{expr} = {res}")

        self.history_list.itemClicked.connect(self.on_item_clicked)
        v_layout.addWidget(self.history_list)
        self.setLayout(v_layout)

    def on_item_clicked(self, item):
        text = item.text()
        if " = " in text:
            self.selected_value = text.split(" = ", 1)[1].strip()
        else:
            self.selected_value = text.strip()
        self.accept()


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.history = load_history()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Калькулятор")
        self.resize(300, 400)
        self.setStyleSheet("background-color: #2b2b2b;")

        v_layout = QVBoxLayout()

        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setStyleSheet(
            "font-size: 28px; font-weight: bold; background-color: #1e1e1e; "
            "color: white; border: 2px solid #444; border-radius: 5px; padding: 10px;"
        )
        v_layout.addWidget(self.display)

        grid_layout = QGridLayout()

        buttons = [
            ("7", 0, 0), ("8", 0, 1), ("9", 0, 2), ("/", 0, 3),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2), ("*", 1, 3),
            ("1", 2, 0), ("2", 2, 1), ("3", 2, 2), ("-", 2, 3),
            ("0", 3, 0), (".", 3, 1), ("=", 3, 2), ("+", 3, 3),
            ("C", 4, 0), ("H", 4, 1),
        ]

        for text, row, col in buttons:
            btn = QPushButton(text)
            btn.setStyleSheet(
                "font-size: 18px; font-weight: bold; background-color: #3c3f41; "
                "color: white; border-radius: 5px; padding: 15px;"
            )
            grid_layout.addWidget(btn, row, col)
            btn.clicked.connect(self.on_button_click)

        v_layout.addLayout(grid_layout)
        self.setLayout(v_layout)

    def open_history(self):
        dialog = HistoryWindow(self.history, self)
        if dialog.exec_() == QDialog.Accepted and dialog.selected_value is not None:
            current_text = self.display.text()
            if current_text == "Помилка":
                current_text = ""
            self.display.setText(current_text + dialog.selected_value)

    def on_button_click(self):
        clicked_button = self.sender()
        if not clicked_button:
            return

        text = clicked_button.text()
        current_text = self.display.text()

        if text == "H":
            self.open_history()
        elif text == "C":
            self.display.clear()
        elif text == "=":
            try:
                result = str(eval(current_text))
                self.display.setText(result)
                self.history.append({"expression": current_text, "result": result})
                save_history(self.history)
            except Exception:
                self.display.setText("Помилка")
        else:
            if current_text == "Помилка":
                current_text = ""
            self.display.setText(current_text + text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())