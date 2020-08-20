import requests
import ujson
from flask import Blueprint, redirect, request, jsonify, render_template
from .spotify_auth import SpotifyAuth
from .spotify_fetch import SpotifyFetch

DBNAME = SpotifyFetch().DBNAME

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
    SpotifyFetch().store_artists_in_db()
    with open(DBNAME) as json_file:
        data = ujson.load(json_file)
    return data["artists"]

@api.route('/new_releases')
def display_new_releases():
    with open(DBNAME) as json_file:
        data = ujson.load(json_file)
    return data["releases"]