import configparser
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
