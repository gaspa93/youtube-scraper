""" Library entry point """
import re, requests
from bs4 import BeautifulSoup

class YoutubeScrape(object):
    """ Scraper object to hold data """
    def __init__(self, soup):
        """ Initialize and scrape """
        self.soup = soup
        self.title = self.parse_string('.watch-title')
        self.poster = self.parse_string('.yt-user-info')
        self.views = self.parse_int('.watch-view-count')
        self.published = self.parse_string('.watch-time-text')
        self.published = re.sub(r'(Published|Uploaded) on', '', self.published).strip()
        self.like = self.parse_int('.yt-uix-clickcard', 4)
        self.dislike = self.parse_int('.yt-uix-clickcard', 5)

    def parse_int(self, selector, pos=0):
        """ Extract one integer element from soup """
        return int(re.sub('[^0-9]', '', self.parse_string(selector, pos)))

    def parse_string(self, selector, pos=0):
        """ Extract one particular element from soup """
        return self.soup.select(selector)[pos].get_text().strip()


class YoutubeScrapeChannel(object):
    """ Scraper object to hold data """
    def __init__(self, soup):
        """ Initialize and scrape """
        self.soup = soup
        self.name = self.parse_string('.spf-link.branded-page-header-title-link.yt-uix-sessionlink')
        self.subscribers = self.parse_string('.yt-subscription-button-subscriber-count-branded-horizontal.subscribed.yt-uix-tooltip')
        self.description = self.parse_string('.about-description.branded-page-box-padding')

        stats = self.soup.select('.about-stat')
        self.views = int(stats[0].get_text().strip().split(' ')[1].replace(',',''))
        self.join_date = stats[1].get_text().strip()

        links = self.soup.select('.channel-links-item')
        self.links = {}
        for l in links:
            name = l.a['title']
            link = l.a['href']

            if 'redirect' not in link:
                self.links[name] = link


    def parse_string(self, selector, pos=0):
        """ Extract one particular element from soup """
        return self.soup.select(selector)[pos].get_text().strip()


def scrape_video_html(html):
    """ Return meta information about a video """
    return YoutubeScrape(BeautifulSoup(html, 'html.parser'))

def scrape_channel_html(html):
    """ Return meta information about a channel """
    return YoutubeScrapeChannel(BeautifulSoup(html, 'html.parser'))


def scrape_url(url):
    """ Scrape a given url for youtube information """

    # set English as scraping language
    headers = {"Accept-Language": "en-US,en;q=0.5"}
    html = requests.get(url, headers=headers).text
    return scrape_channel_html(html)
