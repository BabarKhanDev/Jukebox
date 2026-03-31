import operator

import requests
import json
from enum import StrEnum

from src.config import get_last_fm_api_details
from src.artist import Artist
from src.album import Album
from src.last_fm import get_album_tracks
from src.track import Track

USER_AGENT = "Jukebox/0.0.1"
API_KEY = get_last_fm_api_details().api_key
HEADERS = {'user-agent':USER_AGENT,}

def get_similar_tracks(track: Track, limit: int = 10):
    payload = {
        'limit': limit,
        'api_key': API_KEY,
        'method': 'track.getsimilar',
        'format': 'json'
    }
    if track.mbid is None:
        payload["track"] = track.name
        payload["artist"] = track.artist_name
    else:
        payload["mbid"] =  track.mbid

    r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=HEADERS, params=payload)
    tracks = list(map(
        lambda t: Track(
            name=t["name"],
            url=t["url"],
            images=t["image"],
            artist_url=t["artist"]["url"],
            artist_name=t["artist"]["name"],
            mbid=t.get("mbid", None),
        ),
        r.json().get("similartracks", {"track": []}).get('track', [])))
    return tracks


def get_similar_artists(artist: Artist, limit: int = 10):
    if artist.mbid is None:
        payload = {
            "artist": artist.name,
            'limit': limit,
            'api_key': API_KEY,
            'method': 'artist.getsimilar',
            'format': 'json'
        }
    else:
        payload = {
            "mbid": artist.mbid,
            'limit': limit,
            'api_key': API_KEY,
            'method': 'artist.getsimilar',
            'format': 'json'
        }

    r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=HEADERS, params=payload)
    artists = list(map(
        lambda artist: Artist(
            name=artist["name"],
            url=artist["url"],
            images=artist["image"],
            mbid=artist.get("mbid", None),
        ),
        r.json()["similarartists"]['artist']))
    return artists

def get_similar_albums(album: Album, user: str, limit: int = 10):
    # LastFM does not have an endpoint to get similar albums
    # Step 1. get the tags for this album
    payload = {'api_key': API_KEY, 'method': 'album.gettoptags', 'format': 'json', "album": album.name,
               "artist": album.artist_name}
    r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=HEADERS, params=payload)
    tags = list(map(
        lambda x: {"name": x["name"], "count": x["count"]},
        r.json()["toptags"]["tag"]
    ))

    times_album_found = {}
    for tag in tags:
        payload = {'api_key': API_KEY, 'method': 'tag.gettopalbums', 'format': 'json', 'tag': tag["name"], "limit": 40}
        r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=HEADERS, params=payload)
        albums_found = list(map(
            lambda a: Album(
                name=a["name"],
                url=a["url"],
                images=a["image"],
                artist_url=a["artist"]["url"],
                artist_name=a["artist"]["name"],
                mbid=a.get("mbid", None),
            ),
            r.json()["albums"]["album"]
        ))

        for a in albums_found:
            if a == album:
                continue
            if a not in times_album_found:
                times_album_found[a] = 0
            times_album_found[a] += 1

    sorted_found_albums = sorted(times_album_found.items(), key=operator.itemgetter(1), reverse=True)

    return sorted_found_albums

    # Step 2. get the albums with similar tags to that



    # tracks = get_album_tracks(album)
    # similar_tracks = {}
    # for track in tracks:
    #     for st in get_similar_tracks(track, limit):
    #         if similar_tracks.get(st.name) is None:
    #             similar_tracks[st.name] = 0
    #         similar_tracks[st.name] += 1
    # sorted_similar_albums = sorted(similar_albums, key=similar_albums.get, reverse=True)
    # print(list(zip(sorted_similar_albums, [similar_albums[key] for key in sorted_similar_albums])))

    return similar_tracks