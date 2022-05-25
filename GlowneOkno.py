from Panstwo import CountryCreator
from ListOfObjectsCreator import ListOfObjectsCreator
from Wykres import ChartMaker
from mapa import MapMaker
from Buttons import CountryButton, ChoiceButton, PathButton, AddPatchButton, ErrorDisplay, CountryDisplay
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QGroupBox, QWidget, QGridLayout, QPushButton, QTabWidget, \
    QScrollArea
from PyQt5.QtGui import QIcon
from CzytnikPliku import Czytnik
from Slider import Slider


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__disp = CountryDisplay()
        self.__error_disp = ErrorDisplay()
        self.__short_list = list()
        self.__list = list()
        self.__view = "None"
        self.__Creator = CountryCreator()
        self.__slider = None
        self.__inputer = None
        self.__start_date = None
        self.__end_date = None
        self.__map_button = ChoiceButton("Mapa", self)
        self.__chart_button = ChoiceButton("Wykres", self)

        self.resize(1500, 1000)
        self.__init_view()
        self.tabs = QTabWidget()
        self.start_view()

    def __init_view(self):

        self.setWindowTitle("Aplikacja")
        self.setWindowIcon(QIcon('oip_eZL_icon.ico'))
        self.__layout = QGridLayout()
        # ustala Group boxa ktory pozwala na wyswietlenie dodatkowych ramek/pol/wykresow wewnątrz
        group_box = QGroupBox()
        group_box.setLayout(self.__layout)
        # Mainuje group_boxa cntralnym wigdetem wysweitlanego okna, bez tego gruop_box nie bedzie wyswietlony
        self.setCentralWidget(group_box)
        self.prep_lista()

# tworzy liste CountryButons na podstawie dostarczonej listy (wszystkich) państw

    # def prep_lista(self):
    #     self.tab2 = QWidget()
    #     # ustala rozkład na wertykalny (kolejnye przyciski beda dodawne pod soba)
    #     self.tab2.layout = QVBoxLayout()
    #     for kraj in self.__list:
    #         self.tab2.layout.addWidget(CountryButton(kraj, self))
    #     self.tab2.setLayout(self.tab2.layout)

    def prep_lista(self):
        self.tab2 = QWidget()
        # ustala rozkład na wertykalny (kolejnye przyciski beda dodawne pod soba)
        self.tab2.layout = QVBoxLayout()
        for kraj in self.__list:
            self.tab2.layout.addWidget(CountryButton(kraj, self))
        groupbox = QGroupBox("Country list")
        groupbox.setLayout(self.tab2.layout)
        scroll = QScrollArea()
        scroll.setWidget(groupbox)
        scroll.setWidgetResizable(True)

        Layout = QVBoxLayout()
        Layout.addWidget(scroll)
        self.tab2.setLayout(Layout)


    def start_view(self):
         self.prep_lista()
         self.__short_list.clear()

         for kraj in self.__short_list:
             if not kraj.get_status():
                 self.__short_list.remove(kraj)
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
         self.__layout.addWidget(self.__error_disp, 16, 2, 1, 10)
         self.__layout.addWidget(self.__chart, 2, 0, 14, 22)
         self.__layout.addWidget(self.tab2, 2, 22, 16, 6)
         self.__layout.addWidget(self.__map_button, 0, 0, 2, 10)
         self.__layout.addWidget(self.__chart_button, 0, 10, 2, 10)
         self.__inputer = PathButton()
         self.__layout.addWidget(self.__inputer, 0, 20, 2, 6)
         self.__layout.addWidget(AddPatchButton("Dodaj Plik", self, self.__inputer), 0, 26, 2, 2)
         self.__layout.addWidget(QPushButton("Daty"), 17, 0, 1, 2)
         self.__layout.addWidget(self.__slider, 17, 2, 2, 18)
         self.__layout.addWidget(QPushButton("PDF/JPG"), 17, 20, 1, 2)


    def refresh_view(self):
        self.prep_lista()
        self.__short_list.clear()

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

        self.__chart_button.check_color()
        self.__map_button.check_color()
        self.__layout.addWidget(self.__chart, 2, 0, 14, 22)


    def set_view(self, nazwa):
        self.__view = nazwa

    def show_chart(self):
        # ustala że w głownym oknie będzie wyświetlany wykres
        #self.__layout.removeWidget(self.__chart)
        self.__chart = ChartMaker(self.__short_list, self.__start_date, self.__end_date, self.__error_disp)

    def show_map(self):
        #self.__layout.removeWidget(self.__chart)
        self.__chart = MapMaker(self.__short_list, self.__start_date, self.__end_date,)
        # ustala że w głownym oknie będzie wyświetlany mapa

    def get_view(self):
        return self.__view

    def set_path(self, sciezka):
        self.__sciezka = sciezka
        self.__change_data()

    def set_start_date(self,start_date):
        self.__start_date = start_date

    def set_end_date(self,end_date):
        self.__end_date = end_date



    def __change_data(self):

        NowyCzytnik = Czytnik()
        dane = NowyCzytnik.read_file(self.__sciezka)
        ListCreator = ListOfObjectsCreator(dane,CountryCreator())
        self.__list = ListCreator.get_list()
        self.__slider = Slider(self, self.__list)
        self.start_view()


