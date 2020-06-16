import random
import time


class Rush:
    """
    Class that represents a period of time in which customers will come into the store for a specific rush crowd.
    eg. a Lunch rush
    """

    def __init__(self, start_time, end_time, time_spent, percent):
        self.start_time = start_time
        self.end_time = end_time
        self.time_spent = time_spent
        self.percent = percent

    def percent_of(self, num):
        return round(self.percent * num)

    def calculate_time_spent(self, std=5):
        return round(random.gauss(self.time_spent, std))

