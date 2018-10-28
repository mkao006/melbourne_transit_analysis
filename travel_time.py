import googlemaps
import datetime
import numpy as np

# Read the api key
with open('google_api_key', 'r') as f:
    my_api_key = f.read()

# Instantiate the google map object
gmaps = googlemaps.Client(key=my_api_key)

# Define custom function


def get_next_monday(date):
    day_today = date.weekday()
    day_till_next_monday = (-day_today + 7) % 7
    return date + datetime.timedelta(days=day_till_next_monday)


def calculate_average_travel_time(gmap_obj, origin, destination, mode,
                                  to_work_times, to_home_times):
    # Compute the hour to get to work
    to_work_result = [gmap_obj(origin, destination, mode=mode,
                               departure_time=s)
                      for s in to_work_times]
    to_work_travel_times = [info[0]['legs'][0]['duration']['value']
                            for info in to_work_result]
    to_home_result = [gmap_obj(destination, origin, mode=mode,
                               departure_time=s)
                      for s in to_home_times]
    to_home_travel_times = [info[0]['legs'][0]['duration']['value']
                            for info in to_home_result]
    return np.mean(to_work_travel_times + to_home_travel_times)


# We generate a set of possible commute times to sample the average travel
# time.
next_monday = get_next_monday(datetime.date.today())
working_days = [next_monday + datetime.timedelta(days=i) for i in range(5)]
hour_to_work = [7, 8, 9, 10]
hour_to_home = [16, 17, 18]
minute_sample = [0, 15, 30, 45]
to_work_time = [datetime.datetime.combine(day, datetime.time(hour, minute))
                for hour in hour_to_work
                for minute in minute_sample
                for day in working_days]
to_home_time = [datetime.datetime.combine(day, datetime.time(hour, minute))
                for hour in hour_to_home
                for minute in minute_sample
                for day in working_days]

avg_time = calculate_average_travel_time(gmaps.directions,
                                         origin="camberwell station + train",
                                         destination="Southern cross station",
                                         mode="transit",
                                         to_work_times=to_work_time,
                                         to_home_times=to_home_time)

# There is something wrong with the transit time obtained. Google
# shows 19 minute for the train and a total travel time of 22 min,
# while the API returned 16 min travel time, and a total travel time
# of 16 minutes.
check = gmaps.directions("southern cross station",
                         "camberwell station",
                         mode="transit",
                         departure_time=datetime.datetime(2018, 10, 29, 17, 45, 0))

# TODO (Michael): Check how to restrict search to 'train'.
