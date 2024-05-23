from yandex_music import Client
import os
from dotenv import load_dotenv


load_dotenv()
client = Client(token=os.getenv('YANDEX_MUSIC_TOKEN')).init()


def get_tracks(track_name):
    search_results = client.search(track_name)
    if not search_results or not search_results.tracks:
        return []
    tracks = search_results.tracks['results']
    return tracks


def get_info(track):
    artists = ', '.join(artist['name'] for artist in track['artists'])
    return track['title'], artists
    

def download_track(track_name):
    track = (get_tracks(track_name))[0]
    artists = ', '.join(artist['name'] for artist in track['artists'])
    filename = f'./music/{artists}-{track["title"]}.mp3'
    if not os.path.exists(filename):
        track.download(filename)