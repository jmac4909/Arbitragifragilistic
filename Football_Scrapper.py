import json
import platform
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Scrapper:
	def __init__(self, website):

		# Set up selenium
		if platform.system() == 'Windows':
			self.browser = webdriver.Firefox()
		else:
			self.browser = webdriver.Safari(executable_path='/usr/bin/safaridriver')
		self.browser.get(website)
		self.browser.implicitly_wait(1500)  # wait for page to load
		time.sleep(5)

		self.browser.find_element_by_tag_name('body').send_keys(Keys.END)  # Use send_keys(Keys.HOME)

	def get_website(self, website):
		self.browser.get(website)
		self.browser.implicitly_wait(1500)  # wait for page to load
		time.sleep(5)
		self.browser.find_element_by_tag_name('body').send_keys(Keys.END)  # Use send_keys(Keys.HOME)

	def get_rows(self):
		ret = []
		teams = self.browser.find_elements_by_class_name('name')  # get all of the rows in the table first one is header
		teams.reverse()
		events = self.browser.find_elements_by_class_name(
			'start-date-wrapper')  # get all of the rows in the table first one is header
		events.reverse()
		matched = self.browser.find_elements_by_class_name('matched-amount-value')  # get all of the ro
		matched.reverse()
		bet_price = self.browser.find_elements_by_class_name('bet-button-price')  # get all of the ro
		bet_price.reverse()
		bet_size = self.browser.find_elements_by_class_name('bet-button-size')  # get all of the ro
		bet_size.reverse()

		# These fail on page with live event (as they should. Live event doesnt count as event so doesnt add up)

		# assert len(matched) == len(events)
		assert len(bet_price) / 6 == len(teams) / 2
		# assert len(bet_size) == len(bet_price)

		for i in range(len(events)):
			event = {
				'Time': events.pop().text,
				'Team 1': teams.pop().text,
				'Team 2': teams.pop().text,

				#  Football always has 3 groupings of 2 bets (backwards bc it be like that
				'Back 1': bet_price.pop().text,
				'Lay 1': bet_price.pop().text,

				'Back X': bet_price.pop().text,
				'Lay X': bet_price.pop().text,

				'Back 2': bet_price.pop().text,
				'Lay 2': bet_price.pop().text,

			}
			ret.append(event)
		return ret


if __name__ == '__main__':

	# Football Logger
	data = []
	x = Scrapper('https://www.betfair.com/exchange/plus/football')
	p = x.get_rows()
	data.append(p)
	# no guarantee 13 pages
	for i in range(13):
		if i is not 0 or i is not 1:
			x.get_website('https://www.betfair.com/exchange/plus/football/' + str(i))
			p = x.get_rows()
			data.append(p)
	x.browser.close()
	with open('football_data.json', 'w') as outfile:
		json.dump(data, outfile)
