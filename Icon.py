# #Create App icon in Python GUI Application
# import tkinter as tk
#
# class Icon:
#     def __init__(self):
#
#         app = tk.Tk()
#         #Application Title
#         app.title("Python GUI App with icon")
#         #Set App icon
#         app.iconbitmap(r'oip_eZL_icon.ico')
#
# # root = Tk()
# # root.title("Miejsce na nazwę aplikacji")
# # root.iconbitmap(r'oip_eZL_icon.ico')
# # root.mainloop
#
#
#
# app = tk.Tk()
# #Application Title
# app.title("Python GUI App with icon")
# #Set App icon
# app.iconbitmap(r'oip_eZL_icon.ico')

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

class Icon(QWidget):
    def __init__(self):
        super().__init__()

        self.icon()

    def icon(self):

        self.setWindowTitle("Nazwa Aplikacji")
        icon = QIcon('img.png')
        self.setWindowIcon(icon)

        self.show()

