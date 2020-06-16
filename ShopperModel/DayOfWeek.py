class DayOfWeek:

    def __init__(self, name, shopper_traffic, senior_rush=None):
        self.day_of_week = name
        self.shopper_traffic = shopper_traffic
        self.senior_rush = senior_rush
        self.days = []

    def add_day(self, day):
        self.days.append(day)
