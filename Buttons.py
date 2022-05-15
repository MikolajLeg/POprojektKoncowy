
from PyQt5.QtWidgets import QPushButton, QLineEdit

class CountryButton(QPushButton):
    def __init__(self,Kraj,Okno):
        super().__init__(Kraj.get_name())
        self.__kraj = Kraj
        self.__okno = Okno
        self.clicked.connect(self.__status)
        self.__check_color()

# zmieniana status kraju, na podstawie tego statusu program bedzie potem decydowac czy umiescic dany kraj na wykresie czy nie, ale to trzeba będzie potem dopisac dopiero
    def __status(self):
        self.__kraj.flip_status()
        #zmina koloru aby pokazac czy kraj bedzie uwzgleniony na wykresie/mapie
        self.__check_color()
        #odswiezenie widoku glownego okna
        self.__okno.refresh_view()

    def __check_color(self):

        if self.__kraj.get_status():
            self.setStyleSheet("background-color: yellow")
        else:
            self.setStyleSheet("background-color: light gray")


class ChoiceButton(QPushButton):
    def __init__(self,nazwa,Okno):
        super().__init__(nazwa)
        self.__nazwa = nazwa
        self.__okno = Okno
        self.clicked.connect(self.wybor)
        if self.__okno.get_view() == self.__nazwa:
            self.setStyleSheet("background-color: yellow")
        else:
            self.setStyleSheet("background-color: light gray")


    def wybor(self):
        self.__okno.set_view(self.__nazwa)
        self.__okno.refresh_view()

class PathButton(QLineEdit):
    def __init__(self,Okno):
        super().__init__()

    def get_tekst(self):
        return self.text()

class AddPatchButton(QPushButton):
    def __init__(self, nazwa, Okno, inputer):
        super().__init__(nazwa)
        self.__okno = Okno
        self.__inputer = inputer
        self.clicked.connect(self.set_Path)


    def set_Path(self):
        self.__sciezka = self.__inputer.get_tekst()
        self.__okno.set_path(self.__sciezka)


