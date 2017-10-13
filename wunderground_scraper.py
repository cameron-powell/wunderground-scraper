""" Module: wunderground_scraper.py

The purpose of this module is to:
1) Provide methods to get location and date inputs from the user
2) Provide methods for scraping requested values off of the wunderground
results page
4) Provide methods to convert those results into a JSON object and return them
to the user
5) Provide an entrypoint to the program to execute all this functionality

This module can be run by navigating to the root project directory and running
the following command:

'python wunderground_scraper.py'

This will execute all of the code enclosed in the if __name__ == '__main__'
block.
NOTE: This assumes you are running within an activated virtual environment
and have the project's requirements already installed.  See the project README
for instructions on setting that up.
"""
import calendar
import datetime
import re
import requests
import sys
from bs4 import BeautifulSoup


def validate_month(month_string):
    """ Takes in a month string provided by the user and, using a regex,
    validates that this is a valid month string.
    Months should be numeric between 1 and 12

    :param month_string:
    :return boolean: True if is valid month, False otherwise
    """
    regex = r'^[1-9][0-2]{,1}$'
    return re.search(regex, month_string) is not None


def validate_day(day_string, month_string):
    """ Validates that the user provided day_string is a valid option.
    Ensures day_string is the correct number of digits
    Ensures that day_string is in the correct range depending on the month
    NOTE:  Leap year validation is handled in the validate_year function.

    :param day_string: A user inputted day_string to validate
    :param month_string: A validated month string
    :return: True if valid, False if invalid
    """
    regex = r'^\d{1,2}$'
    # Make sure it's a valid number of digits (one or two)
    if re.search(regex, day_string):
        day_num = int(day_string)
        # Make sure it's at least the first of a month
        if day_num < 1:
            return False
        # Feb only has 28-29 days.
        # Validates if 29 is valid (on leap years) in year validation
        if month_string in ['2'] and day_num > 29:
            return False
        # Validate months with only 30 days
        elif month_string in ['4', '6', '9', '11'] and day_num > 30:
            return False
        # Validate other months with 31 days
        elif day_num > 31:
            return False
        return True
    return False


def validate_year(year_string, month_string, day_string):
    """ Takes in a user inputted year, and validated month/day strings.
    Makes sure that the year is
    1) A Valid 4 digit year
    2) A valid year if the user claimed this is a leap year
        (by providing 2 (feb) as the month and 29 as the day)
    Returns true if is a valid year, false if it is not a valid year.

    :param year_string: User inputted string containing year to validate
    :param month_string: Validated numeric month as a string
    :param day_string: Validated numeric day as a string
    :return: True if year is valid, False if year is not valid
    """
    # Make sure year has 4 digits
    regex = r'^\d\d\d\d$'
    if re.search(regex, year_string):
        # Make sure feb 29 isn't valid unless leap year
        year_num = int(year_string)
        day_num = int(day_string)
        if not calendar.isleap(year_num):
            if month_string == '2':  # February
                if day_num > 28:
                    return False

        # Make sure it doesn't occur in the future
        now = datetime.datetime.now()
        users_date = datetime.datetime(year=year_num, month=int(month_string), day=day_num)
        if now < users_date:
            return False
        # Passed tests and is valid
        return True
    return False


def get_inputs():
    """ This method gets, validates, and returns user inputs.
    Retrieves and validates:
    location, month, day, year
    Also formats the location to be what the redirect url will expect.
    Returns validated strings for each.

    :return location_string: Validated string containing the location
    :return month_string: Validated string containing the month
    :return day_string: Validated string containing the day
    :return year_string: Validated string containing the year
    """
    # Get and validate location
    location_string = input('Location: ')
    # TODO: Format and validate location string
    # Get and validate month
    month_string = input('Month: ')
    if not validate_month(month_string):
        print('{"error": "Month invalid"}')
        sys.exit()
    # Get and validate day
    day_string = input('Day: ')
    if not validate_day(day_string, month_string):
        print('{"error": "Day invalid"}')
        sys.exit()
    # Get and validate year
    year_string = input('Year: ')
    if not validate_year(year_string, month_string, day_string):
        print('{"error": "Year invalid"}')
        sys.exit()
    return location_string, month_string, day_string, year_string


