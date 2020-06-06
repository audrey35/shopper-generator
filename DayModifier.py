"""
Gibberish/Brainstorming
"""
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


if min_minute_spent == -1 & avg_minute_spent != -1 & max_minute_spent == -1:
# create a numpy array of random integer values with a mean of avg_minute_spent.
    time_spent = numpy.round(numpy.random.normal(loc=avg_minute_spent, size=row_count)).astype(int)
else:
    time_spent = numpy.round(numpy.random.normal(loc=avg_minute_spent, scale=round(avg_minute_spent / 2),
                                             size=row_count)).astype(int)

# numpy.clip is used to remove values less than min_minute_spent or greater than max_minute_spent without
# changing the mean of the numpy array
# numpy.clip source: https://stackoverflow.com/a/44603019
time_spent = numpy.clip(time_spent, min_minute_spent, max_minute_spent)

times = numpy.random.rand(row_count) * (closing_time - open_time) + open_time

def get_sunny(the_date, day_of_week, row_count):
    if day_of_week == 'Saturday' or day_of_week == 'Sunday':
        if 4 < the_date.month < 9:  # 70% sunny from May to August
            sunny = [numpy.random.choice(a=numpy.array([True, False]), p=[0.7, 0.3])] * row_count
        else:
            sunny = [numpy.random.choice(a=numpy.array([True, False]))] * row_count
    else:
        sunny = [False] * row_count
    return sunny



