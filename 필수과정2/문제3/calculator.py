from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QLabel
from PyQt6.QtCore import Qt

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
        self.display.setStyleSheet('padding: 12px 10px;')
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
                    self.operator = value
                    self.display.setText(self.add_thousands_separator(self.operand1) + value)
                    self.operator = value
            return

        if self.waiting_for_operand2:
            self.waiting_for_operand2 = False
            self.display.setText(self.add_thousands_separator(self.operand1) + self.operator + value)
        else:
            if self.display.text().replace(',', '').rstrip('+-x÷') == '0' and value != '.':
                self.display.setText(value)
            else:
                text = self.display.text().replace(',', '') + value
                self.display.setText(self.add_thousands_separator(text))

        self.adjust_font_size()

    def reset(self):
        self.display.setText('0')
        self.history_label.setText('')
        self.operand1 = ''
        self.operator = ''
        self.waiting_for_operand2 = False
        self.adjust_font_size()

    def negative_positive(self):
        current = self.display.text().replace(',', '')
        if current != '0':
            if current.startswith('-'):
                self.display.setText(self.add_thousands_separator(current[1:]))
            else:
                self.display.setText(self.add_thousands_separator('-' + current))
        self.adjust_font_size()

    def percent(self):
        current = self.display.text().replace(',', '').rstrip('+-x÷')
        try:
            value = float(current)
            value = value / 100
            self.display.setText(self.add_thousands_separator(self.format_result(value)))
        except ValueError:
            self.display.setText('Error')
        self.adjust_font_size()

    def equal(self):
        if not self.operator or self.waiting_for_operand2:
            return

        full_expr = self.display.text().replace(',', '')
        try:
            parts = full_expr.split(self.operator)
            if len(parts) < 2:
                return
            num1 = float(parts[0])
            num2 = float(parts[1])
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

            formatted_result = self.format_result(result)
            expr_display = f'{self.add_thousands_separator(parts[0])}{self.operator}{self.add_thousands_separator(parts[1])}={self.add_thousands_separator(formatted_result)}'
            self.history_label.setText(expr_display)
            self.display.setText(self.add_thousands_separator(formatted_result))
            self.operand1 = ''
            self.operator = ''
            self.waiting_for_operand2 = False
        except:
            self.display.setText('Error')

        self.adjust_font_size()
        self.adjust_history_font_size()

    def format_result(self, result):
        if result == int(result):
            return str(int(result))
        else:
            return f'{result:.6f}'.rstrip('0').rstrip('.')

    def add_thousands_separator(self, text):
        try:
            if text[-1] in ['+', '-', 'x', '÷']:
                operator = text[-1]
                text = text[:-1]
                return self.add_thousands_separator(text) + operator

            for op in ['+', '-', 'x', '÷']:
                if op in text:
                    parts = text.split(op)
                    if len(parts) == 2:
                        left = self.add_thousands_separator(parts[0])
                        right = self.add_thousands_separator(parts[1])
                        return left + op + right

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

    def adjust_font_size(self):
        length = len(self.display.text())
        if length < 10:
            size = 30
        elif length < 15:
            size = 24
        elif length < 20:
            size = 18
        else:
            size = 14
        self.display.setStyleSheet(f'padding: 10px; font-size: {size}px;')

    def adjust_history_font_size(self):
        length = len(self.history_label.text())
        if length < 20:
            size = 16
        elif length < 30:
            size = 12
        else:
            size = 10
        self.history_label.setStyleSheet(f'padding: 2px; color: gray; font-size: {size}px;')
    
if __name__ == '__main__':
    app = QApplication([])
    window = Calculator()
    window.show()
    sys.exit(app.exec())
