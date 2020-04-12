import configparser
import pandas as pd
import ptv_api as pa

# Read configuration
config = configparser.ConfigParser()
config.read('ptv_api_key')
devid = config.get('default', 'devid')
api_key = config.get('default', 'api_key')

# Instantiate API
con = pa.PtvApiV3(devid=devid, api_key=api_key)

# Get all the routes
all_routes = con.get('routes')['routes']

# Get train routes, these are routes with `route_type` equals to 0.
train_routes = [route for route in all_routes if route['route_type'] == 0]


# I have the train route id
#
# I need to get all departures, to and from
# Extract all train route ID
train_route_dict = {l['route_id']: l['route_name'] for l in train_routes}

# Extract all train stops


def get_stops_by_route_id(route_id):
    endpoint = 'stops/route/{}/route_type/0'.format(route_id)
    return pd.DataFrame(con.get(endpoint)['stops'])


all_train_stops = (
    pd.concat(
        [get_stops_by_route_id(route_id)
         for route_id in train_route_dict.keys()])
    .drop_duplicates())

# Wiki shows there are 218 currently operating, I have 222. So it's
# not too far fetched, but need to double check.


def get_all_service_by_stop(stop_id):
    endpoint = 'departures/route_type/0/stop/{}/?max_results=1000000'.format(
        stop_id)
    return con.get(endpoint)['departures']


con.get('directions/route/1')


test = get_all_service_by_stop(1034)

# We can subset by 7 days.


stop_departures_dict = {stops: len(get_all_service_by_stop(stops))
                        for stops in all_train_stops.stop_id}
stop_departure_df = (
    pd.DataFrame.from_dict(stop_departures_dict, orient='index')
    .reset_index()
    .rename(columns={'index': 'stop_id', 0: 'number_of_services'}))


pd.merge(stop_departure_df, all_train_stops[[
         'stop_id', 'stop_name']]).sort_values('number_of_services').tail(25)
