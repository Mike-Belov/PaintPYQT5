import sys
from PyQt5 import QtGui
from PyQt5.QtWinExtras import QtWin  
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QFrame, QHBoxLayout, QSlider, QFileDialog, QLabel
from PyQt5.QtCore import Qt, QPoint, QPropertyAnimation, QRect
from PyQt5.QtGui import QPainter, QPen, QPixmap,  QColor
from color_definition import *
from tkinter import colorchooser
import threading
from FigureMenu import FigureMenu
import data

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
        
        # Обычное рисование
        # Карандаш
        self.color = "#000000"
        self.penWidth = 10
        self.pen_color = QColor(self.color)

        self.device = "Карандаш"

        #Создаем меню
        self.menu_x = int(1400/2-350)
        self.menu_y = -190
        self.is_mouse_on_menu = False
        self.setMouseTracking(True)

        self.status = self.statusBar()
        self.settingPaint()  

        self.loadStylesheet("style.css")

        # Рисование лииями 
        # Переменные для хранения координат
        self.start_point = QPoint()
        self.end_point = QPoint()

        # Рисование кругами
        self.start_point = QPoint()
        self.end_point = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and data.type == "pen":
            self.drawing = True
            self.last_point = event.pos()
        elif event.button() == Qt.LeftButton and data.type == "direct":
            self.drawing = True
            self.start_point = event.pos()
            self.end_point = event.pos()
        elif event.button() == Qt.LeftButton and data.type == "circle":
            self.drawing = True
            self.start_point = event.pos()
            self.end_point = event.pos()
        else:
            self.dialogWindow("Ошибка", "Произошла ошибка. Перезапустите программу")

    def mouseMoveEvent(self, event):
        # Анимация меню
        x, y = event.x(), event.y()
        if not self.is_mouse_on_menu:
            if x >= self.menu_x and x <= self.menu_x + 700 and y <= 20:
                self.is_mouse_on_menu = True
                self.toggleMenu()
        else:
            if not x >= self.menu_x or not x <= self.menu_x + 700 or not y <= 200:
                self.is_mouse_on_menu = False
                self.toggleMenu() 

        if (event.buttons() & Qt.LeftButton) & self.drawing and data.type == "pen":
            painter = QPainter(self.image)
            self.pen = QPen(self.pen_color, self.penWidth)

            painter.setRenderHint(QPainter.Antialiasing, True) #для плавной рисовки
            pen = QPen(self.pen_color, self.penWidth, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin) #кисть с плавной рисовкой
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update() # Перерисовать виджет

        # Рисованние полосами
        elif (event.buttons() & Qt.LeftButton) and self.drawing and data.type == "direct":
            self.end_point = event.pos()
            self.update()  # Перерисовываем виджет
        # Рисование кругами
        elif (event.buttons() & Qt.LeftButton) and self.drawing and data.type == "circle":
            self.end_point = event.pos()
            self.update() # Обновляем экран для отображения временного круга
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and data.type == "pen":
            self.drawing = False
        elif event.button() == Qt.LeftButton and self.drawing and data.type == "direct":
            self.drawing = False
            
            # Фиксируем линию на холсте
            painter = QPainter(self.image)
            painter.setRenderHint(QPainter.Antialiasing, True) #для плавной рисовки
            pen = QPen(self.pen_color, self.penWidth, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawLine(self.start_point, self.end_point)
            self.update()
        elif event.button() == Qt.LeftButton and self.drawing and data.type == "circle":
            # Фиксируем круг на основном изображении
            painter = QPainter(self.image)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(QPen(self.pen_color, self.penWidth))
            rect = QRect(self.start_point, event.pos())
            painter.drawEllipse(rect.normalized())
            
            self.drawing = False
            self.update() # Финальное обновление
        else:
            self.dialogWindow("Ошибка", "Произошла ошибка. Перезапустите программу")

    def paintEvent(self, event):
        if data.type == "pen":
            painter = QPainter(self)
            painter.drawPixmap(self.rect(), self.image)
        elif data.type == "direct":
            # Отрисовка холста
            painter = QPainter(self)
            painter.drawPixmap(0, 0, self.image)
            
            # Если рисуем, рисуем временную линию
            if self.drawing:
                painter.setRenderHint(QPainter.Antialiasing, True) #для плавной рисовки
                painter.setPen(QPen(self.pen_color, self.penWidth, Qt.SolidLine))
                painter.drawLine(self.start_point, self.end_point)
        elif data.type == "circle":
            painter = QPainter(self)
            painter.drawPixmap(self.rect(), self.image)

            # Отрисовка временного круга в процессе перетаскивания
            if self.drawing:
                rect = QRect(self.start_point, self.end_point)
                painter.setRenderHint(QPainter.Antialiasing, True) #для плавной рисовки
                painter.setPen(QPen(self.pen_color, self.penWidth))
                painter.drawEllipse(rect.normalized())
        else:
            self.dialogWindow("Ошибка", "Произошла ошибка. Перезапустите программу")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape: 
            sys.exit()

    def settingPaint(self):
        threading.Thread(self.stateBar()).start() # Обновляем статус бар

        #Создаем выезжающий фрейм (меню)
        self.menu_frame = QFrame(self)
        self.menu_frame.setGeometry(self.menu_x, self.menu_y, 700, 200)
        self.layout = QHBoxLayout()

        # Привязываем лейаут к фрейму
        self.menu_frame.setLayout(self.layout)

        self.label_size_pen = QLabel("Размер кисти", self.menu_frame)
        self.label_size_pen.move(20, 50)

        # Создание ползунка (горизонтальный)
        self.slider = QSlider(Qt.Horizontal, self.menu_frame)
        self.slider.setRange(1, 45)  # Диапазон размеров # Минимальный и максимальный размер
        self.slider.valueChanged.connect(self.change_size)
        self.slider.setValue(self.penWidth)    # Начальный размер
        self.slider.move(25, 100)

        # Кнопки сохранения и открытия фото
        btnopen = QPushButton("Открыть", self.menu_frame)
        btnsave = QPushButton("Сохранить как", self.menu_frame)
        # Кнопки для рисования
        btnclean = QPushButton("Очистить", self.menu_frame)
        btncolor = QPushButton("Выбор цвета", self.menu_frame)
        btnfigure = QPushButton("Выбрать фигуру", self.menu_frame)
        btncleanpen = QPushButton("Ластик", self.menu_frame)

        btnopen.move(300, 20)
        btnsave.move(500, 20)
        btnclean.move(150, 100)
        btncolor.move(280, 100)
        btnfigure.move(410, 100)
        btncleanpen.move(540, 100)
        
        # Обработка нажатий на кнопки
        btnopen.clicked.connect(self.openImage)
        btnsave.clicked.connect(self.save)
        btnclean.clicked.connect(self.clear)
        btncolor.clicked.connect(self.chooseColor)
        btnfigure.clicked.connect(self.btnFigure)
        btncleanpen.clicked.connect(self.btnCleanPen)
        
    def change_size(self, value: int):
        self.penWidth = value

    def stateBar(self):
        """Создает и обновляет статус бар"""
        if data.type == "pen": self.device = "Карандаш"
        elif data.type == "direct": self.device = "Прямая"
        elif data.type == "circle": self.device = "Круг"
        else: self.device = "Не удалось определить"
        self.status.showMessage(f'{self.device}|Размер:{self.penWidth}|Цвет: {color_definition(self.color)}')
        self.update()

    def chooseColor(self):
        """Открываем диалоговое окно выбора цвета"""
        color_menu = colorchooser.askcolor(title="Выберите цвет", initialcolor=self.color)
        if color_menu[1]:
            self.color = color_menu[1]  # Получаем RGB значения  
            self.pen_color = QColor(self.color)
            threading.Thread(target=self.stateBar).start()
            self.update() 

    def toggleMenu(self):
        self.animation = QPropertyAnimation(self.menu_frame, b"pos")
        self.new_menu_y = -190 if self.menu_y >= 0 else 0
        self.animation.setStartValue(QPoint(self.menu_x, self.menu_y))
        self.animation.setDuration(450)
        self.animation.setEndValue(QPoint(self.menu_x, self.new_menu_y))
        self.animation.start()
        threading.Thread(target=self.stateBar).start()

        self.menu_y = self.new_menu_y

    def dialogWindow(self, title: str, message: str):
        """Создание диалогового окна"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        # Отображение
        msg.exec_()

    def btnCleanPen(self):
        self.pen_color = QColor(255,255,255)
        self.device = "Ластик"
        data.type = "pen"

    def btnFigure(self):
        # Сохраняем ссылку через self.
        self.second_window = FigureMenu()
        self.second_window.show()

    def save(self):
        """Функция для сохранения нарисованного изображения"""
        try:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(self, "Выберите путь", "image.png", "Image (*.png);;All Files (*)", options=options)
            if fileName: self.image.save(fileName) 
            self.dialogWindow("Сохранено", "Картинка успешна сохранена")
        except:
            self.dialogWindow("Ошибка", "Картинка не сохранена. Повторите попытку")

    def openImage(self):
        """Открытия картинки"""
        try:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "All Files (*);;Image (*.png)", options=options)
            if fileName: self.image = QPixmap(fileName)
        except:
            self.dialogWindow("Ошибка", "Картинка не открывается. Повторите попытку")

    def clear(self):
        """Функция очистки экрана"""
        self.image.fill(Qt.white)
        self.update()

    def loadStylesheet(self, file_path):
        """Функция для загрузки файла стилей"""
        with open(file_path, 'r', encoding='utf-8') as f: app.setStyleSheet(f.read())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Program()

    # Создание иконки
    icon = 'icon.jfif'
    app.setWindowIcon(QtGui.QIcon(icon))
    window.setWindowIcon(QtGui.QIcon(icon))
    window.show()
    sys.exit(app.exec_())