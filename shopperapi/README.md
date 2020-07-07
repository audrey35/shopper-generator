# Shopper API

## Get a list of databases and collections
Returns a dictionary of all available databases and collections for each database.

**Required Arguments**
<br>
N/A

**Example**
<br>
*Sample request URI*: http://127.0.0.1:5000/list-databases
<br>
*Sample response*:
<br>
{
<br>
&nbsp;&nbsp;"admin": ["system.version"],
<br>
&nbsp;&nbsp;"config": ["system.sessions"],
<br>
&nbsp;&nbsp;"local": ["startup_log"],
<br>
&nbsp;&nbsp;"shoppers": ["shopper"],
<br>
&nbsp;&nbsp;"shoppers_db": ["parameters", "shoppers", "test_collection2", "test_collection"]
<br>
}

## Get a list of parameters
Returns a dictionary of all the parameters in the database and their info.

**Required Arguments**
<br>
N/A

**Example**
<br>
*Sample request URI*: http://127.0.0.1:5000/parameters
<br>
*Sample response*:
<br>
{
<br>
&nbsp;&nbsp;"documents": [
<br>
&nbsp;&nbsp;{
<br>
&nbsp;&nbsp;&nbsp;&nbsp;"_id": "5f04c7c7eab5d2983faa63ef",
<br>
&nbsp;&nbsp;&nbsp;&nbsp;"close_time": "21:00:00",
<br>&nbsp;&nbsp;&nbsp;&nbsp;"daily_average_traffic": {
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Friday": 2500,
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Monday": 800, 
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Saturday": 4000,
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Sunday": 5000,
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Thursday": 900,
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Tuesday": 1000,
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Wednesday": 1200
<br>&nbsp;&nbsp;&nbsp;&nbsp;},
<br>&nbsp;&nbsp;&nbsp;&nbsp;"day_modifiers": {
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"avg_time_spent": 25,
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"max_time_spent": 75,
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"min_time_spent": 6,
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"sunny_chance_percent": 0.3,
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"sunny_time_spent": 15,
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"sunny_traffic_percent": 0.4,
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"weekend_time_spent": 60
<br>&nbsp;&nbsp;&nbsp;&nbsp;},
<br>&nbsp;&nbsp;&nbsp;&nbsp;"dinner_rush": {
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"end_time": "18:30:00",
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"percent": 0.15,
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"start_time": "17:00:00",
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"time_spent": 10
<br>&nbsp;&nbsp;&nbsp;&nbsp;},
<br>&nbsp;&nbsp;&nbsp;&nbsp;"end_date": "Tue, 31 Mar 2020 00:00:00 GMT",
<br>&nbsp;&nbsp;&nbsp;&nbsp;"holiday_modifiers": {
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "day_before_percent": 0.4,
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"holiday_percent": 0.2,
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"week_before_percent": 0.15
<br>&nbsp;&nbsp;&nbsp;&nbsp;},
<br>&nbsp;&nbsp;&nbsp;&nbsp;"lunch_rush": {
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"end_time": "13:00:00",
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"percent": 0.1,
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"start_time": "12:00:00",
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"time_spent": 10
<br>&nbsp;&nbsp;&nbsp;&nbsp;},
<br>&nbsp;&nbsp;&nbsp;&nbsp;"open_time": "06:00:00",
<br>&nbsp;&nbsp;&nbsp;&nbsp;"senior_discount": {
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"day": "Tuesday",
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"end_time": "12:00:00",
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"max_time_spent": 60,
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"min_time_spent": 45,
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"percent": 0.2,
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"start_time": "10:00:00"
<br>&nbsp;&nbsp;&nbsp;&nbsp;}
<br>&nbsp;&nbsp;}
<br>&nbsp;]
<br>}

## Get all shoppers in a collection
Returns a dictionary of all shoppers in a collection. This may fail if the dataset is too large.

**Required Arguments**
<br>
Database name: name of the database.
<br>
Collection name: name of the collection.

