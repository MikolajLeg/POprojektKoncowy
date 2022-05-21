from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QFormLayout, QGroupBox, QLabel, QScrollArea
import sys
from PyQt5 import QtGui
from Buttons import CountryButton, ChoiceButton, PathButton, AddPatchButton
from Panstwo import CountryCreator
from CzytnikPliku import Czytnik
from DataGrinder import ListOfObjectsCreator


class ScrollArea(QWidget):
    def __init__(self):
        super().__init__()
        self.__Creator = CountryCreator()
        self.prep_lista()
        self.__list = list()


        formLayout = QFormLayout()
        groupbox = QGroupBox("Country list")

        formLayout.addWidget(self.tab2)


        groupbox.setLayout(formLayout)
        scroll = QScrollArea()
        scroll.setWidget(groupbox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(400)

        layout = QVBoxLayout()
        layout.addWidget(scroll)
        self.setLayout(layout)


        # tworzy liste CountryButons na podstawie dostarczonej listy (wszystkich) państw

    def prep_lista(self):
        self.tab2 = QWidget()
        # ustala rozkład na wertykalny (kolejnye przyciski beda dodawne pod soba)
        self.tab2.layout = QVBoxLayout()
        for kraj in self.__list:
            self.tab2.layout.addWidget(CountryButton(kraj, self))
        self.tab2.setLayout(self.tab2.layout)





