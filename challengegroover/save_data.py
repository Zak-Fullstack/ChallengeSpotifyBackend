import json
import requests
import os
import errno

CLIENT_ID='180c7135a1b34458a06f9bcf7facb0b5'
CLIENT_SECRET='9e44d1bf307c49a8b87b9105e261f43d'

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

    # save the access token
    print(auth_response)
    access_token = auth_response_data['access_token']
    url = 'https://api.spotify.com/v1/browse/new-releases?country=FR'

    response = requests.request('GET', url, headers={
        'Authorization': 'Bearer ' + access_token,
    })

    data = response.json()

    # write data to file
    filename = "challengegroover/data/data.json"

    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(filename, "w") as write_file:
        json.dump(data, write_file, indent=2)

# save_data_to_file()