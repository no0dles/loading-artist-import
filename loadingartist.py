import urllib2
import feedparser
import re
from urlparse import urlparse
from dateutil.parser import parse
from datetime import datetime
from bs4 import BeautifulSoup

ARCHIVE_URL = 'http://www.loadingartist.com/archives/?archive_year=%(year)i'
IMG_URL_FORMAT = 'http://www.loadingartist.com/wp-content/uploads/%(year)s/%(month)s/%(year)s-%(month)s-%(day)s-%(title)s.jpg'
THUMB_IMG_URL_FORMAT = 'http://www.loadingartist.com/comic-thumbs/%(title)s.png'
RSS_URL = 'http://www.loadingartist.com/feed/'
PARSER = 'html.parser'


def get_archive_comics():
    comics = []
    for year in range(2011, datetime.now().year + 1):
        url = ARCHIVE_URL % {'year': year}
        response = urllib2.urlopen(url)
        html = response.read()
        response.close()

        soup = BeautifulSoup(html, PARSER)
        for img in soup.find_all('img'):
            url = img.parent['href']
            if urlparse(url).netloc == 'www.loadingartist.com':
                comics.append({'url': url, 'thumb_url': 'http://www.loadingartist.com' + img['src']})
    return comics


def get_comic_detail(comic):
    response = urllib2.urlopen(comic['url'])
    html = response.read()
    response.close()

    soup = BeautifulSoup(html, PARSER)

    page_layout = soup.find('div', {'class': 'page-comic-layout'})
    comic_div = page_layout.find('div', {'class': 'comic'})
    img = comic_div.find('img')

    page_post = soup.find('div', {'class': 'page-comic-post'})
    header = page_post.find('header')
    meta = header.find('div', {'class': 'meta'})

    title = header.find('h1')
    author = meta.find('span', {'class': 'author'})
    date = meta.find('span', {'class': 'date'})

    return {
        'url': comic['url'],
        'thumb_url': comic['thumb_url'],
        'img_url': img['src'],
        'title': title.text.strip(),
        'author': author.text.strip(),
        'date': parse(date.text.strip())
    }


def get_rss_items():
    feed = feedparser.parse(RSS_URL)
    comics = []

    for entry in feed['entries']:
        comic_detail = {
            'url': entry['link'],
            'thumb_url': None,
            'title': entry['title'],
            'author': entry['author'],
            'date': parse(entry['published'].strip())
        }

        match = re.search(r'http://www.loadingartist.com/comic/([a-z-]*)/', comic_detail['url'])

        comic_detail['img_url'] = IMG_URL_FORMAT % {
            'year': comic_detail['date'].year,
            'month': str(comic_detail['date'].month).rjust(2, '0'),
            'day': str(comic_detail['date'].day).rjust(2, '0'),
            'title': match.group(1)
        }

        comic_detail['thumb_url'] = THUMB_IMG_URL_FORMAT % {'title': match.group(1)}

        comics.append(comic_detail)
    return comics
