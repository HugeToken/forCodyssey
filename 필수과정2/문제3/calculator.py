from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QLabel
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

        self.history_label = QLabel('')
        self.history_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.history_label.setStyleSheet('padding: 2px; color: gray;')
        self.history_label.setFixedHeight(30)
        main_layout.addWidget(self.history_label)

        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setStyleSheet('padding: 12px 10px; font-size: 30px;')
        self.display.setFixedHeight(65)
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
        self.adjust_font_size()

    def handle_input(self):
        sender = self.sender()
        value = sender.text()
        current = self.display.text().replace(',', '')

        if value in '0123456789':
            if self.waiting_for_operand2:
                current = ''
                self.waiting_for_operand2 = False
            if current == '0':
                current = value
            else:
                current += value
            self.display.setText(self.format_number(current))

        elif value == '.':
            if '.' not in current:
                current += '.'
                self.display.setText(current)

        elif value in '+-x÷':
            self.operand1 = current
            self.operator = value
            self.history_label.setText(f'{self.format_number(current)} {value}')
            self.waiting_for_operand2 = True

        elif value == '=':
            if self.operator and self.operand1:
                expr = self.operand1.replace(',', '')
                expr += {'+': '+', '-': '-', 'x': '*', '÷': '/'}[self.operator]
                expr += current.replace(',', '')
                try:
                    result = round(eval(expr), 6)
                    self.display.setText(self.format_number(str(result)))
                    self.history_label.setText('')
                    self.operand1 = ''
                    self.operator = ''
                except:
                    self.display.setText('Error')

        elif value == 'AC':
            self.reset()

        elif value == '+/-':
            self.negative_positive()

        elif value == '%':
            self.percent()

        self.adjust_font_size()

    def reset(self):
        self.display.setText('0')
        self.history_label.setText('')
        self.operand1 = ''
        self.operator = ''
        self.waiting_for_operand2 = False

    def negative_positive(self):
        current = self.display.text().replace(',', '')
        if current.startswith('-'):
            current = current[1:]
        else:
            current = '-' + current
        self.display.setText(self.format_number(current))

    def percent(self):
        current = self.display.text().replace(',', '')
        try:
            result = float(current) / 100
            self.display.setText(self.format_number(str(result)))
        except:
            self.display.setText('Error')

    def format_number(self, num_str):
        try:
            num = float(num_str)
            if num.is_integer():
                return '{:,}'.format(int(num))
            else:
                return '{:,}'.format(round(num, 6))
        except:
            return num_str

    def adjust_font_size(self):
        text_length = len(self.display.text())
        if text_length <= 9:
            size = 30
        elif text_length <= 12:
            size = 24
        else:
            size = 18
        self.display.setStyleSheet(f'padding: 12px 10px; font-size: {size}px;')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec())