**Example**
<br>
*Sample request URI*: http://127.0.0.1:5000/get-shoppers/shoppers/shopper
<br>
*Sample response*:
<br>
{
<br>
  "collection": "shopper",
  <br>
  "database": "shoppers",
  <br>
  "documents": [
  <br>
&nbsp;&nbsp;{
    <br>
&nbsp;&nbsp;&nbsp;&nbsp;"Date": "Wed, 03 Jan 2018 00:00:00 GMT",
      <br>
&nbsp;&nbsp;&nbsp;&nbsp;"DayOfWeek": "Monday",
      <br>
&nbsp;&nbsp;&nbsp;&nbsp;"IsSenior": true,
      <br>
&nbsp;&nbsp;&nbsp;&nbsp;"IsSunny": false,
      <br>
&nbsp;&nbsp;&nbsp;&nbsp;"TimeIn": "Wed, 03 Jan 2018 02:30:00 GMT",
      <br>
&nbsp;&nbsp;&nbsp;&nbsp;"TimeSpent": 30,
      <br>
&nbsp;&nbsp;&nbsp;&nbsp;"_id": 1
    <br>
&nbsp;&nbsp;},
    <br>
&nbsp;&nbsp;{
      <br>
&nbsp;&nbsp;&nbsp;&nbsp;"Date": "Sat, 03 Mar 2018 00:00:00 GMT",
      <br>
&nbsp;&nbsp;&nbsp;&nbsp;"DayOfWeek": "Wednesday",
      <br>
&nbsp;&nbsp;&nbsp;&nbsp;"IsSenior": false,
      <br>
&nbsp;&nbsp;&nbsp;&nbsp;"IsSunny": true,
      <br>
&nbsp;&nbsp;&nbsp;&nbsp;"TimeIn": "Sat, 03 Mar 2018 09:40:00 GMT",
      <br>
&nbsp;&nbsp;&nbsp;&nbsp;"TimeSpent": 30,
      <br>
&nbsp;&nbsp;&nbsp;&nbsp;"_id": 2
      <br>
&nbsp;&nbsp;}
    <br>
&nbsp;&nbsp;]
    <br>
}

## Get a list of shoppers based on parameter id
Returns a dictionary of all the parameters in the database and their info.

**Required Arguments**
<br>
Parameter-Id: the id of the parameters used to generate a set of shoppers

**Example**
<br>
*Sample request URI*: http://127.0.0.1:5000/parameters/5f0370cdc5dd25118cd273b4/shoppers
<br>
*Sample response*:
<br>
{
<br>
"shoppers": [
    <br>
&nbsp;&nbsp;&nbsp;&nbsp;{
      <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Date": "2020-03-06 00:00:00",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"DayOfWeek": "Friday",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"IsSenior": "False",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"IsSunny": "False",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"ShopperId": "147301",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"TimeIn": "2020-03-06 20:59:40",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"TimeSpent": "21",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"_id": "147301"
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"parameter_id": "5f04c7c7eab5d2983faa63ef"
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;},
<br>
&nbsp;&nbsp;&nbsp;&nbsp;{
      <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Date": "2020-03-06 00:00:00",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"DayOfWeek": "Friday",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"IsSenior": "False",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"IsSunny": "False",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"ShopperId": "146017",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"TimeIn": "2020-03-06 20:59:48.320000",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"TimeSpent": "25",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"_id": "146017"
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"parameter_id": "5f04c7c7eab5d2983faa63ef"
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;}
      <br>
&nbsp;&nbsp;&nbsp;]
<br>
}

## Get shoppers that visited within a date range
Returns a dictionary of shoppers that visited within a date range. The date range cannot be greater than 3 months.

**Required Arguments**
<br>
Datbase name: name of the database.
<br>
Start date: start date of the date range. (2018-03-04)
<br>
End date: end date of the date range. (2018-3-25)

**Example**
<br>
*Sample request URI:* 

