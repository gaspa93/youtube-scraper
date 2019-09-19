youtube-scraper
===============

Provide information for youtube video metadata (title, user, views, likes, dislikes, publish date) and youtube channel metadata (name, subscribers, description, views, join date, links).

Usage
-----

To scrape Youtube video data, use scrape_video endpoint:

    >>> from youtube_scraper.scraper import scrape_video
    >>> data = scrape_video('http://youtube.com/watch?v=7dlcxXxDGUI')
    >>> print(data.poster)
    'TheViperAOC'

To scrape Youtube channel data, use scrape_channel endpoint:

    >>> from youtube_scraper.scraper import scrape_channel
    >>> channel = scrape_channel('https://www.youtube.com/user/teatroallascala')
    >>> channel.get_channel_metadata()
    >>> print(channel.name)
    'Teatro all Scala'
    >>> print(channel.description)
    'The Opera House making history since 1778'

License
-------

Copyright (c) 2015 Jon Robison

See included LICENSE for licensing information
