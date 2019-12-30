import requests, json


class APIExtract:

    def __init__(self, api='http://futbol.funx.io/api/v2/sporting-cristal/home/match/'):
        self.url = api

    def connect(self):
        response = requests.get(self.url)

        if response.status_code == 200:
            return response
        else:
            raise ('Hubo un error al conectarse a la API, con código '+response.status_code)


