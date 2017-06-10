from __future__ import print_function
from builtins import str
####
import lxml
import requests
from bs4 import BeautifulSoup
import re


#retrieve web page
web_page = requests.get('http://www.nydailynews.com/new-york/bronx/man-found-dead-gunshot-wound-head-bronx-blaze-article-1.3212005')

#convert it to html
text_page = web_page.text


#set up the soup. (I don't totally get what lxml does, but it works.)
soup = BeautifulSoup(text_page, "lxml")


word_exists = False
for elem in soup(text=re.compile(r'gunshot')):
    word_exists = True
    print ('\n' + str(elem.parent))
    print("instance found: " + "gunshot\n")

if (word_exists == False):
	print("\"gunshot\" not found")