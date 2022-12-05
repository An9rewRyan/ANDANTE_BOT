from __future__ import unicode_literals
import yt_dlp
from ytmusicapi import YTMusic
import requests
import re
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def my_hook(d):
    if d['status'] == 'downloading':
        print ("downloading "+ str(round(float(d['downloaded_bytes'])/float(d['total_bytes'])*100,1))+"%")
    if d['status'] == 'finished':
        filename=d['filename']
        print(filename)

ydl_opts = {
    'format': 'bestaudio/best',
    # "quiet":    True,
    # "simulate": True,
    # "forceurl": True,
    'postprocessors': [{  
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }],
    'progress_hooks': [my_hook]
}

yt = YTMusic()

def get_song(title: str):
    results = yt.search(title)
    for elem in results:
        if elem["category"] == "Songs":
            print(elem)
            return elem

def load_video(link: str, title: str, artist: str) -> None:
    ydl_opts['outtmpl'] = os.path.join(BASE_DIR, f'{artist} - {title}.mp3')
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error = ydl.download([link])
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
    title = load_video(link, song["title"], artist)
    return title, artist



