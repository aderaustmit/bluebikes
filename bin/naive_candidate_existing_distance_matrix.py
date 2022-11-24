from key import GMAPS_KEY
import googlemaps
import pandas as pd
import numpy as np


def main():
    """Generate distance matrix. dist[i, :] is the distance (meters) from candidate station i to all other existing
    stations """

    # load existing stations
    stations_df = pd.read_csv('data/stations.csv', header=1)
    salem_df = stations_df[stations_df['District'] == 'Salem']
    existing_stations_coord = list(salem_df[['Latitude', 'Longitude']].itertuples(index=False, name=None))

    # load candidate stations
    naive_df = pd.read_csv('inputs/naive_stations.csv')
    naive_stations_coord = list(naive_df[['lat', 'lng']].itertuples(index=False, name=None))

    gmaps = googlemaps.Client(key=GMAPS_KEY)

    distance_list = []
    for candidate_station in naive_stations_coord:
        candidate_distances = []
        distance_matrix_result = gmaps.distance_matrix(origins=candidate_station,
                                                       destinations=existing_stations_coord,
                                                       mode='bicycling')

        # get distance from current candidate station to all other existing stations and append to list
        for result in distance_matrix_result['rows'][0]['elements']:
            candidate_distances.append(result['distance']['value'])

        distance_list.append(candidate_distances)

    distance_array = np.array(distance_list)

    col_nams = list(salem_df["Number"])
    distance_df = pd.DataFrame(distance_array, columns=col_nams)
    distance_df.to_csv('inputs/naive_distance_matrix.csv', index=False)


if __name__ == '__main__':
    main()
