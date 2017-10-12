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
from bs4 import BeautifulSoup
import requests


def format_location(loc):
    """ This function strips whitespace off the ends of location inputs. """
    return loc.strip()


def scrape_weather_data(url):
    """ Docstring """
    # Get the html from the page using requests
    response = requests.get(url)
    if response.status_code != 200:
        return '{"error": "Received %s status code for url: %s"}' % (response.status_code, url)

    # Use beautiful soup to navigate the html to the rows in the history table
    page = BeautifulSoup(response.text, "html.parser")
    history_table = page.find('table', id='historyTable')
    # Handle the case of if we weren't sent to a webpage with the table/id we want
    if history_table is None:
        return '{"error": "Received a link which does not contain ' \
               'the data we want.  Link received %s"}' % url
    history_table_rows = history_table.findAll('tr')

    # Parse the data from each row with information we care about, and store it in json format
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
            temp_json += cell_to_json('Record Min Temperature', cells[3], False)

    # Finish building the JSON string and return it
    return temp_json+'}'


def cell_to_json(key, cell, needs_comma=True):
    """ Docstring """
    temperature = cell.get_text().strip()
    temperature = temperature.replace('\xa0', '')
    temperature = temperature.replace('\n', ' ')
    return '"%s": "%s"%s' % (key, temperature, ',' if needs_comma else '')


if __name__ == '__main__':
    print(scrape_weather_data('https://www.wunderground.com/history/airport/KFTY/2017/10/11/DailyHistory.html?req_city=Atlanta&req_state=GA&req_statename=Georgia&reqdb.zip=30301&reqdb.magic=1&reqdb.wmo=99999'))
