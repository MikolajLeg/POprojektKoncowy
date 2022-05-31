

# class responsible for extracting data from selected file and returning it as dictionary
class FileReader:

    def __init__(self, set_loader_value_method):
        self.__data = dict()
        self.__set_loading_progress_method = set_loader_value_method
        self.__all_lines = None
        self.__lines = None
        self.__dates = None

    # method which opens file based on provided filepath
    def read_file(self, filepath):
        with open(filepath, "r") as file:
            # read file
            self.__all_lines = file.readlines()[0:]
            # assigns first line (containing dates) do variable self.__dates via self.__prepare_dates()method
            self.__prepare_dates()

            # removes starting lines, leaving only those with data
            self.__lines = self.__all_lines[4:]
            length = len(self.__lines)
            times = 50/length
            progress = 50.1

            for line in self.__lines:
                progress += times
                self.__set_loading_progress_method(progress)
                # replaces commas inside prices to dots, while leaving commas outside prices
                dot_comma = False
                for i in range(0, len(line)):
                    if line[i] == '"':
                        dot_comma = not dot_comma
                    if line[i] == ",":
                        if dot_comma:
                            line = line[:i] + '.' + line[i+1:]

                line = line.rstrip("\n")
                # removes unnecessary quotation mark
                line = line.replace('"', "")
                line = line.replace(':', 'no data')

                # splits line to singular prices basing on outer commas
                line = line.split(',')
                name = line[0]
                name = name.split("(")
                name = name[0]

                price = list()
                # place prices for actually chosen country into list
                for i in range(1, len(line)):
                    if line[i] == "no data":
                        price.append(line[i])
                    else:
                        price.append(float(line[i]))

                # energy prices for country are assigned to corresponding dates
                    # and placed into dictionary with country name serving as key
                count = 1
                self.__data[name] = dict()
                for p in price:
                    actual_date = self.__dates[count]
                    self.__data[name][actual_date] = p
                    count += 1

        return self.__data

    def __prepare_dates(self):
        self.__dates = self.__all_lines[0]
        # removes \n sign from end of the line
        self.__dates = self.__dates.rstrip("\n")
        # splits line into specific dates
        self.__dates = self.__dates.split(",")


# class used to work on data, it returns lists of dates and costs from start date to end date for specific country
class DataGrinder:
    def __init__(self):
        self.__dates = list()
        self.__costs = list()
        self.__check = False

    def grind_data(self, start_date, end_date, country):

        for date, cost in country.get_dates_and_cost().items():

            # starts appending dates/costs after start date is reached
            if date == start_date:
                self.__check = not self.__check

            if self.__check:
                if cost == 'no data':
                    self.__dates.append(date)
                    self.__costs.append(None)
                else:
                    self.__dates.append(date)
                    self.__costs.append(cost)

            # ends appending dates/costs after end date is reached
            if date == end_date:
                self.__check = not self.__check
        return self.__dates, self.__costs
