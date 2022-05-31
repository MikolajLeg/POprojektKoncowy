

from Panstwo import CountryCreator
from ListOfObjectsCreator import ListOfObjectsCreator
from Wykres import ChartMaker
from mapa import MapMaker
from buttons import CountryButton, ChoiceButton, ErrorDisplay, CountryDisplay, PdfSaveButton
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QGroupBox, QWidget, QGridLayout, QScrollArea
from PyQt5.QtGui import QIcon
from file_reader import FileReader
from Slider import Slider
from file_loader import FileLoader


# main class of our application responsible for creating main window GUI and maintaining its functions
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
        self.__start_date = None
        self.__end_date = None
        self.__tab1 = None
        self.__tab2 = None
        self.__chart = None
        self.__filepath = None
        self.__map_button = ChoiceButton("Map", self.set_view, self.get_view, self.refresh_view)
        self.__chart_button = ChoiceButton("Chart", self.set_view, self.get_view, self.refresh_view)
        self.__file_loader = FileLoader("select file", self.__error_disp.append, self.set_path)
        self.__pdf_button = PdfSaveButton("Create PDF", self.__error_disp.append)

        self.__init_view()
        self.__start_view()

    # method responsible for initializing view, and setting basic window/application properties ( tittle/size/icon)
    def __init_view(self):

        self.resize(1500, 1000)
        self.setWindowTitle("Application")
        self.setWindowIcon(QIcon('oip_eZL_icon.ico'))
        self.__layout = QGridLayout()
        # creates group box which allows for putting extra widgets/Labels/Layouts inside
        group_box = QGroupBox()
        group_box.setLayout(self.__layout)
        # sets group box as central widget of Main Window
        self.setCentralWidget(group_box)
        self.__prep_lista()

    # create list of CountryButtons basing on delivered list of countries
    def __prep_lista(self):
        self.__tab2 = QWidget()
        # sets vertical layout (new buttons will be added under previous ones)
        self.__tab2.layout = QVBoxLayout()
        for country in self.__list:
            self.__tab2.layout.addWidget(CountryButton(country, self.refresh_view))
        groupbox = QGroupBox("Country list")
        groupbox.setLayout(self.__tab2.layout)

        # adds scroll to button list
        scroll = QScrollArea()
        scroll.setWidget(groupbox)
        scroll.setWidgetResizable(True)
        Layout = QVBoxLayout()
        Layout.addWidget(scroll)
        self.__tab2.setLayout(Layout)

    # method responsible for starting view (setting layout of widgets appearing in main window for the first time)
    def __start_view(self):

        self.__short_list.clear()
        for country in self.__list:
            if country.get_status():
                self.__short_list.append(country)

        self.tab1 = QWidget()
        self.tab1.setStyleSheet("border: 1px solid red")
        self.__chart = self.tab1

        # sets the layout of initial widgets
        self.__layout.addWidget(self.__error_disp, 16, 0, 1, 10)
        self.__layout.addWidget(self.__disp, 16, 10, 1, 10)
        self.__layout.addWidget(self.__chart, 2, 0, 14, 22)
        self.__layout.addWidget(self.__tab2, 2, 22, 17, 6)
        self.__layout.addWidget(self.__map_button, 0, 0, 2, 10)
        self.__layout.addWidget(self.__chart_button, 0, 10, 2, 10)
        self.__layout.addLayout(self.__file_loader, 0, 20, 2, 8)
        self.__layout.addWidget(self.__slider, 17, 0, 2, 22)
        self.__layout.addWidget(self.__pdf_button, 16, 20, 1, 2)

    # method used to refresh view of main window in order to apply changes
    def refresh_view(self):
        self.__prep_lista()
        self.__short_list.clear()

        for country in self.__list:
            if country.get_status():
                self.__short_list.append(country)

        # checks whether map or chart is chosen and puts the correct one inside main_window chart field
        if self.__view == "Chart":
            self.show_chart()
            self.__pdf_button.update_pdf_data(self.__chart, self.__start_date, self.__end_date, self.__short_list)
        elif self.__view == "Map":
            self.show_map()

        # sets correct color for map/chart button and refreshes displayed chart/map
        self.__chart_button.check_color()
        self.__map_button.check_color()
        self.__layout.addWidget(self.__chart, 2, 0, 14, 22)

    # enables switching between displaying map/chart
    def set_view(self, name):
        self.__view = name

    # sets chart as the one to be displayed in main window
    def show_chart(self):
        self.__chart = ChartMaker(self.__short_list, self.__start_date, self.__end_date, self.__error_disp)

    # sets map as the one to be displayed in main window
    def show_map(self):
        self.__chart = MapMaker(self.__list, self.__start_date, self.__end_date, self.__error_disp, self.__disp)

    # returns what is actually displayed
    def get_view(self):
        return self.__view

    # sets path to file with data
    def set_path(self, filepath):
        self.__filepath = filepath
        self.__change_data()

    def set_start_date(self, start_date):
        self.__start_date = start_date

    def set_end_date(self, end_date):
        self.__end_date = end_date

    # reads and return new data after new path to file have been set
    def __change_data(self):

        new_reader = FileReader(self.__file_loader.set)
        dane = new_reader.read_file(self.__filepath)
        # creates list of country objects
        list_creator = ListOfObjectsCreator(dane, CountryCreator())
        self.__list = list_creator.get_list()
        self.__slider = Slider(self, self.__list)
        self.__start_view()
