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


class TestWundergroundScraper(unittest.TestCase):
    """ The purpose of this class is to define tests for functions within the
    wunderground_scraper.py module.
    """

    def test_format_location(self):
        """ This tests that the format location function strips whitespace off
        of a provided location.
        """
        answer = wunderground_scraper.format_location('   Atlanta, Georgia')
        self.assertEqual(answer, 'Atlanta, Georgia')

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


if __name__ == '__main__':
    unittest.main()
