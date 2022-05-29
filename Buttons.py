
from PyQt5.QtWidgets import QPushButton, QLineEdit, QFileDialog
from pdf_generator import PdfReportGenerator


class CountryButton(QPushButton):
    def __init__(self, Country, Okno):
        super().__init__(Country.get_name())
        self.__kraj = Country
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


class PdfSaveButton(QPushButton):

    def __init__(self, name):
        super().__init__(name)
        self.__pdf_generator = PdfReportGenerator()
        self.__chart = None

        self.clicked.connect(self.__save_btn_action)

    def update_chart(self, chart, data):
        self.__chart = chart
        self.__data = data

    def __save_btn_action(self):
        filename = self.__prepare_file_chooser()
        self.__pdf_generator.create_and_save_pdf(filename, self.__chart, self.__data)

    def __prepare_file_chooser(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save PDF report", filter="PDF ( *.pdf )")
        print(filename)
        return filename

