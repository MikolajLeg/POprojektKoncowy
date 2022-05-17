

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

