# Wunderground Scraper

### Tested With:
* Python 3.5.2
* Ubuntu 16.04 LTS (64bit)
* Firefox 56.0 (64bit Mozilla Firefox for Ubuntu canonical - 1.0)
* geckodriver v0.19.0-linux64

### Project Setup:
##### Virtual Environment
1) Clone this repo to somewhere on your machine
2) Create a virtual environment
--Open a terminal and navigate to the root directory of this project
--Execute `python3 -m venv ws-venv`
--Activate the virtual environment with `source ws-venv/bin/activate`
--Install requirements with `pip install -r requirements.txt`
##### Selenium Setup
1) Download the latest geckodriver from [mozilla's github](https://github.com/mozilla/geckodriver/releases)
--On Ubuntu 16.04 LTS 64bit, I used __geckodriver-v0.19.0-linux64.tar.gz__
2) Open a terminal and navigate to where you downloaded the geckodriver-*-tar.gz
3) Extract with `tar -xvzf geckodriver*`
4) Change it to be executable with `chmod +x geckodriver`
5) Execute `sudo mv geckodriver /usr/local/bin` to make it available in your path.