import pandas as pd


class ShopperTable:

    def __init__(self, store_model, time_frame):
        self.store_model = store_model
        self.time_frame = time_frame
        self.data_frame = None

    def create_table(self):
        day_list = []
        # create all the days
        for date in self.time_frame.dates:
            day_list.append(self.store_model.create_day(date))

        shopper_dict = {'Date': [], 'DayOfWeek': [], 'TimeIn': [], 'TimeSpent': [], 'IsSenior': []}

        for day in day_list:
            day_dict = day.create_shoppers()
            for key, value in day_dict.items():
                shopper_dict[key] += value

        self.data_frame = pd.DataFrame(shopper_dict)
        self.data_frame.reset_index()
        self.data_frame['ShopperId'] = self.data_frame.index
        self.data_frame.sort_values(by=['Date', 'TimeIn'], inplace=True)
        return self.data_frame

    def to_csv(self, path):
        if self.data_frame is None:
            self.create_table()

        return self.data_frame.to_csv(path)

