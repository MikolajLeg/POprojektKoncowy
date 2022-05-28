from file_loader import FileLoader
from PyQt5.QtWidgets import QPushButton, QLineEdit



class CountryButton(QPushButton):
    def __init__(self, Kraj, Okno):
        super().__init__(Kraj.get_name())
        self.__kraj = Kraj
        self.__okno = Okno
        self.clicked.connect(self.__status)
        self.__check_color()

# zmieniana status kraju, na podstawie statusu program bedzie potem decydowac czy umiescic dany kraj na wykresie czy nie
    def __status(self):
        self.__kraj.flip_status()
        # zmina koloru aby pokazac czy kraj bedzie uwzgleniony na wykresie/mapie
        self.__check_color()
        # odswiezenie widoku glownego okna
        self.__okno.refresh_view()

    def __check_color(self):

        if self.__kraj.get_status():
            self.setStyleSheet("background-color: yellow")
        else:
            self.setStyleSheet("background-color: light gray")


class ChoiceButton(QPushButton):
    def __init__(self, nazwa, Okno):
        super().__init__(nazwa)
        self.__nazwa = nazwa
        self.__okno = Okno
        self.clicked.connect(self.wybor)

    def wybor(self):
        self.__okno.set_view(self.__nazwa)
        self.check_color()
        self.__okno.refresh_view()

    def check_color(self):
        if self.__okno.get_view() == self.__nazwa:
            self.setStyleSheet("background-color: yellow")
        else:
            self.setStyleSheet("background-color: light gray")

# class ButtonCreator:
#     def __init__(self, ButtonType, arg_list, Okno, extra_arg = None):
#         self.__arg = arg_list
#         self.__okno = Okno
#         self.__Button = ButtonType
#         self.__extra_arg = extra_arg
#
#     def __make_buttons(self):
#         for arg in self.__arg:
#


class PathButton(QLineEdit):
    def __init__(self):
        super().__init__()

    def get_tekst(self):
        return self.text()


class AddPatchButton(QPushButton):
    def __init__(self, nazwa, Okno, inputer):
        super().__init__(nazwa)
        self.__okno = Okno
        self.__inputer = inputer
        self.clicked.connect(self.set_new_path)

    def set_new_path(self):
        self.__sciezka = self.__inputer.get_tekst()
        self.__okno.set_path(self.__sciezka)


class Display(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)



class CountryDisplay(Display):
    def __init__(self):
        super().__init__()


class ErrorDisplay(Display):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("color: red")

