import csv
import os
import requests
import time
from bs4 import BeautifulSoup
from newspaper import Article

# Placeholder for links
tmp_article_links = []

# Create Dictionary
news_api_links = []
tmp_article_details = {}

def set_search_year():
	while True:
		search_year = input("Please enter the year to search for: ")
		if len(search_year) == 4:
			break
		print("Please enter a valid four-digit year: ")
	return search_year

def set_search_terms():
	while True:
		accept_input = str(input("Please enter search term(s) separated by a comma: "))
		if not accept_input:
			print ("Sorry, I didn't understand that. " + 
			"Please enter search term(s) separated by a comma: ")
			continue
		else:
			break
	strip_input = ''.join(accept_input.split()) # Remove tabs, lines, whitespaces
	search_terms = strip_input.replace("," , ",+") # Replace commas
	#print (format_input)
	return search_terms

# Sets the search terms and year we are searching for in the url
def set_search_url(terms, year):
	tdnews_url = ('http://www.nydailynews.com/search-results/search-results-7.113?q=' + terms + '&selecturl=site&sortOrder='
		      'desc&pdate=' + str(year) + '-01-01&edate=' + str(year) + '-12-31&tfq=articles&afq=&page=')
	return tdnews_url

# Scrapes URL search page from 1 to 48 for links
def tdn_scrape(url):
	page_range = int(input('Enter a number for page search limit:'))
	for page_num in range(1,page_range):
		t0 = time.time()
		headers = {'user-agent': 
			   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) '
			   	'Chrome/57.0.2987.133 Safari/537.36'}
		paged_url = url + str(page_num)
		get_page = requests.get(paged_url, headers=headers)
		page_results = BeautifulSoup(get_page.content, 'html.parser')
		soup_search = page_results.find('div', class_='rtww')
		if soup_search:
			# Scrape for current page and add to temporary links array
			for link in soup_search.find_all('a'):
				tmp_article_links.append(link.get('href'))
		else:
			# Return alert to user
			print ('Cannot proceed, please check HTML DOM')
		response_delay = time.time() - t0 # be polite!
		time.sleep(10*response_delay)  # wait 10x longer than it took site to respond

# Passes links into newspaper api to create dict of titles, keywords, and urls
def newspaper_api_dict(news_links):
	for article_link in news_links:
		article = Article(article_link)
		try:
			article.download()
			article.parse()
			article.nlp()
			tmp_article_details = {
				'title': article.title,
				'keywords': article.keywords,
				'link': article.url,
			}
			news_api_links.append(tmp_article_details)
		except Exception:
			print ('we will continue after this short error')
			continue

	#print (news_api_links)

# Writes dictionary to CSV file
def write_to_file():
	result_file = open(os.path.abspath('BXVR.csv'), 'w')
	csv_columns = ['title', 'keywords', 'link']

	with result_file as f:
		write_to_file = csv.DictWriter(f, dialect="excel", lineterminator='\n', fieldnames=csv_columns);
		write_to_file.writeheader()
		for value in news_api_links:
				write_to_file.writerow(value)

#
def main():
	url = set_search_url(set_search_terms(),set_search_year())
	print (url)

	tdn_scrape(url)
	#print tmp_article_links

	# Prepends daily news url to links
	article_links = ['http://www.nydailynews.com{0}'.format(l) for l in tmp_article_links]
	#print (article_links)

	# Remove paginated links
	news_links = [y for y in article_links if not '&page=' in y]
	#print (news_links)

	newspaper_api_dict(news_links)
	write_to_file()

main()
