import json
from urllib.request import urlopen
import pandas as pd

BLUE_BIKES_URL = "https://gbfs.bluebikes.com/gbfs/gbfs.json"


def download_json(url):
    with urlopen(url) as response:
        return json.loads(response.read().decode())


def get_bluebikes_data(url):
    data = download_json(url)
    df = pd.DataFrame.from_dict(data['data']['stations'])
    return df


if __name__ == '__main__':
    url_list = download_json(BLUE_BIKES_URL)

    STATION_URL = url_list['data']['en']['feeds'][1]['url']
    station_df = get_bluebikes_data(STATION_URL)
    print(station_df.head())
    station_df.to_csv('data/bluebikes.csv', index=False)

    FREE_BIKE_URL = url_list['data']['en']['feeds'][2]['url']
    free_bike_df = get_bluebikes_data(FREE_BIKE_URL)
    print(free_bike_df.head())
    free_bike_df.to_csv('data/bluebikes_free.csv', index=False)
