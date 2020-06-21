class DayOfWeek:

    def __init__(self, day_name, shopper_traffic, senior_rush=None):
        self.day_name = day_name
        self.shopper_traffic = shopper_traffic
        self.senior_rush = senior_rush
        self.days = []

    def add_day(self, day):
        self.days.append(day)
