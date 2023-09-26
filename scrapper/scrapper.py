import requests
from urls import departments
import json
from tqdm import tqdm

from bs4 import BeautifulSoup

KEYS = ['inLanguage', 'headline', 'description', 'datePublished', 'articleBody', 'image']
keys = list(departments.keys())

data = json.loads(open("sample.json", "r").read())

for k in keys:
	print(k)
	for url in departments[k]:
		try:
			soup = BeautifulSoup(requests.get(url).text, 'html.parser')
			news = list(map(lambda ele: ele.find('a'), soup.find_all(attrs = {"class": 'story_list'})))

			for i in tqdm(range(len(news))):
				content_soup = BeautifulSoup(requests.get(url + news[i]['href']).text, 'html.parser')
				jsonData = json.loads(content_soup.find_all("script", attrs = {"type": "application/ld+json"})[1].string)

				article = {}

				for key in KEYS:
					article.update({ key: jsonData[key] })
					
				article.update({ "department": k })
				data.append(article)
		except:
			pass

with open("sample.json", "w") as file:
	file.write(json.dumps(data, indent = 4))