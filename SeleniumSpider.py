import json
from bs4 import BeautifulSoup
from selenium import webdriver
import re


class SeleniumSpider:
	def __init__(self, website):
		self.site = website

		# Set up selenium
		self.browser = webdriver.Safari(executable_path='/usr/bin/safaridriver')
		self.browser.get(self.site)
		self.browser.implicitly_wait(4)  # wait for page to load
		self.currentsport = ""  # im not 100% how strings work so this was the first way i tried that worked

	def extract_games(self):
		# extracting
		table_id = self.browser.find_element_by_class_name('card-content')  # gets table
		rows = table_id.find_elements_by_tag_name('tr')  # get all of the rows in the table first one is header
		games = []
		for row in rows:
			# Get the columns
			col = row.find_elements_by_tag_name('td')    # note: index start from 0, 1 is col 2
			if not col:                                  # if col is empty the row we have is the header
				self.currentsport = (str.split(row.text)[0])
			else:
				if len(col) > 1:                         # if can bet on game (need to see a suspended bet to test)
					teams = row.find_elements_by_class_name('runners')
					bets = row.find_elements_by_class_name('bf-bet-button-info')
					odds = []
					runners = []
					for team in teams:
						runners.extend(re.findall('[A-Z][^A-Z]*', team.text))
					for bet in bets:
						odds.insert(len(odds), str(bet.text))
					bets.clear()
					for odd in odds:
						bets.append(str.split(odd))

					games.insert(len(games), {'Sport': self.currentsport, 'Runners': runners, 'Odds': bets})
		return games

	def kill(self):
		self.browser.close()


if __name__ == '__main__':
	x = SeleniumSpider('https://www.betfair.com/exchange/plus/')
	# x = SeleniumSpider('https://www.betfair.com/exchange/plus/horse-racing/market/1.155063620')
	print(x.extract_games())
	x.kill()