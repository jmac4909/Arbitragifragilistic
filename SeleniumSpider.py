import scrapy
import json
from bs4 import BeautifulSoup
import time

from scrapy.selector import HtmlXPathSelector
from selenium import webdriver


class SeleniumSpider:
	def __init__(self, website):
		self.site = website

		# Set up selenium
		self.browser = webdriver.Safari(executable_path='/usr/bin/safaridriver')
		self.browser.get(self.site)
		self.browser.implicitly_wait(10)  # wait for page to load

	def extract_games(self):
		# extracting
		table_id = self.browser.find_element_by_class_name('card-content')  # gets table
		rows = table_id.find_elements_by_tag_name('tr')  # get all of the rows in the table first one is header
		for row in rows:
			# Get the columns
			col = row.find_elements_by_tag_name('td')    # note: index start from 0, 1 is col 2
			if not col:                                  # if col is empty the row we have is the header
				sport_text = row.text
				print(sport_text)                        # prints the sport currently under
			else:
				if len(col) > 1:                         # if can bet on game (need to see a suspended bet to test)
					print(str.split(col[0].text))        # prints (first col)
					print(str.split(col[1].text))        # prints (second col)

	def kill(self):
		self.browser.close()


if __name__ == '__main__':
	x = SeleniumSpider('https://www.betfair.com/exchange/plus/')
	x.extract_games()