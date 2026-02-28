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
        self.menu_x = int(1400/2-350)
        self.menu_y = -200
        self.is_mouse_on_menu = False
        self.setMouseTracking(True)
        self.setting_paint()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        x, y = event.x(), event.y()
        if not self.is_mouse_on_menu:
            if x >= self.menu_x and x <= self.menu_x + 700 and y <= 50:
                self.is_mouse_on_menu = True
                self.toggle_menu()
        else:
            if not x >= self.menu_x or not x <= self.menu_x + 700 or not y <= 200:
                self.is_mouse_on_menu = False
                self.toggle_menu() 

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

    def setting_paint(self):
        #Создаем выезжающий фрейм (меню)
        self.menu_frame = QFrame(self)
        self.menu_frame.setFrameShape(QFrame.StyledPanel) # Рисуем рамку, чтобы её было видно
        self.menu_frame.setStyleSheet("""
        border-radius: 10px;
        box-shadow: 4px 4px 8px 0px rgba(34, 60, 80, 0.2);
        background: rgb(100, 100, 100);       
        """)
        
        self.menu_frame.setGeometry(self.menu_x, self.menu_y, 700, 200)
        self.layout = QHBoxLayout()

        # Привязываем лейаут к фрейму
        self.menu_frame.setLayout(self.layout)

        # Добавляем кнопки в меню
        btn1 = QPushButton("Кнопка 1")
        btn2 = QPushButton("Кнопка 2")
        btncolor = QPushButton("Выбор цвета")
        btn1.setFixedSize(*self.size_button)
        btn2.setFixedSize(*self.size_button)
        self.layout.addWidget(btn1)
        self.layout.addWidget(btn2)
        self.layout.addStretch() # Добавляет пустое пространство вниз

    def toggle_menu(self):
        self.animation = QPropertyAnimation(self.menu_frame, b"pos")

        self.new_menu_y = -200 if self.menu_y >= 0 else 0

        self.animation.setStartValue(QPoint(self.menu_x, self.menu_y))
        self.animation.setDuration(450)
        self.animation.setEndValue(QPoint(self.menu_x, self.new_menu_y))
        self.animation.start()

        self.menu_y = self.new_menu_y

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