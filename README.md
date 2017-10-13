# Wunderground Scraper

### Tested With:
* Python 3.5.2
* pip 8.1.1 (python 3.5)
* Ubuntu 16.04 LTS (64bit)

### Project Setup:
##### Virtual Environment
1) Clone this repo to somewhere on your machine
2) Open a terminal and navigate to the root directory of this project
3) Execute `python3 -m venv ws-venv`
4) (linux/macOS) Activate the virtual environment with `source ws-venv/bin/activate`
5) (Windows) Activate the virtual environment by running the activate.bat file in the ws-venv's bin folder
6) Install requirements with `pip install -r requirements.txt`

### Running the Project:
* Activate the virtual environment (see 'Project Setup')
* Navigate to the project's root directory
* Execute `python wunderground_scraper.py`

### Running the Tests:
* Activate the virtual environment (see 'Project Setup')
* Navigate to the project's root directory
* Execute `python wunderground_scraper_tests.py`
* This will execute all the tests in the _wunderground_scraper_tests.py_ file.

### How it Works:
##### A High-Level Overview
* Prints input formatting requirements to the terminal for the user
* Gets user input, validates input against the aforementioned formatting requirements
* Creates a url to take us to the results page on wunderground for the data requested
* Executes a get request to retrieve the html for the results page
* Verifies that all the table headers expected are in the table returned
* Parses out the data and prints the data in json format (sorted by keys)
##### Notes
* If an error occurs (invalid input, request error, etc) the script will print the error in json format for the user
  * Example: `{"error": "An error occurred when attempting to x"}`
* Does not attempt to parse tables with incomplete data, prints an error message like the one above
* Assumes that the user wants the F for farenheit included.
* Assumes that the user wants to know the date of the record temperatures.
* Excludes the degree symbol from the returned temperatures

### Error Reporting:
* If errors are found, please report them on the [issues page](https://github.com/cameronspowell/wunderground-scraper/issues) at this projects github repo