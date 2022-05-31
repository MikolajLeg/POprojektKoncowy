

# class responsible for storing data regarding specific country
class Country:
    def __init__(self, country_name, data):
        self.__name = country_name
        self.__prices = dict()
        self.__add_data(data)
        self.__status = False

    def __add_data(self, dictionary):
        for name, item in dictionary.items():
            # transfers data from outer dictionary to Country class object
            if name == self.__name:
                for date, price in item.items():
                    self.__prices[date] = price

    def get_dates_and_cost(self):
        return self.__prices

    def get_name(self):
        return self.__name

    # changes country status to show if country should be displayed on map/chart or not
    def flip_status(self):
        self.__status = not self.__status

    def get_status(self):
        return self.__status

    def __repr__(self):
        name = self.__class__.__name__
        attributes = {k.split("__")[-1]: v for k, v in self.__dict__.items()}
        return f"{name}: {attributes} "


class ObjectCreator:
    def __init__(self):
        pass

    def make_object(self, *args):
        pass


class CountryCreator(ObjectCreator):

    def __init__(self):
        super().__init__()

    def make_object(self, name, dane):
        super().make_object()
        return Country(name, dane)
