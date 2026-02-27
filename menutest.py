import sys  
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class SlideMenu(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_animations()
        
    def setup_ui(self):
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.setFixedWidth(250)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)
        
        # Заголовок меню  
        title = QLabel("Меню")
        title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333;
                padding-bottom: 10px;
                border-bottom: 1px solid #eee;
            }
        """)
        layout.addWidget(title)
        
        # Элементы меню с иконками  
        menu_data = [
            ("", "Профиль"),
            ("", "Настройки"),
            ("", "Документы"),
            ("", "Уведомления"),
            ("", "Помощь"),
            ("", "Выйти")
        ]
        
        for icon, text in menu_data:
            btn = QPushButton(f"{icon}  {text}")
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 10px;
                    border: none;
                    border-radius: 6px;
                    font-size: 14px;
                    color: #333;
                }
                QPushButton:hover {
                    background-color: #f0f0f0;
                    color: #0078d4;
                }
            """)
            layout.addWidget(btn)
            
        layout.addStretch()
        self.hide()
        
    def setup_animations(self):
        # Анимация позиции (выезд)
        self.pos_animation = QPropertyAnimation(self, b"pos")
        self.pos_animation.setDuration(400)
        self.pos_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # Анимация прозрачности  
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(300)
        
    def show_menu(self, pos, direction="right"):
        # Начальная позиция (смещена влево для эффекта выезда)
        start_pos = QPoint(pos.x() - 50, pos.y())
        self.move(start_pos)
        
        # Конечная позиция  
        end_pos = pos
        
        # Настраиваем анимацию  
        self.pos_animation.setStartValue(start_pos)
        self.pos_animation.setEndValue(end_pos)
        
        self.opacity_animation.setStartValue(0)
        self.opacity_animation.setEndValue(1)
        
        # Показываем и запускаем  
        self.show()
        self.raise_()  # Поднимаем на передний план  
        self.pos_animation.start()
        self.opacity_animation.start()
        
    def hide_menu(self):
        # Анимация скрытия  
        current_pos = self.pos()
        hide_pos = QPoint(current_pos.x() - 50, current_pos.y())
        
        self.pos_animation.setStartValue(current_pos)
        self.pos_animation.setEndValue(hide_pos)
        
        self.opacity_animation.setStartValue(1)
        self.opacity_animation.setEndValue(0)
        
        self.pos_animation.start()
        self.opacity_animation.start()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Анимированное меню")
        self.setGeometry(100, 100, 800, 600)
        
        # Центральный виджет  
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Кнопка для открытия меню  
        self.menu_button = QPushButton("☰ Открыть меню")
        self.menu_button.setFixedSize(150, 40)
        self.menu_button.clicked.connect(self.toggle_menu)
        layout.addWidget(self.menu_button, alignment=Qt.AlignTop | Qt.AlignLeft)
        
        # Создаем меню  
        self.menu = SlideMenu(self)
        
        # Флаг видимости меню  
        self.menu_visible = False
        
    def toggle_menu(self):
        if not self.menu_visible:
            # Получаем позицию кнопки  
            button_pos = self.menu_button.mapToGlobal(QPoint(0, self.menu_button.height()))
            # Конвертируем в координаты окна  
            window_pos = self.mapFromGlobal(button_pos)
            
            self.menu.show_menu(window_pos)
            self.menu_visible = True  
        else:
            self.menu.hide_menu()
            self.menu_visible = False
            
    def mousePressEvent(self, event):
        # Закрываем меню при клике вне его  
        if self.menu_visible and not self.menu.geometry().contains(event.pos()):
            self.menu.hide_menu()
            self.menu_visible = False  
        super().mousePressEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())