from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt6.QtCore import Qt
import sys

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('iPhone 스타일 계산기')
        self.setFixedSize(300, 400)
        self.create_ui()
        self.operand1 = ''
        self.operator = ''
        self.waiting_for_operand2 = False

    def create_ui(self):
        main_layout = QVBoxLayout()

        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setStyleSheet('font-size: 30px; padding: 10px;')
        main_layout.addWidget(self.display)

        buttons = [
            ['AC', '+/-', '%', '÷'],
            ['7', '8', '9', 'x'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '0', '.', '=']
        ]

        grid = QGridLayout()
        for row, line in enumerate(buttons):
            for col, btn_text in enumerate(line):
                if btn_text == '0' and col == 0 and row == 4:
                    button = QPushButton(btn_text)
                    button.setFixedHeight(60)
                    button.setStyleSheet('font-size: 20px;')
                    grid.addWidget(button, row, col, 1, 2)
                    button.clicked.connect(self.handle_input)
                    continue
                elif btn_text == '0' and col == 1 and row == 4:
                    continue
                else:
                    button = QPushButton(btn_text)
                    button.setFixedHeight(60)
                    button.setStyleSheet('font-size: 20px;')
                    grid.addWidget(button, row, col)
                    button.clicked.connect(self.handle_input)

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    def handle_input(self):
        sender = self.sender()
        value = sender.text()
        current = self.display.text().replace(',', '')

        if current == 'Error':
            self.reset()

        if value in ['AC', '+/-', '%', '=']:
            if value == 'AC':
                self.reset()
            elif value == '+/-':
                self.negative_positive()
            elif value == '%':
                self.percent()
            elif value == '=':
                self.equal()
            return

        if value in ['+', '-', 'x', '÷']:
            if not self.operator:
                self.operand1 = current
                self.operator = value
                self.waiting_for_operand2 = True
                self.display.setText(self.add_thousands_separator(current) + value)
            else:
                if self.waiting_for_operand2:
                    self.display.setText(self.add_thousands_separator(self.operand1) + value)
                    self.operator = value
            return

        if self.waiting_for_operand2:
            self.display.setText('' if value != '.' else '0.')
            self.waiting_for_operand2 = False

        if self.display.text().replace(',', '').rstrip('+-x÷') == '0' and value != '.':
            self.display.setText(self.add_thousands_separator(value))
        else:
            text = self.display.text().replace(',', '') + value
            self.display.setText(self.add_thousands_separator(text))

    def reset(self):
        self.display.setText('0')
        self.operand1 = ''
        self.operator = ''
        self.waiting_for_operand2 = False

    def negative_positive(self):
        current = self.display.text().replace(',', '')
        if current != '0':
            if current.startswith('-'):
                self.display.setText(self.add_thousands_separator(current[1:]))
            else:
                self.display.setText(self.add_thousands_separator('-' + current))

    def percent(self):
        current = self.display.text().replace(',', '').rstrip('+-x÷')
        try:
            value = float(current)
            value = value / 100
            self.display.setText(self.add_thousands_separator(str(value)))
        except ValueError:
            self.display.setText('Error')

    def equal(self):
        if not self.operator or self.waiting_for_operand2:
            return

        operand2 = self.display.text().replace(',', '').split(self.operator)[-1]
        try:
            num1 = float(self.operand1)
            num2 = float(operand2)
            result = 0

            if self.operator == '+':
                result = num1 + num2
            elif self.operator == '-':
                result = num1 - num2
            elif self.operator == 'x':
                result = num1 * num2
            elif self.operator == '÷':
                if num2 == 0:
                    raise ZeroDivisionError
                result = num1 / num2

            self.display.setText(self.add_thousands_separator(str(result)))
            self.operand1 = ''
            self.operator = ''
            self.waiting_for_operand2 = False
        except:
            self.display.setText('Error')

    def add_thousands_separator(self, text):
        try:
            if text[-1] in ['+', '-', 'x', '÷']:
                operator = text[-1]
                text = text[:-1]
                return self.add_thousands_separator(text) + operator

            if '.' in text:
                integer_part, decimal_part = text.split('.')
                integer_part = integer_part.replace(',', '')
                integer_part = f"{int(integer_part):,}"
                return f"{integer_part}.{decimal_part}"
            else:
                text = text.replace(',', '')
                return f"{int(text):,}"
        except:
            return text

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec())
