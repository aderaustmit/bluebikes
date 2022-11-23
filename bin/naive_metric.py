import pandas as pd
import numpy as np
from geopy.distance import geodesic
from utils import load_config, isitwater

np.random.seed(42)

config = load_config()

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


def main():
    demand = pd.read_csv('inputs/salem_demand.csv')

    # make copy of demand df
    demand_copy = demand.copy()

    candidate_stations = []
    while len(candidate_stations) < N_NEW_STATIONS:
        # get the station with the highest demand
        highest_demand_idx = demand_copy['demand'].idxmax()

        # get lat, lng of highest demand station
        highest_dmd_lat = demand_copy.loc[highest_demand_idx, 'Latitude']
        highest_dmd_lng = demand_copy.loc[highest_demand_idx, 'Longitude']

        # create candidate station at random point on circle of radius DISTANCE_THRESHOLD
        rnd_coord = create_random_point_on_circle(x0=highest_dmd_lat, y0=highest_dmd_lng, distance=DISTANCE_THRESHOLD)
        print(f"Creating initial random candidate station at {rnd_coord}")

        # keep generating random points until we find one that is not water
        while isitwater(rnd_coord[0], rnd_coord[1]):
            print(f"Random water coord: {rnd_coord} is in the water generating new one")
            rnd_coord = create_random_point_on_circle(x0=highest_dmd_lat, y0=highest_dmd_lng,
                                                      distance=DISTANCE_THRESHOLD)
        print(f"Random coord: {rnd_coord} is out of the water")

        # check if candidate station is within DISTANCE_THRESHOLD of any existing station
        # if not, append to candidate_stations.csv
        # if yes, remove the highest demand station from demand_copy and repeat
        if not any([geodesic(rnd_coord, (lat, lng)).meters < DISTANCE_THRESHOLD for lat, lng in candidate_stations]) \
                and not any([geodesic(rnd_coord, (lat, lng)).meters < DISTANCE_THRESHOLD for lat, lng in
                             zip(demand_copy.drop(highest_demand_idx)['Latitude'],
                                 demand_copy.drop(highest_demand_idx)['Longitude'])]):
            print(f"Random coord: {rnd_coord} meets distance threshold")
            candidate_stations.append(rnd_coord)
        else:
            print(f"Random coord: {rnd_coord} does not meet distance threshold")
            demand_copy.drop(highest_demand_idx, inplace=True)

    naive_stations_dict = {"naive_stations": candidate_stations}
    naive_stations_df = pd.DataFrame(naive_stations_dict)
    naive_stations_df.to_csv('inputs/naive_stations.csv', index=False)


if __name__ == '__main__':
    main()
