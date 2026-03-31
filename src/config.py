import configparser

class LastFMDetails:
    def __init__(self, api_key, shared_secret):
        self.api_key = api_key
        self.shared_secret = shared_secret


def get_last_fm_api_details(config_location: str = "config.ini") -> LastFMDetails:
    config = configparser.ConfigParser()
    config.read(config_location)

    api_key = config.get("LastFM", "API_KEY")
    shared_secret = config.get("LastFM", "SHARED_SECRET")

    return LastFMDetails(api_key, shared_secret)
