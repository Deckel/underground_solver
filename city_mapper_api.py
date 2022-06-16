import requests
from config import secret_key


class CityMapper:
    def __init__(self, secret_key, end_point):
        self.secret_key = secret_key
        self.end_point = end_point

    def travel_time(self, start, end):
        requests.get(
            self.end_point + '1/traveltimes',
            params={'secret_key': self.secret_key}
        )


city_mapper = CityMapper(secret_key, 'https://api.external.citymapper.com/api/')