def get_url(search_location, search_day, search_month, search_year):
    """ Takes in variables to create a valid url which, when a get request
    is sent to that url, redirects us to the results page the user is
    looking for.

    :param search_location: formatted string containing the location the
    user wants temperature data for.
    :param search_day: validated string for day that exists
    :param search_month: validated string for month which exists
    :param search_year: validated string for year which exists
    :return formatted_url:  A url to be used in a get request which will
    point us to the results page for the data provided
    """
    formatted_url = 'https://www.wunderground.com/cgi-bin/findweather/' \
                    'getForecast?airportorwmo=query&historytype=DailyHistory&backurl=/history/index.html&' \
                    'code=%s&month=%s&day=%s&year=%s' \
                    % (search_location, search_month, search_day, search_year)
    return formatted_url


def scrape_weather_data(results_url):
    """ Takes in a 'results_url' which, when a get request is performed on
    that url, redirects to the results page.  Navigates the HTML on that page
    searching for the weather history table.  Parses the following from the
    weather history table:
    -Actual Mean Temp, Average Mean Temp
    -Actual Max Temp, Average Max Temp, Record Max Temp
    -Actual Min Temp, Average Min Temp, Record Min Temp
    Returns the above data as a string in json format

    :param results_url:
    :return temp_json: A string containing the temperature data of interest
    formatted as a json
    """
    # Follow the results_url to the results page
    response = requests.get(results_url)
    if response.status_code != 200:
        return '{"error": "Received %s status code for url: ' \
               '%s"}' % (response.status_code, results_url)

    # Use beautiful soup to navigate the html
    # to the rows in the history table
    page = BeautifulSoup(response.text, "html.parser")
    history_table = page.find('table', id='historyTable')
    # Handle the case of if we weren't sent to a web page
    # with the table/id we want
    if history_table is None:
        return '{"error": "Received a link which does not contain ' \
               'the data we want.  Link received %s"}' % results_url
    history_table_rows = history_table.findAll('tr')

    # Parse the data from each row with information we care about,
    # and store it in json format
    temp_json = '{'
    for row in history_table_rows:
        if 'Mean Temperature' in row.get_text():
            cells = row.findAll('td')
            temp_json += cell_to_json('Actual Mean Temperature', cells[1])
            temp_json += cell_to_json('Average Mean Temperature', cells[2])
        elif 'Max Temperature' in row.get_text():
            cells = row.findAll('td')
            temp_json += cell_to_json('Actual Max Temperature', cells[1])
            temp_json += cell_to_json('Average Max Temperature', cells[2])
            temp_json += cell_to_json('Record Max Temperature', cells[3])
        elif 'Min Temperature' in row.get_text():
            cells = row.findAll('td')
            temp_json += cell_to_json('Actual Min Temperature', cells[1])
            temp_json += cell_to_json('Average Min Temperature', cells[2])
            temp_json += cell_to_json('Record Min Temperature',
                                      cells[3], False)
    # Finish building the JSON string and return it
    return temp_json+'}'


def cell_to_json(key, cell, needs_comma=True):
    """ This converts the inputs into a 'line' for the json string being
     built within scrape_weather_data.
     inputs:
     -key: The key to use in the JSON line
     -cell:  A <td> cell contained with a BeautifulSoup object
     -needs_comma:  if True, add a comma to the end of the string.
                    if False, does not add a comma.
                    *Assumes we need a comma as this is the most common case
     outputs:
         A String built specifically to be concatenated with the temp_json
         string within scrape_weather_data
     """
    temperature = cell.get_text().strip()
    temperature = temperature.replace('\xa0', '')
    temperature = temperature.replace('\n', ' ')
    return '"%s": "%s"%s' % (key, temperature, ',' if needs_comma else '')


if __name__ == '__main__':
    # Get inputs from the user
    location, month, day, year = get_inputs()
    # Get the results url for the location from wunderground
    res_url = get_url(location, day, month, year)
    # Navigate to the res_url's destination and retrieve the data
    data = scrape_weather_data(res_url)
    # Print the JSON formatted string out for the user
    print(data)
