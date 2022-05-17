
from CzytnikPliku import Czytnik



class DataGrinder:
    def __init__(self, sciezka):

        # tworzy czytnik ktory bedzie służył do odczytywania danych
        NowyCzytnik = Czytnik()
        self.__sciezka = sciezka
        self.__dane = NowyCzytnik.read_file(self.__sciezka)

    def get_dane(self):
        return self.__dane


# wzorzec wytworzczy do tworzenia listy obiektow na podstawie podanych danych
class ListOfObjectsCreator:
    def __init__(self, dane, ObjectCreator):
        self.__dane = dane
        self.__lista = list()
        self.__Creator = ObjectCreator
        self.__make_list()


    def __make_list(self):
        for k in self.__dane.keys():
            self.__lista.append(self.__Creator.make_object(k, self.__dane))


    def get_list(self):
        return self.__lista

