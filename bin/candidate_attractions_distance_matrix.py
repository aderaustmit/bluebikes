from key import GMAPS_KEY
import googlemaps
import pandas as pd
import numpy as np


def main():
    """Generate distance matrix. dist[i, :] is the distance (meters) from candidate station i to all other existing
    stations """

    # load attraction locations
    attractions_df = pd.read_csv('inputs/attractions_locations.csv')
    attractions_coords = list(attractions_df[['Latitude', 'Longitude']].itertuples(index=False, name=None))

    # load candidate stations
    candidate_df = pd.read_csv('inputs/candidate_stations.csv')
    candidate_stations_coord = list(candidate_df[['Latitude', 'Longitude']].itertuples(index=False, name=None))

    gmaps = googlemaps.Client(key=GMAPS_KEY)

    distance_list = []
    for candidate_station in candidate_stations_coord:
        candidate_distances = []
        distance_matrix_result = gmaps.distance_matrix(origins=candidate_station,
                                                       destinations=attractions_coords,
                                                       mode='bicycling')

        # get distance from current candidate station to all other existing stations and append to list
        for result in distance_matrix_result['rows'][0]['elements']:
            candidate_distances.append(result['distance']['value'])

        distance_list.append(candidate_distances)

    distance_array = np.array(distance_list)

    col_nams = list(attractions_df["Attraction"])
    distance_df = pd.DataFrame(distance_array, columns=col_nams)
    distance_df.to_csv('inputs/candidate_attraction_distance.csv', index=False)


if __name__ == '__main__':
    main()
