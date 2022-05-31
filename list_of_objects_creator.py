

# Creator generative pattern used to create of a list of Objects of desired class, basing on provided object creator
class ListOfObjectsCreator:
    def __init__(self, data, ObjectCreator):
        self.__data = data
        self.__list = list()
        self.__creator = ObjectCreator
        self.__make_list()

    def __make_list(self):
        # here we create a list of desired objects basing on provided data
        for k in self.__data.keys():
            self.__list.append(self.__creator.make_object(k, self.__data))
        # here we sort a list of our objects of chosen class basing on their name in alphabetical order
        self.__list.sort(key=lambda x: x.get_name())

    def get_list(self):
        return self.__list
