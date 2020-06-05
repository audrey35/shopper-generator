class DayModifier:

    def __init__(self, config):
        self.sunny_percent = config.sunny_percent
        self.holiday_percent = config.holiday_percent
        self.day_before_holiday_percent = config.day_before_holiday_percent
        self.week_before_holiday_percent = config.week_before_holiday_percent

    def apply_sunny_percent(self, num_shoppers):
        return num_shoppers
    def holiday_percent(self, num_shoppers):
        return num_shoppers
    def day_before_holiday_percent(self, num_shoppers):
        return num_shoppers
    def week_before_holiday_percent(self, num_shoppers):
        return num_shoppers

class TimeDistribution:

    def __init__(self, config):

    def apply_time_distribution(self, dictionary):
    def apply_regular_time_spent(self):
    def apply_weekend_time_spent(self):
    def apply_lunch_time_spent(self, n):
    def apply_dinner_time_spent(self, timeIn):
    def apply_senior_time_spent(self, isSenior):


inputs: start time, end time, row count, min time spent, avg time spent, max time spent
time_dict = TimeColumn(configuration, row_count, )
output: {'time in': [],
         'time spent': [],
         'time out': []}

day_mod = DayModifier(configuration)

Saturday = 800 *

Saturday is holiday True
day_mod.apply_holiday_change(800) = 160

Saturday is sunny and weekend? False
day_mod.appy_sunny_change(160) = 224

Get list of
time_in = [224 datetime]

time_in(number_of_rows, open_time, close_time)
seniors(number_of_rows, percentage, tuesday_increase, day_of_week)
sunny = true or false

# Generally shoppers spend about 25 minutes in the store.
# The distribution ranges from about 6 minutes on the super-fast end, to about 75 minutes on the long end.

# Lunch time 12 - 1 is 10 mins
# dinner time 5 - 6:30 is 20 mins

# Weekends is 60 mins
# Weekend and sunny is <60 mins

# Regular day % of seniors is 20%
# Tuesday, more seniors come in from 10 - 12 pm and spend 45 - 60 minutes

time_distribution = TimeDistribution(config)
time_spent = []
# of shopper at lunch?
# of shopper at dinner?

for n in range(225): #??????


one_day_dict = {"Date": [224 dates], "DayOfWeek"; [Monday 224 times], "timeIn": [224 datetime valeus from distribution],
    "timeSpent": [224 int values representing minutes spent], "senior": [224 bool random chosen num of seniors],
    "holiday": [224 bool], "sunny": [224 bool]}





