from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QGroupBox, QWidget, QGridLayout, QPushButton, QTabWidget, QScrollArea, QFormLayout
from Buttons import AddPatchButton, PathButton


import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui, QtWidgets



class ExpWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # self.__inputer = None
        #
        # self.resize(1500, 1000)
        # self.__init_view()
        # self.tabs = QTabWidget()
        # self.start_view()


    # def __init_view(self):
    #
    #     self.setWindowTitle("Aplikacja")
    #     self.__layout = QGridLayout()
    #     # ustala Group boxa ktory pozwala na wyswietlenie dodatkowych ramek/pol/wykresow wewnątrz
    #     group_box = QGroupBox()
    #     group_box.setLayout(self.__layout)
    #     # Mainuje group_boxa cntralnym wigdetem wysweitlanego okna, bez tego gruop_box nie bedzie wyswietlony
    #     self.setCentralWidget(group_box)
    #     self.prep_lista()



        self.__inputer = PathButton()

        AddPatchButton("Dodaj Plik", self, self.__inputer)

        app = QtWidgets.QApplication(sys.argv)

        path = "C:/Users"
        fullpath = os.path.realpath(path)

        if not QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(fullpath)):
            print("failed")




# app = QtWidgets.QApplication(sys.argv)
#
# path = "C:/Users"
# fullpath = os.path.realpath(path)
#
# if not QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(fullpath)):
#     print("failed")


if __name__ == '__main__':


    app = QApplication([])
    window = ExpWindow()
    window.show()
    app.exec_()
