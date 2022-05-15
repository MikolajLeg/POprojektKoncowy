import sys
from Wykres import Rysuj
from CzytnikPliku import Czytnik
from Panstwo import Kraj
from GlowneOkno import MainWindow
from PyQt5.QtWidgets import QApplication

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QGroupBox, QPushButton, QVBoxLayout

class Przycisk(QPushButton):
    def __init__(self, value):
        super().__init__(value)
        self.__value = value

        self.show()
        # self.clicked.connect(self.__update_text_field)
    #
    # def __update_text_field(self):
    #     org_text = self.__text_panel.text()
    #     org_text = "" if org_text == "." else org_text
    #
    #     new_text = f"{org_text}{self.__value}"
    #     self.__text_panel.setText(new_text)


class TopPanel_1(QGroupBox):
    def __init__(self):
        super().__init__()
        self.__siatka_przyciskow()

    def __siatka_przyciskow(self):
        self.__stworz_przyciski()
        layout = QGridLayout()

        layout.addWidget(self.__Mapa, 0, 0)
        layout.addWidget(self.__Wykres, 0, 1)


    def __stworz_przyciski(self):
        self.__Mapa = Przycisk("Mapa")
        self.__Wykres = Przycisk("Wykres")


class TopPanel_2(QGroupBox):
    def __init__(self):
        super().__init__()
        self.__siatka_przyciskow()

    def __siatka_przyciskow(self):
        self.__stworz_przyciski()
        layout = QGridLayout()

        layout.addWidget(self.__miejsce_na_link, 0, 0)


    def __stworz_przyciski(self):
        self.__miejsce_na_link = Przycisk("Tu wklej link")

class PDF_JPG(QGroupBox):
    def __init__(self):
        super().__init__()
        self.__siatka_przyciskow()

    def __siatka_przyciskow(self):
        layout = QGridLayout()
        self.__stworz_przyciski()

        layout.addWidget(self.__PDF, 0, 0)
        layout.addWidget(self.__JPG, 0, 1)


    def __stworz_przyciski(self):
        self.__PDF = Przycisk("PDF")
        self.__JPG = Przycisk("JPG")





class Suwak(QGroupBox):
    def __init__(self):
        super().__init__()
        self.__siatka_przyciskow()

    def __siatka_przyciskow(self):
        self.__stworz_przyciski()
        layout = QGridLayout()

        layout.addWidget(self.__suwak, 0, 0)
        layout.addWidget(self.__daty, 1, 0)


    def __stworz_przyciski(self):
        self.__suwak = Przycisk("suwak")
        self.__daty = Przycisk("daty")


class Chart(QGroupBox):
    def __init__(self,start_date, end_date, lista):
        super().__init__()
        self.__chart = Rysuj(lista, start_date, end_date)
        #self.__siatka_przyciskow()

    def __siatka_przyciskow(self):

        layout = QGridLayout()

        layout.addWidget(self.__chart, 0, 0)




class Lista(QGroupBox):
    def __init__(self):
        super().__init__()
        self.__siatka_przyciskow()

    def __siatka_przyciskow(self):
        self.__stworz_przyciski()
        layout = QGridLayout()

        layout.addWidget(self.__lista, 0, 0)


    def __stworz_przyciski(self):
        self.__lista = Przycisk("lista")



class Okno(QWidget):
    def __init__(self, start_date, end_date, lista):
        super().__init__()
        self.__przygotuj_okno(start_date, end_date, lista)

    def __przygotuj_okno(self, start_date, end_date, lista):
        self.__top_left = TopPanel_1()
        self.__top_right = TopPanel_2()
        self.__main_window = Chart(start_date, end_date, lista)
        self.__lista = Lista()
        self.__PDF = PDF_JPG()
        self.__Suwak = Suwak()

        main_layout = QGridLayout()
        main_layout.addWidget(self.__top_left, 0, 0)
        main_layout.addWidget(self.__top_right, 0, 1)
        main_layout.addWidget(self.__main_window, 1, 0)
        main_layout.addWidget(self.__lista, 1, 1)
        main_layout.addWidget(self.__PDF, 2, 1)
        main_layout.addWidget(self.__Suwak, 1, 2)

        self.setLayout(main_layout)
        self.show()


if __name__ == "__main__":

    NowyCzytnik = Czytnik()

    # sciezka = input("sciezka")
    sciezka = 'Electricity prices for household consumers - bi-annual data (from 2007 onwards) [NRG_PC_204].csv'

    dane = NowyCzytnik.read_file(sciezka)
    print(dane)

    Belgium = Kraj("Belgium", dane)
    print(Belgium)

    proba = Belgium.get_dates_and_cost()
    print("test")
    print(proba)

    Czechia = Kraj("Czechia", dane)
    print(Czechia)

    Germany = Kraj("Germany", dane)
    print(Germany)

    Ireland = Kraj("Ireland", dane)
    print(Ireland)

    Spain = Kraj("Spain", dane)
    print(Spain)

    Kosovo = Kraj("Kosovo", dane)
    print(Kosovo)

    Bosnia = Kraj("Bosnia", dane)
    print(Bosnia)

    lista = list()
    lista.append(Belgium)
    lista.append(Bosnia)
    lista.append(Kosovo)
    lista.append(Ireland)
    lista.append(Spain)

    # start_date = input("data początkową")
    # end_date = input("data konca ")
    start_date = '2009-S2'
    end_date = '2015-S2'




    app = QApplication([])

    okno = Okno(start_date, end_date, lista)



    sys.exit(app.exec_())
