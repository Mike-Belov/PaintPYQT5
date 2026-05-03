from PyQt5.QtWidgets import QWidget, QPushButton
import data 

class FigureMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выбор фигуры для рисования")
        self.menuButton()
        # Фиксируем размеры
        self.setFixedHeight(400)
        self.setFixedWidth(600) 
        self.typeStart = data.type

    def menuButton(self):
        btnDirect = QPushButton("Прямая", self)
        btnPen = QPushButton("Карандаш", self)
        btnCircle = QPushButton("Круг", self)

        btnOk = QPushButton("ОК", self)
        btnBack = QPushButton("Назад", self)

        btnCircle.move(350, 100)
        btnPen.move(250, 100)
        btnDirect.move(150, 100)
        btnOk.move(70, 300)
        btnBack.move(500, 300)

        # Подключаем действие к кнопкам 
        btnCircle.clicked.connect(self.typeCircle)
        btnDirect.clicked.connect(self.typeDirect)
        btnPen.clicked.connect(self.typePen)
        btnOk.clicked.connect(self.saveMenu)
        btnBack.clicked.connect(self.closeMenu)

    def typeCircle(self):
        data.type = "circle"

    def saveMenu(self):
        self.close()

    def typePen(self):
        data.type = "pen"
    
    def typeDirect(self):
        data.type = "direct"

    def closeMenu(self):
        data.type = self.typeStart
        self.close()

    def loadStylesheet(self, file_path):
        """Функция для загрузки файла стилей"""
        with open(file_path, 'r', encoding='utf-8') as f: self.setStyleSheet(f.read())