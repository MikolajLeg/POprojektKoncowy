

from Wykres import Rysuj
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QGroupBox,QWidget, QApplication



class MainWindow(QMainWindow):
    def __init__(self,lista,start_date,end_date):
        super().__init__()

        self.resize(1000,500)
        self.__init_view()
        self.prepare_chart(lista,start_date,end_date)

    def __init_view(self):
        self.setWindowTitle("Aplikacja")


        self.__layout = QVBoxLayout()
        # ustala Group boxa ktory pozwala na wyswietlenie dodatkowych ramek/pol/wykresow wewnątrz
        group_box= QGroupBox()
        group_box.setLayout(self.__layout)
        #Mainuje group_boxa cntralnym wigdetem wysweitlanego okna, bez tego gruop_box nie bedzie wyswietlony
        self.setCentralWidget(group_box)
        self.show()

    def prepare_chart(self,lista,start_date,end_date):
        self.__chart = Rysuj(lista,start_date,end_date)
        # "wstawia" wykres do wnetrza okna
        self.__layout.addWidget(self.__chart)


