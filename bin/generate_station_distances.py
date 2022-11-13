from key import API_KEY
import googlemaps
import pandas as pd
import numpy as np

DUMMY_CANDIDATE_STATIONS = [(42.51293825329633, -70.90182181789602), (42.511799420282124, -70.91572638951338)]


def main():
    """Generate distance matrix. dist[i, :] is the distance (meters) from candidate station i to all other existing
    stations """

    # load existing stations
    stations_df = pd.read_csv('data/stations.csv', header=1)
    salem_df = stations_df[stations_df['District'] == 'Salem']
    existing_stations_coord = list(salem_df[['Latitude', 'Longitude']].itertuples(index=False, name=None))

    gmaps = googlemaps.Client(key=API_KEY)

    master_list = []
    for candidate_station in DUMMY_CANDIDATE_STATIONS:
        candidate_distances = []
        distance_matrix_result = gmaps.distance_matrix(origins=candidate_station,
                                                       destinations=existing_stations_coord,
                                                       mode='bicycling')

        # get distance from current candidate station to all other existing stations
        for result in distance_matrix_result['rows'][0]['elements']:
            candidate_distances.append(result['distance']['value'])

        master_list.append(candidate_distances)

    distance_array = np.array(master_list)
    distance_df = pd.DataFrame(distance_array, columns=salem_df["Number"])
    distance_df.to_csv('input/distance_matrix.csv', index=False)


if __name__ == '__main__':
    main()
