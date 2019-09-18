from youtube_scraper.scraper import scrape_url

# https://www.youtube.com/user/teatroallascala/videos
# https://www.youtube.com/user/teatroallascala/about
data = scrape_url('https://www.youtube.com/user/teatroallascala/about')
print(data.name)
print(data.subscribers)
print(data.views)
print(data.description)
print(data.join_date)
print(data.links)
