# Copyright (C) 2015  aws

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.

# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
import math
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QPushButton, QLineEdit, QSizePolicy


class MyButton(QPushButton):

    def __init__(self, text, connect, parent=None):
        super().__init__(text, parent)
        self.clicked.connect(connect)
        self.setFixedSize(40,35)

class Main(QWidget):

    def __init__(self):
        super().__init__()

        self.currentDigit = []
        self.currentDigitInt = 0
        self.stepDigit = 0
        self.operation = ''
        self.setWindowIcon(QIcon('icon.png'))
        grid = QGridLayout(self)
        self.display = QLineEdit('0')
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setMaxLength(13)
        font = QFont('', 22, QFont.Monospace)
        self.display.setFont(font)
        grid.addWidget(self.display, 0, 0, 1, 5)

        backSpaceBtn = MyButton('<-', self.backSpace)
        grid.addWidget(backSpaceBtn, 1, 0)
        clearBtn = MyButton('CE', self.clear)
        grid.addWidget(clearBtn, 1, 1)
        clearAllBtn = MyButton('C', self.clearAll)
        grid.addWidget(clearAllBtn, 1, 2)
        changeSignBtn = MyButton('+  -', self.changeSign)
        grid.addWidget(changeSignBtn, 1, 3)
        sqrtBtn = MyButton('sqrt', self.sqrt)
        grid.addWidget(sqrtBtn, 1, 4)

        digits = 10
        for i in range(1, digits):
            row = ((9 - i) / 3) + 2
            column = ((i - 1) % 3)
            grid.addWidget(MyButton(str(i), self.digitBtn), row, column)
        zero = MyButton('0', self.digitBtn)
        zero.setMaximumSize(100, 35)
        grid.addWidget(zero, 5, 0, 1, 2)

        divBtn = MyButton('/', self.division)
        grid.addWidget(divBtn, 2, 3)
        percentBtn = MyButton('1/x', self.reciproc)
        grid.addWidget(percentBtn, 2, 4)
        multipleBtn = MyButton('*', self.multiple)
        grid.addWidget(multipleBtn, 3, 3)
        powBtn = MyButton('x^2', self.pow)
        grid.addWidget(powBtn, 3, 4)
        subBtn = MyButton('-', self.sub_)
        grid.addWidget(subBtn, 4, 3)

        floatBtn = MyButton(',', self.setFloat)
        grid.addWidget(floatBtn, 5, 2, 1, 1)
        addBtn = MyButton('+', self.add_)
        grid.addWidget(addBtn, 5, 3, 1, 1)
        equalBtn = MyButton('=', self.equal)
        equalBtn.setMaximumSize(40, 100)
        equalBtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        grid.addWidget(equalBtn, 4, 4, 2, 1)

        self.setFixedSize(250, 280)
        self.show()

    def waitCurrentDigit(self):
        self.currentDigit.clear()
        self.currentDigitInt = 0
        return

    def digitBtn(self):
        #Вывод цифр на дисплей
        self.currentDigit.append(self.sender().text())
        self.currentDigitInt = float(''.join(self.currentDigit))
        if self.currentDigit[0] == '.':
            self.display.setText('0' + ''.join(self.currentDigit))
        else:
            self.display.setText(''.join(self.currentDigit))

    def backSpace(self):
        #Удаление последней цифры
        if self.currentDigit:
            self.currentDigit.pop()
            self.currentDigitInt = ''.join(self.currentDigit)
            self.display.setText(str(self.currentDigitInt))

        if not self.currentDigit:
            self.display.setText('0')

    def clear(self):
        #Очистить последнее действие
        self.waitCurrentDigit()
        self.display.setText('0')

    def clearAll(self):
        #Очищаем память калькулятора
        self.currentDigit.clear()
        self.currentDigitInt = 0
        self.stepDigit = 0
        self.display.setText('0')

    def changeSign(self):
        # Меняем знак на противоположный
        if float(self.currentDigitInt) > 0:
            digit = ''.join(self.currentDigit)
            self.currentDigitInt = -float(digit)
            self.currentDigit = list(str(self.currentDigitInt))
            self.display.setText(''.join(self.currentDigit))
        else:
            self.currentDigitInt = abs(float(''.join(self.currentDigit)))
            self.currentDigit = list(str(self.currentDigitInt))
            self.display.setText(str(self.currentDigitInt))

    def sqrt(self):
        #Корень квадратный
        if float(self.currentDigitInt) <= 0:
            self.waitCurrentDigit()
        else:
            digit = float(self.currentDigitInt)
            self.currentDigitInt = math.sqrt(digit)
            self.currentDigit = list(str(self.currentDigitInt))
            self.display.setText(str(self.currentDigitInt))

    def division(self):
        #Деление
        self.operation = '/'
        self.stepDigit = self.currentDigitInt
        self.waitCurrentDigit()

    def reciproc(self):
        #1/x
        try:
            self.currentDigitInt = 1 / float(self.currentDigitInt)
        except ZeroDivisionError:
            self.display.setText('Деление на 0!')
            self.waitCurrentDigit()
        else:
            self.currentDigit = list(str(self.currentDigitInt))
            self.display.setText(str(self.currentDigitInt))

    def multiple(self):
        #Умножение
        self.operation = '*'
        self.stepDigit = self.currentDigitInt
        self.waitCurrentDigit()

    def pow(self):
        self.currentDigitInt *= float(self.currentDigitInt)
        self.currentDigit = list(str(self.currentDigitInt))
        self.display.setText(str(self.currentDigitInt))

    def sub_(self):
        # Вычитание
        self.operation = '-'
        self.stepDigit = self.currentDigitInt
        self.waitCurrentDigit()

    def setFloat(self):
        #Число с плавающей точкой
        if '.' not in self.currentDigit:
            self.currentDigit.append('.')
            self.display.setText(str(self.currentDigitInt))

    def add_(self):
        # Сложение
        self.operation = '+'
        self.stepDigit = self.currentDigitInt
        self.waitCurrentDigit()

    def equal(self):
        # Равно
        if self.operation == '/':
            try:
                self.currentDigitInt = float(self.stepDigit) / self.currentDigitInt
            except ZeroDivisionError:
                self.display.setText('Деление на 0!')
                self.waitCurrentDigit()
                return
            else:
                self.display.setText(str(self.currentDigitInt))
                self.currentDigit.clear()
                self.currentDigit = list(str(self.currentDigitInt))

        if self.operation == '*':
            self.currentDigitInt *= float(self.stepDigit)
            self.display.setText(str(self.currentDigitInt))
            self.currentDigit.clear()
            self.currentDigit = list(str(self.currentDigitInt))

        if self.operation == '-':
            self.currentDigitInt = float(self.stepDigit) - self.currentDigitInt
            self.display.setText(str(self.currentDigitInt))
            self.currentDigit.clear()
            self.currentDigit = list(str(self.currentDigitInt))

        if self.operation == '+':
            self.currentDigitInt += float(self.stepDigit)
            self.display.setText(str(self.currentDigitInt))
            self.currentDigit.clear()
            self.currentDigit = list(str(self.currentDigitInt))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())
