from tinydb import TinyDB, Query, where
import json
import requests
import os
import errno

class SpotifyFetch(object):
    CLIENT_ID=os.environ.get("CLIENT_ID")
    CLIENT_SECRET=os.environ.get("CLIENT_SECRET")
    AUTH_URL = 'https://accounts.spotify.com/api/token'
    RELEASES_URL = 'https://api.spotify.com/v1/browse/new-releases'
    ARTISTS_URL = 'https://api.spotify.com/v1/artists/'
    DBNAME = "challengegroover/data/data.json"


    def fetch_new_releases(self):
        # POST
        auth_response = requests.post(self.AUTH_URL, {
            'grant_type': 'client_credentials',
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
        })

        auth_response_data = auth_response.json()

        access_token = auth_response_data['access_token']
        os.environ['ACCESS_TOKEN'] = access_token

        headers={
            'Authorization': 'Bearer ' + access_token,
        }
        params={
            'country':'FR',
            'limit': 50
        }

        response = requests.request('GET',self.RELEASES_URL, headers=headers, params=params)

        return response.json()


    def filter_data(self):
        response = self.fetch_new_releases()
        n = len(response["albums"]["items"])
        artist_name = []
        id = []
        track_name = []
        release_date = []
        album_type = []
        url = []

        for i in range(n):
            artist_name.append(response["albums"]["items"][i]["artists"][0]["name"])
            id.append(response["albums"]["items"][i]["artists"][0]["id"])
            track_name.append(response["albums"]["items"][i]["name"])
            release_date.append(response["albums"]["items"][i]["release_date"])
            album_type.append(response["albums"]["items"][i]["album_type"])
            url.append(response["albums"]["items"][i]["external_urls"]["spotify"])

        return (artist_name, id, track_name, release_date, url)


    def store_new_releases_in_db(self):
        (artist_names, ids, track_names, release_dates, urls) = self.filter_data()

        if not os.path.exists(os.path.dirname(self.DBNAME)):
            try:
                os.makedirs(os.path.dirname(self.DBNAME))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
        else: #empty the file
            open(self.DBNAME, 'w').close()

        # fill the database
        db = TinyDB(self.DBNAME, indent=2)
        releases = db.table("releases")

        for i in range(len(artist_names)):
            releases.insert(
                {
                    'artist name': artist_names[i],
                    'artist id': ids[i],
                    'name of the release' : track_names[i],
                    'release date': release_dates[i],
                    'url': urls[i]
                }
            )

        return


    def retrieve_artist_ids(self):
        ids = []
        db = TinyDB(self.DBNAME, indent=2)
        for artist in db.table('releases'):
            ids.append(artist["artist id"])
        return ids


    def store_artists_in_db(self):
        db = TinyDB(self.DBNAME, indent=2)
        artists = db.table("artists")
        releases = db.table("releases")

        ids = self.retrieve_artist_ids()
        headers={
            'Authorization': 'Bearer ' + os.environ['ACCESS_TOKEN'],
        }
        for artist_id in ids:
            response = requests.request('GET',self.ARTISTS_URL + artist_id, headers=headers).json()
            new_release = releases.get(where('artist id') == response['id'])
            artists.insert(
                {
                    'artist name': response["name"],
                    'followers count': response["followers"]["total"],
                    'genres': response['genres'] if len(response['genres']) else None,
                    'artist popularity': response['popularity'],
                    'latest release': new_release['name of the release'],
                    'release date': new_release['release date'],
                    'link to latest release': new_release['url'],
                }
            )
        return
