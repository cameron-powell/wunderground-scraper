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


def format_location(loc):
    """ This function strips whitespace off the ends of location inputs. """
    return loc.strip()


if __name__ == '__main__':
    location = format_location(input('Location: '))
    print(location)
