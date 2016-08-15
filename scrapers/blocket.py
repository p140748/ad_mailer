# coding: utf-8
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pickle
import logging, logging.handlers

#This variable is a regex which will match urls connected to this scraper
REGEX_PATTERN = r'https?://(?:www|mobil)\.blocket\.se/.*'

#The actual scraper
class BlocketScraper():
	def __init__(self,url,**filters):
		self.url = url
		self.ad_ids = []
		self.upper_price = upper_price
		self.filters = filters

	def pickle_dump(self):
		with open('blocket_pickle.txt','wb') as f:
			pickle.dump(self.ad_ids,f)
		logging.info('Blocket Pickle Dump')

	def pickle_load(self):
		with open('blocket_pickle.txt','rb') as f:
			return pickle.load(f)

	def get_price(self,ad):
		text = ad.find('span',{'class':'item_price'}).text
		price = text.split(' kr')[0]
		price = price.replace(' ','') or 0 #If price doesn't exist
		return int(price)

	def get_id(self,ad):
		return ad.get('id')

	def is_good(self,ad):
		criterias = [
			self.get_id(ad) not in self.ad_ids,
			self.get_price(ad) < self.upper_price
		]
		return False not in criterias

	def parse(self,ad):
		return {
			'id' : self.get_id(ad),
			'title' : ad.find('h2',{'class':'item_title'}).text,
			'link' : ad.find('a',{'class':'item_link'}).get('href'),
			'date' : ad.find('p',{'class':'item_date'}).text,
			'price' : self.get_price(ad)
		}

	def scrape(self):
		self.ad_ids = self.pickle_load()

		with urlopen(self.url) as response:
			r = response.read()
		soup = BeautifulSoup(r, 'html.parser')
		ads = soup.find_all('li',{'class':'item'})
		parsed_ads = [self.parse(ad) for ad in ads if self.is_good(ad)]

		for ad in parsed_ads:
			self.ad_ids.append(self.get_id(ad))

		return parsed_ads
