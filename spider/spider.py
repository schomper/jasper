#! /usr/bin/python3

# TODO media-transcript for video files
# TODO remove source section
# TODO make into jason export

from bs4 import BeautifulSoup
import re
import urllib.request
import string
import os
import random
import json

OUTPUT_FILE = 'output.extended/'

def get_year_links():
    """ Get the links of all the relevant year tabs."""
    
    links = ['http://www.abc.net.au/news/archive/2004', 
             'http://www.abc.net.au/news/archive/2005', 
             'http://www.abc.net.au/news/archive/2006', 
             'http://www.abc.net.au/news/archive/2007', 
             'http://www.abc.net.au/news/archive/2008', 
             'http://www.abc.net.au/news/archive/2009', 
             'http://www.abc.net.au/news/archive/2010', 
             'http://www.abc.net.au/news/archive/2011', 
             'http://www.abc.net.au/news/archive/2012', 
             'http://www.abc.net.au/news/archive/2013', 
             'http://www.abc.net.au/news/archive/2014']
    
    return links

def get_day_links(year_url):
    """ Get link for every day in the year.
    
    Keyword arguments:
    year_url -- the url of the year page.
    """
    f = urllib.request.urlopen(year_url)
    soup = BeautifulSoup(f.read())
    nav = soup.find("div", { "class" : "c75l" })
    links = []

    for link in nav.findAll("a", href=True):
        link = 'http://www.abc.net.au' + link["href"]
        links.append(link)

    return links

def process_day(day_link, year_name):
    """ Get the all the links to articles posted on a specified day.
    
    Keyword arguments:
    day_url -- url of the day's first page
    year_name -- name of the year to which the day belongs
    """
    article_list = []

    day = day_link.split('/')[-1].split(',')[1]
    month = day_link.split('/')[-1].split(',')[2] 
    date = day + ' ' + ' ' + month + ' ' + year_name

    day_name = day + '_' + month + '.txt'

    file_name = OUTPUT_FILE + year_name + '/' + day_name 

    if os.path.exists(file_name):
        print('\tDay %s %s exists.' % (day_name, year_name))
        return
    
    print('\tDay: %s %s.' % (day_name, year_name))

    f = urllib.request.urlopen(day_link)

    soup = BeautifulSoup(f.read())
    nav = soup.find("div", { "class" : "nav pagination" })
    articles = soup.find('ul', {'class' : 'article-index'})
    next_list = nav.find_all('a', {'class' :'next'})
    day = day + next_list[0]['href']

    for link in articles.findAll("a", href=True):
        link = 'http://www.abc.net.au' + link["href"]
        if (not '/topic/' in link) and (not link in article_list):
            article_list.append(link)
    
    while len(next_list) != 0:
        
        f = urllib.request.urlopen(day_link)
        soup = BeautifulSoup(f.read())

        nav = soup.find("div", { "class" : "nav pagination" })
        articles = soup.find('ul', {'class' : 'article-index'})
    
        next_list = nav.find_all('a', {'class' :'next'})
        if len(next_list):
            day_link = day_link.split('?')[0] + next_list[0]['href']

        for link in articles.findAll("a", href=True):
            link = 'http://www.abc.net.au' + link["href"]
            if not '/topic/' in link:
                article_list.append(link)

    
    f_ptr = open(file_name, 'w')
    
    days_information = {}
    day_docs = []

    for article in article_list:
        doc = write_article(date, article, f_ptr)
        day_docs.append(doc)

    days_information['number'] = len(day_docs)
    days_information['documents'] = day_docs

    f_ptr.write(json.dumps(days_information, sort_keys=True, indent=4))

def process_body(section):
    body_items = []
   
    # Remove published
    exists = section.findAll('p', {'class':'published'})

    for e in range(0, len(exists)):
        exists = section.find('p', {'class':'published'}).extract()

    ###################################
    # Get document topics
    ###################################
    topics = section.find('p', {'class':'topics'}).extract()
    topics = topics.getText()
    topics = re.sub(r"\s+", "", topics, flags=re.UNICODE)
    topics = topics.replace('Topics:', '')
    topics = topics.split(',')
    
    body_items.append(topics)
    
    ###################################
    # Get body content
    ###################################
    contents = section.findAll('p')

    para_string = ''
    for para in contents:
        para = para.getText()
        para = para.strip()

        para_string += para

    body_items.append(para_string)

    return body_items


def write_article(date, url, f_ptr):
    """ Write the information about the article to a file.

    Keyword arguments:
    url -- url of the article to write to file
    file_name -- name of the file to which to write
    """
    document = {}
    
    try: 
        f = urllib.request.urlopen(url)
    except urllib.error.URLError as e:
        print(e.reason)
        return

    soup = BeautifulSoup(f.read())
    section = soup.find('div', {'class':'c75l'})
    
    try:
        title = section.find('h1').getText()
        document['title'] = title
        print('\t\t' + title)

        body_items = process_body(section)
        document['topics'] = body_items[0]
        document['contents'] = body_items[1]
        document['date'] = date

    except Exception as e:
        print('Exception:' + str(e))
        return

    return document

def main():
    year_links = get_year_links()

    for year in year_links:
        year_name = year.split('/')[-1]
        
        print('In year: ' + year_name)
        if not os.path.exists(OUTPUT_FILE + year_name):
            os.makedirs(OUTPUT_FILE + year_name)
        
        days = get_day_links(year)

        for day in days:
            process_day(day, year_name)


if __name__ == "__main__":
    main() 
