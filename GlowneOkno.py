

from Wykres import Rysuj
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QGroupBox,QWidget, QApplication, QGridLayout, QPushButton,QTabWidget, QLineEdit


# możliwe że to trzeba bedzie do osobnego pliku wyrzuic
class CountryButton(QPushButton):
    def __init__(self,Kraj):
        super().__init__(Kraj.get_name())
        self.__kraj = Kraj
        self.clicked.connect(self.__status)

# zmieniana status kraju, na podstawie tego statusu program bedzie potem decydowac czy umiescic dany kraj na wykresie czy nie, ale to trzeba będzie potem dopisac dopiero
    def __status(self):
        self.__kraj.flip_status()
        print("test")
        print(self.__kraj)





class MainWindow(QMainWindow):
    def __init__(self,lista,start_date,end_date):
        super().__init__()

        self.resize(1500,1000)
        self.__init_view()
        self.prepare_chart(lista,start_date,end_date)

    def __init_view(self):
        self.setWindowTitle("Aplikacja")


        self.__layout = QGridLayout()
        # ustala Group boxa ktory pozwala na wyswietlenie dodatkowych ramek/pol/wykresow wewnątrz
        group_box= QGroupBox()
        group_box.setLayout(self.__layout)
        #Mainuje group_boxa cntralnym wigdetem wysweitlanego okna, bez tego gruop_box nie bedzie wyswietlony
        self.setCentralWidget(group_box)
        #self.show()

    def prepare_chart(self,lista,start_date,end_date):
        self.tabs = QTabWidget()
        # self.tab1 = QWidget()
        # self.tab1.layout = QVBoxLayout()
        # self.tab1.layout.addWidget(QPushButton("Paweł"))
        # self.tab1.layout.addWidget(QPushButton("to"))
        # self.tab1.layout.addWidget(QPushButton("największy"))
        # self.tab1.layout.addWidget(QPushButton("zbir"))
        # self.tab1.layout.addWidget(QPushButton("i"))
        # self.tab1.layout.addWidget(QPushButton("nicpoń"))
        # self.tab1.layout.addWidget(QPushButton("gałgan"))
        # self.tab1.layout.addWidget(QPushButton("nic nie"))
        # self.tab1.layout.addWidget(QPushButton("robi cały dzień"))
        # self.tab1.setLayout(self.tab1.layout)
        self.prep_lista(lista)

        self.__chart = Rysuj(lista,start_date,end_date)
        # "wstawia" wykres do wnetrza okna
        self.__layout.addWidget(self.__chart,2,0,14,22)
        self.__layout.addWidget(self.tab2,2,22,16,6)
        self.__layout.addWidget(QPushButton("Mapa"), 0, 0,2,10)
        self.__layout.addWidget(QPushButton("Wykres"), 0, 10,2,10)
        self.__layout.addWidget(QPushButton("Dodaj Plik"), 0, 20,2,8)
        self.__layout.addWidget(QPushButton("Daty"), 16,0,2,2)
        self.__layout.addWidget(QPushButton("suwak"), 16, 2,2,18)
        self.__layout.addWidget(QPushButton("PDF/JPG"), 16,20,2,2)

#trzorzy liste CountryButons na podstawie dostarczonej listy (wszystkich) państw
    def prep_lista(self,lista):
        self.tab2 = QWidget()
        #ustala rozkład na wertykalny (kolejnye przyciski beda dodawne pod soba)
        self.tab2.layout = QVBoxLayout()
        for kraj in lista:
            self.tab2.layout.addWidget(CountryButton(kraj))
        self.tab2.setLayout(self.tab2.layout)



