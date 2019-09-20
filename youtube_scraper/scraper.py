""" Library entry point """
import re, requests
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient

YOUTUBE_URL = 'http://www.youtube.com'
YT_DATE_FORMAT = '%b %d, %Y'

class YoutubeScrape(object):
    """ Scraper object to hold video data """
    def __init__(self, soup):
        """ Initialize and scrape """
        self.soup = soup
        self.title = self.parse_string('.watch-title')
        self.poster = self.parse_string('.yt-user-info')
        self.views = self.parse_int('.watch-view-count')
        self.published = self.parse_string('.watch-time-text')
        self.published = re.sub(r'(Published|Uploaded) on', '', self.published).strip()
        self.published = re.sub(r'Streamed live on', '', self.published).strip()
        self.published = datetime.strptime(self.published, YT_DATE_FORMAT)
        self.like = self.parse_int('.yt-uix-clickcard', 4)
        self.dislike = self.parse_int('.yt-uix-clickcard', 5)

    def parse_int(self, selector, pos=0):
        """ Extract one integer element from soup """
        return int(re.sub('[^0-9]', '', self.parse_string(selector, pos)))

    def parse_string(self, selector, pos=0):
        """ Extract one particular element from soup """
        return self.soup.select(selector)[pos].get_text().strip()


class YoutubeScrapeChannel(object):
    """ Scraper object to hold channel data """
    def __init__(self, url):
        """ Initialize and scrape """
        self.url = url
        self.headers = {"Accept-Language": "en-US,en;q=0.5"}

    def get_channel_metadata(self):
        """ Extract channel metadata """
        html = requests.get(self.url + '/about', headers=self.headers).text

        self.soup = BeautifulSoup(html, 'html.parser')
        self.username = self.url.split('/')[4]
        self.name = self.parse_string('.spf-link.branded-page-header-title-link.yt-uix-sessionlink')
        self.subscribers = self.parse_string('.yt-subscription-button-subscriber-count-branded-horizontal.subscribed.yt-uix-tooltip')
        self.description = self.parse_string('.about-description.branded-page-box-padding').replace('\n', ' ').replace('\t', ' ')

        stats = self.soup.select('.about-stat')
        self.views = int(stats[0].get_text().strip().split(' ')[1].replace(',',''))
        self.join_date = stats[1].get_text()
        self.join_date = re.sub(r'Joined', '', self.join_date).strip()
        self.join_date = datetime.strptime(self.join_date, YT_DATE_FORMAT)

        links = self.soup.select('.channel-links-item')
        self.links = {}
        for l in links:
            name = l.a['title']
            link = l.a['href']

            if 'redirect' not in link:
                self.links[name] = link

    def get_channel_videos(self):
        """ Extract channel's videos metadata """
        html = requests.get(self.url + '/videos', headers=self.headers).text

        self.soup = BeautifulSoup(html, 'html.parser')
        video_links = self.soup.select('.yt-lockup-title')
        self.videos = []
        for video in video_links:
            video_id = int(video.a['aria-describedby'].split('-')[2])
            video_url = YOUTUBE_URL + video.a['href']
            video_duration = video.span.get_text().split(':')[1].replace('.','')

            v_html = requests.get(video_url, headers=self.headers).text
            video_metadata = YoutubeScrape(BeautifulSoup(v_html, 'html.parser'))
            video_metadata.id = video_id
            video_metadata.url = video_url
            video_metadata.duration = video_duration
            video_metadata.channel = self.username

            self.videos.append(video_metadata)

    def parse_string(self, selector, pos=0):
        """ Extract one particular element from soup """
        return self.soup.select(selector)[pos].get_text().strip()


class DBConnection:
    """ DB object to store data in MongoDB """
    def __init__(self, url):
        """ Initialize DB connection """
        self.client = MongoClient(url)['youtube']

    def save_video(self, video):
        """ Save data stored in YoutubeScrape object """
        db = self.client['video']

        if hasattr(video, 'channel'):
            vdata = {'id': video.id,
                     'url': video.url,
                     'duration': video.duration,
                     'channel': video.channel}
        else:
            vdata = {}

        vdata['title'] = video.title
        vdata['user'] = video.poster
        vdata['views'] = video.views
        vdata['likes'] = video.like
        vdata['dislikes'] = video.dislike
        vdata['published'] = video.published

        try:
            db.insert_one(vdata)
        except Exception as e:
            print(e)

    def save_channel(self, channel):
        """ Save data stored in YoutubeScrape object """
        db = self.client['channel']

        cdata = {'username': channel.username,
                 'name': channel.name,
                 'subscribers': channel.subscribers,
                 'description': channel.description,
                 'views': channel.views,
                 'join_date': channel.join_date
                 }

        # update links with '.' because they are not allowed as mongo keys
        for l in channel.links:
            if '.' in l:
                old_l = l
                l = l.replace('.', '-')
                channel.links[l] = channel.links.pop(old_l)

        cdata = {**cdata, **(channel.links)}

        try:
            db.insert_one(cdata)
        except Exception as e:
            print(e)


def scrape_video(url):
    """ Scrape a given video url for youtube information """
    headers = {"Accept-Language": "en-US,en;q=0.5"}
    html = requests.get(url, headers=headers).text
    return YoutubeScrape(BeautifulSoup(html, 'html.parser'))

def scrape_channel(url):
    """ Return meta information about a channel and its videos """
    return YoutubeScrapeChannel(url)

def get_mongodb(url):
    return DBConnection(url)
