import requests
from urllib.request import urlopen
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep,time
from random import randint
from IPython.core.display import clear_output
from newspaper import Article

#URL to be scraped
websiteURL = "https://www.cnet.com"
Scrape1 = "/sitemaps/articles/"
Scrape2 = "/"

#list to store the scraped data in
Headlines = []
Dates = []
Contents = []
pages = []
years_url = []
Keywords_all = []

#scrape for multiple years and multiple pages
pages = [str(i) for i in range(1,2)]
years_url = [str(i) for i in range (2000,2001)]

#monitoring loop
start_time = time()
req = 0

#For every year in the interval 
for year_url in years_url:
	#for every page in interval
	for page in pages:
			#make get request
			url = requests.get(websiteURL+Scrape1+year_url+Scrape2+page)
			#Monitor the requests
			sleep(randint(1,1))
			req = req + 1
			elapsed_time = time() - start_time
			print('Request:{}; Frequency: {} requests/s'.format(req,req/elapsed_time))
			clear_output(wait = True)
			if url.status_code == 200:
				print("{} downloaded successfully".format(str(websiteURL+Scrape1+year_url+Scrape2+page)))
			else:
				print("some error occured")
			#parse contents
			url_soup = BeautifulSoup(url.text,'html.parser')
			Article_containers = url_soup.find_all('li', class_='row')
			#Extract data from one article container
			for container in Article_containers:
				#Date extract
				Date = container.find('div', class_ = 'col-1 date').text
				Dates.append(Date)

				#go to individual pages
				for lnk in container.find_all('a'):
					ArticlePage = lnk.get('href')
					Articleurl = websiteURL+lnk.get('href')
					print(Articleurl)
					ArticleDetails = requests.get(Articleurl)
					Article_html = BeautifulSoup(ArticleDetails.content,'html.parser')
					Content = Article_html.find('div', class_="col-7 article-main-body row").get_text()
					Content= str(Content)
					Content=Content.replace("\n", '')
					Content=Content.lstrip()
					Contents.append(Content)
					#Headline extract
					Headline = Article_html.find('h1', class_="speakableText").text
					Headlines.append(Headline)
					#Extract keywords
					article = Article(Content)
					article.download()
					article.parse()
					article.nlp()
					article.keywords
					keywords = Content.keywords
					Keywords_all.append(keywords)



Cnet_articles = pd.DataFrame({'Headline': Headlines, 'Date': Dates, 'Content': Contents,  'keywords': Keywords_all})
Cnet_articles.to_csv("Cnet_articles6.csv", encoding='utf-8', index=False)



