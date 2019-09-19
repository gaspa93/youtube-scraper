from youtube_scraper.scraper import scrape_video, scrape_channel

# get video data given the url
video = scrape_video('http://youtube.com/watch?v=7dlcxXxDGUI')

print(video.title)
print(video.poster)
print(video.views)
print(video.published)
print(video.like)
print(video.dislike)


# get channel metadata given the username
channel = scrape_channel('https://www.youtube.com/user/teatroallascala')
channel.get_channel_metadata()

print(channel.name)
print(channel.subscribers)
print(channel.views)
print(channel.description)
print(channel.join_date)
print(channel.links)
