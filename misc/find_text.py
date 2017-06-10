#from __future__ import print_function
#from builtins import str
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

#used to print a message if the word doesn't exist on the page.
word_exists = False

#iterate through html elements on the webpage
for elem in soup(text=re.compile(r'gunshot')):
    word_exists = True

    #prints the context every time we find the word
    print ('\n' + str(elem.parent))
    print("instance found: " + "gunshot\n")

#if the word was not found, it never got marked as true
if (word_exists == False):
	print("\"gunshot\" not found")
