import pandas
import datetime
import calendar
import holidays
import numpy
import random
import numpy

pandas.set_option('display.max_rows', None)
pandas.set_option('display.max_columns', None)
pandas.set_option('display.width', None)
pandas.set_option('display.max_colwidth', -1)

"""
Also gibberish but useful to look back on
Works with bulk data rather than iterating per day
"""
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
        day = calendar.day_name[(start_date + datetime.timedelta(days=i+1)).weekday()]
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
    #else:
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
# user-defined/default variables
min_minute_spent = 6  # default from project spec
avg_minute_spent = 25  # default from project spec
max_minute_spent = 75  # default from project spec
std_minute_spent = 10  # arbitrary default

# Generate random float numbers with average and standard deviation from above.
# Count is set to 2 * len(shopperTable) because some of the generated numbers have to be removed.
# Source: https://stackoverflow.com/a/54896949
rand_minute_spent = numpy.random.normal(loc=avg_minute_spent, scale=std_minute_spent, size=len(shopperTable.index) * 2)

# Convert the float numbers to integers
rand_minute_spent = numpy.round(rand_minute_spent).astype(int)

# Remove numbers less than min_minute_spent
rand_minute_spent = rand_minute_spent[rand_minute_spent >= min_minute_spent]

# Remove numbers greater than max_minute_spent
rand_minute_spent = rand_minute_spent[rand_minute_spent <= max_minute_spent]

# Make rand_minute_spent length identical to shopperTable length
rand_minute_spent = rand_minute_spent[:len(shopperTable.index)]

# Set rand_minute_spent to timeSpent column in shopperTable
shopperTable['timeSpent'] = rand_minute_spent

# Populate Time In
## Evan: uniform distribution https://www.datacamp.com/community/tutorials/probability-distributions-python
#year, month, day, hour=0, minute=0, second=0
openTime = datetime.datetime(2020, 1, 1)
closingTime = datetime.datetime(2020, 1, 2)
# combine date with time to create datetime objects
# account for buffer before closing time
times = [random.random() * (closingTime - openTime) + openTime for i in range(len(shopperTable.index))]
shopperTable["timeIn"] = times

# Sunny
# Audrey: normal distribution with peak centered around July

# Create numpy array of random True/False for Sunny column
random_sunny = numpy.random.choice(a=numpy.array([True, False]), size=len(shopperTable.index))

# Populate Sunny column with the numpy array of random True/False
shopperTable['sunny'] = random_sunny

'''
# select beginning of May to end of August and get count
mask = shopperTable[(shopperTable['date'] >= '05/01/2018') & (shopperTable['date'] <= '08/31/2018')].count()[0]

# Create numpy array of random True/False for selected portion of Sunny column.
# Make True occur more frequently (70%) for summer months
random_sunny2 = numpy.random.choice(a=numpy.array([True, False]), size=mask, p=[0.7, 0.3])
# Confirm Date column type is datetime
# Source: https://stackoverflow.com/a/29370182
shopperTable['date'] = pandas.to_datetime(shopperTable['date'])

# Create numpy array of random True/False for selected portion of Sunny column.
# Make True occur more frequently (70%) for summer months
random_sunny2 = numpy.random.choice(a=numpy.array([True, False]), size=mask, p=[0.7, 0.3])

# Confirm Date column type is datetime
# Source: https://stackoverflow.com/a/29370182
shopperTable['date'] = pandas.to_datetime(shopperTable['date'])

# Replace Sunny column values for rows with date between 5/1/2018 to 8/31/2018
shopperTable['sunny'].mask((shopperTable['date'] >= '05/01/2018') & (shopperTable['date'] <= '08/31/2018'),
                            random_sunny2, inplace=True)
'''

# Print 100 random rows to check
print(shopperTable.head(10))
print(shopperTable.sample(n=100))
# Senior
percentSeniors = 0.2
seniors = numpy.random.choice(a=[True, False], size=len(shopperTable.index), p=[percentSeniors, 1-percentSeniors])
shopperTable["senior"] = seniors

# Holiday
## Carlo: get list of holidays within a given time
# https://pypi.org/project/holidays/
holidays = holidays.US()