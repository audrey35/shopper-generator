import Day


class SunnyDay(Day):

    def __init__(self, percent_increase, open_time, close_time, date, num_of_shoppers,
                 lunch_rush=None, dinner_rush=None, senior_rush=None):
        self.percent_increase = percent_increase
        super().__init__(open_time, close_time, date, num_of_shoppers, lunch_rush, dinner_rush, senior_rush)

