
from CzytnikPliku import Czytnik
from Panstwo import Kraj


class DataGrinder:
    def __init__(self, sciezka):

        NowyCzytnik = Czytnik()
        self.__sciezka = sciezka
        self.__lista = list()
        self.__dane = NowyCzytnik.read_file(self.__sciezka)
        self.__make_list()

    def __make_list(self):
        Belgium = Kraj("Belgium", self.__dane)
        Czechia = Kraj("Czechia", self.__dane)
        Germany = Kraj("Germany", self.__dane)
        Ireland = Kraj("Ireland", self.__dane)
        Spain = Kraj("Spain", self.__dane)
        Kosovo = Kraj("Kosovo", self.__dane)
        Bosnia = Kraj("Bosnia", self.__dane)
        Poland = Kraj("Poland", self.__dane)

        self.__lista.append(Belgium)
        self.__lista.append(Bosnia)
        self.__lista.append(Kosovo)
        self.__lista.append(Ireland)
        self.__lista.append(Spain)
        self.__lista.append(Poland)
        self.__lista.append(Czechia)
        self.__lista.append(Germany)

    def get_list(self):
        return self.__lista
