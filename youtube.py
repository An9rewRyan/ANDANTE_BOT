from __future__ import unicode_literals
import yt_dlp
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
    'postprocessors': [{  
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }]
}

yt = YTMusic()

def get_song(title: str):
    results = yt.search(title)
    for elem in results:
        if elem["category"] == "Songs":
            return elem

def load_video(link: str, title: str, artist: str) -> str|None:
    ydl_opts['outtmpl'] = f'ANDANTE_BOT/{artist} - {title}.mp3'
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(link)
    if error_code:
        print(error_code)
        return None
    return title

def get_artist_name(song) -> str:
    if "artists" in song:
        artists = ''
        for artist in song["artists"]:
            artists+=artist["name"]+", "
        return artists[:-2]
    return 'Unknown'

def get_link(elem: dict):
    return f'https://music.youtube.com/watch?v={elem["videoId"]}' 

def out(title: str):
    song = get_song(title)
    link = get_link(song)
    artist = get_artist_name(song)
    return load_video(link, song["title"], artist), artist


