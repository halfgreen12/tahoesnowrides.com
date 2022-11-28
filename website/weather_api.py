import requests
import datetime
from pprint import pprint
import os
import json

with open('/etc/tahoe_rides_config.json') as config_file:
        config = json.load(config_file)

# weather api function
def main(city_input):
    api_key = config.get('NEW_FLASK_SNOWBOARD_OPENWEATHER_API_KEY')
    # function to calculate time from 5 days ago and convert to unix time

    def twentyfour_hours_ago():
        current_time = datetime.datetime.now(datetime.timezone.utc)
        unix_timestamp = int(current_time.timestamp())
        unix_timestamp_minus_24_hours = str(unix_timestamp - 86_400)
        return unix_timestamp_minus_24_hours

    try:
        # api to convert city to geographical coordinates
        geocode_url = "http://api.openweathermap.org/geo/1.0/direct?q=" + city_input + "&limit=1&appid=" + api_key

        geo_api_link = requests.get(geocode_url)
        geo_api_data = geo_api_link.json()
        # print(geo_api_data)

        # store geographical coordinates in variables for main function api call
        latitude = str(geo_api_data[0]['lat'])
        longitude = str(geo_api_data[0]['lon'])

    # exception for invalid city
    except Exception as err:
        error_string = str(err)

    def call_api():
        # end function if an invalid city was entered
        if not geo_api_data:
            result1 = "Please enter a valid city."
            result2 = ""  # must return empty string because views.home() is expecting two variables.
            return result1, result2
        else:
            base_url = "https://api.openweathermap.org/data/2.5/onecall/timemachine?lat=" \
                       + latitude + "&lon=" + longitude + "&dt="\
                       + twentyfour_hours_ago() + "&units=imperial&appid=" + api_key

            api_link = requests.get(base_url)
            api_data = api_link.json()

            # get the total historical temperature data by indexing two levels into json data
            total = 0
            for row in api_data['hourly']:
                total = total + row['temp']
            # pprint(api_data)

            # compute the average temperature data and return result to views.home()
            length = len(api_data['hourly'])
            average = total / length
            if average <= 45:
                result1 = f"{city_input} is a good place to snowboard!"
            else:
                result1 = f"It's too hot to snowboard in {city_input}."
            result2 = f'The average temp. from the last 24 hours is {average:.2f} °F.'
            # print(result1, result2)
        return result1, result2

    return call_api()
