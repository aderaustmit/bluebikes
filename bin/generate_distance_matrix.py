from key import API_KEY
import googlemaps
import pandas as pd
import numpy as np


def main():
    """Generate distance matrix. dist[i, :] is the distance (meters) from candidate station i to all other existing
    stations """

    # load existing stations
    stations_df = pd.read_csv('data/stations.csv', header=1)
    existing_df = stations_df[stations_df['District'] == 'Salem']
    existing_stations_coord = list(existing_df[['Latitude', 'Longitude']].itertuples(index=False, name=None))

    # load candidate stations
    candidate_df = pd.read_csv('inputs/new_stations_df')
    candidate_stations_coord = list(candidate_df[['Latitude', 'Longitude']].itertuples(index=False, name=None))

    gmaps = googlemaps.Client(key=API_KEY)

    master_list = []
    for candidate_station in candidate_stations_coord:
        candidate_distances = []
        distance_matrix_result = gmaps.distance_matrix(origins=candidate_station,
                                                       destinations=existing_stations_coord,
                                                       mode='bicycling')

        # get distance from current candidate station to all other existing stations and append to list
        for result in distance_matrix_result['rows'][0]['elements']:
            candidate_distances.append(result['distance']['value'])

        # then append origin address to list
        candidate_distances.append(distance_matrix_result['origin_addresses'][0])

        master_list.append(candidate_distances)

    distance_array = np.array(master_list)

    col_nams = list(existing_df["Number"])
    col_nams.append("origin_address")

    distance_df = pd.DataFrame(distance_array, columns=col_nams)
    distance_df.to_csv('inputs/distance_matrix.csv', index=False)


if __name__ == '__main__':
    main()
