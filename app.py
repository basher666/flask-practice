# -*- coding: utf-8 -*-
import sys
import re
import urllib2
from bs4 import BeautifulSoup
from mechanize import Browser
import os
from flask import Flask
#from tabulate import tabulate
import string

web_url2= "http://tvscheduleindia.com/channel/"
base_url = 'http://www.imdb.com/find?q='

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

def getBSoup(url):
    req = urllib2.urlopen(url)
    soup = BeautifulSoup(req.read(), "lxml")
    return soup


@app.route('/<channel2>')

def search_channel(channel2):
    #channel_url = web_url + channel + ".html"
    #soup = getBSoup(channel_url)
    time = []
    ratings = []
    title_search = re.compile('/title/tt\d+')

    #movie_name = soup.find_all('p', {"class": "title2"})

    channel2_url= web_url2 + channel2

    req = urllib2.urlopen(channel2_url)
    soup2 = BeautifulSoup(req.read(), "lxml")
    #soup2 = getBSoup(channel2_url)

    for s in soup2.find_all("strong"):
        if s.string:
            s.string.replace_with(s.string.strip())

    movie_name=[]
    movie_name2 = soup2.find_all("strong")

    for i in range(0,len(movie_name2)):
        movie_name2[i]=movie_name2[i].text

    #for i in range(0, len(movie_name)):
    #    movie_name[i] = movie_name[i].text

    #print movie_name

    #time1 = soup.find_all('div', {"class": "col-lg-12"})

    for s in soup2.find_all('b',{"class":"from"}):
        if s.string:
            s.string.replace_with(s.string.strip())

    for s in soup2.find_all('b',{"class":"to"}):
        if s.string:
            s.string.replace_with(s.string.strip())

    time2_from = soup2.find_all('b',{"class":"from"})
    time2_to = soup2.find_all('b',{"class":"to"})
    
    for i in range(0,len(time2_from)):
        time2_from[i]=time2_from[i].text

    for i in range(0,len(time2_to)):
        time2_to[i]=time2_to[i].text

    #for i in range(1, len(time1)-1, 2):
    #    time.append(time1[i].text[0:13].strip(''))

    #time = [x for x in time if x != '']

    for i in range(0,len(movie_name2)):
        movie_name.append(movie_name2[i])
        movie_name[i]=movie_name[i].encode('utf-8')
        movie_name[i]=movie_name[i].encode('ascii','ignore').strip()
        time.append(time2_from[i]+"-"+time2_to[i])

    #print movie_name

    # time = filter(None, time)

    for i in range(0, len(movie_name)):
        try:
            print "Checking IMDb rating of "+ movie_name[i]
            movie_search = '+'.join(movie_name[i].split())
            movie_url = base_url + movie_search + '&s=all'
            #print movie_url
            br = Browser()
            #print "check1"
            br.open(movie_url)
            #print "check2"
            link = br.find_link(url_regex=re.compile(r'/title/tt.*'))
            res = br.follow_link(link)
            #print "check3"
            soup = BeautifulSoup(res.read(), "lxml")
            #print "check4"
            movie_title = soup.find('title').contents[0]
            #print "check5"
            rate = soup.find('span', itemprop='ratingValue')
            if rate is not None:
                ratings.append(str(rate.contents[0]))
            else:
                ratings.append("-")
        except:
            ratings.append("-")
    headers = ['Movies', 'Time', 'Rating']
    data_movies = []
    for i in range(0, len(movie_name)):
        data_movies.append([str(movie_name[i]), str(time[i]), ratings[i]])
    return str(data_movies)

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run()
