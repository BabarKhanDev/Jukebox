class Track:
    def __init__(self, name, url, images, mbid, artist_name, artist_url):
        self.name = name
        self.url = url
        self.images = images
        self.mbid = mbid
        self.artist_name = artist_name
        self.artist_url = artist_url

    def __repr__(self):
        return f"Track({self.name} by {self.artist_name})"

    def __eq__(self, other: Track):
        if self.mbid is not None and other.mbid is not None:
            return self.mbid == other.mbid
        return self.name == other.name and self.artist_name == other.artist_name

    def __hash__(self):
        return hash((self.name, self.artist_name))