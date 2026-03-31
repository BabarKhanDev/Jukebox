from src.last_fm import get_user_top_artists, get_user_top_albums, get_top_artists, get_user_top_tracks
from src.recommender import get_similar_tracks, get_similar_artists, get_similar_albums

# print("\nMy Top Artists")
# artists, playcounts, _ = get_user_top_artists("BabarStreisand", limit=5)
# for artist, playcount in zip(artists, playcounts):
#     print(artist, playcount)
#     similar_artists = get_similar_artists(artist, limit=5)
#     print(list(st.name for st in similar_artists))

print("\nTop Albums:")

albums, playcounts, _ = get_user_top_albums("BabarStreisand", limit=5)
for album, playcount in zip(albums, playcounts):
    print(album, playcount)
    similar_albums = get_similar_albums(album, user = "BabarStreisand", limit=5)
    print(list((a[0].name, a[1]) for a in similar_albums))
print("\nTop Tracks:")

# tracks, playcounts, _ = get_user_top_tracks("BabarStreisand", limit=5)
# for track, playcount in zip(tracks, playcounts):
#     print(track, playcount)
#     similar_tracks = get_similar_tracks(track, limit=5)
#     print(list(st.name for st in similar_tracks))