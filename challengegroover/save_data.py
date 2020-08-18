from tinydb import TinyDB, Query
import json
import requests
import os
import errno


CLIENT_ID=os.environ.get("CLIENT_ID")
CLIENT_SECRET=os.environ.get("CLIENT_SECRET")

def save_data_to_file():
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



    # write data to file
    # with open(filename, "w") as write_file:

    artist_name = []
    track_name = []
    release_date = []
    for i in range(len(response.json()["albums"]["items"])):
        artist_name.append(response.json()["albums"]["items"][i]["artists"][0]["name"])
        track_name.append(response.json()["albums"]["items"][i]["name"])
        release_date.append(response.json()["albums"]["items"][i]["release_date"])
    return (artist_name, track_name, release_date)
            # json.dump(artist_name, write_file, indent=2)
            # json.dump(track_name, write_file, indent=2)
            # json.dump(release_data, write_file, indent=2)



def store_in_tinydb():
    (artist_names, track_names, release_dates) = save_data_to_file()

    #create output file
    filename = "challengegroover/data/data.json"

    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    db = TinyDB('challengegroover/data/data.json', indent=2)
    for i in range(len(artist_names)):
        db.insert({'artist': artist_names[i], 'track name': track_names[i], 'release date': release_dates[i]})
    # db.insert({'artist': artist_names[0], 'track name': track_names[0], 'release date': release_dates[0]})
    # print()
    # print()
    # print(artist_names[0])

# store_in_tinydb()