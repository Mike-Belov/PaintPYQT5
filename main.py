import sys
from PyQt5 import QtGui
from PyQt5.QtWinExtras import QtWin  
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QFrame, QHBoxLayout, QSlider
from PyQt5.QtCore import Qt, QPoint, QPropertyAnimation
from PyQt5.QtGui import QPainter, QPen, QPixmap,  QColor
from color_definition import *
from tkinter import colorchooser
import threading

class Program(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PaintMisha")
        self.WIDTH, self.HIGHT = 1400, 900
        self.setFixedSize(self.WIDTH, self.HIGHT)
        myappid = 'mycompany.myproduct.subproduct.version'                         
        QtWin.setCurrentProcessExplicitAppUserModelID(myappid)  

        self.drawing = False
        self.last_point = QPoint

        # Создаем холст (QPixmap)
        self.image = QPixmap(self.size())
        self.image.fill(Qt.white)
        
        # Карандаш
        self.color = "#000000"
        self.penWidth = 10
        self.pen_color = QColor(self.color)

        #Создаем меню
        self.menu_x = int(1400/2-350)
        self.menu_y = -190
        self.is_mouse_on_menu = False
        self.setMouseTracking(True)

        self.status = self.statusBar()
        self.settingPaint()  

        self.loadStylesheet("style.css")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        x, y = event.x(), event.y()
        if not self.is_mouse_on_menu:
            if x >= self.menu_x and x <= self.menu_x + 700 and y <= 20:
                self.is_mouse_on_menu = True
                self.toggleMenu()
        else:
            if not x >= self.menu_x or not x <= self.menu_x + 700 or not y <= 200:
                self.is_mouse_on_menu = False
                self.toggleMenu() 

        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            self.pen = QPen(self.pen_color, self.penWidth)

            painter.setRenderHint(QPainter.Antialiasing, True) #для плавной рисовки
            pen = QPen(self.pen_color, self.penWidth, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin) #кисть с плавной рисовкой
            painter.setPen(pen)
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

    def settingPaint(self):
        self.stateBar()

        #Создаем выезжающий фрейм (меню)
        self.menu_frame = QFrame(self)
        self.menu_frame.setGeometry(self.menu_x, self.menu_y, 700, 200)
        self.layout = QHBoxLayout()

        # Привязываем лейаут к фрейму
        self.menu_frame.setLayout(self.layout)

        # Создание ползунка (горизонтальный)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 45)  # Диапазон размеров # Минимальный и максимальный размер
        self.slider.valueChanged.connect(self.change_size)
        self.slider.setValue(self.penWidth)     # Начальный размер
        self.layout.addWidget(self.slider)

        btn1 = QPushButton("Открыть")
        btn2 = QPushButton("Сохранить как")
        btn3 = QPushButton("Очистить")
        btncolor = QPushButton("Выбор цвета")
  
        self.layout.addWidget(btn1)
        self.layout.addWidget(btn2)
        self.layout.addWidget(btn3)
        self.layout.addWidget(btncolor)
        
        btn2.clicked.connect(self.actionTwo)
        btn3.clicked.connect(self.clear)

        btncolor.clicked.connect(self.chooseColor)

    def change_size(self, value):
        self.penWidth = value


    def stateBar(self):
        """Создает и обновляет статус бар"""
        self.status.showMessage(f'Карандаш|Размер:{self.penWidth}|Цвет: {color_definition(self.color)}')
        self.update()

    def chooseColor(self):
        """Открываем диалоговое окно выбора цвета"""
        color_menu = colorchooser.askcolor(title="Выберите цвет", initialcolor=self.color)
        if color_menu[1]:
            self.color = color_menu[1]  # Получаем RGB значения  
            self.pen_color = QColor(self.color)
            t2 = threading.Thread(target=self.stateBar)
            t2.start()
            self.update() 

    def toggleMenu(self):
        self.animation = QPropertyAnimation(self.menu_frame, b"pos")
        self.new_menu_y = -190 if self.menu_y >= 0 else 0
        self.animation.setStartValue(QPoint(self.menu_x, self.menu_y))
        self.animation.setDuration(450)
        self.animation.setEndValue(QPoint(self.menu_x, self.new_menu_y))
        self.animation.start()
        t2 = threading.Thread(target=self.stateBar)
        t2.start()

        self.menu_y = self.new_menu_y

    def actionOne(self):
        # Создание диалогового окна
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Информация")
        msg.setText("Это информационное сообщение")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        QMessageBox.information("Menu", "Выбрано Действие 2")

        # Отображение
        msg.exec_()

    def actionTwo(self):
        self.image.save("saved_image.png") # Сохраняет в формате PNG

    def clear(self):
        self.image.fill(Qt.white)
        self.update()

    def loadStylesheet(self, file_path):
        """Функция для загрузки файла стилей"""
        with open(file_path, 'r', encoding='utf-8') as f:
            app.setStyleSheet(f.read())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Program()

    # Создание иконки
    icon = 'icon.jfif'
    app.setWindowIcon(QtGui.QIcon(icon))
    window.setWindowIcon(QtGui.QIcon(icon))
    window.show()
    sys.exit(app.exec_())