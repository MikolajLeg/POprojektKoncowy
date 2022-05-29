
from PyQt5.QtWidgets import  QFileDialog, QApplication, QMainWindow ,QPushButton , QWidget, QVBoxLayout
from datetime import date
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch
from tabulate import tabulate
from reportlab.platypus import  Table, TableStyle



class PdfReportGenerator:

    def __init__(self):
        self.__title =  "pdf"
        self.__country_list = list()
        self.__dates_and_prices_list = list()


    def create_and_save_pdf(self,filepath, chart, countries, pagesize=A4):
        pdf_template = self.__create_pdf_template(filepath, chart, countries, pagesize)
        pdf_template.setTitle(self.__title)
        pdf_template.save()

    def __create_pdf_template(self, filepath, chart, countries, pagesize):
        self.__get_data(countries)
        img = self.__turn_chart_to_img(chart)
        canvas = Canvas(filepath, pagesize=pagesize)
        canvas.setFont("Times-Roman",20)
        title = " test title"
        title_offset, img_offset, data_offset = 50, 500, 1200
        title_x, title_y = A4[0] / 2, A4[1] - title_offset
        chart_x, chart_y = 0, A4[1] - img_offset
        data_x, data_y =  30, A4[1] - img_offset

        canvas.drawCentredString(title_x, title_y, title)
        canvas.drawImage(img,chart_x,chart_y, 600, 450)
        print("drawstring")
        i = 0
        # self.t.wrapOn(canvas, 2, 2)
        # self.t.drawOn(canvas, 2, 2)

        textobject = canvas.beginText(data_x,data_y)
        num_of_page = 0
        #textobject.setTextOrigin(data_x, data_y)
        textobject.setFont("Times-Roman",20)
        for country in self.__country_list:
            textobject.textLine(country)
            print("Y")
            print(textobject.getY())
            if textobject.getY() < 0:
                textobject.setTextOrigin(data_x, data_y)
                canvas.drawText(textobject)
                textobject = None
                num_of_page += 1
                canvas.showPage()
                data_y = A4[1] -25
                textobject = canvas.beginText(data_x,data_y)
                textobject.setFont("Times-Roman", 20)
                print(data_y)
        textobject.setTextOrigin(data_x, data_y)
        canvas.drawText(textobject)

        # canvas.showPage()

        #canvas.drawString(self.__tab, data_x, data_y)
        #canvas.drawString(self.t,data_x, data_y)

        return canvas

    def __turn_chart_to_img(self, chart):

        img_data = chart.get_img()
        img = ImageReader(img_data)

        return img

    def __get_data(self, countries):
        for country in countries:
            self.__country_list.append(country.get_name())
            for d, price in country.get_dates_and_cost().items():
                l = list()
                l.append(d)
                l.append(price)
                self.__dates_and_prices_list.append(l)

        self.t = Table(self.__country_list)



