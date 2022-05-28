import os
import sys
#from Buttons import AddPatchButton
from PyQt5.QtWidgets import QPushButton, QProgressBar, QFileDialog, QHBoxLayout

from file_chooser import Czytnik


class FileLoader(QHBoxLayout):

    def __init__(self, btn_name, okno):
        super().__init__()

        self.__okno = okno
        self.__create_all(btn_name)

    def __create_all(self, btn_name="Select file", parent=None):
        self.__file_loader_dialog_btn = self.__create_file_loader_dialog_btn(btn_name)
        self.__loader = QProgressBar(parent)

        self.addWidget(self.__file_loader_dialog_btn)
        self.addWidget(self.__loader)

    def __create_file_loader_dialog_btn(self, btn_name):
        loader_btn = QPushButton(btn_name)
        loader_btn.clicked.connect(self.__choose_and_read_file)

        return loader_btn

    def __choose_and_read_file(self):
        self.__loader.setValue(1)
        parent = None
        current_dir = os.path.dirname(sys.argv[0])
        self.__loader.setValue(10)
        options = QFileDialog.DontUseNativeDialog
        self.__loader.setValue(20)
        self.maybe_selected_file, _ = QFileDialog.getOpenFileName(parent, "Choose csv file",
                                                             current_dir, "CSV (*.csv);;All Files (*)",
                                                             options=options)
        self.__loader.setValue(40)
        if self.maybe_selected_file:
            self.__loader.setValue(50)
            self.__loader.setValue(100)
            # auto_btn = AddPatchButton("autoprzycisk", self,  self.maybe_selected_file)
            # auto_btn.clicked()
            print(self.maybe_selected_file)
            self.__okno.set_path(self.maybe_selected_file)
            return self.maybe_selected_file

        else:
            print("sth wrong???")
            self.__loader.setValue(1)


