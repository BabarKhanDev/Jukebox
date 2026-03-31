import requests
import json
from enum import StrEnum

from src.config import get_last_fm_api_details
from src.artist import Artist
from src.album import Album
from src.track import Track

USER_AGENT = "Jukebox/0.0.1"
API_KEY = get_last_fm_api_details().api_key
HEADERS = {'user-agent':USER_AGENT,}

class TimePeriod(StrEnum):
    overall = "overall"
    week = "7day"
    month = "1month"
    quarter = "3month"
    half_year = "6month"
    year = "12month"


def get_top_artists(limit=200):
    payload = {
        'api_key': API_KEY,
        "limit": limit,
        'method': 'chart.gettopartists',
        'format': 'json'
    }

    r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=HEADERS, params=payload)

    artists = []
    for artist in r.json()["artists"]["artist"]:
        artists.append(Artist(
            name=artist["name"],
            url=artist["url"],
            images=artist["image"],
            mbid=artist.get("mbid", None),
        ))
    playcounts = [artist["playcount"] for artist in r.json()["artists"]["artist"]]
    return artists, playcounts, r.json()["artists"]["@attr"]


def get_user_top_artists(user, limit = 200, time_period: TimePeriod = TimePeriod.overall):
    payload = {
        'user': user,
        'limit': limit,
        'api_key': API_KEY,
        "period": time_period,
        'method': 'library.getartists',
        'format': 'json'
    }

    r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=HEADERS, params=payload)

    artists = []
    for artist in r.json()["artists"]["artist"]:
        artists.append(Artist(
            name=artist["name"],
            url=artist["url"],
            images=artist["image"],
            mbid=artist.get("mbid", None),
        ))
    playcounts = [artist["playcount"] for artist in r.json()["artists"]["artist"]]

    return artists, playcounts, r.json()['artists']["@attr"]


def get_user_top_albums(user: str, limit: int = 200, time_period: TimePeriod = TimePeriod.overall):
    payload = {
        'user': user,
        'limit': limit,
        "period": time_period,
        'api_key': API_KEY,
        'method': 'user.gettopalbums',
        'format': 'json'
    }

    r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=HEADERS, params=payload)

    albums = []
    for album in r.json()['topalbums']["album"]:
        albums.append(Album(
            name=album["name"],
            url=album["url"],
            images=album["image"],
            artist_url=album["artist"]["url"],
            artist_name=album["artist"]["name"],
            mbid = album.get("mbid", None),
        ))
    playcounts = [artist["playcount"] for artist in r.json()['topalbums']["album"]]

    return albums, playcounts, r.json()['topalbums']["@attr"]


def get_user_top_tracks(user: str, limit: int = 200, time_period: TimePeriod = TimePeriod.overall):
    payload = {
        'user': user,
        'limit': limit,
        "period": time_period,
        'api_key': API_KEY,
        'method': 'user.gettoptracks',
        'format': 'json'
    }

    r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=HEADERS, params=payload)

    tracks = []
    for track in r.json()["toptracks"]["track"]:
        tracks.append(Track(
            name=track["name"],
            url=track["url"],
            images=track["image"],
            artist_url=track["artist"]["url"],
            artist_name=track["artist"]["name"],
            mbid = track.get("mbid", None),
        ))
    playcounts = [artist["playcount"] for artist in r.json()["toptracks"]["track"]]

    return tracks, playcounts, r.json()['toptracks']["@attr"]


def get_album_tracks(album: Album, limit: int = 10):
    if album.mbid is None:
        payload = {
            "album": album.name,
            "artist": album.artist_name,
            'limit': limit,
            'api_key': API_KEY,
            'method': 'album.getinfo',
            'format': 'json'
        }
    else:
        payload = {
            "mbid": album.mbid,
            'limit': limit,
            'api_key': API_KEY,
            'method': 'album.getinfo',
            'format': 'json'
        }

    r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=HEADERS, params=payload)
    tracks = []
    for track in r.json()["album"]["tracks"]["track"]:
        tracks.append(Track(
            name=track["name"],
            url=track["url"],
            images=track.get("image", []),
            artist_url=track["artist"]["url"],
            artist_name=track["artist"]["name"],
            mbid=track.get("mbid", None),
        ))
    return tracks