"""
Geocoding and Web APIs Project Toolbox exercise

Find the MBTA stops closest to a given location.

Full instructions are at:
https://sites.google.com/site/sd15spring/home/project-toolbox/geocoding-and-web-apis
"""
import mbta_finder
from urllib.request import urlopen
import json
from pprint import pprint
import requests

# Useful URLs (you need to add the appropriate parameters for your requests)
GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
MBTA_BASE_URL = "http://realtime.mbta.com/developer/api/v2/stopsbylocation"
MBTA_DEMO_API_KEY = "wX9NwuHnZU2ToO7GmGR9uw"


# A little bit of scaffolding if you want to use it

def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urlopen(url)
    response_text = f.read()
    response_data = json.loads(str(response_text, "utf-8"))
    #pprint(response_data)
    return response_data
    #print(response_data["results"][0]["formatted_address"])

def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.

    See https://developers.google.com/maps/documentation/geocoding/
    for Google Maps Geocode API URL formatting requirements.
    """
    address = place_name
    api_key = "AIzaSyD2JPzBFmxl47xySMsHYTdp3_q4A4xJjTI"
    api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
    api_response_dict = api_response.json()

    if api_response_dict['status'] == 'OK':
        latitude = api_response_dict['results'][0]['geometry']['location']['lat']
        longitude = api_response_dict['results'][0]['geometry']['location']['lng']
        print ('Latitude:', latitude)
        print ('Longitude:', longitude)

    return latitude, longitude

def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, distance)
    tuple for the nearest MBTA station to the given coordinates.

    See http://realtime.mbta.com/Portal/Home/Documents for URL
    formatting requirements for the 'stopsbylocation' API.
    """
    url2 = "http://realtime.mbta.com/developer/api/v2/stopsbylocation?api_key=wX9NwuHnZU2ToO7GmGR9uw&lat=42.346961&lon=-71.076640&format=json"
    chosen_location = '&lat=' + str(latitude) + '&lon=' + str(longitude) + "&format=json"
    url2_specific = url2+chosen_location
    response_data = get_json(url2_specific)
    near_station = response_data["stop"][0]["stop_name"]
    station_dist = response_data["stop"][0]["distance"]

    return near_station, station_dist


def find_stop_near(place_name):
    """
    Given a place name or address, print the nearest MBTA stop and the
    distance from the given place to that stop.
    """
    loc_input = input('Please enter a location:    ')
    latitude, longitude = get_lat_long(loc_input)
    nearest_station = get_nearest_station(latitude, longitude)
    nearest_station_input = nearest_station[0]
    nearest_station_dist_input = nearest_station[1]
    print('The nearest station to ' + loc_input + ' is ' + nearest_station_input + ' which is ' + nearest_station_dist_input + ' miles away.')

    # return nearest_station
    # print (nearest_station)

if __name__ == "__main__":
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=Fenway%20Park"
    get_json(url)
    place_name = "4 Yawkey Way, Boston, MA 02215, USA"
    latitude, longitude = get_lat_long(place_name)
    near_station, station_dist = get_nearest_station(latitude, longitude)
    find_stop_near(place_name)
