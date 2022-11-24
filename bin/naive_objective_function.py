import pandas as pd

from utils import load_config

config = load_config()

N_NEW_STATIONS = config["N_NEW_STATIONS"]
DISTANCE_THRESHOLD = config["DISTANCE_THRESHOLD"]


def main():
    naive_distance_df = pd.read_csv('inputs/naive_distance_matrix.csv')
    demand = pd.read_csv('inputs/salem_demand.csv')['demand'].values

    # sum(-distance[i, j] * demand[j] * z[i] for i = 1:N_CANDIDATE_STATIONS, j = 1:N_CURRENT_STATIONS

    obj = 0
    # loop through rows of naive_distance_df using iterrows
    for index, row in naive_distance_df.iterrows():
        # loop through columns of row
        for col in row:
            # multiply col by demand[index] and add to obj
            obj += -col * demand[index]
    print(obj)


if __name__ == '__main__':
    main()
