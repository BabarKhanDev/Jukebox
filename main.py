from src.album import Album
from src.config import get_username
from src.last_fm import get_user_recent_tracks, find_album_from_track, is_single, get_album_tracks
from src.recommender import get_similar_albums, get_similar_tracks

RECOMMEND_ALBUMS_WITH_LISTENS_FEWER_THAN = 30
NUM_ALBUMS_TO_FIND = 10

def main():
    print("Welcome to Jukebox!")
    print("----------\n")

    username = get_username()

    # Get the most recent 200 songs and albums so that we don't recommend anything recently listened to
    recent_tracks, recent_albums, _ = get_user_recent_tracks(user = username, limit=200)

    # We only use the 20 most recent listened to songs to generate album recommendations
    recommended_albums = set()
    while len(recommended_albums) < NUM_ALBUMS_TO_FIND:
        for track in recent_tracks:
            for recommendation in get_similar_tracks(track, limit=10):
                if recommendation in recent_tracks:
                    continue
                album, listens = find_album_from_track(
                    track=track,
                    user=username
                )

                if album is None or album in recommended_albums or is_single(album):
                    continue

                recommended_albums.add(album)
                print(album)
                if len(recommended_albums) >= NUM_ALBUMS_TO_FIND:
                    break

if __name__ == "__main__":
    main()