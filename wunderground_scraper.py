""" Module: wunderground_scraper.py

The purpose of this module is to:
1) Provide methods to get location and date inputs from the user
2) Provide methods for inserting those inputs into the wunderground history
search
3) Provide methods for scraping requested values off of the wunderground
results page
4) Provide methods to convert those results into a JSON object and return them
to the user
5) Provide an entrypoint to the program to execute all this functionality

This module can be run by navigating to the root project directory and running
the following command:

'python wunderground_scraper.py'

This will execute all of the code defined with the if __name__ == '__main__'
block.
NOTE: This assumes you are running within an activated virtual environment
and have the project's requirements already installed.  See the project README
for instructions on setting that up.
"""
import requests
from bs4 import BeautifulSoup
from selenium import webdriver


def get_url(location):
    """ This method takes in a location string and, using selenium, opens
    a Firefox browser, executes javascript to insert the location
    provided into the search box at https://www.wunderground.com/history,
    clicks the search button, and returns the url once the page
    changes.
    """
    import time
    driver = webdriver.Firefox()
    driver.get('https://www.wunderground.com/history')
    time.sleep(5)
    driver.execute_script('''
    window.stop();
    document.getElementById("histSearch").value = "Atlanta, GA";
    var tags = document.getElementsByTagName("input");
    for(var i=0; i<tags.length; i++) {
      if(tags[i].value == "Submit") {
        tags[i].click();
      }
    }''')
    time.sleep(5)
    url = driver.current_url
    driver.quit()
    return url


def scrape_weather_data(url):
    """ Docstring """
    # Get the html from the page using requests
    response = requests.get(url)
    if response.status_code != 200:
        return '{"error": "Received %s status code for url: ' \
               '%s"}' % (response.status_code, url)

    # Use beautiful soup to navigate the html
    # to the rows in the history table
    page = BeautifulSoup(response.text, "html.parser")
    history_table = page.find('table', id='historyTable')
    # Handle the case of if we weren't sent to a web page
    # with the table/id we want
    if history_table is None:
        return '{"error": "Received a link which does not contain ' \
               'the data we want.  Link received %s"}' % url
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
    # TODO: Create methods to validate input
    location = input('Location: ')
    month = input('Month: ')
    day = input('Day: ')
    year = input('Year: ')
    # Get the url for the location from wunderground
    url = get_url(location)
    # Modify the url for the correct date and use that to get the data
    data = scrape_weather_data(url)
    print(data)
