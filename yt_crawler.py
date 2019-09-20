from youtube_scraper.scraper import scrape_video, scrape_channel, get_mongodb

print('Test scraper functionalities')

# get channel metadata given the username
channel = scrape_channel('https://www.youtube.com/user/teatroallascala')

channel.get_channel_metadata()
print(channel.name, channel.subscribers, channel.views, channel.join_date)
print(channel.description)
print(channel.links)

channel.get_channel_videos()
for v in channel.videos:
    print(v.id, v.title, v.duration, v.published, v.like, v.dislike)

# store data in MongoDB
db = get_mongodb('mongodb://127.0.0.1:27017')

# save channel metadata
db.save_channel(channel)

# save channel videos data
for v in channel.videos:
    db.save_video(v)

# get video data given the url and save it (no ID for now!)
video = scrape_video('http://youtube.com/watch?v=7dlcxXxDGUI')
db.save_video(video)
