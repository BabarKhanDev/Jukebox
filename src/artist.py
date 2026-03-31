class Artist:
    def __init__(self, name, url, images, mbid):
        self.name = name
        self.url = url
        self.images = images
        self.mbid = mbid

    def __repr__(self):
        return f"Artist({self.name}, mbid={self.mbid})"