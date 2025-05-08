from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QLabel
from PyQt6.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('iPhone 스타일 계산기')
        self.setFixedSize(300, 400)
        self.create_ui()
        self.reset()

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

        if self.display.text() == 'Error':
            self.reset()

        if value == 'AC':
            self.reset()
        elif value in '0123456789.':
            if self.new_input:
                self.expression = self.expression if self.last_result else ''
                self.new_input = False

            if value == '.':
                if not self.expression:
                    self.expression = '0.'
                    self.display.setText(self.format_expression(self.expression))
                    return
                last_num = self.get_last_number()
                if '.' in last_num:
                    return
                self.expression += '.'
                self.display.setText(self.format_expression(self.expression))
                return

            self.expression += value
            self.display.setText(self.expression)

        elif value in '+-x÷':
            if not self.expression:
                return
            if self.expression[-1] in '+-x÷':
                self.expression = self.expression[:-1] + value
            else:
                self.expression += value

            self.display.setText(self.expression)
            self.new_input = False

        elif value == '=':
            if not self.expression or self.expression[-1] in '+-x÷.':
                return
            self.evaluate_expression()

        elif value == '+/-':
            self.negative_positive()

        elif value == '%':
            self.apply_percent()

        self.adjust_font_size()

    def add(self, a, b):
        return a + b
    def subtract(self, a, b):   
        return  a - b
    def multiply(self, a, b):
        return  a * b
    def divide(self, a, b):
        return a / b if b != 0 else 'Error'
    
    def evaluate_expression(self):
        try:
            expr = self.expression.replace(',', '').replace('x', '*').replace('÷', '/')
            result = round(eval(expr), 6)
            result_str = self.format_number(str(result))
            self.history_label.setText(self.format_expression(self.expression) + '=' + result_str)
            self.display.setText(result_str)
            self.expression = str(result)
            self.last_result = True
            self.new_input = True
        except:
            self.display.setText('Error')
            self.expression = ''

    def negative_positive(self):
        if not self.expression:
            return
        if self.expression.startswith('-'):
            self.expression = self.expression[1:]
        else:
            self.expression = '-' + self.expression
        self.display.setText(self.format_expression(self.expression))

    def apply_percent(self):
        if not self.expression:
            return
        last = self.get_last_number()
        try:
            new_last = str(float(last) / 100)
            self.expression = self.expression[:-len(last)] + new_last
            self.display.setText(self.format_expression(self.expression))
        except:
            self.display.setText('Error')
            self.expression = ''

    def reset(self):
        self.expression = ''
        self.new_input = False
        self.last_result = False
        self.display.setText('0')
        self.history_label.setText('')

    def get_last_number(self):
        tokens = ''
        for c in reversed(self.expression):
            if c in '+-x÷':
                break
            tokens = c + tokens
        return tokens

    def format_expression(self, expr):
        result = ''
        temp = ''
        for c in expr:
            if c in '+-x÷':
                if temp:
                    result += self.format_number(temp)
                    temp = ''
                result += c
            else:
                temp += c
        if temp:
            if temp == '.':
                result += '0.'
            elif temp[-1] == '.' and temp.count('.') == 1:
                result += self.format_number(temp[:-1]) + '.'
            else:
                result += self.format_number(temp)
        return result

    def format_number(self, num_str):
        try:
            if '.' in num_str:
                num = float(num_str)
                int_part, dec_part = str(num).split('.')
                dec_part = dec_part[:6]
                formatted = '{:,}'.format(int(int_part))
                
                return formatted + ('.' + dec_part if dec_part else '')
            else:
                return '{:,}'.format(int(num_str))
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
    app = QApplication([])
    window = Calculator()
    window.show()
    app.exec()
