import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        # Пример:
        # 59.150520, 37.924341
        # 0.02, 0.002
        self.coords = input('Введите координаты\n')
        self.size = input('Введите маштаб\n')
        self.c1 = int(self.coords.split(', ')[1])
        self.c2 = int(self.coords.split(', ')[0])
        self.s1 = int(self.size.split(', ')[0])
        self.s2 = int(self.size.split(', ')[1])
        self.getImage()
        self.initUI()

    def getImage(self):

        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.c1},{self.c2}&spn={self.s1},{self.s2}&l=map"
        print(map_request)
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code,
                  "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        try:
            if event.key() == Qt.Key_Up:
                self.s1 *= 2
                self.s2 *= 2
                self.getImage()
                self.pixmap = QPixmap(self.map_file)
                self.image.setPixmap(self.pixmap)
            if event.key() == Qt.Key_Down:
                self.s1 /= 2
                self.s2 /= 2
                self.getImage()
                self.pixmap = QPixmap(self.map_file)
                self.image.setPixmap(self.pixmap)
        except:
            self.s1 = 90
            self.s2 = 90

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
