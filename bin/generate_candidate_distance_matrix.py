from key import GMAPS_KEY
import googlemaps
import pandas as pd
import numpy as np
from utils import isitwater


def main():
    """Generate distance matrix. dist[i, :] is the distance (meters) from candidate station i to all other existing
    stations """

    # load existing stations
    stations_df = pd.read_csv('data/stations.csv', header=1)
    salem_df = stations_df[stations_df['District'] == 'Salem']
    existing_stations_coord = list(salem_df[['Latitude', 'Longitude']].itertuples(index=False, name=None))

    # load candidate stations
    candidate_df = pd.read_csv('inputs/candidate_stations.csv')
    candidate_stations_coord = list(candidate_df[['Latitude', 'Longitude']].itertuples(index=False, name=None))

    gmaps = googlemaps.Client(key=GMAPS_KEY)

    distance_list = []
    candidate_address_list = []
    for candidate_station in candidate_stations_coord:
        candidate_distances = []
        distance_matrix_result = gmaps.distance_matrix(origins=candidate_station,
                                                       destinations=existing_stations_coord,
                                                       mode='bicycling')
        # append origin address to candidate_address_list
        origin_address = distance_matrix_result['origin_addresses'][0]

        # skip if Unnamed Road
        if isitwater(candidate_station[0], candidate_station[1]):
            print("coordinate in water, skipping")
            continue

        # append address list for later
        candidate_address_list.append(origin_address)

        # get distance from current candidate station to all other existing stations and append to list
        for result in distance_matrix_result['rows'][0]['elements']:
            candidate_distances.append(result['distance']['value'])

        distance_list.append(candidate_distances)

    distance_array = np.array(distance_list)

    col_nams = list(salem_df["Number"])
    distance_df = pd.DataFrame(distance_array, columns=col_nams)
    distance_df.to_csv('inputs/candidate_existing_distance.csv', index=False)

    candidate_coords = []
    for candidate_address in candidate_address_list:
        geocode_result = gmaps.geocode(candidate_address)
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
        coord = (lat, lng)

        candidate_coords.append(coord)

    candidate_address_dict = {"Address": candidate_address_list, "Coordinates": candidate_coords}

    candidate_address_df = pd.DataFrame(candidate_address_dict)
    candidate_address_df['lat'], candidate_address_df['lng'] = candidate_address_df.Coordinates.str
    candidate_address_df.to_csv('inputs/candidate_address.csv', index=False)


if __name__ == '__main__':
    main()
