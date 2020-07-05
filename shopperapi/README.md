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
