import pandas
import datetime
import calendar
import holidays
import random
import numpy

pandas.set_option('display.max_rows', None)
pandas.set_option('display.max_columns', None)
pandas.set_option('display.width', None)
pandas.set_option('display.max_colwidth', None)

# Create the dataframe with shopper id and day of week columns
cols = ['ShopperID', 'DayOfWeek']
shopperTable = pandas.DataFrame(columns=cols)


# calculate number of Mondays, ..., Sundays between 1/1/2018 and 12/31/2019
def weekday_count(start, end):
    # https://stackoverflow.com/a/43692648
    start_date = datetime.datetime.strptime(start, '%m/%d/%Y')
    end_date = datetime.datetime.strptime(end, '%m/%d/%Y')
    week = {}
    for i in range((end_date - start_date).days):
        day = calendar.day_name[(start_date + datetime.timedelta(days=i + 1)).weekday()]
        week[day] = week[day] + 1 if day in week else 1
    return week


weekdayCountDictionary = weekday_count("01/01/2018", "12/31/2019")

for weekDay, dayCount in weekdayCountDictionary.items():
    if weekDay == 'Monday':
        weekdayCountDictionary[weekDay] = dayCount * 800
    elif weekDay == "Tuesday":
        weekdayCountDictionary[weekDay] = dayCount * 1000
    elif weekDay == "Wednesday":
        weekdayCountDictionary[weekDay] = dayCount * 1200
    elif weekDay == "Thursday":
        weekdayCountDictionary[weekDay] = dayCount * 900
    elif weekDay == "Friday":
        weekdayCountDictionary[weekDay] = dayCount * 2500
    elif weekDay == "Saturday":
        weekdayCountDictionary[weekDay] = dayCount * 4000
    elif weekDay == "Sunday":
        weekdayCountDictionary[weekDay] = dayCount * 5000
    # else:
    # todo: throw exception

# Populate dayOfWeek
count = 1
for weekDay, dayCount in weekdayCountDictionary.items():
    weekDayTable = pandas.DataFrame(index=range(dayCount))
    weekDayTable['dayOfWeek'] = weekDay
    if (count == 1):
        shopperTable = weekDayTable
        count += 1
    else:
        shopperTable = shopperTable.append(weekDayTable)

# Populate ShopperID
shopperTable.reset_index()
shopperTable['shopperId'] = shopperTable.index + 1


# Populate dates
## Carlo
def find_dates(start, end):
    """
    Find the dates of each day in the week between a start date and end date

    :param start: start of date range as string in format 'YYYY-MM-DD'
    :param end:   end of date range as string in format 'YYYY-MM-DD'
    :return:      dictionary of {DayOfWeek: [date1, date2, ...]}
    """
    start_date = datetime.date.fromisoformat(start)
    end_date = datetime.date.fromisoformat(end)
    delta = datetime.timedelta(days=1)
    week = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []}

    while start_date <= end_date:
        day = calendar.day_name[start_date.weekday()]
        week[day].append(start_date)
        start_date += delta

    return week


# Populate Time Spent
# Audrey: normal distribution


def get_time_spent(row_count, min_minute_spent=6, avg_minute_spent=25, max_minute_spent=75):
    """
    Returns a list of time spent.
    :param row_count: number of rows in the table.
    :param min_minute_spent: minimum minutes a customer spent.
    :param avg_minute_spent: average minutes a customer spent.
    :param max_minute_spent: maximum minutes a customer spent.
    :return: a list of time spent. Number of items determined by row_count.
    """
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
    return time_spent


# Populate Time In
## Evan: uniform distribution https://www.datacamp.com/community/tutorials/probability-distributions-python
# year, month, day, hour=0, minute=0, second=0

def get_time_in(row_count, open_time=datetime.datetime(2020, 1, 1, 6, 0),
                closing_time=datetime.datetime(2020, 1, 1, 21, 0)):
    """
    Returns a list of time in.
    :param row_count: number of rows in the table. Used to determine number of items in the output list.
    :param open_time: time the store opens.
    :param closing_time: time the store closes.
    :return: a list of time in.
    """
    # combine date with time to create datetime objects
    # account for buffer before closing time
    times = [random.random() * (closing_time - open_time) + open_time for i in range(row_count)]
    return times


# Sunny
# Audrey: normal distribution with peak centered around July
def get_sunny(date_day_of_week_dict):
    day_of_week_list = date_day_of_week_dict['DayOfWeek']
    date_list = date_day_of_week_dict['Date']
    dates = {}
    sunny = []
    i = 0
    for day_of_week in day_of_week_list:
        a_date = date_list[i]
        if a_date in dates:
            sunny.append(dates[a_date])
        else:
            if day_of_week == 'Saturday' or day_of_week == 'Sunday':
                if 4 < a_date.month < 9:  # 70% sunny from May to August
                    boolean = numpy.random.choice(a=numpy.array([True, False]), p=[0.7, 0.3])
                else:
                    boolean = numpy.random.choice(a=numpy.array([True, False]))
            else:
                boolean = False
            sunny.append(boolean)
            dates[a_date] = boolean
        i += 1
    return sunny


# Senior
def get_senior(day_of_week_time_in_dict, tuesday_senior_percent=.4, usual_senior_percent=.2):
    day_of_week_list = day_of_week_time_in_dict['DayOfWeek']
    time_in_list = day_of_week_time_in_dict['TimeIn']
    senior = []
    i = 0
    for day_of_week in day_of_week_list:
        if day_of_week == 'Tuesday' and time_in_list[i].hour in [10, 11, 12]:
            senior.append(numpy.random.choice(a=[True, False], p=[usual_senior_percent, 1 - usual_senior_percent]))
        else:
            senior.append(numpy.random.choice(a=[True, False], p=[tuesday_senior_percent, 1 - tuesday_senior_percent]))
    return senior


# Possible input: list of shopper counts
shopper_count_by_day = [800, 1000, 1200, 900, 2500, 4000, 5000]

# Possible input: start and end date range
start = '2019-01-01'
end = '2020-12-31'

# Range of dates
date_list = pandas.date_range(start, end)

# Get holiday list
holidays = holidays.US()

# create dictionary to fill with values
shopper_dict = {"DayOfWeek": [], "Date": []}

# loop through each date
for date in date_list:
    day_int = date.dayofweek
    day_of_week = calendar.day_name[day_int]

    num_of_shoppers = shopper_count_by_day[day_int]
    if date in holidays:
        num_of_shoppers = round(0.2 * num_of_shoppers)

    shopper_dict["DayOfWeek"] += [day_of_week] * num_of_shoppers
    shopper_dict["Date"] += [date.date()] * num_of_shoppers

row_count = len(shopper_dict['Date'])

shopper_dict.update({'Sunny': get_sunny({'Date': shopper_dict['Date'], 'DayOfWeek': shopper_dict['DayOfWeek']})})

shopper_dict.update({'TimeIn': get_time_in(row_count)})

shopper_dict.update({'TimeSpent': get_time_spent(row_count)})

shopper_dict.update({'Senior': get_senior({'TimeIn': shopper_dict['TimeIn'], 'DayOfWeek': shopper_dict['DayOfWeek']})})

shopperTable = pandas.DataFrame(shopper_dict)

# Print 100 random rows to check
print(shopperTable.head(10))
print(shopperTable.sample(n=100))
