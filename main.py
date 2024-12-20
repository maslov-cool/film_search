import io
import sys
import sqlite3

from PyQt6 import uic  # Импортируем uic
from PyQt6.QtWidgets import QApplication, QMainWindow

template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>450</height>
   </rect>
  </property>
  <property name="minimumSize">
   <size>
    <width>800</width>
    <height>450</height>
   </size>
  </property>
  <property name="maximumSize">
   <size>
    <width>800</width>
    <height>450</height>
   </size>
  </property>
  <property name="windowTitle">
   <string>Поиск по фильмам</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QComboBox" name="parameterSelection">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>20</y>
      <width>201</width>
      <height>31</height>
     </rect>
    </property>
   </widget>
   <widget class="QLineEdit" name="queryLine">
    <property name="geometry">
     <rect>
      <x>280</x>
      <y>20</y>
      <width>241</width>
      <height>31</height>
     </rect>
    </property>
   </widget>
   <widget class="QLabel" name="label">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>70</y>
      <width>221</width>
      <height>41</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>12</pointsize>
     </font>
    </property>
    <property name="text">
     <string>ID:</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_2">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>130</y>
      <width>201</width>
      <height>41</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>12</pointsize>
     </font>
    </property>
    <property name="text">
     <string>Название:</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_3">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>180</y>
      <width>151</width>
      <height>41</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>12</pointsize>
     </font>
    </property>
    <property name="text">
     <string>Год выпуска:</string>
    </property>
   </widget>
   <widget class="QLineEdit" name="idEdit">
    <property name="geometry">
     <rect>
      <x>270</x>
      <y>80</y>
      <width>311</width>
      <height>31</height>
     </rect>
    </property>
   </widget>
   <widget class="QLineEdit" name="titleEdit">
    <property name="geometry">
     <rect>
      <x>270</x>
      <y>130</y>
      <width>311</width>
      <height>31</height>
     </rect>
    </property>
   </widget>
   <widget class="QLineEdit" name="yearEdit">
    <property name="geometry">
     <rect>
      <x>270</x>
      <y>190</y>
      <width>311</width>
      <height>31</height>
     </rect>
    </property>
    <property name="autoFillBackground">
     <bool>false</bool>
    </property>
   </widget>
   <widget class="QLineEdit" name="genreEdit">
    <property name="geometry">
     <rect>
      <x>270</x>
      <y>250</y>
      <width>311</width>
      <height>31</height>
     </rect>
    </property>
   </widget>
   <widget class="QLineEdit" name="durationEdit">
    <property name="geometry">
     <rect>
      <x>270</x>
      <y>310</y>
      <width>311</width>
      <height>31</height>
     </rect>
    </property>
   </widget>
   <widget class="QLabel" name="label_4">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>240</y>
      <width>171</width>
      <height>41</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>12</pointsize>
     </font>
    </property>
    <property name="text">
     <string>Жанр:</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_5">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>310</y>
      <width>211</width>
      <height>31</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>12</pointsize>
     </font>
    </property>
    <property name="text">
     <string>Продолжительность:</string>
    </property>
   </widget>
   <widget class="QLabel" name="errorLabel">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>360</y>
      <width>311</width>
      <height>51</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>12</pointsize>
     </font>
    </property>
    <property name="text">
     <string/>
    </property>
   </widget>
   <widget class="QPushButton" name="queryButton">
    <property name="geometry">
     <rect>
      <x>590</x>
      <y>10</y>
      <width>131</width>
      <height>41</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>12</pointsize>
     </font>
    </property>
    <property name="text">
     <string>Поиск</string>
    </property>
   </widget>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)  # Загружаем дизайн

        self.parameterSelection.addItem('Год выпуска')
        self.parameterSelection.addItem('Название')
        self.parameterSelection.addItem('Продолжительность')

        self.queryButton.clicked.connect(self.act)

    def act(self):
        try:
            if self.parameterSelection.currentText() == 'Год выпуска':
                # Подключение к БД
                con = sqlite3.connect('films_db.sqlite')

                # Создание курсора
                cur = con.cursor()

                # Выполнение запроса и получение всех результатов
                result = cur.execute("""SELECT * FROM films
                                WHERE year = ?""", (self.queryLine.text(),)).fetchall()
                con.close()
                if not result:
                    self.errorLabel.setText('Ничего не найдено')
                else:
                    result = sorted(result, key=lambda x: x[0])[0]
                    self.idEdit.setText(str(result[0]))
                    self.titleEdit.setText(result[1])
                    self.yearEdit.setText(str(result[2]))
                    self.genreEdit.setText(str(result[3]))
                    self.durationEdit.setText(str(result[4]))
            elif self.parameterSelection.currentText() == 'Название':
                 # Подключение к БД
                con = sqlite3.connect('films_db.sqlite')

                # Создание курсора
                cur = con.cursor()

                # Выполнение запроса и получение всех результатов
                result = cur.execute("""SELECT * FROM films
                                WHERE title = ?""", (self.queryLine.text(),)).fetchall()
                con.close()
                if not result:
                    self.errorLabel.setText('Ничего не найдено')
                else:
                    result = sorted(result, key=lambda x: x[0])[0]
                    self.idEdit.setText(str(result[0]))
                    self.titleEdit.setText(result[1])
                    self.yearEdit.setText(str(result[2]))
                    self.genreEdit.setText(str(result[3]))
                    self.durationEdit.setText(str(result[4]))
            else:
                # Подключение к БД
                con = sqlite3.connect('films_db.sqlite')

                # Создание курсора
                cur = con.cursor()

                # Выполнение запроса и получение всех результатов
                result = cur.execute("""SELECT * FROM films
                                WHERE duration = ?""", (self.queryLine.text(),)).fetchall()
                con.close()
                if not result:
                    self.errorLabel.setText('Ничего не найдено')
                else:
                    result = sorted(result, key=lambda x: x[0])[0]
                    self.idEdit.setText(str(result[0]))
                    self.titleEdit.setText(result[1])
                    self.yearEdit.setText(str(result[2]))
                    self.genreEdit.setText(str(result[3]))
                    self.durationEdit.setText(str(result[4]))
        except sqlite3.OperationalError:
            self.errorLabel.setText("Неправильный запрос")


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
