""" Module: wunderground_scraper_tests.py

The purpose of this module is to provide unit tests for functions described
in the wunderground_scraper.py module.  In order to run these tests, navigate
to the root project directory and run the following command:

'python wunderground_scraper_tests.py'

This will run each test defined within this module and output any errors or
regressions which are found.
NOTE:  This assumes you are running within an activated virtual environment
and have the project's requirements already installed.  See the project README
for instructions on setting that up.
"""
import unittest
import wunderground_scraper
from bs4 import BeautifulSoup


class TestWundergroundScraper(unittest.TestCase):
    """ The purpose of this class is to define tests for functions within the
    wunderground_scraper.py module.
    """

    def test_validate_month(self):
        """ Checks a random middle value to verify validate_month is
        still returning true for a valid input.
        """
        answer = wunderground_scraper.validate_month('6')
        self.assertEqual(answer, True)

    def test_validate_month_two_digit(self):
        """ Checks to make sure a valid two digit month is valid with the
        validate month method.
        """
        answer = wunderground_scraper.validate_month('10')
        self.assertEqual(answer, True)

    def test_validate_month_low(self):
        """ Tests to make sure that values too low don't return true
        in the validate month function
        """
        answer = wunderground_scraper.validate_month('0')
        self.assertEquals(answer, False)

    def test_validate_month_high(self):
        """ Tests to make sure month is a string numerically representing a
         month within the range 1 - 12.  Makes sure numbers too high return false.
        """
        answer = wunderground_scraper.validate_month('13')
        expected_answer = False
        self.assertEqual(answer, expected_answer)

    def test_validate_month_long(self):
        """ Tests to make sure month string isn't too long.
        Should be one or two digits.
        """
        answer = wunderground_scraper.validate_month('123')
        self.assertEqual(answer, False)

    def test_validate_day(self):
        """ Makes sure a valid day and valid month are returned true by
        the validate_day method.
        """
        answer = wunderground_scraper.validate_day('3', '3')
        self.assertEqual(answer, True)

    def test_validate_day_feb(self):
        """ Makes sure when the month is feb, if day is over 29 the day
        is not valid.
        """
        answer = wunderground_scraper.validate_day('30', '2')
        self.assertEqual(answer, False)

    def test_validate_day_30(self):
        """ Makes sure a month with only 30 days doesn't show as valid
        if the user provided 31 as the day of the month.
        """
        answer = wunderground_scraper.validate_day('31', '9')
        self.assertEqual(answer, False)

    def test_validate_day_31(self):
        """ Makes sure a month with 31 days doesn't show anything higher
        as being a valid date.
        """
        answer = wunderground_scraper.validate_day('32', '5')
        self.assertEqual(answer, False)

    def test_get_url(self):
        """ This tests the get_url method within wunderground_scraper.py
        to ensure that, when given valid inputs, it constructs the url that
        the page uses to redirect to the results page.
        """
        answer = wunderground_scraper.get_url('Atlanta,+GA', '12', '10', '2017')
        expected = 'https://www.wunderground.com/cgi-bin/findweather/' \
                   'getForecast?airportorwmo=query&historytype=DailyHistory&' \
                   'backurl=/history/index.html&code=Atlanta,+GA&' \
                   'month=10&day=12&year=2017'
        self.maxDiff = None
        self.assertEqual(answer, expected)

    def test_scrape_weather_data(self):
        """ This tests to see if, when provided with a valid wunderground
         history url, the scrape weather data function correctly
         retrieves the page, parses the data, and returns it in a string
         formatted as a JSON object.
         """
        url = 'https://www.wunderground.com/history/airport/KFTY/' \
              '2017/10/11/DailyHistory.html?req_city=Atlanta&' \
              'req_state=GA&req_statename=Georgia&reqdb.zip=30301&' \
              'reqdb.magic=1&reqdb.wmo=99999'''
        json_answer = wunderground_scraper.scrape_weather_data(url)
        expected_answer = '{"Actual Mean Temperature": "76°F","Average Mean' \
                          ' Temperature": "64°F","Actual Max Temperature": ' \
                          '"86°F","Average Max Temperature": "75°F","Record ' \
                          'Max Temperature": "104°F (1999)","Actual Min ' \
                          'Temperature": "66°F","Average Min Temperature": ' \
                          '"53°F","Record Min Temperature": "32°F (2000)"}'
        self.assertEqual(json_answer, expected_answer)

    def test_scrape_weather_data_404(self):
        """ This tests to see if, when provided with an invalid wunderground
         url which we know will return a 404 error, the scrape weather data
         function within wunderground_scraper.py will handle the error
         gracefully and return the error in the json that the user
         receives.
         """
        url = 'https://www.wunderground.com/a404url'
        answer = wunderground_scraper.scrape_weather_data(url)
        expected_answer = '{"error": "Received 404 status code for url: ' \
                          'https://www.wunderground.com/a404url"}'
        self.assertEqual(answer, expected_answer)

    def test_scrape_weather_data_wrong(self):
        """ This tests to see if, when provided with a url which does not take
        us to the wunderground history page, the scrape weather data function
        realizes that the data table element we're looking for is not on the
        page and returns the appropriate error string.
        """
        url = 'https://www.google.com'
        answer = wunderground_scraper.scrape_weather_data(url)
        expected_answer = '{"error": "Received a link which does not ' \
                          'contain the data we want.  ' \
                          'Link received %s"}' % url
        self.assertEqual(answer, expected_answer)

    def test_cell_to_json(self):
        """ This function tests the cell to json function.  It creates a fake
        table row to get cells from, and parses a cell into the format string
        we expect.
        """
        row_html = '''<tr>
        <td class="indent"><span>Mean Temperature</span></td>
        <td>
        <span class="wx-data"><span class="wx-value">76</span><span class="wx-unit"> °F</span></span>
        </td>
        <td>
        <span class="wx-data"><span class="wx-value">64</span><span class="wx-unit"> °F</span></span>
        </td>
        <td> </td>
        </tr>
        '''
        row = BeautifulSoup(row_html, 'html.parser')
        cells = row.findAll('td')
        answer = wunderground_scraper\
            .cell_to_json('Actual Mean Temperature', cells[1], False)
        expected = '"Actual Mean Temperature": "76°F"'
        self.assertEqual(answer, expected)

    def test_cell_to_json_comma(self):
        """ This tests to make sure that cell_to_json is appending a comma
        to the end of our json element string when requested. """
        row_html = '''<tr>
        <td class="indent"><span>Mean Temperature</span></td>
        <td>
        <span class="wx-data"><span class="wx-value">76</span><span class="wx-unit"> °F</span></span>
        </td>
        <td>
        <span class="wx-data"><span class="wx-value">64</span><span class="wx-unit"> °F</span></span>
        </td>
        <td> </td>
        </tr>
        '''
        row = BeautifulSoup(row_html, 'html.parser')
        cells = row.findAll('td')
        answer = wunderground_scraper\
            .cell_to_json('Actual Mean Temperature', cells[1])
        expected = '"Actual Mean Temperature": "76°F",'
        self.assertEqual(answer, expected)


if __name__ == '__main__':
    unittest.main()
