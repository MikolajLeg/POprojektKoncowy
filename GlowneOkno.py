from Panstwo import CountryCreator
from DataGrinder import DataGrinder , ListOfObjectsCreator
from Wykres import Rysuj
from Buttons import CountryButton, ChoiceButton, PathButton, AddPatchButton
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QGroupBox, QWidget, QGridLayout, QPushButton, QTabWidget


class MainWindow(QMainWindow):
    def __init__(self, start_date, end_date):
        super().__init__()
        self.__list = list()
        self.__start_date = start_date
        self.__end_date = end_date
        self.__view = "None"
        self.__Creator = CountryCreator()
        self.__inputer = None

        self.resize(1500, 1000)
        self.__init_view()
        self.tabs = QTabWidget()
        self.refresh_view()

    def __init_view(self):

        self.setWindowTitle("Aplikacja")
        self.__layout = QGridLayout()
        # ustala Group boxa ktory pozwala na wyswietlenie dodatkowych ramek/pol/wykresow wewnątrz
        group_box = QGroupBox()
        group_box.setLayout(self.__layout)
        # Mainuje group_boxa cntralnym wigdetem wysweitlanego okna, bez tego gruop_box nie bedzie wyswietlony
        self.setCentralWidget(group_box)
        self.prep_lista()


# tworzy liste CountryButons na podstawie dostarczonej listy (wszystkich) państw

    def prep_lista(self):
        self.tab2 = QWidget()
        # ustala rozkład na wertykalny (kolejnye przyciski beda dodawne pod soba)
        self.tab2.layout = QVBoxLayout()
        for kraj in self.__list:
            self.tab2.layout.addWidget(CountryButton(kraj, self))
        self.tab2.setLayout(self.tab2.layout)

    def refresh_view(self):
        self.prep_lista()
        self.__short_list = list()
        for kraj in self.__list:
            if kraj.get_status():
                self.__short_list.append(kraj)

        if self.__view == "Wykres":
            self.show_chart()
        elif self.__view == "Mapa":
            self.show_map()
        else:
            self.tab1 = QWidget()
            self.tab1.setStyleSheet("border: 1px solid red")
            self.__chart = self.tab1

        # "wstawia" wykres do wnetrza okna, oraz ustala widok glownego okna
        # self.__layout.removeWidget(self.__chart)
        # self.__layout.removeWidget(self.tab2)
        # self.__layout.removeWidget(ChoiceButton("Mapa", self))
        # self.__layout.removeWidget(ChoiceButton("Wykres", self))
        # self.__layout.removeWidget(self.__inputer)
        # self.__layout.removeWidget(AddPatchButton("Dodaj Plik", self, self.__inputer))
        # self.__layout.removeWidget(QPushButton("Daty"))
        # self.__layout.removeWidget(QPushButton("suwak"))
        # self.__layout.removeWidget(QPushButton("PDF/JPG"))

        self.__layout.addWidget(self.__chart, 2, 0, 14, 22)
        self.__layout.addWidget(self.tab2, 2, 22, 16, 6)
        self.__layout.addWidget(ChoiceButton("Mapa", self), 0, 0, 2, 10)
        self.__layout.addWidget(ChoiceButton("Wykres", self), 0, 10, 2, 10)
        self.__inputer = PathButton()
        self.__layout.addWidget(self.__inputer, 0, 20, 2, 6)
        self.__layout.addWidget(AddPatchButton("Dodaj Plik", self, self.__inputer), 0, 26, 2, 2)
        self.__layout.addWidget(QPushButton("Daty"), 16, 0, 2, 2)
        self.__layout.addWidget(QPushButton("suwak"), 16, 2, 2, 18)
        self.__layout.addWidget(QPushButton("PDF/JPG"), 16, 20, 2, 2)


    def set_view(self, nazwa):
        self.__view = nazwa

    def show_chart(self):
        # ustala że w głownym oknie będzie wyświetlany wykres
        self.__chart = Rysuj(self.__short_list, self.__start_date, self.__end_date)

    def show_map(self):
        self.__chart = None
        # ustala że w głownym oknie będzie wyświetlany mapa

    def get_view(self):
        return self.__view

    def set_path(self, sciezka):
        self.__sciezka = sciezka
        self.__change_data()

    def __change_data(self):

        Grinder = DataGrinder(self.__sciezka)
        dane = Grinder.get_dane()
        ListCreator = ListOfObjectsCreator(dane,CountryCreator())
        self.__list = ListCreator.get_list()
        self.refresh_view()
