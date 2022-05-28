
from PyQt5.QtWidgets import  QFileDialog, QApplication, QMainWindow ,QPushButton , QWidget, QVBoxLayout
from datetime import date
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas



class PdfReportGenerator:

    def __init__(self):
        self.__title =  "pdf"

    def create_and_save_pdf(self,filepath, chart, pagesize=A4):
        pdf_template = self.__create_pdf_template(filepath, chart, pagesize)
        pdf_template.setTitle(self.__title)
        pdf_template.save()

    def __create_pdf_template(self, filepath, chart, pagesize):
        img = self.__turn_chart_to_img(chart)
        canvas = Canvas(filepath, pagesize=pagesize)
        canvas.setFont("Times-Roman",20)
        title = " test title"
        title_offset, img_offset = 50, 600
        title_x, title_y = A4[0] / 2, A4[1] - title_offset
        chart_x, chart_y = 0, A4[1] - img_offset

        canvas.drawCentredString(title_x, title_y, title)
        canvas.drawImage(img,chart_x,chart_y, 600, 450)

        return canvas

    def __turn_chart_to_img(self, chart):

        img_data = chart.get_img()
        img = ImageReader(img_data)

        return img





# class ButtonView(QWidget):
#     def __init__(self):
#         super().__init__()
#
#         self.setWindowTitle("Button view")
#         width, height = 300, 150
#         self.setFixedSize(width, height)
#
#         click_me_btn = PdfSaveButton("Please, click me now!")
#
#         layout = QVBoxLayout()
#         layout.addWidget(click_me_btn)
#         self.setLayout(layout)
#
#         self.show()



# if __name__ == "__main__":
#
#
#
#     app = QApplication([])
#
#     button = ButtonView()
#
#     app.exec_()