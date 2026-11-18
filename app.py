import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QGridLayout, QVBoxLayout
)

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
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
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('=', 3, 2), ('+', 3, 3),
            ('C', 4, 0)
        ]

       
        for text, row, col in buttons:
            btn = QPushButton(text)
            btn.setStyleSheet(
                "font-size: 18px; font-weight: bold; background-color: #3c3f41; "
                "color: white; border-radius: 5px; padding: 15px;"
            )
            
            if text == 'C':
                grid_layout.addWidget(btn, row, col, 1, 4)
            else:
                grid_layout.addWidget(btn, row, col)

            
            btn.clicked.connect(self.on_button_click)

        v_layout.addLayout(grid_layout)
        self.setLayout(v_layout)

    def on_button_click(self):
        
        clicked_button = self.sender()
        text = clicked_button.text()
        current_text = self.display.text()

        if text == 'C':
            
            self.display.clear()
        elif text == '=':
            try:
                
                result = str(eval(current_text))
                self.display.setText(result)
            except Exception:
                self.display.setText("Помилка")
        else:
            
            self.display.setText(current_text + text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
