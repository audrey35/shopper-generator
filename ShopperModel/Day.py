from ShopperModel import Shopper, Util
import datetime
import pandas as pd
import numpy as np


class Day:
    """
    The Day represent a specific day for the grocery store. It contains necessary information to generate
    a list of shoppers that has visited the store at the specific date.
    """

    def __init__(self, store_model, day_of_week, date):
        self.open_time = store_model.open_time
        self.close_time = store_model.close_time
        self.date = date
        self.num_of_shoppers = day_of_week.num_of_shoppers
        self.day_of_week = day_of_week.name
        self.percent_senior = store_model.percent_senior
        self.shoppers = []
        if date.dayofweek in [5, 6]:
            self.is_weekend = True
        else:
            self.is_weekend = False

    def create_shoppers(self, lunch_percent, dinner_percent):

        lunch_shoppers = round(self.num_of_shoppers * lunch_percent)
        dinner_shoppers = round(self.num_of_shoppers * dinner_percent)
        overall_shoppers = self.num_of_shoppers - lunch_shoppers - dinner_shoppers

        # TODO: pull out as constants
        lunch_start = datetime.time(12, 0)
        lunch_end = datetime.time(13, 0)

        dinner_start = datetime.time(17, 0)
        dinner_end = datetime.time(18, 30)

        times = Util.random_datetimes(pd.Timestamp.combine(self.date, self.open_time),
                                      pd.Timestamp.combine(self.date, self.close_time),
                                      overall_shoppers)

        lunch_times = Util.random_datetimes(pd.Timestamp.combine(self.date, lunch_start),
                                            pd.Timestamp.combine(self.date, lunch_end),
                                            lunch_shoppers)

        dinner_times = Util.random_datetimes(pd.Timestamp.combine(self.date, dinner_start),
                                             pd.Timestamp.combine(self.date, dinner_end),
                                             dinner_shoppers)

        shoppers = []

        for time_in in times:
            if np.random.choice(a=np.array([True, False]), p=[self.percent_senior, 1 - self.percent_senior]):
                shoppers.append(Shopper.SeniorShopper(self, time_in))
            else:
                if self.is_weekend:
                    shoppers.append(Shopper.WeekendShopper(self, time_in))
                else:
                    shoppers.append(Shopper.Shopper(self, time_in))

        for time_in in lunch_times:
            shoppers.append(Shopper.LunchShopper(self, time_in))

        for time_in in dinner_times:
            shoppers.append(Shopper.DinnerShopper(self, time_in))

        self.shoppers = shoppers

    def shoppers_to_dict(self):

        day_dict = {'Date': [], 'DayOfWeek': [], 'TimeIn': [], 'TimeSpent': [], 'IsSenior': []}

        for shopper in self.shoppers:
            for key, value in shopper.shopper_parameters_to_dictionary().items():
                day_dict[key].append(value)

        return day_dict
