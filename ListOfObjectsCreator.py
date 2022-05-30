

# Creator generative pattern used to create of a list of Objects of desired class, basing on provided object creator
class ListOfObjectsCreator:
    def __init__(self, dane, ObjectCreator):
        self.__dane = dane
        self.__lista = list()
        self.__Creator = ObjectCreator
        self.__make_list()

    def __make_list(self):
        # here we create a list of desired objects basing on provided data
        for k in self.__dane.keys():
            self.__lista.append(self.__Creator.make_object(k, self.__dane))
        # here we sort a list of our objects of chosen class basing on their name in alphabetical order
        self.__lista.sort(key=lambda x: x.get_name())

    def get_list(self):
        return self.__lista
