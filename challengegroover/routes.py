import requests
from flask import Blueprint, redirect, request, jsonify, render_template
from .spotify_auth import SpotifyAuth


# Landing page of the app.
root = Blueprint("root", "root", url_prefix="/")

@root.route("/")
def index():
    return render_template("index.html")


# Spotify Authorization.
auth = Blueprint("auth", "auth", url_prefix="/auth")


@auth.route("/")
def get_user():
    response = SpotifyAuth().getUser()
    return redirect(response)


@auth.route("/callback")
def callback():
    code = request.values["code"]
    tokens = SpotifyAuth().getUserToken(code)
    return jsonify(tokens)


# API
api = Blueprint("api", "api", url_prefix="/api")

@api.route('/artists')
def display_artists():
    AUTH_URL = 'https://accounts.spotify.com/api/token'

    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': SpotifyAuth.CLIENT_ID,
        'client_secret': SpotifyAuth.CLIENT_SECRET,
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    access_token = auth_response_data['access_token']

    url = 'https://api.spotify.com/v1/browse/new-releases?country=FR'
    response = requests.request('GET', url, headers={
        'Authorization': 'Bearer ' + access_token,
    })

    data = response.json()["albums"]["items"]
    return jsonify(data)
    # code = request.values["code"]
    # tokens = SpotifyAuth().getUserToken(code)
# def fetch_artists():
#     code = request.values["code"]
#     tokens = SpotifyAuth().getUserToken(code)
#     accessToken = jsonify(tokens)['access_token']
#     return accessToken
#     url = 'https://api.spotify.com/v1/browse/new-releases'
#     return response.json()
    # code = response.json().values["code"]
    # tokens = SpotifyAuth().getUserToken(code)
    # return '<h1>artists list loading...</h1>'


# def api_all():
#     conn = sqlite3.connect('books.db')
#     conn.row_factory = dict_factory
#     cur = conn.cursor()
#     all_books = cur.execute('SELECT * FROM books;').fetchall()

#     return jsonify(all_books)

