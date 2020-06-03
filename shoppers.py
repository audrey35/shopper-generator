import pandas
import datetime
import calendar

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
print(weekday_count("01/01/2018", "12/31/2019"))

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
print(weekdayCountDictionary)
count = 1
for weekDay, dayCount in weekdayCountDictionary.items():
    weekDayTable = pandas.DataFrame(index=range(dayCount))
    weekDayTable['dayOfWeek'] = weekDay
    if (count == 1):
        shopperTable = weekDayTable
        count += 1
    else:
        shopperTable = shopperTable.append(weekDayTable)
    print(weekDay + " " + str(weekDayTable.shape))

# Populate ShopperID
shopperTable.reset_index()
shopperTable['shopperId'] = shopperTable.index + 1

print(shopperTable.shape)
print(shopperTable.head(5))

# Populate dates
## Carlo

# Populate Time Spent
## Audrey: normal distribution
minimumMinuteSpent = 6
averageMinuteSpent = 25
maximumMinuteSpent = 75

# Populate Time In
## Evan:   uniform distribution https://www.datacamp.com/community/tutorials/probability-distributions-python

# Sunny
## Audrey: normal distribution with peak centered around July

# Senior
## Evan: 20% of shoppers for any given day are seniors

# Holiday
## Carlo: get list of holidays within a given time