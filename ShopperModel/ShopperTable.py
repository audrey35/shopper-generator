import pandas as pd


class ShopperTable:
    """
    This class contains the objects necessary to create a shopper table and a
    method to create the shopper data
    """

    def __init__(self, store_model, time_frame):
        self.store_model = store_model
        self.time_frame = time_frame
        self.data_frame = None

    def create_table(self):
        """
        Populates this class with a data frame of the shoppers generated based
        on the passed in parameters
        :return: None
        """
        day_list = []
        # create all the days
        for date in self.time_frame.dates:
            day_list.append(self.store_model.create_day(date))

        shopper_dict = {'Date': [], 'DayOfWeek': [], 'TimeIn': [], 'TimeSpent': [],
                        'IsSenior': [], 'IsSunny': []}

        for day in day_list:
            day.create_shoppers()
            day_dict = day.shoppers
            for key, value in day_dict.items():
                shopper_dict[key] += value

        self.data_frame = pd.DataFrame(shopper_dict)
        self.data_frame.reset_index()
        self.data_frame['ShopperId'] = self.data_frame.index
        self.data_frame.sort_values(by=['Date', 'TimeIn'], inplace=True)
        return self.data_frame

    def to_csv(self, path):
        """
        Generates a csv of the shoppers given file path
        :param path: a filepath to save the generated shopper data
        :return: None
        """
        if self.data_frame is None:
            self.create_table()

        return self.data_frame.to_csv(path)
