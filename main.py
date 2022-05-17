

from GlowneOkno import MainWindow
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':

    # start_date = input("data początkową")
    # end_date = input("data konca ")
    start_date = '2009-S2'
    end_date = '2015-S2'

    app = QApplication([])
    window = MainWindow(start_date, end_date)
    window.show()
    app.exec_()