*Sample response:*
<br>
{
<br>
&nbsp;&nbsp;"collections": {
  <br>
&nbsp;&nbsp;"shoppers": [
    <br>
&nbsp;&nbsp;&nbsp;&nbsp;{
      <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Date": "2020-03-06 00:00:00",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"DayOfWeek": "Friday",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"IsSenior": "False",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"IsSunny": "False",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"ShopperId": "147301",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"TimeIn": "2020-03-06 20:59:40",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"TimeSpent": "21",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"_id": "147301"
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;}
      <br>
&nbsp;&nbsp;&nbsp;],
      <br>
    "test_collection": [
    <br>
&nbsp;&nbsp;&nbsp;&nbsp;{
      <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Date": "2020-03-06 00:00:00",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"DayOfWeek": "Friday",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"IsSenior": "False",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"IsSunny": "False",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"ShopperId": "146017",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"TimeIn": "2020-03-06 20:59:48.320000",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"TimeSpent": "25",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"_id": "146017"
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;}
      <br>
&nbsp;&nbsp;&nbsp;]
      <br>
&nbsp;&nbsp;}
      <br>
      }

## Get senior shoppers that visited within a date range
Returns a dictionary of senior shoppers or non-senior shoppers that visited within a date range. The date range cannot be greater than 3 months.

**Required Arguments**
<br>
Datbase name: name of the database.
<br>
Is senior: true if selecting senior shoppers, false otherwise.
<br>
Start date: start date of the date range. (2018-03-04)
<br>
End date: end date of the date range. (2018-3-25)

**Example**
<br>
*Sample request URI:* http://127.0.0.1:5000/get-senior-shoppers/shoppers_db/true/2020-03-5/2020-03-6

*Sample response:*
<br>
{
<br>
&nbsp;&nbsp;"collections": {
  <br>
&nbsp;&nbsp;"shoppers": [
    <br>
&nbsp;&nbsp;&nbsp;&nbsp;{
      <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Date": "2020-03-06 00:00:00",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"DayOfWeek": "Friday",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"IsSenior": "True",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"IsSunny": "False",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"ShopperId": "147301",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"TimeIn": "2020-03-06 20:59:40",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"TimeSpent": "21",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"_id": "147301"
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;}
      <br>
&nbsp;&nbsp;&nbsp;],
      <br>
    "test_collection": [
    <br>
&nbsp;&nbsp;&nbsp;&nbsp;{
      <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Date": "2020-03-06 00:00:00",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"DayOfWeek": "Friday",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"IsSenior": "True",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"IsSunny": "False",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"ShopperId": "146017",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"TimeIn": "2020-03-06 20:59:48.320000",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"TimeSpent": "25",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"_id": "146017"
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;}
      <br>
&nbsp;&nbsp;&nbsp;]
      <br>
&nbsp;&nbsp;}
      <br>
      }

## Get sunny weekend shoppers that visited within a date range
Returns a dictionary of shoppers that visited on a sunny weekend within a date range. The date range cannot be greater than 3 months.

**Required Arguments**
<br>
Datbase name: name of the database.
<br>
Is sunny: true if selecting sunny days, false otherwise.
<br>
Is weekend: true if selecting weekends, false if selecting weekdays.
<br>
Start date: start date of the date range. (2018-03-04)
<br>
End date: end date of the date range. (2018-3-25)

**Example**
<br>
*Sample request URI:* http://127.0.0.1:5000/get-sunny-weekend-shoppers/shoppers_db/true/false/2020-03-05/2020-03-25

*Sample response:*
<br>
{
<br>
&nbsp;&nbsp;"collections": {
  <br>
&nbsp;&nbsp;"shoppers": [
    <br>
&nbsp;&nbsp;&nbsp;&nbsp;{
      <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Date": "2020-03-06 00:00:00",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"DayOfWeek": "Friday",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"IsSenior": "True",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"IsSunny": "True",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"ShopperId": "147301",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"TimeIn": "2020-03-06 20:59:40",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"TimeSpent": "21",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"_id": "147301"
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;}
      <br>
&nbsp;&nbsp;&nbsp;],
      <br>
    "test_collection": [
    <br>
&nbsp;&nbsp;&nbsp;&nbsp;{
      <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Date": "2020-03-06 00:00:00",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"DayOfWeek": "Friday",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"IsSenior": "True",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"IsSunny": "True",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"ShopperId": "146017",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"TimeIn": "2020-03-06 20:59:48.320000",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"TimeSpent": "25",
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"_id": "146017"
        <br>
&nbsp;&nbsp;&nbsp;&nbsp;}
      <br>
&nbsp;&nbsp;&nbsp;]
      <br>
&nbsp;&nbsp;}
      <br>
      }
