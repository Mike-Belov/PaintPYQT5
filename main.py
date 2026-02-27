import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel, QAction, QMenu, QMessageBox, QGroupBox, QFrame, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint, QCoreApplication, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPainter, QPen, QPixmap,  QColor, QBrush, QIcon, QFont
from color import choose_color
from color_definition import *

class Program(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PaintMisha")
        self.WIDTH, self.HIGHT = 1400, 900
        self.setFixedSize(self.WIDTH, self.HIGHT)

        self.drawing = False
        self.last_point = QPoint

        # Создаем холст (QPixmap)
        self.image = QPixmap(self.size())
        self.image.fill(Qt.white)
        
        # Карандаш
        self.color = (0,0,0)
        self.pen_color = QColor(*self.color)
        self.penWidth = 3
        self.pen = QPen(self.pen_color, self.penWidth)

        # Создаем объект шрифта и задаем размер (например, 14)
        self.font = QFont()
        self.font.setPointSize(12)

        #Переменные для меню
        self.size_button = [120, 25]
        #Создаем меню
        self.menu()
        self.setting_paint()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(self.pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update() # Перерисовать виджет
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.image)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            sys.exit()

    def menu(self):
        # Создание кнопки
        btn = QPushButton('Файл', self)
        btn.setFixedSize(*self.size_button) 
        btn.move(0,0)

        # Меню действий
        menu = QMenu(self)
        # Добавляем действия (пункты меню)
        action1 = QAction("Сохранить как", self)
        action2 = QAction("Открыть", self)
        action3 = QAction("Выйти", self)

       # Добавляем действия в меню  
        menu.addAction(action1)
        menu.addAction(action2)
        menu.addSeparator()  # Разделитель  
        menu.addAction(action3)

        # Подключаем сигналы к действиям
        action1.triggered.connect(self.action_one)
        action2.triggered.connect(self.action_two)
        action3.triggered.connect(QCoreApplication.instance().quit)

        # Подключение сигнала нажатия к функции
        btn.setMenu(menu)

        # Статус бар
        self.status = self.statusBar()
        self.status.showMessage(f'Карандаш|Размер:{self.penWidth}|Цвет: {color_definition(self.color)}')
        self.status.setFont(self.font)

    def setting_paint(self):
        # Кнопка для открытия/закрытия меню
        self.toggle_button = QPushButton("☰ Меню", self)
        self.toggle_button.setFixedSize(*self.size_button)
        self.toggle_button.move(120,0)
        self.toggle_button.clicked.connect(self.toggle_menu)
        
        #Создаем выезжающий фрейм (меню)
        self.menu_frame = QFrame(self)
        self.menu_frame.setFrameShape(QFrame.StyledPanel) # Рисуем рамку, чтобы её было видно
        self.menu_frame.setStyleSheet("background-color: #787878; " \
        "border: 2px solid gray;" \
        "  border-radius: 10px;")
        
        self.menu_frame.setGeometry(int(1400/2-350), 0, 700, 10)
        self.layout = QHBoxLayout()

        # Привязываем лейаут к фрейму
        self.menu_frame.setLayout(self.layout)

        # Добавляем кнопки в меню
        btn1 = QPushButton("Кнопка 1")
        btn2 = QPushButton("Кнопка 2")
        btn1.setFixedSize(*self.size_button)
        btn2.setFixedSize(*self.size_button)
        self.layout.addWidget(btn1)
        self.layout.addWidget(btn2)
        self.layout.addStretch() # Добавляет пустое пространство вниз

    def toggle_menu(self):
        if self.menu_frame.height()==10:
            self.animation = QPropertyAnimation(self.menu_frame, b"minimumHeight")
            self.menu_frame.height()
        else:
            self.animation = QPropertyAnimation(self.menu_frame, b"maximumHeight")
        height = self.menu_frame.height()
        new_height = 200 if height == 10 else 10  # Переключение ширины
        self.animation.setStartValue(height)
        self.animation.setDuration(400)
        self.animation.setEndValue(new_height)
        self.animation.start()

    def action_one(self):
        ...

    def action_two(self):
        # Создание диалогового окна
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Информация")
        msg.setText("Это информационное сообщение")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        # Отображение
        msg.exec_()

    def action_two(self):
        QMessageBox.information("Menu", "Выбрано Действие 2")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Program()
    window.show()
    sys.exit(app.exec_())