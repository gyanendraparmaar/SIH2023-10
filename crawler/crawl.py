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

	def getNews(self, count, url):
		data = []
		# Creating soup for url
		soup = BeautifulSoup(requests.get(url).text, 'html.parser')

		if self.provider == 'economictimes':
			# Get news articles by class name 'story_list'
			news = list(map(lambda ele: ele.find('a'), soup.find_all(attrs = {"class": 'story_list'})))[:count]

			for i in tqdm(range(len(news))):
				content_soup = BeautifulSoup(requests.get(url + news[i]['href']).text, 'html.parser')
				# Get JSON data from the site
				jsonData = json.loads(content_soup.find_all("script", attrs = {"type": "application/ld+json"})[1].string)

				article = {}
				
				# Iterate all KEYS
				for key in self.KEYS:
					article.update({ key: jsonData[key] })
					
				data.append(article)

		elif self.provider == "dainik":

			news = list(map(lambda ele: ele.find('a')['href'], soup.find_all('ul')[4]))[:count]
			
			for i in tqdm(range(len(news))):
				content_soup = BeautifulSoup(requests.get(url + news[i]).text, 'html.parser')

				article = { 'inLanguage': 'hi' }
				article.update({"articleBody": content_soup.find_all('article')[0].find_all('p')[0].string})

				title = content_soup.find("h1").contents
				article.update({"headline": title[0].string + title[1]})

				data.append(article)

		return data

if __name__ == "__main__":
	crawler = Crawl(provider = "dainik")
	with open("try.json", "w", encoding = "utf8") as file:
		json.dump(crawler.getNews(url = url, count = 10), file, indent = 4, ensure_ascii = False)