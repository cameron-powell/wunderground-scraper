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


if __name__ == '__main__':
    unittest.main()
