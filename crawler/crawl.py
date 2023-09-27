from urls import urls
import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
from translate import Translator

url = "https://www.bhaskar.com/national/"

class Crawl:
	def __init__(self, lang = 'en', provider = 'economictimes'):
		# INIT variables
		self.lang = 'en'
		self.provider = provider
		self.translator = Translator(from_lang = 'hi', to_lang = "en")

		# INIT constants
		self.KEYS = ['inLanguage', 'headline', 'description', 'datePublished', 'articleBody']

	def getNews(self, url):
		# Creating soup for url
		if self.provider == 'economictimes':
			# Get news articles by class name 'story_list'

			content_soup = BeautifulSoup(requests.get(url).text, 'html.parser')
			# Get JSON data from the site
			jsonData = json.loads(content_soup.find_all("script", attrs = {"type": "application/ld+json"})[1].string)

			article = {}
			
			# Iterate all KEYS
			for key in self.KEYS:
				article.update({ key: jsonData[key] })
				
			return article

		elif self.provider == "dainik":
			content_soup = BeautifulSoup(requests.get(url).text, 'html.parser')

			article = { 'inLanguage': 'hi' }
			article.update({"articleBody": content_soup.find_all('article')[0].find_all('p')[0].string})

			title = content_soup.find("h1").contents
			article.update({"headline": title[0].string + title[1]})

			return article
		

if __name__ == "__main__":
	crawler = Crawl(provider = "dainik")
	parsedArticle = crawler.getNews(url="https://www.bhaskar.com/national//national/news/retired-airman-hiv-positive-rs-15-crore-update-131899717.html")
	prevData = json.loads(open("try.json", "r").read())
		