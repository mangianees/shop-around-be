import requests
import json
import os

# Your Google Places API key
api_key = 'AIzaSyDug2H25Ibza9XgkDvk3zLtEWwbxK0LCxA'

# Coordinates for Leeds, UK
location = '53.8065269,-1.5257495'  # Latitude and Longitude of Leeds
radius = 500  # radius for nearby search

# Base URLs for Places API
places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
details_url = "https://maps.googleapis.com/maps/api/place/details/json"

# Function to get nearby places
def get_nearby_places(location, radius, type, api_key):
    params = {
        'location': location,
        'radius': radius,
        'type': type,
        'key': api_key
    }
    response = requests.get(places_url, params=params)
    return response.json()

# Function to get details of a place
def get_place_details(place_id, api_key):
    params = {
        'place_id': place_id,
        'fields': 'name,geometry,opening_hours,photos',
        'key': api_key
    }
    response = requests.get(details_url, params=params)
    return response.json()

# Main function to get list of shops and their details
def main():
    type = 'store'  # type of place to search for
    nearby_places = get_nearby_places(location, radius, type, api_key)
    
    shops = []
    for place in nearby_places['results'][:60]:
        place_id = place['place_id']
        details = get_place_details(place_id, api_key)
        shop_info = details.get('result', {})
        shops.append(shop_info)
    
    print(len(shops))
    
    # Choose the location for the new JSON file
    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath('../full_json_files/leeds_shops8.json', cur_path)

    # Save the results to a JSON file
    with open(new_path, 'w') as f:
        json.dump(shops, f, indent=4)
        

if __name__ == "__main__":
    main()

