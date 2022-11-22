
import json
import pandas as pd
import random
import numpy as np
from geopy.distance import geodesic
from key import API_KEY
import googlemaps

# random.seed(42)
# np.random.seed(42)

with open('config.json', 'r') as openfile:
    config = json.load(openfile)

N_NEW_STATIONS = config["N_NEW_STATIONS"]
DISTANCE_THRESHOLD = config["DISTANCE_THRESHOLD"]


# kind of works....
def create_random_point_on_circle(x0, y0, distance):
    """Create random point on circle of radius distance from x0, y0"""
    r = distance / 111300  # assuming distance is in meters
    v = np.random.uniform(0, 1)
    theta = 2 * np.pi * v
    x = r * np.cos(theta)
    # x_new = x / np.cos(y0)
    y = r * np.sin(theta)
    return x0 + x, y0 + y

gmaps = googlemaps.Client(key=API_KEY)


demand = pd.read_csv('inputs/salem_demand.csv')

# make copy of demand df
demand_copy = demand.copy()


candidate_stations = []
while len(candidate_stations) < N_NEW_STATIONS:
    # get the station with the highest demand
    highest_demand_idx = demand_copy['demand'].idxmax()

    # get lat, lng of highest demand station
    highest_dmd_lat = demand_copy.loc[highest_demand_idx, 'Latitude']
    print(highest_dmd_lat)
    highest_dmd_lng = demand_copy.loc[highest_demand_idx, 'Longitude']

    # create candidate station at random point on circle of radius DISTANCE_THRESHOLD
    rnd_coord = create_random_point_on_circle(x0=highest_dmd_lat, y0=highest_dmd_lng, distance=DISTANCE_THRESHOLD)
    reverse_geocode_result = gmaps.reverse_geocode(rnd_coord)
    print("reverse_geocode_result: ", reverse_geocode_result)

    # check if candidate station is within DISTANCE_THRESHOLD of any existing station
    # if not, append to candidate_stations
    # if yes, remove highest demand station from demand_copy and repeat
    if not any([geodesic(rnd_coord, (lat, lng)).meters < DISTANCE_THRESHOLD for lat, lng in candidate_stations])\
            and not any([geodesic(rnd_coord, (lat, lng)).meters < DISTANCE_THRESHOLD for lat, lng in
                     zip(demand_copy.drop(highest_demand_idx)['Latitude'],
                         demand_copy.drop(highest_demand_idx)['Longitude'])]):
        candidate_stations.append(rnd_coord)
    else:
        print('removing station')
        demand_copy.drop(highest_demand_idx, inplace=True)

print(candidate_stations)

# for idx, row in demand_copy.iterrows():
#     if idx == highest_demand_idx:
#         continue
#     lat_i = row['Latitude']
#     lng_i = row['Longitude']
#     distance = geodesic(rnd_coord, (lat_i, lng_i)).meters
#     print(f"distance: {distance}")
#     if distance < DISTANCE_THRESHOLD:
#         print("distance is less than DISTANCE_THRESHOLD, removing from demand_copy")
#         # delete row from demand_copy
#         demand_copy.drop(idx, inplace=True)
#
#         # exit loop
#         break
