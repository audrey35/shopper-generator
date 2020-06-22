from random import random

from ShopperModel import Shopper, Util
import datetime
import calendar
import numpy as np


class Day:
    """
    The Day represent a specific day for the grocery store. It contains necessary information to generate
    a list of shoppers that has visited the store at the specific date.
    """
    def __init__(self, store_model, num_of_shoppers, date):
        self.store_model = store_model
        self.open_time = store_model.open_time
        self.close_time = store_model.close_time
        self.date = date
        self.num_of_shoppers = num_of_shoppers
        self.day_of_week = calendar.day_name[date.dayofweek]
        self.percent_senior = store_model.percent_senior
        self.shoppers = {"Date": [], "DayOfWeek": [], "TimeIn": [], "TimeSpent": [],
                         "IsSenior": [], "IsSunny": []}
        self.sunny_modifiers = self.store_model.sunny_modifiers
        self.is_sunny = np.random.choice(a=np.array([True, False]), p=[self.sunny_modifiers.sunny_chance_percent,
                                                                       1 - self.sunny_modifiers.sunny_chance_percent])
        if date.dayofweek in [5, 6]:
            self.is_weekend = True
        else:
            self.is_weekend = False

    def create_shoppers(self):
        lunch_percent = self.store_model.lunch_rush.percent
        lunch_start = self.store_model.lunch_rush.start_time
        lunch_start2 = datetime.datetime.combine(self.date, lunch_start)
        lunch_end = self.store_model.lunch_rush.end_time
        lunch_end2 = datetime.datetime.combine(self.date, lunch_end)
        lunch_avg_time_spent = self.store_model.lunch_rush.time_spent

        dinner_percent = self.store_model.dinner_rush.percent
        dinner_start = self.store_model.dinner_rush.start_time
        dinner_start2 = datetime.datetime.combine(self.date, dinner_start)
        dinner_end = self.store_model.dinner_rush.end_time
        dinner_end2 = datetime.datetime.combine(self.date, dinner_end)
        dinner_avg_time_spent = self.store_model.dinner_rush.time_spent

        seniorhour_start = self.store_model.senior_discount.start_time
        seniorhour_start2 = datetime.datetime.combine(self.date, seniorhour_start)
        seniorhour_end = self.store_model.senior_discount.end_time
        seniorhour_end2 = datetime.datetime.combine(self.date, seniorhour_end)
        senior_max_time_spent = self.store_model.senior_discount.max_time_spent
        senior_min_time_spent = self.store_model.senior_discount.min_time_spent

        # TODO weekend values
        weekend_increase = 0.4
        weekend_avg_time_spent = 60
        sunny_weekend_avg_time_spent = self.sunny_modifiers.sunny_time_spent

        times = Util.random_datetimes(datetime.datetime.combine(self.date, self.open_time),
                                      datetime.datetime.combine(self.date, self.close_time),
                                      self.num_of_shoppers)

        for time_in in times:
            newShopper = Shopper.Shopper(self, time_in, self.is_sunny, self.store_model.percent_senior)
            # lunch_percent more lunch shoppers than any other time
            if (np.random.rand() < lunch_percent) and not (lunch_start2 < newShopper.time_in < lunch_end2):
                temp = Util.random_datetimes(datetime.datetime.combine(self.date, lunch_start),
                                             datetime.datetime.combine(self.date, lunch_end), 1)
                newShopper.time_in = temp[0]
                newShopper.time_spent = lunch_avg_time_spent
            # dinner_percent more dinner shoppers than any other time
            if (np.random.rand() < dinner_percent) and not (dinner_start2 < newShopper.time_in < dinner_end2):
                temp = Util.random_datetimes(datetime.datetime.combine(self.date, dinner_start),
                                             datetime.datetime.combine(self.date, dinner_end), 1)
                newShopper.time_in = temp[0]
                newShopper.time_spent = dinner_avg_time_spent
            # check weekend
            if self.is_weekend:
                if self.is_sunny and np.random.rand() < weekend_increase:
                    newShopper.time_spent = sunny_weekend_avg_time_spent
                else:
                    newShopper.time_spent = weekend_avg_time_spent
            # senior hours
            if calendar.day_name[self.date.dayofweek] == self.store_model.senior_discount.day_name and not \
                    (seniorhour_start2 < newShopper.time_in < seniorhour_end2):
                temp = Util.random_datetimes(datetime.datetime.combine(self.date, seniorhour_start),
                                             datetime.datetime.combine(self.date, seniorhour_end), 1)
                newShopper.time_in = temp[0]
                newShopper.time_spent = random.randint(senior_min_time_spent, senior_max_time_spent)

            for key, value in newShopper.shopper_parameters_to_dictionary().items():
                self.shoppers[key].append(value)