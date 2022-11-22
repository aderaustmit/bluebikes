import requests
from key import ISITWATER_KEY
import json


def load_config() -> dict:
    with open('config.json', 'r') as openfile:
        config = json.load(openfile)
    return config


def isitwater(lat: float, lng: float) -> bool:
    url = "https://isitwater-com.p.rapidapi.com/"

    querystring = {"latitude": str(lat), "longitude": str(lng)}

    headers = {
        "X-RapidAPI-Key": ISITWATER_KEY,
        "X-RapidAPI-Host": "isitwater-com.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return json.loads(response.text)["water"]


if __name__ == '__main__':
    print(isitwater(12.9716, 77.5946))
