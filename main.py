
from Wykres import Rysuj
from CzytnikPliku import Czytnik
from Panstwo import Kraj
from GlowneOkno import MainWindow
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    NowyCzytnik = Czytnik()

    sciezka = input("sciezka")
    #sciezka = 'Electricity prices for household consumers - bi-annual data (from 2007 onwards) [NRG_PC_204].csv'

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

    start_date = input("data początkową")
    end_date = input("data konca ")
    # start_date = '2009-S2'
    # end_date = '2015-S2'


    app = QApplication([])
    window = MainWindow(lista, start_date, end_date)
    window.show()
    app.exec_()
