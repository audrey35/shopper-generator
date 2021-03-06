"""
This module handles data and methods related to our representation of a shopper
"""
import numpy as np


class Shopper:
    """
    A Shopper that is visiting the store. The constructor takes in the Day the shopper is visiting
    the store at. Uses default values for all fields.
    """

    def __init__(self, day, time_in, is_sunny, percent_senior, day_modifiers):
        self.date = day.date
        self.day_of_week = day.day_of_week
        self.time_in = time_in
        self.is_sunny = is_sunny
        self.day_modifiers = day_modifiers
        self.time_spent = self.__generate_time_spent()
        self.percent_senior = percent_senior
        self.is_senior = np.random.choice(a=np.array([True, False]),
                                          p=[self.percent_senior, 1 - self.percent_senior])

    def __generate_time_spent(self):
        return self.day_modifiers.time_spent()

    def shopper_parameters_to_dictionary(self):
        """
        Returns this shoppers and its variables as a dictionary
        :return: dictionary with the wanted variables for a shopper
        """
        return {'Date': self.date, "DayOfWeek": self.day_of_week, "TimeIn": self.time_in,
                "TimeSpent": self.time_spent, "IsSenior": self.is_senior, "IsSunny": self.is_sunny}
