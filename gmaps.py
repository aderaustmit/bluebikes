import googlemaps
from key import API_KEY

if __name__ == '__main__':
    gmaps = googlemaps.Client(key=API_KEY)

    bb_station = (42.51825444416107, -70.89571747970832)
    market_basket_location = (42.504556602893025, -70.92013631089728)

    distance_matrix_result = gmaps.distance_matrix(origins=bb_station, destinations=market_basket_location,
                                                   mode='bicycling')

    print(distance_matrix_result)

    # find places near market_basket grocery store within a ~.5 mile radius
    places_nearby_results = gmaps.places_nearby(location=market_basket_location, radius=1000)
    print(places_nearby_results)