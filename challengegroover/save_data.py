from tinydb import TinyDB, Query
import json
import requests
import os
import errno

CLIENT_ID=os.environ.get("CLIENT_ID")
CLIENT_SECRET=os.environ.get("CLIENT_SECRET")

def fetch_data():
    AUTH_URL = 'https://accounts.spotify.com/api/token'

    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()

    access_token = auth_response_data['access_token']
    url = 'https://api.spotify.com/v1/browse/new-releases?country=FR&&limit=50'

    response = requests.request('GET', url, headers={
        'Authorization': 'Bearer ' + access_token,
    })

    artist_name = []
    track_name = []
    release_date = []
    album_type = []
    url = []
    n = len(response.json()["albums"]["items"])
    for i in range(n):
        artist_name.append(response.json()["albums"]["items"][i]["artists"][0]["name"])
        track_name.append(response.json()["albums"]["items"][i]["name"])
        release_date.append(response.json()["albums"]["items"][i]["release_date"])
        album_type.append(response.json()["albums"]["items"][i]["album_type"])
        url.append(response.json()["albums"]["items"][i]["external_urls"]["spotify"])

    return (artist_name, track_name, release_date, album_type, url)



def store_data_in_db():
    (artist_names, track_names, release_dates, album_types, urls) = fetch_data()

    #create the output json file
    filename = "challengegroover/data/data.json"

    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    else: #empty the file
        open(filename, 'w').close()

    # fill the database
    db = TinyDB(filename, indent=2)
    for i in range(len(artist_names)):
        db.insert({'artist': artist_names[i], 'name of the ' + album_types[i] : track_names[i],
                 'release date': release_dates[i], 'url': urls[i]})