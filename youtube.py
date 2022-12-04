from __future__ import unicode_literals
import youtube_dl
from ytmusicapi import YTMusic

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

yt = YTMusic()

def get_song(title: str):
    results = yt.search(title)
    for elem in results:
        if elem["category"] == "Songs":
            return elem

def load_video(link: str, title: str) -> str:
    ydl_opts['outtmpl'] = f'ANDANTE_BOT/{title}.mp3'
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
    return f'{title}.mp3'

def get_link(elem: dict):
    return f'https://music.youtube.com/watch?v={elem["videoId"]}' 

def out(title: str):
    song = get_song(title)
    link = get_link(song)
    print(song)
    return load_video(link, song["title"])

# main('highway to hell')






# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#     ydl.download(['https://music.youtube.com/watch?v=gEPmA3USJdI'])

