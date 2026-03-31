class Album:
    def __init__(self, name, url, artist_url, artist_name, images, mbid):
        self.name = name
        self.artist_url = artist_url
        self.artist_name = artist_name
        self.images = images
        self.url = url
        self.mbid = mbid

    def __repr__(self):
        return f"Album({self.name} by {self.artist_name})"

    def __eq__(self, other: Album):
        if self.mbid is not None and other.mbid is not None:
            return self.mbid == other.mbid
        return self.name == other.name and self.artist_name == other.artist_name

    def __hash__(self):
        return hash((self.name, self.artist_name))