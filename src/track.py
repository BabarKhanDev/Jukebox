class Track:
    def __init__(self, name, url, images, mbid, artist_name, artist_url):
        self.name = name
        self.url = url
        self.images = images
        self.mbid = mbid
        self.artist_name = artist_name,
        self.artist_url = artist_url

    def __repr__(self):
        return f"Track({self.name}, mbid={self.mbid})"